#include <assert.h>
#include <stdio.h>
#include "city_policy.h"
static bool impact(WTKnock *k,int axis,uint32_t t){int x=0,y=0,z=-1000;if(axis==0)x=1200;if(axis==1)y=1200;if(axis==2)z=200;return wt_knock(k,x,y,z,false,true,false,t);}
int main(void){
 for(int axis=0;axis<3;axis++){
  WTKnock k={0};assert(!wt_knock(&k,0,0,-1000,false,true,false,0));assert(!impact(&k,axis,200));assert(!wt_knock(&k,0,0,-1000,false,true,false,220));assert(impact(&k,axis,440));
  assert(!wt_knock(&k,0,0,-1000,false,true,true,460));assert(!impact(&k,axis,600));assert(!wt_knock(&k,0,0,-1000,false,true,false,620));
  assert(!wt_knock(&k,0,0,-1000,false,true,false,6000));assert(!impact(&k,axis,6200));assert(!wt_knock(&k,0,0,-1000,false,true,false,6220));assert(impact(&k,axis,6400));
 }
 WTKnock k={0};wt_knock(&k,0,0,-1000,false,true,false,0);assert(!impact(&k,1,200));assert(!wt_knock(&k,0,0,-1000,false,true,false,220));assert(!impact(&k,1,1000));
 assert(!wt_knock(&k,0,0,-1000,true,true,false,1200));assert(!impact(&k,1,1400));
 assert(!wt_knock(&k,0,0,-1000,false,false,false,1600));assert(!impact(&k,1,1800));
 k=(WTKnock){0};wt_knock(&k,0,0,-1000,false,true,false,UINT32_MAX-400);assert(!impact(&k,2,UINT32_MAX-200));assert(!wt_knock(&k,0,0,-1000,false,true,false,UINT32_MAX-180));assert(impact(&k,2,100));
 for(int city=0;city<WT_CITY_COUNT;city++)for(uint32_t t=WT_ZONE_START;t<WT_ZONE_END;t+=3600*71){WTCivil value;assert(wt_city_time(city,t,&value));assert(value.year>=2019&&value.year<=2038);assert(value.month>=1&&value.month<=12);assert(value.hour>=0&&value.hour<24);}
 puts("PASS: sanitized city/calendar sweep and knock rebound/timeout/cooldown/busy/disabled/wraparound");return 0;
}
