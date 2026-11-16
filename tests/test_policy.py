"""Compile the same pure C policy used by native rendering."""
from pathlib import Path
import subprocess
import unittest
ROOT=Path(__file__).resolve().parents[1]
class PolicyTest(unittest.TestCase):
 def test_native_time_policy(self):
  temp=ROOT/'.tmp';temp.mkdir(exist_ok=True)
  source=temp/'policy_test.c';binary=temp/'policy_test'
  source.write_text(r'''#include <assert.h>
#include "policy.h"
int main(void){
 assert(display_hour(0,1,1)==12);assert(display_hour(12,1,0)==12);assert(display_hour(23,1,1)==11);
 assert(display_hour(23,2,0)==23);assert(display_hour(23,0,1)==23);assert(display_hour(23,0,0)==11);
 for(int i=0;i<=104;i++)assert(offset_minutes(i)==(i-48)*15);
 assert(offset_minutes(0)==-720);assert(offset_minutes(104)==840);assert(offset_minutes(70)==330);
 time_t utc=fixture_epoch(10,8,30);struct tm base=*gmtime(&utc);
 assert(base.tm_year==126&&base.tm_mon==10&&base.tm_mday==6&&base.tm_wday==5);
 assert(base.tm_hour==16&&base.tm_min==8&&base.tm_sec==30);
 time_t next=shifted_epoch(utc,104);struct tm t=*gmtime(&next);assert(t.tm_mday==7&&t.tm_hour==6&&t.tm_min==8);assert(civil_day(&t)-civil_day(&base)==1);
 next=shifted_epoch(utc,0);t=*gmtime(&next);assert(t.tm_mday==6&&t.tm_hour==4&&t.tm_min==8);
 next=shifted_epoch(utc,70);t=*gmtime(&next);assert(t.tm_hour==21&&t.tm_min==38);
 utc=fixture_epoch(0,0,0);next=shifted_epoch(utc,0);t=*gmtime(&next);assert(t.tm_mday==5&&t.tm_hour==18);
 struct tm dec={.tm_year=126,.tm_yday=364},jan={.tm_year=127,.tm_yday=0};assert(civil_day(&jan)-civil_day(&dec)==1);
 dec.tm_yday=363;assert(civil_day(&jan)-civil_day(&dec)==2);assert(civil_day(&dec)-civil_day(&jan)==-2);
 assert(valid_fixture_date(2026,11,6));assert(!valid_fixture_date(2026,2,29));assert(valid_fixture_date(2028,2,29));
 utc=fixture_epoch_date(2026,12,31,23,0,0,-720);next=shifted_epoch(utc,104);t=*gmtime(&next);
 assert(t.tm_year==127&&t.tm_mon==0&&t.tm_mday==2&&t.tm_hour==1);
 time_t local_epoch=utc-720*60;struct tm wall=*gmtime(&local_epoch);assert(civil_day(&t)-civil_day(&wall)==2);
 utc=fixture_epoch_date(2027,1,1,0,0,0,840);next=shifted_epoch(utc,0);t=*gmtime(&next);local_epoch=utc+840*60;wall=*gmtime(&local_epoch);assert(civil_day(&t)-civil_day(&wall)==-2);
 return 0;}
''')
  subprocess.run(['cc','-std=c99','-Wall','-Wextra','-Werror','-I'+str(ROOT/'watchface/src/c'),str(source),'-o',str(binary)],check=True)
  subprocess.run([str(binary)],check=True)
if __name__=='__main__':unittest.main()
