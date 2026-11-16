"""Compose reviewed native amber/olive screenshots for local delivery."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
def main()->None:
 board=Image.new('RGB',(1200,990),(235,230,217));draw=ImageDraw.Draw(board);font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',22)
 draw.text((600,27),'WORLD TIMER · NATIVE BUILD',font=font,anchor='mm',fill=(30,30,30))
 for target,cx,name in [('emery',200,'Time 2'),('chalk',600,'Time Round'),('gabbro',1000,'Round 2')]:
  draw.text((cx,68),name,font=font,anchor='mm',fill=(30,30,30))
  for theme,cy in [('amber',300),('olive',755)]:
   im=Image.open(ROOT/f'.tmp/combined-native/{target}/{theme}.png').convert('RGB');im=im.resize((round(im.width*1.5),round(im.height*1.5)),Image.Resampling.NEAREST);mask=None
   if target!='emery':mask=Image.new('L',im.size,0);ImageDraw.Draw(mask).ellipse((0,0,im.width-1,im.height-1),fill=255)
   board.paste(im,(cx-im.width//2,cy-im.height//2),mask)
 draw.text((25,105),'AMBER',font=font,fill=(30,30,30));draw.text((25,560),'OLIVE',font=font,fill=(30,30,30))
 draw.text((600,970),'Native emulator captures · selected cities, not detected locations',font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',16),anchor='mm',fill=(50,50,50))
 board.save(ROOT/'.tmp/combined-native-comparison.png');print(ROOT/'.tmp/combined-native-comparison.png')
if __name__=='__main__':main()
