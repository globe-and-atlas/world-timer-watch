#pragma once
#include <stdbool.h>
#include <stddef.h>
#define WT_FLAP_MS 600
#define WT_ROW_DELAY_MS 90
#define WT_BOARD_MS (WT_FLAP_MS+WT_ROW_DELAY_MS)
typedef struct {int width,height,margin,head,label[2],tile[2],scale,day;} WTBoard;
WTBoard wt_board(int width,int height);
void wt_difference(int minutes,char *out,size_t size);
void wt_clock(int hour,int minute,bool twenty_four,char out[5]);
int wt_flap_phase(int elapsed,int row);
