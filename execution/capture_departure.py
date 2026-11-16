"""Capture native departure-board states and hinged digit phases on the owned emulator."""
from pathlib import Path
import argparse,json,time,subprocess
from datetime import datetime,timezone
from PIL import Image
from native_io import ROOT,run,capture,monitor_port
BASE=int(datetime(2026,11,7,16,42,tzinfo=timezone.utc).timestamp())
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--platform',choices=['emery','chalk','gabbro'],required=True);opt=parser.parse_args()
 keys=json.loads((ROOT/'watchface/build/js/message_keys.json').read_text());uuid=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['uuid'];port=monitor_port();out=ROOT/'.tmp/departure-native'/opt.platform;out.mkdir(parents=True,exist_ok=True);state={}
 def command(values):return ['pebble','send-app-message','--emulator',opt.platform,'--app-uuid',uuid,'--int']+[f'{keys.get(k,k)}={v}' for k,v in values.items()]
 def send(v):state.update(v);run(command(v));time.sleep(.08)
 def shot():return capture(port,170 if state.get('Theme',0)==1 else 255)
 defaults={'Theme':0,'MainCity':0,'OtherCity':1,'FlapOn':1,'ShowSeconds':0,'DateFormat':1,'TimeFormat':2,11000:BASE,11001:-1,11002:2,11004:0}
 cases=[('amber',defaults),('olive',{'Theme':1}),('negative',{'Theme':0,'MainCity':1,'OtherCity':0}),('fractional',{'MainCity':2,'OtherCity':24}),('zero',{'MainCity':0,'OtherCity':0}),('long-iso',{'MainCity':21,'OtherCity':14,'DateFormat':2}),('twelve',{11000:BASE,'MainCity':0,'OtherCity':1,'DateFormat':1,11002:1}),('twelve-seconds',{'ShowSeconds':1}),('date-off',{'ShowSeconds':0,11002:2,'DateFormat':0}),('us',{'DateFormat':3}),('eu',{'DateFormat':4}),('expired',{11000:2145916800}),('custom',{'Theme':2,'Background':0x000055,'Foreground':0xFFFFFF,'Accent':0xFF5500,11000:BASE})]
 for name,v in cases:
  send(v);im=shot();assert im.size=={'emery':(200,228),'chalk':(180,180),'gabbro':(260,260)}[opt.platform];im.save(out/f'{name}.png');print('CAPTURED',opt.platform,name,flush=True)
 send(defaults);old=shot();send({11000:BASE+60});new=shot();phases=[]
 for elapsed in range(0,701,50):
  send({11004:BASE,11001:elapsed});im=shot();im.save(out/f'phase-{elapsed}.png');phases.append(im)
 assert phases[0].tobytes()==old.tobytes(),'First phase differs from previous minute'
 assert phases[-1].tobytes()==new.tobytes(),'End phase fails to settle exactly'
 assert any(im.tobytes() not in [old.tobytes(),new.tobytes()] for im in phases),'No intermediate flap'
 # The only moving pixels must be within the two changed minute tiles.
 w=old.width;scale,ys={'emery':(4,[62,144]),'chalk':(3,[56,114]),'gabbro':(5,[81,161])}[opt.platform];cw=5*scale+8;left=(w-(4*cw+16))//2+3*(cw+3)+7
 for im in phases:
  for y in range(im.height):
   for x in range(im.width):
    if any(left<=x<left+cw and yy<=y<yy+7*scale+10 for yy in ys):continue
    assert im.getpixel((x,y))==new.getpixel((x,y)),f'Unexpected motion at{x},{y}'
 frames=[old]+phases+[new];durations=[1000]+[50]*len(phases)+[3250]
 frames[0].save(out/'split-flap-five-seconds.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2,optimize=False)
 with Image.open(out/'split-flap-five-seconds.gif') as gif:
  total=0
  for i in range(gif.n_frames):gif.seek(i);total+=gif.info['duration']
  assert total==5000
 # Exercise actual AppTimer completion rather than relying solely on fixed phases.
 send(defaults);process=subprocess.Popen(command({11000:BASE+60,11003:1}),cwd=ROOT/'watchface',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 runtime=[]
 for i in range(45):runtime.append(shot());time.sleep(.04)
 assert process.wait(timeout=30)==0
 time.sleep(.2);end=shot();assert end.tobytes()==new.tobytes(),'Runtime timer did not settle'
 moving=[im for im in runtime if im.tobytes() not in [old.tobytes(),new.tobytes()]];assert moving,'Runtime flip not observed'
 runtime[0].save(out/'runtime.gif',save_all=True,append_images=runtime[1:],duration=40,loop=0)
 # Disabled transition must snap without starting animation.
 send(defaults);send({'FlapOn':0,11000:BASE+60,11003:1});assert shot().tobytes()==new.tobytes()
 send(defaults)
 (out/'checks.json').write_text(json.dumps({'platform':opt.platform,'states':[n for n,v in cases],'phase_start_exact':True,'phase_end_exact':True,'unchanged_pixels_stable':True,'duration_ms':5000,'actual_timer_intermediate_frames':len(moving),'actual_timer_settles':True,'animation_off_snaps':True},indent=2))
 print('PASS native board/animation',opt.platform,flush=True)
if __name__=='__main__':main()
