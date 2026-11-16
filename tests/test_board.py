"""Exercise the native board policy at signed-offset, layout and animation boundaries."""
from pathlib import Path
import subprocess,unittest
ROOT=Path(__file__).resolve().parents[1]
class BoardTest(unittest.TestCase):
 def test_board_boundaries(self):
  source=ROOT/'.tmp/board-test.c';binary=ROOT/'.tmp/board-test'
  source.write_text(r'''#include <assert.h>
#include <string.h>
#include "board_policy.h"
#include "city_policy.h"
int main(void){
 char value[20],clock[5];
 int differences[]={900,-900,0,345,-345,30,-30,1560,-1560};
 const char *expected[]={"+15H","-15H","+0H","+5:45H","-5:45H","+0:30H","-0:30H","+26H","-26H"};
 for(int i=0;i<9;i++){wt_difference(differences[i],value,sizeof(value));assert(!strcmp(value,expected[i]));}
 wt_clock(0,0,true,clock);assert(!strcmp(clock,"0000"));wt_clock(0,0,false,clock);assert(!strcmp(clock,"1200"));
 wt_clock(13,59,false,clock);assert(!strcmp(clock," 159"));wt_clock(23,59,true,clock);assert(!strcmp(clock,"2359"));
 for(int h=0;h<24;h++)for(int m=0;m<60;m++)for(int f=0;f<2;f++){wt_clock(h,m,f,clock);assert(strlen(clock)==4);assert(clock[2]>='0'&&clock[2]<='5');}
 for(int row=0;row<2;row++){int prior=-1;for(int t=-100;t<1000;t++){int p=wt_flap_phase(t,row);assert(p>=prior&&p>=0&&p<=1000);prior=p;}assert(wt_flap_phase(WT_BOARD_MS,row)==1000);}
 assert(wt_flap_phase(90,1)==0);assert(wt_flap_phase(300,0)==500);assert(wt_flap_phase(390,1)==500);
 int widths[]={200,180,260},heights[]={228,180,260};
 for(int i=0;i<3;i++){WTBoard b=wt_board(widths[i],heights[i]);assert(b.width==widths[i]&&b.height==heights[i]);int cw=5*b.scale+8,total=4*cw+16,left=(b.width-total)/2;assert(left>=0);for(int row=0;row<2;row++){assert(b.label[row]+7<b.tile[row]);assert(b.tile[row]+7*b.scale+10<b.height);if(i){int xs[]={left,b.width-left-1};int ys[]={b.tile[row],b.tile[row]+7*b.scale+9};for(int x=0;x<2;x++)for(int y=0;y<2;y++){int dx=xs[x]-b.width/2,dy=ys[y]-b.height/2;assert(dx*dx+dy*dy<(b.width/2)*(b.width/2));}}}assert(b.day+7<b.height);}
 // Chicago/Tokyo difference changes at Chicago's actual DST boundary.
 int a,b;assert(wt_offset(0,1772956740u,&a));assert(wt_offset(1,1772956740u,&b));assert(b-a==900);
 assert(wt_offset(0,1772956800u,&a));assert(wt_offset(1,1772956800u,&b));assert(b-a==840);
 return 0;
}''')
  subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-Iwatchface/src/c',str(source),'watchface/src/c/board_policy.c','watchface/src/c/city_policy.c','watchface/src/c/city_data.c','-o',str(binary)],cwd=ROOT,check=True)
  subprocess.run([str(binary)],check=True)
if __name__=='__main__':unittest.main()
