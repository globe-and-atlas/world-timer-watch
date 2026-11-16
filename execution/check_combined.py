"""Native sensor, map-only animation, and configuration persistence checks."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,time
from PIL import Image
from native_io import ROOT,run,capture,monitor_port
BASE=int(datetime(2026,11,7,16,42,tzinfo=timezone.utc).timestamp())
def main()->None:
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--platform',choices=['emery','chalk','gabbro'],required=True);opt=parser.parse_args()
 keys=json.loads((ROOT/'watchface/build/js/message_keys.json').read_text());uuid=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['uuid'];port=monitor_port();out=ROOT/'.tmp/combined-native'/opt.platform
 def send(v:dict)->None:run(['pebble','send-app-message','--emulator',opt.platform,'--app-uuid',uuid,'--int']+[f'{keys.get(k,k)}={value}' for k,value in v.items()]);time.sleep(.12)
 def neutral():run(['pebble','emu-accel','--emulator',opt.platform,'gravity-z']);time.sleep(1.0)
 def replay(double):
  samples=['0,0,-1000']*5+['0,1200,-1000']*2+['0,0,-1000']*8
  if double:samples+=['0,1200,-1000']*2
  samples+=['0,0,-1000']*200
  f=ROOT/'.tmp/world-knock.csv';f.write_text('\n'.join(samples)+'\n');run(['pebble','emu-accel','--emulator',opt.platform,'custom',str(f)])
 def observe(seconds,baseline):
  states=[];frames=[];start=time.monotonic()
  while time.monotonic()-start<seconds:
   elapsed=time.monotonic()-start;im=capture(port);states.append((elapsed,im.tobytes()!=baseline.tobytes()));frames.append(im);time.sleep(.07)
  return states,frames
 defaults={'Theme':0,'MainCity':0,'OtherCity':1,'MainStart':9,'MainEnd':18,'OtherStart':9,'OtherEnd':18,'TravelOn':1,'ShowSeconds':0,'DateFormat':1,'TimeFormat':2,11000:BASE,11001:-1,11002:2}
 send(defaults);neutral();baseline=capture(port)
 # Version/fixture guard: frozen clock and city fields must match reviewed amber render.
 assert baseline.tobytes()==Image.open(out/'amber.png').convert('RGB').tobytes(),'Active layout differs from reviewed clock'
 replay(False);states,_=observe(.9,baseline);assert not any(c for _,c in states),'Single knock triggered';neutral()
 replay(True);states,frames=observe(3.6,baseline);neutral();assert any(c for _,c in states),'Double knock not detected';assert not any(c for t,c in states if t>3.2),'Travel did not finish'
 clock=baseline.crop((0,baseline.height*61//180,baseline.width,baseline.height)).tobytes()
 assert all(f.crop((0,f.height*61//180,f.width,f.height)).tobytes()==clock for f in frames),'Travel altered clock'
 frames[0].save(out/'sensor-travel.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
 send({'TravelOn':0});neutral();replay(True);states,_=observe(.8,baseline);assert not any(c for _,c in states),'Travel Off failed';neutral()
 send({'Theme':1,'MainCity':2,'OtherCity':34,'MainStart':22,'MainEnd':7,'OtherStart':0,'OtherEnd':24,'TravelOn':0});expected=capture(port,170);expected.save(out/'persistence-expected.png')
 run(['pebble','install','--emulator',opt.platform,str(ROOT/'.tmp/World-Timer-fixture.pbw')]);deadline=time.monotonic()+5
 while True:
  actual=capture(port,170)
  if actual.tobytes()==expected.tobytes():break
  if time.monotonic()>deadline:actual.save(out/'persistence-failed.png');raise AssertionError('Theme/cities/windows failed persistence')
  time.sleep(.1)
 actual.save(out/'persisted.png');send(defaults);neutral()
 (out/'sensor-checks.json').write_text(json.dumps({'double_knock':True,'single_rejected':True,'clock_stays_visible':True,'automatic_return':True,'travel_off':True,'theme_city_window_persistence':True},indent=2));print('PASS native sensor/travel/clock/persistence',opt.platform)
if __name__=='__main__':main()
