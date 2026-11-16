#include "board_policy.h"
#include <stdio.h>
WTBoard wt_board(int width,int height){
 if(width==180)return (WTBoard){180,180,24,17,{43,101},{56,114},3,152};
 if(width==260)return (WTBoard){260,260,34,26,{65,145},{81,161},5,213};
 return (WTBoard){200,height,16,15,{47,129},{62,144},4,189};
}
void wt_difference(int minutes,char *out,size_t size){
 char sign=minutes<0?'-':'+';int magnitude=minutes<0?-minutes:minutes;
 if(magnitude%60)snprintf(out,size,"%c%d:%02dH",sign,magnitude/60,magnitude%60);
 else snprintf(out,size,"%c%dH",sign,magnitude/60);
}
void wt_clock(int hour,int minute,bool twenty_four,char out[5]){
 if(!twenty_four)hour=hour%12?hour%12:12;
 out[0]=(!twenty_four&&hour<10)?' ':'0'+hour/10;out[1]='0'+hour%10;
 out[2]='0'+minute/10;out[3]='0'+minute%10;out[4]=0;
}
int wt_flap_phase(int elapsed,int row){
 int phase=elapsed-row*WT_ROW_DELAY_MS;
 if(phase<=0)return 0;
 if(phase>=WT_FLAP_MS)return 1000;
 return phase*1000/WT_FLAP_MS;
}
