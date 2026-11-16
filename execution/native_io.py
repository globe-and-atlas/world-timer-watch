"""Capture deterministic fixture states from the currently owned emulator; never boots it."""
from pathlib import Path
import argparse, json, re, socket, subprocess, time
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def run(args:list[str])->str:
 return subprocess.run(args,cwd=ROOT/'watchface',check=True,capture_output=True,text=True,timeout=60).stdout
def monitor_port()->int:
 # Query arguments only for the owned emulator, never pypkjs credential arguments.
 rows=run(['ps','-axo','pid,comm']).splitlines()
 matches=[r.split(None,1)[0] for r in rows if len(r.split(None,1))==2 and r.split(None,1)[1].strip().endswith('qemu-pebble')]
 if len(matches)!=1:raise RuntimeError('Expected exactly one QEMU owner')
 args=run(['ps','-p',matches[0],'-o','args='])
 return int(re.search(r'-monitor tcp::(\d+)',args).group(1))
def capture(port:int,expected_peak:int=255)->Image.Image:
 path=ROOT/'.tmp/native.ppm';path.unlink(missing_ok=True)
 with socket.create_connection(('localhost',port),timeout=5) as conn:
  conn.recv(65536);conn.sendall(f'screendump "{path}"\n'.encode())
  deadline=time.monotonic()+5
  while time.monotonic()<deadline:
   try:
    with Image.open(path) as source:im=source.convert('RGB');im.load()
    break
   except (OSError,FileNotFoundError):time.sleep(.01)
  else:raise TimeoutError('Native framebuffer missing')
 # QEMU screen brightness scales its palette. Restore the known full-scale palette.
 peak=max(max(pixel) for pixel in im.get_flattened_data())
 im=im.point(lambda c:round(c/max(peak,1)*expected_peak/85)*85);path.unlink(missing_ok=True);return im

