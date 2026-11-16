#pragma once
static const unsigned char DIGIT_MASK[10]={0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F};
static inline int uses_24(int pref,int watch){return pref==2||(pref==0&&watch);}
static inline int display_hour(int h,int pref,int watch){return uses_24(pref,watch)?h:(h%12?h%12:12);}
static inline int offset_minutes(int index){return (index-48)*15;}
static inline int floor_day(int minutes){return minutes>=0?minutes/1440:-((-minutes+1439)/1440);}
static inline int wrap_minutes(int minutes){int r=minutes%1440;return r<0?r+1440:r;}
#include <time.h>
static inline time_t shifted_epoch(time_t utc,int index){return utc+offset_minutes(index)*60;}
static inline time_t fixture_epoch(int hour,int minute,int second){return (time_t)1793944800+hour*3600+minute*60+second;}
static inline int civil_day(const struct tm *value){int y=value->tm_year+1899;return y*365+y/4-y/100+y/400+value->tm_yday;}

static inline int leap_year(int year){return year%4==0&&(year%100!=0||year%400==0);}
static inline int valid_fixture_date(int year,int month,int day){
 static const int days[]={31,28,31,30,31,30,31,31,30,31,30,31};
 return year>=2000&&year<=2037&&month>=1&&month<=12&&day>=1&&day<=days[month-1]+(month==2&&leap_year(year));
}
static inline time_t fixture_epoch_date(int year,int month,int day,int hour,int minute,int second,int utc_offset){
 static const int before[]={0,31,59,90,120,151,181,212,243,273,304,334};
 int y=year-1;int ordinal=y*365+y/4-y/100+y/400+before[month-1]+(month>2&&leap_year(year))+day-1;
 return (time_t)(ordinal-719162)*86400+hour*3600+minute*60+second-utc_offset*60;
}
