#pragma once
#include <stdint.h>
#include <stdbool.h>

#include "city_data.h"
#define WT_TRAVEL_MS 2500
#define WT_COOLDOWN_MS 5000
typedef struct {int year,month,day,hour,minute,second,weekday,ordinal;} WTCivil;
bool wt_offset(int city,uint32_t utc,int *minutes);
bool wt_city_time(int city,uint32_t utc,WTCivil *result);
bool wt_call_allowed(int city,uint32_t utc,int start_hour,int end_hour);
bool wt_in_window(int minute,int start_hour,int end_hour);
int wt_day_delta(const WTCivil *a,const WTCivil *b);
typedef struct {bool initialized,pending,seen,cooling;int x,y,z;uint32_t impact,cooldown;} WTKnock;
bool wt_knock(WTKnock *state,int x,int y,int z,bool vibration,bool enabled,bool busy,uint32_t stamp);
