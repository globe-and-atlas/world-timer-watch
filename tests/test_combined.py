"""Compare native C city math with independent ZoneInfo interpretation of pinned TZif files."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import ctypes,json,random,subprocess,unittest
ROOT=Path(__file__).resolve().parents[1]
class Civil(ctypes.Structure):_fields_=[(n,ctypes.c_int) for n in ['year','month','day','hour','minute','second','weekday','ordinal']]
class CombinedTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  
  if not (ROOT/'.tmp/tzdata-2026f/zoneinfo').exists():raise RuntimeError('Prepare pinned TZif oracle cache with python3 execution/generate_zones.py --fetch')
  cls.meta=json.loads((ROOT/'release/timezone-source.json').read_text());cls.ids={c['zone']:i for i,c in enumerate(cls.meta['cities'])}
  binary=ROOT/'.tmp/city-test.dylib'
  subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-dynamiclib','-fPIC','-Iwatchface/src/c','watchface/src/c/city_policy.c','watchface/src/c/city_data.c','-o',str(binary)],cwd=ROOT,check=True)
  cls.lib=ctypes.CDLL(str(binary));cls.lib.wt_offset.argtypes=[ctypes.c_int,ctypes.c_uint32,ctypes.POINTER(ctypes.c_int)];cls.lib.wt_offset.restype=ctypes.c_bool
  cls.lib.wt_city_time.argtypes=[ctypes.c_int,ctypes.c_uint32,ctypes.POINTER(Civil)];cls.lib.wt_city_time.restype=ctypes.c_bool
  cls.lib.wt_call_allowed.argtypes=[ctypes.c_int,ctypes.c_uint32,ctypes.c_int,ctypes.c_int];cls.lib.wt_call_allowed.restype=ctypes.c_bool
  cls.lib.wt_in_window.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_int];cls.lib.wt_in_window.restype=ctypes.c_bool
  cls.lib.wt_day_delta.argtypes=[ctypes.POINTER(Civil),ctypes.POINTER(Civil)];cls.lib.wt_day_delta.restype=ctypes.c_int
 def epoch(self,s):return int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())
 def value(self,key,s):
  offset=ctypes.c_int();self.assertTrue(self.lib.wt_offset(self.ids[key],self.epoch(s),ctypes.byref(offset)));return offset.value
 def test_named_boundaries(self):
  cases=[('America/Chicago','2026-03-08T07:59:59Z',-360),('America/Chicago','2026-03-08T08:00:00Z',-300),('America/Chicago','2026-11-01T06:59:59Z',-300),('America/Chicago','2026-11-01T07:00:00Z',-360),('Europe/London','2026-03-15T12:00:00Z',0),('America/Chicago','2026-03-15T12:00:00Z',-300),('Europe/London','2026-10-28T12:00:00Z',0),('Australia/Lord_Howe','2026-04-04T14:59:59Z',660),('Australia/Lord_Howe','2026-04-04T15:00:00Z',630),('Asia/Kathmandu','2026-11-07T16:42:00Z',345),('America/Havana','2026-11-06T12:00:00Z',-240)]
  for key,t,expected in cases:
   with self.subTest(key=key,t=t):self.assertEqual(self.value(key,t),expected)
 def test_every_transition_and_random_dates(self):
  random.seed(731);count=0
  for i,c in enumerate(self.meta['cities']):
   with (ROOT/f'.tmp/tzdata-2026f/zoneinfo/{c["zone"]}').open('rb') as f:z=ZoneInfo.from_file(f)
   stamps=[self.meta['valid_from'],self.meta['valid_until_exclusive']-1]+[random.randrange(self.meta['valid_from'],self.meta['valid_until_exclusive']) for _ in range(120)]
   for t,offset in self.meta['transitions'][c['first']:c['first']+c['count']]:stamps += [v for v in [t-1,t,t+1] if self.meta['valid_from']<=v<self.meta['valid_until_exclusive']]
   for t in stamps:
    actual=Civil();self.assertTrue(self.lib.wt_city_time(i,t,ctypes.byref(actual)));expected=datetime.fromtimestamp(t,timezone.utc).astimezone(z)
    self.assertEqual((actual.year,actual.month,actual.day,actual.hour,actual.minute,actual.second),(expected.year,expected.month,expected.day,expected.hour,expected.minute,expected.second),(c['name'],t));self.assertEqual(actual.weekday,(expected.weekday()+1)%7);count+=1
  print('PASS: native civil time vs TZif oracle at',count,'city instants')
 def test_windows_and_dst_day(self):
  for minute in range(1440):
   self.assertEqual(self.lib.wt_in_window(minute,9,18),540<=minute<1080)
   self.assertEqual(self.lib.wt_in_window(minute,22,7),minute>=1320 or minute<420)
   self.assertFalse(self.lib.wt_in_window(minute,9,9));self.assertTrue(self.lib.wt_in_window(minute,0,24))
  city=self.ids['America/Chicago'];start=self.epoch('2026-03-08T00:00:00Z')
  with (ROOT/'.tmp/tzdata-2026f/zoneinfo/America/Chicago').open('rb') as f:z=ZoneInfo.from_file(f)
  for step in range(96):
   t=start+step*900;local=datetime.fromtimestamp(t,timezone.utc).astimezone(z)
   self.assertEqual(self.lib.wt_call_allowed(city,t,1,3),60<=local.hour*60+local.minute<180)
 def test_rollover_and_expiration(self):
  epoch=self.epoch('2026-11-07T16:42:00Z');a,b=Civil(),Civil();self.assertTrue(self.lib.wt_city_time(0,epoch,ctypes.byref(a)));self.assertTrue(self.lib.wt_city_time(1,epoch,ctypes.byref(b)));self.assertEqual((a.hour,a.minute,b.hour,b.minute,b.day),(10,42,1,42,8));self.assertEqual(self.lib.wt_day_delta(ctypes.byref(b),ctypes.byref(a)),1)
  for t in [self.meta['valid_from']-1,self.meta['valid_until_exclusive']]:self.assertFalse(self.lib.wt_city_time(0,t,ctypes.byref(a)))
  self.assertFalse(self.lib.wt_city_time(-1,epoch,ctypes.byref(a)));self.assertFalse(self.lib.wt_city_time(40,epoch,ctypes.byref(a)))
if __name__=='__main__':unittest.main()
