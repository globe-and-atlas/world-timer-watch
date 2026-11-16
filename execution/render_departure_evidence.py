"""Present native departure-board evidence without fractional display rescaling."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'.tmp/departure-native'
PLATFORMS=[('emery','TIME 2 / 200 x 228'),('chalk','TIME ROUND / 180 x 180'),('gabbro','ROUND 2 / 260 x 260')]
BG=(232,229,217)
FONT=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',22);SMALL=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',15)
def show(im,platform):
 im=im.convert('RGB')
 if platform!='emery':
  mask=Image.new('L',im.size);ImageDraw.Draw(mask).ellipse((0,0,im.width-1,im.height-1),fill=255);canvas=Image.new('RGB',im.size,BG);canvas.paste(im,(0,0),mask);im=canvas
 return im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST)
def sheet(images,title,subtitle,height=740):
 board=Image.new('RGB',(1660,height),BG);draw=ImageDraw.Draw(board);draw.text((34,22),title,font=FONT,fill='#151918');draw.text((34,59),subtitle,font=SMALL,fill='#4b504c')
 for i,(p,name) in enumerate(PLATFORMS):
  cx=[260,780,1330][i];im=show(images[p],p);draw.text((cx-210,110),name,font=SMALL,fill='#151918');board.paste(im,(cx-im.width//2,150))
 return board
for theme in ['amber','olive']:
 images={p:Image.open(OUT/p/f'{theme}.png') for p,n in PLATFORMS}
 sheet(images,'WORLD TIMER / NATIVE DEPARTURE BOARD','Actual emulator captures / native pixels enlarged exactly2x / no call hours').save(OUT/f'{theme}-comparison.png')
timelines={}
for p,n in PLATFORMS:
 with Image.open(OUT/p/'split-flap-five-seconds.gif') as im:
  frames=[];elapsed=0
  for i in range(im.n_frames):im.seek(i);elapsed+=im.info['duration'];frames.append((elapsed,im.convert('RGB')))
  assert elapsed==5000;timelines[p]=frames
boards=[]
for t in range(0,5000,50):
 images={p:next(im for end,im in frames if t<end) for p,frames in timelines.items()}
 boards.append(sheet(images,'WORLD TIMER / NATIVE SPLIT-FLAP TRANSITION','Actual native renderer phase captures / five seconds / pixel grid shown2x'))
boards[0].save(OUT/'three-display-five-seconds.gif',save_all=True,append_images=boards[1:],duration=50,loop=0,disposal=2,optimize=False)
print('Native comparison sheets and5second composite saved')
