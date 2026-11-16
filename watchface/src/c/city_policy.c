#include "city_policy.h"

#include <stdlib.h>
bool wt_offset(int city,uint32_t utc,int *minutes){
 if(city<0||city>=WT_CITY_COUNT||utc<WT_ZONE_START||utc>=WT_ZONE_END)return false;
 const WTCity *c=&WT_CITIES[city];int lo=c->first,hi=c->first+c->count;
 while(lo+1<hi){int mid=(lo+hi)/2;if(WT_TRANSITIONS[mid].epoch<=utc)lo=mid;else hi=mid;}
 *minutes=WT_TRANSITIONS[lo].offset;return true;
}
static bool leap(int year){return year%4==0&&(year%100!=0||year%400==0);}
bool wt_city_time(int city,uint32_t utc,WTCivil *result){
 int offset;if(!wt_offset(city,utc,&offset))return false;
 int64_t adjusted=(int64_t)utc+offset*60;int days=adjusted/86400,seconds=adjusted%86400;
 int year=1970,remaining=days;while(remaining>=365+leap(year)){remaining-=365+leap(year);year++;}
 int ordinal=remaining;static const int months[]={31,28,31,30,31,30,31,31,30,31,30,31};int month=0;
 while(remaining>=months[month]+(month==1&&leap(year))){remaining-=months[month]+(month==1&&leap(year));month++;}
 *result=(WTCivil){year,month+1,remaining+1,seconds/3600,seconds/60%60,seconds%60,(days+4)%7,ordinal};return true;
}
bool wt_in_window(int minute,int start_hour,int end_hour){
 if(start_hour<0||start_hour>23||end_hour<0||end_hour>24||minute<0||minute>=1440)return false;
 int a=start_hour*60,b=end_hour*60;if(a==b)return false;
 return a<b?(minute>=a&&minute<b):(minute>=a||minute<b);
}
bool wt_call_allowed(int city,uint32_t utc,int start_hour,int end_hour){WTCivil t;if(!wt_city_time(city,utc,&t))return false;return wt_in_window(t.hour*60+t.minute,start_hour,end_hour);}
static int ordinal_day(const WTCivil *a){int y=a->year-1;return y*365+y/4-y/100+y/400+a->ordinal;}
int wt_day_delta(const WTCivil *a,const WTCivil *b){return ordinal_day(a)-ordinal_day(b);}
bool wt_knock(WTKnock *g,int x,int y,int z,bool vibration,bool enabled,bool busy,uint32_t stamp){
 if(vibration||!enabled||busy){g->initialized=false;g->pending=false;return false;}
 if(!g->initialized){g->x=x;g->y=y;g->z=z;g->initialized=true;return false;}
 int delta=abs(x-g->x);if(abs(y-g->y)>delta)delta=abs(y-g->y);if(abs(z-g->z)>delta)delta=abs(z-g->z);g->x=x;g->y=y;g->z=z;
 if(g->cooling&&(int32_t)(stamp-g->cooldown)<0)return false;
 g->cooling=false;
 if(g->pending&&(uint32_t)(stamp-g->impact)>650)g->pending=false;
 if(delta<700)return false;
 uint32_t gap=stamp-g->impact;if(g->seen&&gap<120)return false;
 bool fire=g->pending&&gap<=650;g->seen=true;g->impact=stamp;g->pending=!fire;
 if(fire){g->cooling=true;g->cooldown=stamp+WT_COOLDOWN_MS;}return fire;
}
