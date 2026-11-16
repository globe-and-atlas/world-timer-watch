#pragma once
#include "round_support.h"
#if defined(PBL_ROUND)
/* Style IDs: Mono1,LCD2,Desk3,HiFi4,Margin5,Dot6,Rally7,Terminal8,Ledger9,
   Classic10,World11. Actual bitmap numeral families are supplied by the face. */
static inline void round_digital(GContext *ctx,RoundData *d,int style,RoundDigit digit){
 r_layout_bad=false;rclear(ctx,d->bg);graphics_context_set_fill_color(ctx,GColorFromHEX(d->fg));
 char date[40],charge[16];rdate(d,date,sizeof(date));snprintf(charge,sizeof(charge),"%d%%",d->battery);
 if(style==1){
  rt(ctx,date,25,13,130,0,d->fg);
  int hour=rhour(d);digit(ctx,hour/10,45+d->hour_shift,34,42,48);digit(ctx,hour%10,93+d->hour_shift,34,42,48);
  digit(ctx,d->now.tm_min/10,45+d->minute_shift,90,42,48);digit(ctx,d->now.tm_min%10,93+d->minute_shift,90,42,48);
  rfill(ctx,55,145,70,3,0,rmix(d->bg,d->fg));if(d->battery)rfill(ctx,55,145,70*d->battery/100,3,0,d->accent);
  if(!r24(d->time_mode)){snprintf(charge,sizeof(charge),"%s %d%%",d->now.tm_hour>=12?"PM":"AM",d->battery);}rt(ctx,charge,45,155,90,0,d->fg);return;
 }
 if(style==2){
  rt(ctx,date,24,13,132,0,d->fg);
  const int orders[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
  if(d->seconds){for(int i=0;i<60;i++){int h=(i+1)%10?4:7;rfill(ctx,30+i*2,35-h,1,h,0,i<=d->now.tm_sec?d->fg:rmix(d->bg,d->fg));}}
  int y=d->seconds?48:37;
  for(int row=0;row<3;row++){
   int kind=orders[d->layout][row];
   if(kind==0){graphics_context_set_fill_color(ctx,GColorFromHEX(d->fg));rclock(ctx,d,y,40,digit);rperiod(ctx,d,y+37);y+=51;}
   else if(kind==1){rbat(ctx,d,y+1);y+=26;}
   else{rweekday(ctx,d,y+1);y+=23;}
  }
  return;
 }
 if(style==3){
  rcircle(ctx,90,90,84,2,d->accent);rperiod(ctx,d,25);
  rfill(ctx,12,51,156,73,11,d->accent);graphics_context_set_fill_color(ctx,GColorFromHEX(d->bg));rclock(ctx,d,63,47,digit);
  rt(ctx,date,23,132,134,0,d->fg);rbat(ctx,d,150);return;
 }
 if(style==4){
  rt(ctx,"HI-FI",45,13,90,0,d->accent);
  rfill(ctx,16,39,68,35,3,rmix(d->bg,d->fg));rfill(ctx,96,39,68,35,3,rmix(d->bg,d->fg));
  for(int i=0;i<8;i++){rline(ctx,22+i*7,43,22+i*7,47,1,d->accent);rline(ctx,102+i*7,43,102+i*7,47,1,d->accent);}
  if(d->seconds)rline(ctx,50,60,24+d->now.tm_sec*49/59,43,1,d->fg);
  rline(ctx,130,60,102+d->now.tm_min*49/59,43,1,d->fg);
  rt(ctx,d->seconds?"SEC":"OFF",24,59,52,0,d->fg);rt(ctx,"MIN",104,59,52,0,d->fg);
  graphics_context_set_fill_color(ctx,GColorFromHEX(d->fg));rclock(ctx,d,80,38,digit);rperiod(ctx,d,119);
  rt(ctx,date,24,136,132,0,d->fg);rbat(ctx,d,153);return;
 }
 if(style==5){
  int hour=rhour(d);graphics_context_set_fill_color(ctx,GColorFromHEX(d->fg));
  digit(ctx,hour/10,24+d->hour_shift,32,39,53);digit(ctx,hour%10,67+d->hour_shift,32,39,53);
  digit(ctx,d->now.tm_min/10,24+d->minute_shift,95,39,53);digit(ctx,d->now.tm_min%10,67+d->minute_shift,95,39,53);
  rline(ctx,113,39,113,143,1,d->accent);
  const char *days[]={"SUN","MON","TUE","WED","THU","FRI","SAT"},*months[]={"JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"};
  if(d->date_mode){
   rt(ctx,days[d->now.tm_wday],116,43,44,0,d->fg);
   char a[12],b[12],c[12];
   if(d->date_mode==1){snprintf(a,sizeof(a),"%s",months[d->now.tm_mon]);snprintf(b,sizeof(b),"%02d",d->now.tm_mday);c[0]=0;}
   else if(d->date_mode==2){snprintf(a,sizeof(a),"%04d",d->now.tm_year+1900);snprintf(b,sizeof(b),"%02d",d->now.tm_mon+1);snprintf(c,sizeof(c),"%02d",d->now.tm_mday);}
   else{snprintf(a,sizeof(a),"%02d",d->date_mode==3?d->now.tm_mon+1:d->now.tm_mday);snprintf(b,sizeof(b),"%02d",d->date_mode==3?d->now.tm_mday:d->now.tm_mon+1);snprintf(c,sizeof(c),"%04d",d->now.tm_year+1900);}
   rt(ctx,a,116,60,44,0,d->fg);rt(ctx,b,116,77,44,0,d->fg);rt(ctx,c,116,94,44,0,d->fg);
  }
  if(!r24(d->time_mode))rt(ctx,d->now.tm_hour>=12?"PM":"AM",116,111,44,0,d->fg);
  rt(ctx,charge,116,129,44,0,d->fg);rfill(ctx,122,148,28,2,0,rmix(d->bg,d->fg));if(d->now.tm_min)rfill(ctx,122,148,28*d->now.tm_min/59,2,0,d->accent);return;
 }
 if(style==6 || style==8){
  if(style==8)rt(ctx,">",35,28,25,1,d->accent);
  graphics_context_set_fill_color(ctx,GColorFromHEX(d->fg));rclock(ctx,d,68,42,digit);
  if(style==8 && d->phase%2==0)rfill(ctx,162,69,5,40,0,d->accent);
  rperiod(ctx,d,112);rt(ctx,date,24,131,132,0,d->fg);
  for(int x=40;x<=140;x+=5){if(style==6)rdisk(ctx,x,151,1,d->accent);else rfill(ctx,x,151,3,1,0,d->accent);}
  rbat(ctx,d,156);return;
 }
 if(style==7){
  rperiod(ctx,d,23);rfill(ctx,14,53,72,73,5,d->fg);rfill(ctx,94,53,72,73,5,d->accent);
  int h=rhour(d);graphics_context_set_fill_color(ctx,GColorFromHEX(d->bg));digit(ctx,h/10,19+d->hour_shift,63,29,43);digit(ctx,h%10,51+d->hour_shift,63,29,43);rt(ctx,"HOUR",22,106,55,0,d->bg);
  graphics_context_set_fill_color(ctx,GColorFromHEX(d->fg));digit(ctx,d->now.tm_min/10,99+d->minute_shift,63,29,43);digit(ctx,d->now.tm_min%10,131+d->minute_shift,63,29,43);rt(ctx,"MIN",102,106,55,0,d->fg);
  rt(ctx,date,24,135,132,0,d->fg);rbat(ctx,d,154);return;
 }
 if(style==9){
  rline(ctx,39,32,141,32,2,d->accent);if(!r24(d->time_mode))rlabel(ctx,d,d->now.tm_hour>=12?"PM":"AM",55,34,70,0,d->fg);graphics_context_set_fill_color(ctx,GColorFromHEX(d->fg));rclock(ctx,d,59,49,digit);
  rline(ctx,20,119,160,119,1,d->fg);rlabel(ctx,d,date,23,128,134,0,d->fg);rline(ctx,40,149,140,149,1,d->fg);rlabel(ctx,d,"BATTERY",43,153,60,0,d->fg);rlabel(ctx,d,charge,106,153,35,0,d->accent);return;
 }
 if(style==10){
  rcircle(ctx,90,90,86,2,d->accent);rt(ctx,"CLASSIC LCD",30,25,120,0,d->accent);rfill(ctx,10,54,160,73,5,d->bg);
  rline(ctx,20,58,160,58,1,0xAA0000);rline(ctx,20,126,160,126,1,0xAA0000);
  graphics_context_set_fill_color(ctx,GColorFromHEX(d->fg));
  // Main time leaves a dedicated right-hand cell for seconds.
  int h=rhour(d),n[]={h/10,h%10,d->now.tm_min/10,d->now.tm_min%10},x[]={17,43,84,110};
  for(int i=0;i<4;i++)digit(ctx,n[i],x[i],72,23,42);
  rfill(ctx,72,84,3,3,0,d->fg);rfill(ctx,72,99,3,3,0,d->fg);
  if(d->seconds){graphics_context_set_fill_color(ctx,GColorFromHEX(d->fg));digit(ctx,d->now.tm_sec/10,140,91,10,22);digit(ctx,d->now.tm_sec%10,153,91,10,22);}
  rperiod(ctx,d,114);rt(ctx,date,25,135,130,0,d->fg);rbat(ctx,d,153);return;
 }
 if(style==11){
  // Two compact instruments occupy the safe upper chord.
  for(int i=0;i<12;i++){int a=i*300;GPoint p=rpolar(58,43,a,23),q=rpolar(58,43,a,20);graphics_context_set_stroke_color(ctx,GColorFromHEX(d->fg));graphics_context_set_stroke_width(ctx,1);graphics_draw_line(ctx,p,q);}
  graphics_context_set_stroke_color(ctx,GColorFromHEX(d->fg));graphics_context_set_stroke_width(ctx,rr(2));graphics_draw_line(ctx,rp(58,43),rpolar(58,43,(d->other.tm_hour%12)*300+d->other.tm_min*5,13));graphics_draw_line(ctx,rp(58,43),rpolar(58,43,d->other.tm_min*60,19));
  const char *map[]={
 "........###..................####.........",
 ".....#########.......##....########.......",
 "...#############....#################.....",
 "..############.....####################...",
 "...#########.......###################....",
 "....#######.........################......",
 ".....######...........##############......",
 ".......###.........#########.#######......",
 "........###........########...######......",
 ".........####.......#######...#####.......",
 "..........#####......######....###........",
 "..........######.....#####......##........",
 "...........#####......####.......##.......",
 "...........####.......###.................",
 "...........###.........#.......######.....",
 "...........###................########....",
 "...........##..................######.....",
 "............#....................##.......",
 "....................................##....",
 ".........................................."};
  for(int y=0;y<20;y++)for(int x=0;x<42;x++)if(map[y][x]=='#')rfill(ctx,103+x,28+y,1,1,0,d->fg);
  rt(ctx,"WORLD",101,49,55,0,d->fg);
  rline(ctx,22,70,158,70,1,d->fg);graphics_context_set_fill_color(ctx,GColorFromHEX(d->fg));
  int h=rhour(d),n[]={h/10,h%10,d->now.tm_min/10,d->now.tm_min%10},xs[]={17,43,84,110};for(int i=0;i<4;i++)digit(ctx,n[i],xs[i],80,23,37);
  rfill(ctx,72,91,3,3,0,d->fg);rfill(ctx,72,104,3,3,0,d->fg);
  if(d->seconds){graphics_context_set_fill_color(ctx,GColorFromHEX(d->fg));digit(ctx,d->now.tm_sec/10,140,96,10,21);digit(ctx,d->now.tm_sec%10,153,96,10,21);}
  rperiod(ctx,d,116);
  char zone[40];int off=(d->zone-48)*15,abs=off<0?-off:off;
  if(off==0)snprintf(zone,sizeof(zone),"UTC  %02d:%02d",d->other.tm_hour,d->other.tm_min);else snprintf(zone,sizeof(zone),"%c%02d:%02d  %02d:%02d",off<0?'-':'+',abs/60,abs%60,d->other.tm_hour,d->other.tm_min);
  rt(ctx,zone,25,130,130,0,d->fg);char dated[48];if(d->phase)snprintf(dated,sizeof(dated),"%s %+dd",date,d->phase);else snprintf(dated,sizeof(dated),"%s",date);rt(ctx,dated,28,146,124,0,d->fg);rt(ctx,charge,66,161,48,0,d->fg);return;
 }
}
#endif
