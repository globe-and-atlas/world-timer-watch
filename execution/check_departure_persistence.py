"""Verify the board restores saved city/theme/date/animation settings after reinstall."""
from pathlib import Path
import argparse,json,time
from native_io import ROOT,run,capture,monitor_port
from capture_departure import BASE
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--platform',required=True,choices=['emery','chalk','gabbro']);opt=parser.parse_args()
 keys=json.loads((ROOT/'watchface/build/js/message_keys.json').read_text());uuid=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['uuid'];out=ROOT/'.tmp/departure-native'/opt.platform
 def send(v):run(['pebble','send-app-message','--emulator',opt.platform,'--app-uuid',uuid,'--int']+[f'{keys.get(k,k)}={value}' for k,value in v.items()]);time.sleep(.12)
 send({'Theme':1,'MainCity':2,'OtherCity':24,'DateFormat':2,'TimeFormat':2,'ShowSeconds':0,'FlapOn':0,11000:BASE,11001:-1,11002:2,11004:0})
 expected=capture(monitor_port(),170);expected.save(out/'persist-expected.png')
 run(['pebble','install','--emulator',opt.platform,str(ROOT/'.tmp/World-Timer-fixture.pbw')]);time.sleep(.3)
 deadline=time.monotonic()+12
 while True:
  observed=capture(monitor_port(),170)
  if observed.tobytes()==expected.tobytes():break
  if time.monotonic()>deadline:raise AssertionError('Settings changed on reinstall after foreground settling')
  time.sleep(.15)
 observed.save(out/'persist-restored.png')
 # Check persisted disabled-transition behavior independently of palette/city pixels.
 send({11000:BASE+60,11003:1});frames=[]
 for i in range(20):frames.append(capture(monitor_port(),170));time.sleep(.04)
 assert len({frame.tobytes() for frame in frames})==1,'Disabled animation setting was lost'
 checks=json.loads((out/'checks.json').read_text());checks['reinstall_exact_settings']=True;checks['reinstall_animation_off']=True;(out/'checks.json').write_text(json.dumps(checks,indent=2))
 print('PASS reinstall saved theme/cities/date and animation-off',opt.platform)
if __name__=='__main__':main()
