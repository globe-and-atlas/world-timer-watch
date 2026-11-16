"""Capture fixture cases on one round Pebble emulator with foreground/bounds proof.

Run build_round_fixture.py first. This script never copies fixtures to dist/.
--reset-emulator backs up existing flash before clearing the shared SDK emulator.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import socket
import subprocess
import tempfile
import time
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Install native QA dependencies: python3 -m pip install -r requirements.txt") from exc

ROOT = Path(__file__).resolve().parents[1]
TEMP = ROOT / ".tmp/round-qa"


def call(args: list[str]) -> None:
    result = subprocess.run(args, cwd=ROOT / "watchface", text=True,
                            capture_output=True, timeout=120)
    with (TEMP / "run.log").open("a") as log:
        log.write(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f"{args[:3]} failed; see {TEMP / 'run.log'}")


def owned_monitors() -> dict[int, int]:
    result = subprocess.run(["ps", "-axo", "pid,comm,args"], capture_output=True,
                            text=True, check=True)
    found = {}
    for line in result.stdout.splitlines():
        if re.match(r"^\s*\d+\s+qemu-pebble\s", line) and "/Pebble SDK/" in line:
            match = re.search(r"-monitor tcp::(\d+)", line)
            if match:
                found[int(line.split()[0])] = int(match.group(1))
    return found


def quit_monitor(port: int) -> None:
    with socket.create_connection(("localhost", port), timeout=5) as conn:
        conn.recv(65536)
        conn.sendall(b"quit\n")


def remove_boot_orphans(platform: str) -> None:
    metadata = json.loads((Path(tempfile.gettempdir()) / "pb-emulator.json").read_text())
    active = {entry["qemu"]["pid"] for entry in metadata[platform].values()}
    for pid, port in owned_monitors().items():
        if pid not in active:
            quit_monitor(port)
    time.sleep(0.1)


def capture(peak: int = 255) -> Image.Image:
    monitors = owned_monitors()
    if len(monitors) != 1:
        raise RuntimeError("Expected exactly one SDK emulator; stop other native QA runs")
    path = TEMP / "native.ppm"
    path.unlink(missing_ok=True)
    with socket.create_connection(("localhost", next(iter(monitors.values()))), timeout=5) as conn:
        conn.recv(65536)
        conn.sendall(f'screendump "{path}"\n'.encode())
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            conn.recv(65536)
            try:
                image = Image.open(path).convert("RGB")
                break
            except (FileNotFoundError, OSError):
                continue
        else:
            raise TimeoutError("QEMU screendump incomplete")
    maximum = max(max(pixel) for pixel in image.get_flattened_data())
    image = image.point(lambda component: round(component / max(maximum, 1) * peak / 85) * 85)
    path.unlink(missing_ok=True)
    return image


def run(platform: str, reset: bool, only: str | None = None) -> None:
    TEMP.mkdir(parents=True, exist_ok=True)
    if shutil.which("pebble") is None:
        raise RuntimeError("Pebble CLI is required for native QA")
    fixture = TEMP / "fixture.pbw"
    if not fixture.exists():
        raise FileNotFoundError("Run python3 execution/build_round_fixture.py first")
    if reset:
        sdk = Path.home() / "Library/Application Support/Pebble SDK"
        for flash in sdk.glob("*/*/*flash*.bin"):
            backup = TEMP / "emulator-backups" / flash.relative_to(sdk)
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                shutil.copy2(flash, backup)
        for port in owned_monitors().values():
            quit_monitor(port)
        call(["pebble", "kill"])
        time.sleep(0.3)
        call(["pebble", "wipe"])
    package = json.loads((ROOT / "watchface/package.json").read_text())
    uuid = package["pebble"]["uuid"]
    keys = json.loads((TEMP / "message_keys.json").read_text())
    install = ["pebble", "install", "--emulator", platform, str(fixture)]
    call(install)
    time.sleep(0.8)
    remove_boot_orphans(platform)
    call(install)
    remove_boot_orphans(platform)
    size = 180 if platform == "chalk" else 260
    proof = (89 * size // 180 + 1, 10 * size // 180 + 1)
    geometry = (93 * size // 180 + 1, 10 * size // 180 + 1)
    output = ROOT / "media/round"
    output.mkdir(parents=True, exist_ok=True)
    evidence = []

    def message(values: dict) -> None:
        pairs = []
        for key, value in values.items():
            if str(key).isdigit() or key in keys:
                pairs.append(f"{keys.get(key, key)}={value}")
        call(["pebble", "send-app-message", "--emulator", platform,
              "--app-uuid", uuid, "--int", *pairs])

    for case in json.loads((ROOT / "execution/round_cases.json").read_text()):
        name = case["case"]
        if only and name != only:
            continue
        for retry in range(3):
            message({**case["settings"], "11022": 1})
            for attempt in range(15):
                image = capture()
                if image.size == (size, size) and image.getpixel(proof) == (255, 0, 255):
                    if image.getpixel(geometry) != (0, 255, 0):
                        image.save(TEMP / f"geometry-failed-{platform}-{name}.png")
                        raise AssertionError(f"{name}: unsafe text/glyph geometry")
                    break
                time.sleep(0.1)
            else:
                call(install)
                remove_boot_orphans(platform)
                continue
            break
        else:
            raise AssertionError(f"{name}: expected face not in foreground")
        message({"11022": 0})
        for attempt in range(20):
            time.sleep(0.1)
            if capture().getpixel(proof) != (255, 0, 255):
                break
        else:
            raise AssertionError("Fixture marker did not clear")
        path = output / f"{platform}-{name}.png"
        capture(case["peak"]).save(path)
        evidence.append({"case": name, "size": [size, size], "path": str(path),
                         "foreground_verified": True, "safe_geometry": True})
        print(platform, name, flush=True)
    if not evidence:
        raise ValueError(f"Unknown case: {only}")
    suffix = f"-{only}" if only else ""
    (TEMP / f"native-{platform}{suffix}.json").write_text(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=["chalk", "gabbro"], required=True)
    parser.add_argument("--reset-emulator", action="store_true")
    parser.add_argument("--case", help="capture one named case")
    args = parser.parse_args()
    try:
        run(args.platform, args.reset_emulator, args.case)
    except (OSError, RuntimeError, ValueError, AssertionError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"Round QA failed: {exc}\n")
