"""Build isolated round QA fixtures; never copies them to production dist/."""
from pathlib import Path
import json
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    if shutil.which("pebble") is None:
        raise RuntimeError("Pebble CLI is required for fixture builds")
    config = json.loads((ROOT / "execution/round_fixture.json").read_text())
    env = {key: value for key, value in os.environ.items()
           if not key.startswith(config["prefix"] + "_")}
    env.update(config["flags"])
    target = ROOT / ".tmp/round-qa"
    target.mkdir(parents=True, exist_ok=True)
    with (target / "fixture-build.log").open("w") as log:
        for args in [["pebble", "clean"], ["pebble", "build"]]:
            subprocess.run(args, cwd=ROOT / "watchface", env=env, check=True,
                           stdout=log, stderr=subprocess.STDOUT)
    for source, name in [("watchface.pbw", "fixture.pbw"),
                         ("js/message_keys.json", "message_keys.json")]:
        shutil.copy2(ROOT / "watchface/build" / source, target / name)
    print(f"Fixture: {target / 'fixture.pbw'} (production dist/ untouched)")


if __name__ == "__main__":
    main()
