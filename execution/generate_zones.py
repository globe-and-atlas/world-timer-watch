"""Generate offline city offsets from official IANA2026f; no host timezone fallback."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import argparse,hashlib,json,subprocess,tarfile,time
import requests
ROOT=Path(__file__).resolve().parents[1]
VERSION='2026f';URL=f'https://data.iana.org/time-zones/releases/tzdata{VERSION}.tar.gz'
START=int(datetime(2020,1,1,tzinfo=timezone.utc).timestamp());END=int(datetime(2038,1,1,tzinfo=timezone.utc).timestamp())
# Stable IDs: append new cities, never reorder this published settings catalog.
CITIES=[
 ('Chicago','CHI','America/Chicago',41.878,-87.630),('Tokyo','TYO','Asia/Tokyo',35.676,139.650),
 ('London','LON','Europe/London',51.507,-0.128),('New York','NYC','America/New_York',40.713,-74.006),
 ('Los Angeles','LAX','America/Los_Angeles',34.052,-118.244),('Denver','DEN','America/Denver',39.739,-104.990),
 ('Phoenix','PHX','America/Phoenix',33.448,-112.074),('Honolulu','HNL','Pacific/Honolulu',21.307,-157.858),
 ('Anchorage','ANC','America/Anchorage',61.218,-149.900),('Toronto','YYZ','America/Toronto',43.653,-79.383),
 ('St Johns','YYT','America/St_Johns',47.561,-52.713),('Mexico City','MEX','America/Mexico_City',19.433,-99.133),
 ('Havana','HAV','America/Havana',23.113,-82.367),('Sao Paulo','SAO','America/Sao_Paulo',-23.551,-46.633),
 ('Buenos Aires','BUE','America/Argentina/Buenos_Aires',-34.604,-58.382),('Santiago','SCL','America/Santiago',-33.449,-70.669),
 ('Paris','PAR','Europe/Paris',48.857,2.352),('Berlin','BER','Europe/Berlin',52.520,13.405),
 ('Istanbul','IST','Europe/Istanbul',41.008,28.978),('Cairo','CAI','Africa/Cairo',30.044,31.236),
 ('Casablanca','CAS','Africa/Casablanca',33.573,-7.590),('Johannesburg','JNB','Africa/Johannesburg',-26.204,28.047),
 ('Dubai','DXB','Asia/Dubai',25.205,55.271),('Delhi','DEL','Asia/Kolkata',28.614,77.209),
 ('Kathmandu','KTM','Asia/Kathmandu',27.717,85.324),('Dhaka','DAC','Asia/Dhaka',23.810,90.413),
 ('Bangkok','BKK','Asia/Bangkok',13.756,100.502),('Singapore','SIN','Asia/Singapore',1.352,103.820),
 ('Hong Kong','HKG','Asia/Hong_Kong',22.319,114.169),('Shanghai','SHA','Asia/Shanghai',31.230,121.474),
 ('Seoul','SEL','Asia/Seoul',37.566,126.978),('Sydney','SYD','Australia/Sydney',-33.869,151.209),
 ('Adelaide','ADL','Australia/Adelaide',-34.929,138.601),('Perth','PER','Australia/Perth',-31.952,115.861),
 ('Lord Howe','LDH','Australia/Lord_Howe',-31.550,159.083),('Auckland','AKL','Pacific/Auckland',-36.849,174.763),
 ('Chatham','CHT','Pacific/Chatham',-43.950,-176.550),('Apia','APW','Pacific/Apia',-13.833,-171.750),
 ('Kiritimati','CXI','Pacific/Kiritimati',1.872,-157.427),('Madrid','MAD','Europe/Madrid',40.417,-3.704)]
def prepare(fetch:bool=False)->tuple[Path,Path,str]:
 folder=ROOT/f'.tmp/tzdata-{VERSION}';folder.mkdir(parents=True,exist_ok=True);archive=folder/'source.tar.gz'
 if not archive.exists():
  if not fetch:raise RuntimeError('Run generate_zones.py --fetch to obtain the pinned official source')
  for attempt in range(3):
   try:
    r=requests.get(URL,timeout=(10,45))
    if r.status_code in {408,425,429,500,502,503,504} and attempt<2:
     retry=r.headers.get('Retry-After','');time.sleep(min(int(retry),10) if retry.isdigit() else 2**attempt);continue
    r.raise_for_status();archive.write_bytes(r.content);break
   except (requests.ConnectionError,requests.Timeout):
    if attempt==2:raise
    time.sleep(2**attempt)
 sources=['africa','antarctica','asia','australasia','europe','northamerica','southamerica','etcetera']
 with tarfile.open(archive) as tar:
  assert tar.extractfile('version').read().decode().strip()==VERSION
  for name in sources+['version','LICENSE']:(folder/name).write_bytes(tar.extractfile(name).read())
 target=folder/'zoneinfo';target.mkdir(exist_ok=True)
 subprocess.run(['zic','-b','fat','-d',str(target)]+[str(folder/name) for name in sources],check=True,timeout=60)
 return folder,target,hashlib.sha256(archive.read_bytes()).hexdigest()
def zone(root:Path,name:str)->ZoneInfo:
 with (root/name).open('rb') as f:return ZoneInfo.from_file(f,key=name)
def offset(z:ZoneInfo,t:int)->int:return int(datetime.fromtimestamp(t,timezone.utc).astimezone(z).utcoffset().total_seconds()/60)
def transitions(z:ZoneInfo)->list[tuple[int,int]]:
 out=[(START,offset(z,START))];t=START
 # Every six hours brackets offset changes; then locate the exact second.
 while t<END-1:
  end=min(t+21600,END-1);old=offset(z,t);new=offset(z,end)
  if old!=new:
   lo,hi=t,end
   while hi-lo>1:
    mid=(lo+hi)//2
    if offset(z,mid)==old:lo=mid
    else:hi=mid
   out.append((hi,new))
  t=end
 return out
def main()->None:
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--fetch',action='store_true');args=parser.parse_args();folder,zroot,digest=prepare(args.fetch)
 entries=[];cities=[]
 for name,code,key,lat,lon in CITIES:
  data=transitions(zone(zroot,key));cities.append({'name':name,'code':code,'zone':key,'lat':lat,'lon':lon,'first':len(entries),'count':len(data)});entries+=data
 header='''/* Generated by execution/generate_zones.py. Source: IANA2026f, public domain. */
#pragma once
#include <stdint.h>
#define WT_ZONE_START %du
#define WT_ZONE_END %du
#define WT_CITY_COUNT %d
#define WT_TZ_VERSION "%s"
typedef struct {uint32_t epoch;int16_t offset;} WTTransition;
typedef struct {const char *name,*code,*zone;int16_t lat,lon;uint16_t first,count;} WTCity;
extern const WTTransition WT_TRANSITIONS[];
extern const WTCity WT_CITIES[WT_CITY_COUNT];
'''%(START,END,len(cities),VERSION)
 source='#include "city_data.h"\nconst WTTransition WT_TRANSITIONS[]={\n'+''.join('{%du,%d},\n'%row for row in entries)+'};\nconst WTCity WT_CITIES[WT_CITY_COUNT]={\n'
 for c in cities:source+='{'+','.join([json.dumps(c['name'].upper()),json.dumps(c['code']),json.dumps(c['zone']),str(round(c['lat']*100)),str(round(c['lon']*100)),str(c['first']),str(c['count'])])+'},\n'
 source+='};\n'
 dest=ROOT/'watchface/src/c';(dest/'city_data.h').write_text(header);(dest/'city_data.c').write_text(source)
 js=[{'id':i,**c} for i,c in enumerate(cities)];(ROOT/'watchface/src/pkjs/cities.json').write_text(json.dumps(js,indent=2)+'\n')
 meta={'version':VERSION,'url':URL,'sha256':digest,'valid_from':START,'valid_until_exclusive':END,'cities':cities,'transitions':entries};(ROOT/'release').mkdir(exist_ok=True);(ROOT/'release/timezone-source.json').write_text(json.dumps(meta,indent=2)+'\n')
 (ROOT/'watchface/resources').mkdir(exist_ok=True)
 (ROOT/'watchface/resources/tzdata-LICENSE.txt').write_text((folder/'LICENSE').read_text())
 print('Generated',len(cities),'cities,',len(entries),'transitions, IANA',VERSION,'source SHA256',digest)
if __name__=='__main__':main()
