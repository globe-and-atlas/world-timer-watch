"""Stage lossless departure-board store media from verified native capture evidence."""
from pathlib import Path
import argparse,hashlib,json,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SIZES={'emery':(200,228),'chalk':(180,180),'gabbro':(260,260)}
def main()->None:
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true',help='Verify staged assets without changing them');options=parser.parse_args()
 out=ROOT/'media/store/departure-0.3.0';out.mkdir(parents=True,exist_ok=True)
 for platform,size in SIZES.items():
  source=ROOT/'.tmp/departure-native'/platform;checks=json.loads((source/'checks.json').read_text())
  assert checks['actual_timer_settles'] and checks['unchanged_pixels_stable']
  preview=out/f'{platform}_01_split_flap.gif'
  if not options.check:shutil.copy2(source/'split-flap-five-seconds.gif',preview)
  assert preview.read_bytes()==(source/'split-flap-five-seconds.gif').read_bytes()
  with Image.open(preview) as image:
   assert image.size==size and image.n_frames>1;total=0
   for frame in range(image.n_frames):image.seek(frame);total+=image.info['duration']
   assert total==5000
  for index,theme in enumerate(['amber','olive','custom'],2):
   path=out/f'{platform}_{index:02}_{theme}.gif'
   with Image.open(source/f'{theme}.png') as native:
    assert native.size==size
    if not options.check:native.save(path)
    with Image.open(path) as staged:assert staged.n_frames==1 and staged.convert('RGB').tobytes()==native.convert('RGB').tobytes()
 print('PASS:12 native departure-board store assets; all three previews5000ms')
if __name__=='__main__':main()
