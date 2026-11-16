#pragma once
/* Round-only layout primitives. Coordinates use a 180-unit circle; bitmap glyphs
   are rasterized at the target's real pixel density (180 Chalk / 260 Gabbro). */
#if defined(PBL_ROUND)

typedef struct {
 struct tm now,other;
 uint32_t bg,fg,accent;
 int battery,time_mode,date_mode,font,layout,zone,phase;
 int hour_shift,minute_shift,clock_shift;
 void (*label)(GContext*,const char*,int,int,int,int,uint32_t);
 bool seconds,digital,show_battery;
 int dial,units,steps,temp,code,stamp;
} RoundData;
typedef void (*RoundDigit)(GContext*,int,int,int,int,int);
#if (defined(T9_FIXTURE_HOUR) && defined(T9_FIXTURE_MINUTE) && T9_FIXTURE_HOUR>=0 && T9_FIXTURE_MINUTE>=0) || MONO_FIXTURE || LCD_FIXTURE || DESK_FIXTURE || HIFI_FIXTURE || MARGIN_FIXTURE || DOT_FIXTURE || RALLY_FIXTURE || TERM_FIXTURE || LEDGER_FIXTURE || FACET_FIXTURE || RAIL_FIXTURE || CLCD_FIXTURE || WORLD_FIXTURE || TRI_FIXTURE || LUME_FIXTURE
#define ROUND_TEST 1
#else
#define ROUND_TEST 0
#endif
static int rox=0,roy=0;static bool r_proof=false,r_layout_bad=false;
static inline void rcheck(int x,int y,int w,int h){
#if ROUND_TEST
 int c=PBL_DISPLAY_WIDTH/2,r=c-1;int xx[]={x,x+w-1},yy[]={y,y+h-1};for(int i=0;i<2;i++)for(int j=0;j<2;j++){int dx=xx[i]-c,dy=yy[j]-c;if(dx*dx+dy*dy>r*r)r_layout_bad=true;}
#else
 (void)x;(void)y;(void)w;(void)h;
#endif
}
static inline int rr(int n){return n*PBL_DISPLAY_WIDTH/180;}
static inline GPoint rp(int x,int y){return GPoint(rr(x)-rr(rox),rr(y)-rr(roy));}
static inline GRect rb(int x,int y,int w,int h){return GRect(rr(x)-rr(rox),rr(y)-rr(roy),rr(w),rr(h));}
static inline uint32_t rmix(uint32_t a,uint32_t b){uint32_t v=0;for(int shift=0;shift<=16;shift+=8){int c=(((a>>shift)&255)*2+((b>>shift)&255))/3;v|=(uint32_t)(((c+42)/85)*85)<<shift;}return v;}
static inline const char *rfont(int size){
 if(size==3)return PBL_DISPLAY_WIDTH>200?FONT_KEY_GOTHIC_18:FONT_KEY_GOTHIC_14;
 if(size==0)return PBL_DISPLAY_WIDTH>200?FONT_KEY_GOTHIC_18_BOLD:FONT_KEY_GOTHIC_14_BOLD;
 if(size==1)return PBL_DISPLAY_WIDTH>200?FONT_KEY_GOTHIC_24_BOLD:FONT_KEY_GOTHIC_18_BOLD;
 return PBL_DISPLAY_WIDTH>200?FONT_KEY_BITHAM_34_MEDIUM_NUMBERS:FONT_KEY_GOTHIC_24_BOLD;
}
static inline int risqrt(int n){int lo=0,hi=256;while(lo<hi){int mid=(lo+hi+1)/2;if(mid*mid<=n)lo=mid;else hi=mid-1;}return lo;}
static inline void rt(GContext *ctx,const char *value,int x,int y,int w,int size,uint32_t ink){
 if(!value[0])return;
 const char *key=rfont(size);GFont font=fonts_get_system_font(key);
 int px=rr(x),py=rr(y),width=rr(w),center=PBL_DISPLAY_WIDTH/2,radius=center-3;
 int top=(size==0 || size==3)?(PBL_DISPLAY_WIDTH>200?5:4):6;
 int bottom=(size==0 || size==3)?(PBL_DISPLAY_WIDTH>200?17:13):(PBL_DISPLAY_WIDTH>200?23:18);
 int a=py+top-center,b=py+bottom-center,dy=abs(a)>abs(b)?abs(a):abs(b);
 int half=dy<radius?risqrt(radius*radius-dy*dy):0;
 int left=center-half,right=center+half;
 if(px<left){width-=left-px;px=left;}
 if(px+width>right)width=right-px;
 if(width<1)return;
 GSize extent=graphics_text_layout_get_content_size(value,font,GRect(0,0,512,128),GTextOverflowModeFill,GTextAlignmentCenter);
 if(extent.w>width && size!=3 && (size>0 || PBL_DISPLAY_WIDTH>200)){font=fonts_get_system_font(FONT_KEY_GOTHIC_14_BOLD);extent=graphics_text_layout_get_content_size(value,font,GRect(0,0,512,128),GTextOverflowModeFill,GTextAlignmentCenter);}
#if ROUND_TEST
 if(extent.w>width)r_layout_bad=true;
#endif
 graphics_context_set_text_color(ctx,GColorFromHEX(ink));
 graphics_draw_text(ctx,value,font,GRect(px-rr(rox),py-rr(roy),width,rr(size==2?38:25)),GTextOverflowModeTrailingEllipsis,GTextAlignmentCenter,NULL);
}
static inline void rfill(GContext *ctx,int x,int y,int w,int h,int radius,uint32_t ink){graphics_context_set_fill_color(ctx,GColorFromHEX(ink));graphics_fill_rect(ctx,rb(x,y,w,h),rr(radius),GCornersAll);}
static inline void rproof_marker(GContext *ctx){if(r_proof){rfill(ctx,89,10,2,2,0,0xFF00FF);rfill(ctx,93,10,2,2,0,r_layout_bad?0xFF0000:0x00FF00);}}
static inline void rline(GContext *ctx,int x1,int y1,int x2,int y2,int width,uint32_t ink){graphics_context_set_stroke_color(ctx,GColorFromHEX(ink));graphics_context_set_stroke_width(ctx,rr(width)>0?rr(width):1);graphics_draw_line(ctx,rp(x1,y1),rp(x2,y2));}
static inline void rcircle(GContext *ctx,int x,int y,int radius,int width,uint32_t ink){graphics_context_set_stroke_color(ctx,GColorFromHEX(ink));graphics_context_set_stroke_width(ctx,rr(width)>0?rr(width):1);graphics_draw_circle(ctx,rp(x,y),rr(radius));}
static inline void rdisk(GContext *ctx,int x,int y,int radius,uint32_t ink){graphics_context_set_fill_color(ctx,GColorFromHEX(ink));graphics_fill_circle(ctx,rp(x,y),rr(radius));}
static inline GPoint rpolar(int x,int y,int angle,int radius){int32_t a=TRIG_MAX_ANGLE*angle/3600;return GPoint(rr(x)-rr(rox)+(int32_t)sin_lookup(a)*rr(radius)/TRIG_MAX_RATIO,rr(y)-rr(roy)-(int32_t)cos_lookup(a)*rr(radius)/TRIG_MAX_RATIO);}
static inline void rpoly(GContext *ctx,GPoint *points,int count,uint32_t ink){for(int i=0;i<count;i++)rcheck(points[i].x+rr(rox),points[i].y+rr(roy),1,1);GPathInfo info={count,points};GPath *path=gpath_create(&info);graphics_context_set_fill_color(ctx,GColorFromHEX(ink));gpath_draw_filled(ctx,path);gpath_destroy(path);}
static inline void rrot(GContext *ctx,const GPoint *v,int count,int x,int y,int angle,uint32_t ink){GPoint p[20];int32_t a=TRIG_MAX_ANGLE*angle/3600,sn=sin_lookup(a),cs=cos_lookup(a);for(int i=0;i<count;i++)p[i]=GPoint(rr(x)-rr(rox)+(int32_t)(v[i].x*cs-v[i].y*sn)*PBL_DISPLAY_WIDTH/180/TRIG_MAX_RATIO,rr(y)-rr(roy)+(int32_t)(v[i].x*sn+v[i].y*cs)*PBL_DISPLAY_WIDTH/180/TRIG_MAX_RATIO);rpoly(ctx,p,count,ink);}
static inline void rclear(GContext *ctx,uint32_t bg){graphics_context_set_antialiased(ctx,false);rfill(ctx,0,0,180,180,0,bg);}
static inline bool r24(int mode){return mode==2 || (mode==0 && clock_is_24h_style());}
static inline int rhour(RoundData *d){return r24(d->time_mode)?d->now.tm_hour:(d->now.tm_hour%12?d->now.tm_hour%12:12);}
static inline void rdate(RoundData *d,char *out,size_t length){
 const char *week[]={"SUN","MON","TUE","WED","THU","FRI","SAT"};const char *months[]={"JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"};
 switch(d->date_mode){case 0:out[0]=0;break;case 1:snprintf(out,length,"%s %s %02d",week[d->now.tm_wday],months[d->now.tm_mon],d->now.tm_mday);break;case 2:snprintf(out,length,"%04d-%02d-%02d",d->now.tm_year+1900,d->now.tm_mon+1,d->now.tm_mday);break;case 3:snprintf(out,length,"%02d/%02d/%04d",d->now.tm_mon+1,d->now.tm_mday,d->now.tm_year+1900);break;default:snprintf(out,length,"%02d/%02d/%04d",d->now.tm_mday,d->now.tm_mon+1,d->now.tm_year+1900);break;}
}
static inline void rperiod(GContext *ctx,RoundData *d,int y){if(!r24(d->time_mode))rt(ctx,d->now.tm_hour>=12?"PM":"AM",55,y,70,0,d->fg);}
static inline void rbat(GContext *ctx,RoundData *d,int y){char value[12];snprintf(value,sizeof(value),"%d%%",d->battery);rline(ctx,57,y+7,78,y+7,1,d->accent);rline(ctx,57,y+14,78,y+14,1,d->accent);rline(ctx,57,y+7,57,y+14,1,d->accent);rline(ctx,78,y+7,78,y+14,1,d->accent);if(d->battery)rfill(ctx,59,y+9,17*d->battery/100,3,0,d->accent);rt(ctx,value,82,y,42,0,d->fg);}
static inline void rmask(GContext *ctx,const uint8_t *data,int sw,int sh,int stride,int x,int y,int w,int h){
 int width=rr(w),height=rr(h);for(int row=0;row<height;row++){int source_y=row*sh/height,start=-1;for(int col=0;col<=width;col++){int source_x=col*sw/width;bool on=col<width && (data[source_y*stride+source_x/8]&(0x80>>(source_x%8)));if(on && start<0)start=col;if(!on && start>=0){rcheck(rr(x)+start,rr(y)+row,col-start,1);graphics_fill_rect(ctx,GRect(rr(x)-rr(rox)+start,rr(y)-rr(roy)+row,col-start,1),0,GCornerNone);start=-1;}}}
}
static inline void rmask_bounds(const uint8_t *data,int sw,int sh,int stride,int w,int h,int *left,int *right){*left=rr(w);*right=0;for(int row=0;row<rr(h);row++)for(int col=0;col<rr(w);col++)if(data[(row*sh/rr(h))*stride+(col*sw/rr(w))/8]&(0x80>>((col*sw/rr(w))%8))){if(col<*left)*left=col;if(col>*right)*right=col;}}
static inline int rpair_shift(const uint8_t *first,const uint8_t *last,int sw,int sh,int stride,int x1,int x2,int w,int h,int center){int a,b,c,d;rmask_bounds(first,sw,sh,stride,w,h,&a,&b);rmask_bounds(last,sw,sh,stride,w,h,&c,&d);return ((2*rr(center)-1-rr(x1)-a-rr(x2)-d)/2)*180/PBL_DISPLAY_WIDTH;}
static inline void rlabel(GContext *ctx,RoundData *d,const char *text,int x,int y,int w,int size,uint32_t ink){if(d->label)d->label(ctx,text,x,y,w,size,ink);else rt(ctx,text,x,y,w,size,ink);}
static const uint8_t RSEG_MASK[10]={0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F};
static inline void rsegment(GContext *ctx,int value,int x,int y,int w,int h){
 const int v[7][6][2]={{{7,0},{27,0},{31,4},{27,8},{7,8},{3,4}},{{30,5},{34,9},{34,24},{30,29},{26,24},{26,10}},{{30,31},{34,36},{34,51},{30,57},{26,52},{26,36}},{{7,52},{27,52},{31,56},{27,60},{7,60},{3,56}},{{4,31},{8,36},{8,52},{4,57},{0,51},{0,36}},{{4,5},{8,10},{8,24},{4,29},{0,24},{0,9}},{{7,26},{27,26},{31,30},{27,34},{7,34},{3,30}}};
 for(int s=0;s<7;s++)if(RSEG_MASK[value]&(1<<s)){GPoint p[6];for(int j=0;j<6;j++)p[j]=GPoint(rr(x)+v[s][j][0]*rr(w)/34,rr(y)+v[s][j][1]*rr(h)/60);for(int j=0;j<6;j++)rcheck(p[j].x+rr(rox),p[j].y+rr(roy),1,1);GPathInfo info={6,p};GPath *path=gpath_create(&info);gpath_draw_filled(ctx,path);gpath_destroy(path);}
}
static inline void rseven(GContext *ctx,int value,int x,int y,int w,int h){rsegment(ctx,value,x,y,w,h);}
static inline void rclock(GContext *ctx,RoundData *d,int y,int height,RoundDigit digit){int h=rhour(d),n[4]={h/10,h%10,d->now.tm_min/10,d->now.tm_min%10};int xs[]={18,50,100,132};int shift=d->clock_shift;if(digit==rseven)shift=n[0]==1?-11:0;for(int i=0;i<4;i++)digit(ctx,n[i],xs[i]+shift,y,30,height);graphics_fill_rect(ctx,rb(88+shift,y+height/3,4,4),0,GCornerNone);graphics_fill_rect(ctx,rb(88+shift,y+height*2/3,4,4),0,GCornerNone);}
static inline void rweekday(GContext *ctx,RoundData *d,int y){const char *days[]={"M","T","W","T","F","S","S"};int selected=(d->now.tm_wday+6)%7;for(int i=0;i<7;i++){int x=27+i*18;if(i==selected)rfill(ctx,x,y,17,18,1,d->fg);rt(ctx,days[i],x,y-1,17,0,i==selected?d->bg:d->fg);}}
#endif
