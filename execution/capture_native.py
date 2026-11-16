"""Capture fixture watchface using parent's existing emulator monitor. Never boots or installs."""
from pathlib import Path
import argparse
from datetime import datetime,timedelta,timezone
import json
import math
import socket
import subprocess
import time
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
WORLD=True
PREFIX='world-timer'
PALETTES=[(0xAAAA55,0,0x0055FF),(0xFFFFFF,0,0xAAAAAA),(0xFFAA55,0,0xFFAA00),(0xAAFFFF,0x000055,0x00AAAA),(0,0xAAFFAA,0x55AA55),(0xFFAAAA,0x550000,0xAA5555),(0x000055,0xFFFFFF,0xFF55AA)]
MASKS=[0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F]
CENTERS=[(17,4),(30,17),(30,44),(17,56),(4,44),(4,17),(17,30)]
def rgb(n):return ((n>>16)&255,(n>>8)&255,n&255)
def screenshot(port):
 path=ROOT/'.tmp/native.ppm';path.unlink(missing_ok=True)
 with socket.create_connection(('localhost',port),timeout=5) as connection:
  connection.recv(65536);connection.sendall(f'screendump "{path.resolve()}"\n'.encode());deadline=time.monotonic()+5
  while time.monotonic()<deadline:
   connection.recv(65536)
   try:im=Image.open(path).convert('RGB');break
   except (FileNotFoundError,OSError):continue
  else:raise TimeoutError('Incomplete screendump')
 actual=max(max(pixel) for pixel in im.get_flattened_data())
 # Every preset/custom capture has a channel at255, including the Classic red line.
 im=im.point(lambda c:round(c/max(actual,1)*255/85)*85);path.unlink(missing_ok=True)
 assert im.size==(200,228)
 return im

def send(keys,uuid,values):
 result=subprocess.run(['pebble','send-app-message','--emulator','emery','--app-uuid',uuid,'--int']+[f'{keys.get(k,k)}={v}' for k,v in values.items()],cwd=ROOT/'watchface',capture_output=True,text=True,timeout=45)
 if result.returncode:raise RuntimeError(result.stderr[-1500:])

def digit_check(im,n,x,y,w,h,bg,fg):
 for k,(cx,cy) in enumerate(CENTERS):
  px=x+cx*w//34;py=y+cy*h//60
  assert im.getpixel((px,py))==(fg if MASKS[n]&(1<<k) else bg),f'digit {n} segment {k} at {px},{py}'

