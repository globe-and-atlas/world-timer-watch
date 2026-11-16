"""Native layout and fixed-UTC evidence for the approved combined design."""
from pathlib import Path
import argparse,json,time
from datetime import datetime,timezone
from PIL import Image,ImageDraw,ImageFont
from native_io import ROOT,run,capture,monitor_port
BASE=int(datetime(2026,11,7,16,42,tzinfo=timezone.utc).timestamp())
def epoch(y,m,d,h,minute=0):return int(datetime(y,m,d,h,minute,tzinfo=timezone.utc).timestamp())
def main()->None:
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--platform',choices=['emery','chalk','gabbro'],required=True);parser.add_argument('--only',choices=['long-iso']);opt=parser.parse_args()
 keys=json.loads((ROOT/'watchface/build/js/message_keys.json').read_text());uuid=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['uuid'];port=monitor_port();out=ROOT/'.tmp/combined-native'/opt.platform;out.mkdir(parents=True,exist_ok=True)
 state={}
 def send(v:dict)->None:
  state.update(v)
  run(['pebble','send-app-message','--emulator',opt.platform,'--app-uuid',uuid,'--int']+[f'{keys.get(k,k)}={value}' for k,value in v.items()]);time.sleep(.12)
 defaults={'Theme':0,'MainCity':0,'OtherCity':1,'MainStart':9,'MainEnd':18,'OtherStart':9,'OtherEnd':18,'TravelOn':0,'ShowSeconds':0,'DateFormat':1,'TimeFormat':2,11000:BASE,11001:-1,11002:2}
 cases=[('amber',defaults),('olive',{'Theme':1}),('travel',{'Theme':0,11001:1250}),('date-off',{11001:-1,'DateFormat':0}),('iso',{'DateFormat':2}),('us',{'DateFormat':3}),('eu',{'DateFormat':4}),('twelve',{11000:epoch(2026,11,7,7,8),11002:1,'DateFormat':1}),('twelve-seconds',{'ShowSeconds':1}),('london-lord-howe',{'ShowSeconds':0,11000:BASE,11002:2,'MainCity':2,'OtherCity':34}),('overnight',{'MainStart':22,'MainEnd':7,'OtherStart':0,'OtherEnd':24}),('expired',{11000:2145916800}),('long-iso',{11000:BASE,'Theme':0,'MainCity':21,'OtherCity':14,'DateFormat':2}),('custom',{'Theme':2,'Background':0x000055,'Foreground':0xFFFFFF,'Accent':0xFF5500,11000:BASE,'MainCity':0,'OtherCity':1})]
 if opt.only:
  send(defaults);cases=[case for case in cases if case[0]==opt.only]
 for name,v in cases:
  send(v);im=capture(port,170 if state.get('Theme',0)==1 else 255);assert im.size=={'emery':(200,228),'chalk':(180,180),'gabbro':(260,260)}[opt.platform]
  if name=='amber':
   assert im.getpixel((im.width//2,im.height//2))!=(255,255,170),'Wrong app active'
   assert sum(px==(255,170,0) for px in im.get_flattened_data())>300,'Amber ink absent or wrong app'
  im.save(out/f'{name}.png');print('CAPTURED',opt.platform,name,flush=True)
 if opt.only:
  send(defaults);return
 # Animated map-only motion; protect clock/date content while the dot travels.
 send(defaults);baseline=capture(port,170 if state.get('Theme',0)==1 else 255);frames=[]
 for phase in range(0,2501,125):
  send({11001:phase});im=capture(port,170 if state.get('Theme',0)==1 else 255);assert im.crop((0,im.height*61//180,im.width,im.height)).tobytes()==baseline.crop((0,im.height*61//180,im.width,im.height)).tobytes(),'Animation changed clock region';frames.append(im)
 assert any(im.tobytes()!=baseline.tobytes() for im in frames);assert frames[-1].tobytes()==baseline.tobytes()
 frames[0].save(out/'travel.gif',save_all=True,append_images=frames[1:],duration=125,loop=0)
 send(defaults)
 (out/'checks.json').write_text(json.dumps({'platform':opt.platform,'cases':[name for name,v in cases],'clock_unchanged_during_travel':True,'restored_exactly':True},indent=2))
if __name__=='__main__':main()
