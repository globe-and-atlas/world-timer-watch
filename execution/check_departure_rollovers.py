"""Exercise native hour, midnight and fall-DST reassembly on an already owned emulator."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,time
from native_io import ROOT,run,capture,monitor_port
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--platform',choices=['emery','chalk','gabbro'],required=True);opt=parser.parse_args()
 keys=json.loads((ROOT/'watchface/build/js/message_keys.json').read_text());uuid=json.loads((ROOT/'watchface/package.json').read_text())['pebble']['uuid'];port=monitor_port();out=ROOT/'.tmp/departure-native'/opt.platform
 def send(v):run(['pebble','send-app-message','--emulator',opt.platform,'--app-uuid',uuid,'--int']+[f'{keys.get(k,k)}={value}' for k,value in v.items()]);time.sleep(.08)
 def utc(s):return int(datetime.fromisoformat(s).replace(tzinfo=timezone.utc).timestamp())
 for name,value in [('hour','2026-11-07T16:59:00'),('midnight','2026-11-08T05:59:00'),('dst-fall','2026-11-01T06:59:00')]:
  before=utc(value);send({'Theme':0,'MainCity':0,'OtherCity':1,'DateFormat':1,'ShowSeconds':0,'FlapOn':1,11002:2,11000:before+60,11004:0,11001:-1});rest=capture(port);rest.save(out/f'{name}-rest.png')
  send({11004:before,11001:300});middle=capture(port);middle.save(out/f'{name}-middle.png');assert middle.tobytes()!=rest.tobytes()
  send({11001:700});assert capture(port).tobytes()==rest.tobytes(),name+' did not reassemble'
 checks=json.loads((out/'checks.json').read_text());checks['hour_midnight_dst_reassemble']=True;(out/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS hour/midnight/DST reassembly',opt.platform)
if __name__=='__main__':main()