def check(im,case):
 bg,fg,accent=map(rgb,PALETTES[case['Palette']]);hour=case[11000];minute=case[11001]
 h=hour if case['TimeFormat']==2 else hour%12 or 12
 xs=[16,45,85,114] if WORLD else [20,51,93,124];y=103 if WORLD else 108;w=25 if WORLD else 26;height=48 if WORLD else 54
 for n,x in zip([h//10,h%10,minute//10,minute%10],xs):digit_check(im,n,x,y,w,height,bg,fg)
 sy=125 if WORLD else 136;sx=151 if WORLD else 158
 if case['ShowSeconds']:
  digit_check(im,case[11002]//10,sx,sy,11,26,bg,fg);digit_check(im,case[11002]%10,sx+14,sy,11,26,bg,fg)
 else:assert set(im.crop((sx,sy,sx+27,sy+28)).get_flattened_data())=={bg},'Seconds Off left ink'
 assert im.getpixel((0,0))==(0,0,0)
 assert im.getpixel((10 if WORLD else 15,11 if WORLD else 62))==bg,'LCD color'
 dx,dy,dw,dh=(12,192,143,15) if WORLD else(18,66,98,22)
 hasdate=fg in set(im.crop((dx,dy,dx+dw,dy+dh)).get_flattened_data())
 assert hasdate==(case['DateFormat']!=0),'Date visibility'
 ax,ay=(18,154) if WORLD else(21,165)
 hasperiod=fg in set(im.crop((ax,ay,ax+33,ay+17)).get_flattened_data())
 assert hasperiod==(case['TimeFormat']==1),'AM/PM visibility'
 bx,by=(67,210) if WORLD else(119,72)
 fill=19*case[11004]//100
 for i in range(19):assert im.getpixel((bx+2+i,by+5))==(fg if i<fill else bg),'Battery fill'
 result={'digit_segments':True,'date_visible':hasdate,'seconds_visible':bool(case['ShowSeconds'])}
 if WORLD:
  wall=datetime(case[11005],case[11006],case[11007],hour,minute,case[11002],tzinfo=timezone.utc)
  utc=wall-timedelta(minutes=(case[11008]-48)*15);other=utc+timedelta(minutes=(case['ZoneOffset']-48)*15)
  for n,x in zip([other.hour//10,other.hour%10,other.minute//10,other.minute%10],[117,130,149,162]):digit_check(im,n,x,175,10,15,bg,fg)
  expected_delta=(other.date()-wall.date()).days
  hasdelta=fg in set(im.crop((155,192,185,207)).get_flattened_data())
  assert hasdelta==(expected_delta!=0),'Secondary date rollover indicator'
  def near_ink(x,y):
   return any(im.getpixel((xx,yy))==fg for xx in range(x-1,x+2) for yy in range(y-1,y+2))
  for angle,radii in [(((other.hour%12)*60+other.minute)*math.tau/720,[10,14,17]),(other.minute*math.tau/60,[20,23,25])]:
   for radius in radii:
    x=47+int(math.sin(angle)*radius);y=47-int(math.cos(angle)*radius)
    assert near_ink(x,y),f'Secondary analog orientation missing expected ink near {x},{y}'
  result.update(expected_secondary=other.isoformat(),day_delta=expected_delta,secondary_digit_segments=True,secondary_analog_orientation=True,day_delta_visibility=hasdelta)
 return result

def cases():
 base={'Palette':0,'Background':0x000055,'Foreground':0xFFFFFF,'Accent':0xFF55AA,'TimeFormat':2,'DateFormat':1,'ShowSeconds':1,11000:10,11001:8,11002:30,11004:82}
 if WORLD:base.update(ZoneOffset=48);base.update({11005:2026,11006:11,11007:6,11008:24})
 values=[('default',{}),*[(f'palette-{i}',{'Palette':i}) for i in range(6)],('custom',{'Palette':6}),*[(f'date-{i}',{'DateFormat':i}) for i in range(5)],('seconds-off',{'ShowSeconds':0}),('battery-empty',{11004:0}),('battery-full',{11004:100})]
 values += [(f'{label}-{fmt}h',{11000:h,11001:m,'TimeFormat':fmt}) for label,h,m in [('midnight',0,0),('noon',12,0),('late',23,59),('eleven',11,11),('twenty',20,20)] for fmt in [1,2]]
 if WORLD:values += [('utc-minus12',{'ZoneOffset':0}),('utc-plus14',{'ZoneOffset':104}),('utc-plus0530',{'ZoneOffset':70}),('utc-plus0545',{'ZoneOffset':71}),('previous-day',{'ZoneOffset':0,11000:0,11001:1}),('next-day',{'ZoneOffset':104,11000:23,11001:59}),('offset-minute-carry',{'ZoneOffset':49,11001:59}),('new-year-plus-two',{'ZoneOffset':104,11005:2026,11006:12,11007:31,11008:0,11000:23,11001:0}),('new-year-minus-two',{'ZoneOffset':0,11005:2027,11006:1,11007:1,11008:104,11000:0,11001:0})]
 return [(name,{**base,**change}) for name,change in values]

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--monitor',type=int,required=True);args=parser.parse_args()
 (ROOT/'.tmp').mkdir(exist_ok=True);(ROOT/'media').mkdir(exist_ok=True)
 keys=json.loads((ROOT/'watchface/build/js/message_keys.json').read_text());uuid=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['uuid'];evidence=[]
 try:
  for name,case in cases():
   send(keys,uuid,case)
   for attempt in range(30):
    im=screenshot(args.monitor)
    try:result=check(im,case);break
    except AssertionError as failure:error=failure;time.sleep(.1)
   else:raise AssertionError(f'{name}: {error}')
   im.save(ROOT/f'media/{PREFIX}-{name}.png');evidence.append({'case':name,**result});print('PASS:',name,flush=True)
  (ROOT/'.tmp/native-checks.json').write_text(json.dumps(evidence,indent=2))
  board=Image.new('RGB',(660,536),(32,32,32));draw=ImageDraw.Draw(board)
  for i,label in enumerate(['Classic','Silver','Amber','Ice','Night','Rose']):
   x=i%3*220+10;y=i//3*268;board.paste(Image.open(ROOT/f'media/{PREFIX}-palette-{i}.png'),(x,y));draw.text((x,y+236),label,fill='white')
  board.save(ROOT/f'media/{PREFIX}-palettes.png')
  Image.open(ROOT/f'media/{PREFIX}-default.png').resize((400,456),Image.Resampling.NEAREST).save(ROOT/f'media/{PREFIX}-default-2x.png')
 finally:
  send(keys,uuid,dict(cases()[0][1],TimeFormat=0))
if __name__=='__main__':main()
