"""Prepare lossless store media from verified native combined captures; never rebuild PBW."""
from pathlib import Path
from PIL import Image
r=Path(__file__).resolve().parents[1]
for p in ['emery','chalk','gabbro']:
 src=r/'.tmp/combined-native'/p; out=r/'media/store/combined-0.2.0';out.mkdir(parents=True,exist_ok=True)
 frames=[];times=[]
 with Image.open(src/'travel.gif') as im:
  for i in range(im.n_frames):im.seek(i);frames.append(im.convert('RGB'));times.append(im.info.get('duration',120))
 times[0]+=800;times[-1]+=600
 for name in ['olive','custom','amber']:frames.append(Image.open(src/f'{name}.png').convert('RGB'));times.append(1600)
 frames[0].save(out/f'{p}_01_travel_colors.gif',save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=2,optimize=False)
 for i,name in enumerate(['amber','olive','custom'],2):Image.open(src/f'{name}.png').save(out/f'{p}_{i:02}_{name}.gif')
