#include <pebble.h>
#include "config.h"
#include "policy.h"
#include "city_policy.h"
#include "board_policy.h"
#include "microfont.h"
// Retired settings retain their numbers so existing installations remain compatible.
enum {P_PALETTE=1,P_BG,P_FG,P_ACCENT,P_TIME,P_DATE,P_SECONDS,P_ZONE,P_THEME,P_HOME,P_AWAY,P_HSTART,P_HEND,P_ASTART,P_AEND,P_TRAVEL,P_FLAP};
typedef struct {int theme,bg,fg,accent,format,date,seconds,home,away,flap;} Settings;
static Settings s={0,0,0xFFAA00,0x555555,0,1,0,0,1,1};
static Window *window;static Layer *face;static AppTimer *timer;
static bool valid=false,focused=true,animating=false,initialized=false;
static uint32_t started,utc_now;static WTCivil home_time,away_time;
static char previous[2][5],current[2][5];
#if WORLD_FIXTURE
static uint32_t f_epoch=1794069720u;static int f_phase=-1,f_format=2;static uint32_t f_previous;
#endif
static uint32_t bg(void){return s.theme==0?0:s.theme==1?0xAAAA55:(uint32_t)s.bg;}
static uint32_t fg(void){return s.theme==0?0xFFAA00:s.theme==1?0:(uint32_t)s.fg;}
static uint32_t edge(void){return s.theme==0?0x555555:s.theme==1?0x555500:(uint32_t)s.accent;}
static GColor readable(uint32_t requested){GColor c=GColorFromHEX(requested),b=GColorFromHEX(bg());if(c.argb==b.argb)c=(299*b.r+587*b.g+114*b.b>1500)?GColorBlack:GColorWhite;return c;}
static uint32_t milliseconds(void){time_t sec;uint16_t ms;time_ms(&sec,&ms);return (uint32_t)sec*1000+ms;}
static void rect(GContext *ctx,int x,int y,int w,int h,GColor color){if(w<=0||h<=0)return;graphics_context_set_fill_color(ctx,color);graphics_fill_rect(ctx,GRect(x,y,w,h),0,GCornerNone);}
static void rule(GContext *ctx,int x,int y,int width,GColor color){rect(ctx,x,y,width,1,color);}
static int glyph(char c,int row){
 if(c=='0')return row==0||row==6?14:17;
 int i=c>='A'&&c<='Z'?c-'A':c>='0'&&c<='9'?26+c-'0':c==':'?36:c=='+'?37:c=='-'?38:c=='/'?39:-1;
 return i<0?0:MF[i][row];
}
static void text(GContext *ctx,const char *value,int x,int y,int align,GColor color){
 int length=strlen(value),width=length?length*6-1:0;if(align==1)x-=width/2;else if(align==2)x-=width;
 for(int i=0;i<length;i++)for(int row=0;row<7;row++){int bits=glyph(value[i],row);for(int col=0;col<5;col++)if(bits&(1<<(4-col)))rect(ctx,x+i*6+col,y+row,1,1,color);}
}
static bool use24(void){
#if WORLD_FIXTURE
 return f_format==2;
#else
 return uses_24(s.format,clock_is_24h_style());
#endif
}
static void date_text(const WTCivil *tm,char *out,size_t n){
 static const char *days[]={"SUN","MON","TUE","WED","THU","FRI","SAT"};
 static const char *months[]={"JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"};
 if(s.date==0)out[0]=0;
 else if(s.date==1)snprintf(out,n,"%s %02d %s",days[tm->weekday],tm->day,months[tm->month-1]);
 else if(s.date==2)snprintf(out,n,"%04d-%02d-%02d",tm->year,tm->month,tm->day);
 else if(s.date==3)snprintf(out,n,"%02d/%02d/%04d",tm->month,tm->day,tm->year);
 else snprintf(out,n,"%02d/%02d/%04d",tm->day,tm->month,tm->year);
}
// Render one source panel into its hinged destination; nearest-row projection keeps
// every output on the actual native pixel grid. Source glyphs never stretch sideways.
static void panel(GContext *ctx,char c,int x,int y,int scale,int from,int count,int dest,int height,GColor ink,GColor paper){
 if(height<=0)return;
 int width=5*scale+6;
 rect(ctx,x+1,y+dest,width,height,paper);
 for(int dy=0;dy<height;dy++){
  int source=from+dy*count/height;int gy=source-5;
  if(gy<0||gy>=7*scale)continue;
  int bits=glyph(c,gy/scale);
  for(int col=0;col<5;col++)if(bits&(1<<(4-col)))rect(ctx,x+4+col*scale,y+dest+dy,scale,1,ink);
 }
}
static void tile(GContext *ctx,char old,char now,int x,int y,int scale,int phase,GColor ink,GColor paper,GColor border){
 int cw=5*scale+8,height=7*scale+10,hinge=5+3*scale+1;
 rect(ctx,x,y,cw,height,paper);rule(ctx,x,y,cw,border);rule(ctx,x,y+height-1,cw,border);rect(ctx,x,y,1,height,border);rect(ctx,x+cw-1,y,1,height,border);
 if(old==now||phase>=1000||phase<=0){char c=phase<=0?old:now;panel(ctx,c,x,y,scale,1,height-2,1,height-2,ink,paper);}
 else{
  panel(ctx,now,x,y,scale,1,hinge-1,1,hinge-1,ink,paper);
  panel(ctx,old,x,y,scale,hinge+1,height-hinge-2,hinge+1,height-hinge-2,ink,paper);
  if(phase<500){int h=(hinge-1)*(500-phase)/500;panel(ctx,old,x,y,scale,1,hinge-1,hinge-h,h,ink,paper);}
  else{int h=(height-hinge-2)*(phase-500)/500;panel(ctx,now,x,y,scale,hinge+1,height-hinge-2,hinge+1,h,ink,paper);}
 }
 rule(ctx,x+1,y+hinge,cw-2,paper);rect(ctx,x+1,y+hinge,1,1,ink);rect(ctx,x+cw-2,y+hinge,1,1,ink);
}
static void board_clock(GContext *ctx,WTBoard b,int row,int elapsed,GColor ink,GColor paper,GColor border){
 int cw=5*b.scale+8,gap=3,colon=7,total=4*cw+3*gap+colon,x=(b.width-total)/2;
 for(int i=0;i<4;i++){
  if(i==2){rect(ctx,x+2,b.tile[row]+3*b.scale,2,2,ink);rect(ctx,x+2,b.tile[row]+5*b.scale,2,2,ink);x+=colon;}
  tile(ctx,previous[row][i],current[row][i],x,b.tile[row],b.scale,wt_flap_phase(elapsed,row),ink,paper,border);x+=cw+gap;
 }
}
static void draw(Layer *layer,GContext *ctx){
 GRect bounds=layer_get_bounds(layer);WTBoard b=wt_board(bounds.size.w,bounds.size.h);GColor paper=GColorFromHEX(bg()),ink=readable(fg()),border=readable(edge());
 graphics_context_set_antialiased(ctx,false);rect(ctx,0,0,b.width,b.height,paper);text(ctx,"WORLD TIMER",b.width/2,b.head,1,ink);
 if(!valid){text(ctx,"ZONE DATA EXPIRED",b.width/2,b.label[0],1,ink);text(ctx,"UPDATE REQUIRED",b.width/2,b.label[1],1,ink);return;}
 char label[32],difference[16];date_text(&home_time,label,sizeof(label));text(ctx,label,b.width/2,b.head+12,1,ink);
 int a,b_offset;wt_offset(s.home,utc_now,&a);wt_offset(s.away,utc_now,&b_offset);wt_difference(b_offset-a,difference,sizeof(difference));
 int elapsed=animating?(int)(milliseconds()-started):WT_BOARD_MS;
#if WORLD_FIXTURE
 if(f_phase>=0)elapsed=f_phase;
#endif
 for(int row=0;row<2;row++){
  const WTCity *city=&WT_CITIES[row?s.away:s.home];const char *status=row?difference:"MAIN";
  int capacity=(b.width-2*b.margin-((int)strlen(status)*6-1)-8)/6;
  const char *name=(int)strlen(city->name)>capacity?city->code:city->name;
  text(ctx,name,b.margin,b.label[row],0,ink);text(ctx,status,b.width-b.margin,b.label[row],2,ink);
  board_clock(ctx,b,row,elapsed,ink,paper,border);
  if(!use24())text(ctx,(row?away_time.hour:home_time.hour)>=12?"PM":"AM",b.margin+8,b.tile[row]+7*b.scale+13,0,ink);
 }
 int days=wt_day_delta(&away_time,&home_time);if(days){snprintf(label,sizeof(label),"%s%dD",days>0?"+":"",days);text(ctx,label,b.width/2,b.day,1,ink);}
 if(s.seconds){snprintf(label,sizeof(label),":%02d",home_time.second);text(ctx,label,b.width-b.margin-8,b.day,2,ink);}
}
static void stop(void){if(timer){app_timer_cancel(timer);timer=NULL;}animating=false;}
static void animation(void *context){(void)context;timer=NULL;if((uint32_t)(milliseconds()-started)>=WT_BOARD_MS){animating=false;}else{timer=app_timer_register(50,animation,NULL);if(!timer)animating=false;}if(face)layer_mark_dirty(face);}
static void refresh(bool transition){
 bool was_valid=valid;char old[2][5];memcpy(old,current,sizeof(old));utc_now=(uint32_t)time(NULL);
#if WORLD_FIXTURE
 utc_now=f_epoch;
#endif
 valid=wt_city_time(s.home,utc_now,&home_time)&&wt_city_time(s.away,utc_now,&away_time);
 if(valid){wt_clock(home_time.hour,home_time.minute,use24(),current[0]);wt_clock(away_time.hour,away_time.minute,use24(),current[1]);}
 bool changed=memcmp(old,current,sizeof(old))!=0;
 if(!valid){stop();}
 else if(!initialized||!transition){stop();memcpy(previous,current,sizeof(current));}
 else if(changed){stop();memcpy(previous,old,sizeof(old));if(was_valid&&s.flap&&focused){animating=true;started=milliseconds();timer=app_timer_register(50,animation,NULL);if(!timer)animating=false;}}
#if WORLD_FIXTURE
 if(f_previous){WTCivil prior;if(wt_city_time(s.home,f_previous,&prior))wt_clock(prior.hour,prior.minute,use24(),previous[0]);if(wt_city_time(s.away,f_previous,&prior))wt_clock(prior.hour,prior.minute,use24(),previous[1]);}
#endif
 initialized=true;if(face)layer_mark_dirty(face);
}
static void tick(struct tm *tm,TimeUnits units){(void)tm;(void)units;refresh(true);}
static void focus_changed(bool value){focused=value;if(!value)stop();else refresh(false);}
static bool setting(DictionaryIterator *iter,int key,int storage,int maximum,int *value){Tuple *t=dict_find(iter,key);if(!t||(t->type!=TUPLE_INT&&t->type!=TUPLE_UINT)||t->value->int32<0||t->value->int32>maximum)return false;*value=t->value->int32;persist_write_int(storage,*value);return true;}
static void inbox(DictionaryIterator *iter,void *context){
 (void)context;setting(iter,MESSAGE_KEY_TimeFormat,P_TIME,2,&s.format);setting(iter,MESSAGE_KEY_DateFormat,P_DATE,4,&s.date);setting(iter,MESSAGE_KEY_ShowSeconds,P_SECONDS,1,&s.seconds);
 setting(iter,MESSAGE_KEY_Background,P_BG,0xFFFFFF,&s.bg);setting(iter,MESSAGE_KEY_Foreground,P_FG,0xFFFFFF,&s.fg);setting(iter,MESSAGE_KEY_Accent,P_ACCENT,0xFFFFFF,&s.accent);
 setting(iter,MESSAGE_KEY_Theme,P_THEME,2,&s.theme);setting(iter,MESSAGE_KEY_MainCity,P_HOME,WT_CITY_COUNT-1,&s.home);setting(iter,MESSAGE_KEY_OtherCity,P_AWAY,WT_CITY_COUNT-1,&s.away);setting(iter,MESSAGE_KEY_FlapOn,P_FLAP,1,&s.flap);
 bool transition=false;
#if WORLD_FIXTURE
 Tuple *t;if((t=dict_find(iter,11000)))f_epoch=(uint32_t)t->value->int32;if((t=dict_find(iter,11001)))f_phase=t->value->int32;if((t=dict_find(iter,11002)))f_format=t->value->int32;if((t=dict_find(iter,11004)))f_previous=(uint32_t)t->value->int32;
 transition=dict_find(iter,11003)!=NULL;
#endif
 tick_timer_service_unsubscribe();tick_timer_service_subscribe(s.seconds?SECOND_UNIT:MINUTE_UNIT,tick);refresh(transition);
}
static void load(Window *w){face=layer_create(layer_get_bounds(window_get_root_layer(w)));layer_set_update_proc(face,draw);layer_add_child(window_get_root_layer(w),face);refresh(false);}
static void unload(Window *w){(void)w;layer_destroy(face);face=NULL;}
static void read_setting(int key,int max,int *target){if(persist_exists(key)){int v=persist_read_int(key);if(v>=0&&v<=max)*target=v;}}
static void init(void){
 read_setting(P_BG,0xFFFFFF,&s.bg);read_setting(P_FG,0xFFFFFF,&s.fg);read_setting(P_ACCENT,0xFFFFFF,&s.accent);read_setting(P_TIME,2,&s.format);read_setting(P_DATE,4,&s.date);read_setting(P_SECONDS,1,&s.seconds);
 if(!persist_exists(P_THEME)&&persist_read_int(P_PALETTE)==6)s.theme=2;
 read_setting(P_THEME,2,&s.theme);read_setting(P_HOME,WT_CITY_COUNT-1,&s.home);read_setting(P_AWAY,WT_CITY_COUNT-1,&s.away);read_setting(P_FLAP,1,&s.flap);
 window=window_create();window_set_window_handlers(window,(WindowHandlers){.load=load,.unload=unload});window_stack_push(window,true);
 app_message_register_inbox_received(inbox);app_message_open(512,512);tick_timer_service_subscribe(s.seconds?SECOND_UNIT:MINUTE_UNIT,tick);app_focus_service_subscribe(focus_changed);
}
static void deinit(void){stop();app_focus_service_unsubscribe();tick_timer_service_unsubscribe();app_message_deregister_callbacks();window_destroy(window);}
int main(void){init();app_event_loop();deinit();}
