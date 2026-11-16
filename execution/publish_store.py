"""Publish reviewed World Timer bytes once; independently verify public media afterward.

Run using the installed Pebble tool Python environment for SDK account authentication.
No .env or waf locks are read. POSTs are guarded and never retried automatically.
"""
from pathlib import Path
import argparse,hashlib,io,json,mimetypes,re,sys,time,zipfile
from contextlib import ExitStack
import requests
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'execution'))
from publish_watchface_updates import account_mapping,fetch,save
from pebble_tool.commands.publish import PublishCommand
STATE=ROOT/'.tmp/store-0.2.0'
UUID='0bd9074a-d5df-4b6b-99e7-90b829ab2aa7'
API='https://appstore-api.repebble.com'
PLATFORMS={'emery':(200,228),'chalk':(180,180),'gabbro':(260,260)}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def mapping_id(mapping):return PublishCommand._lookup_app_id_case_insensitive(mapping,UUID)
def make_plan():
 token,mapping=account_mapping();actual=mapping_id(mapping)
 assert actual=='dc42aa6ca1cf447785720f80', 'Existing listing identity changed'
 version=json.loads((ROOT/'watchface/package.json').read_text())['version']
 path=ROOT/f'dist/World-Timer-{version}.pbw'
 assets=[]
 assets += sorted((ROOT/'media/store/combined-0.2.0').glob('emery_*.gif'))+sorted((ROOT/'media/store/combined-0.2.0').glob('chalk_*.gif'))+sorted((ROOT/'media/store/combined-0.2.0').glob('gabbro_*.gif'))
 plan={'uuid':UUID,'version':version,'artifact':str(path),'sha256':digest(path),'app_id':'dc42aa6ca1cf447785720f80','description_sha256':digest(ROOT/'media/store/description.txt'),'assets':[{'path':str(p),'sha256':digest(p)} for p in assets],'release_notes':'New map and twin-city layout, 40 IANA cities with DST, daily call windows, amber/olive/custom colors, and double-knock travel. Open settings after updating to choose cities and call hours.'}
 validate(plan);save(STATE/'plan.json',plan);save(ROOT/'release/combined-update/0.2.0/store-plan.json',plan);print('PLAN READY',version,plan['sha256'],len(assets),'media files')
 return plan
def validate(plan):
 assert plan['uuid']==UUID and plan['version']=='0.2.0'
 artifact=Path(plan['artifact']);assert digest(artifact)==plan['sha256']=='fb48e1d9a3a15d448b0d3533c8050f03c330a09e22a9c8ebb1ca5842fdb87ab2'
 with zipfile.ZipFile(artifact) as bundle:
  meta=json.loads(bundle.read('appinfo.json'));assert meta['uuid']==UUID and meta['versionLabel']==plan['version']
  assert set(meta['targetPlatforms'])==set(PLATFORMS);assert meta['watchapp']['watchface']
  for platform in PLATFORMS:
   data=bundle.read(platform+'/pebble-app.bin');assert data and b'WT knock' not in data
 assert digest(ROOT/'media/store/description.txt')==plan['description_sha256']
 assert len(plan['assets'])==12
 for value in plan['assets']:
  path=Path(value['path']);assert digest(path)==value['sha256']
  with Image.open(path) as image:
   if path.name.startswith('icon-'):assert image.size==((80,80) if path.name=='icon-small.png' else (144,144))
   else:
    platform=path.name.split('_')[0];assert image.size==PLATFORMS[platform]
    assert image.n_frames>1 if '_01_' in path.name else image.n_frames==1
 for platform in PLATFORMS:assert len([a for a in plan['assets'] if Path(a['path']).name.startswith(platform+'_')])==4
 assert not json.loads((ROOT/'.tmp/last-build.json').read_text())['fixture']
def publish(plan):
 validate(plan);receipt=ROOT/'release/combined-update/0.2.0/store-release.json';guard=STATE/'inflight.json'
 if receipt.exists():print('Existing receipt: skipping POST');return
 if guard.exists():raise RuntimeError('Ambiguous previous POST; reconcile before retry')
 token,mapping=account_mapping()
 assert mapping_id(mapping)==plan['app_id'], 'Account UUID mapping changed'
 save(guard,{'uuid':UUID,'version':plan['version'],'pbw_sha256':plan['sha256'],'started_at':time.time()})
 data={'version':plan['version'],'releaseNotes':plan['release_notes'],'isPublished':'true','replaceScreenshots':'true','name':'World Timer','type':'watchface','expectedUuid':UUID,'description':(ROOT/'media/store/description.txt').read_text(),'source':'','visible':'true'}
 with ExitStack() as stack:
  paths=[('pbwFile',Path(plan['artifact']))]
  for a in plan['assets']:
   path=Path(a['path']);field='iconSmall' if path.name=='icon-small.png' else 'iconLarge' if path.name=='icon-large.png' else 'screenshots_'+path.name.split('_')[0]
   paths.append((field,path))
  files=[(field,(path.name,stack.enter_context(path.open('rb')),mimetypes.guess_type(path.name)[0] or 'application/octet-stream')) for field,path in paths]
  try:response=requests.post(API+'/api/dashboard/apps/'+plan['app_id']+'/releases',headers={'Authorization':'Bearer '+token},data=data,files=files,timeout=(15,300))
  except requests.RequestException:raise RuntimeError('POST outcome ambiguous; guard retained; do not retry') from None
 if not response.ok:
  save(STATE/'upload-error.json',{'status':response.status_code,'body':response.text[:1500]});raise RuntimeError(f'POST HTTP{response.status_code}; guard retained')
 payload=response.json();save(STATE/'response.json',payload)
 app_id=plan['app_id']
 if not app_id:raise RuntimeError('Missing app id; reconcile saved response')
 result={'name':'World Timer','app_id':app_id,'uuid':UUID,'version':plan['version'],'url':f'https://apps.repebble.com/{app_id}','pbw_sha256':plan['sha256'],'public_verified':False,'screenshot_results':payload.get('screenshotResults',{})}
 save(receipt,result);save(STATE/'receipt.json',result);guard.unlink();print('PUBLISHED',result['url'])
 failed=result['screenshot_results'].get('failed',[])
 if failed:raise RuntimeError('Listing created but media failed; do not create another release')
def frames(data):
 with Image.open(io.BytesIO(data)) as im:
  result=[]
  for i in range(im.n_frames):im.seek(i);result.append((im.size,im.convert('RGB').tobytes(),im.info.get('duration',0)))
 return result
def verify(plan):
 validate(plan);receipt=json.loads((ROOT/'release/combined-update/0.2.0/store-release.json').read_text());app_id=receipt['app_id'];html=fetch(receipt['url']+'?public_check='+str(time.time_ns())).decode()
 links=list(dict.fromkeys(re.findall(r'https://appstore-api\.repebble\.com/api/assets/pbw/[^"<>\\\s]+\.pbw',html)))
 downloads=[u for u in links if '/'+plan['version']+'/' in u];assert downloads,'Published version not yet present'
 remote_pbw=fetch(downloads[0]);assert hashlib.sha256(remote_pbw).hexdigest()==plan['sha256'],'Public PBW differs'
 ui=json.loads((STATE/'ui-galleries.json').read_text());results=[]
 for platform in PLATFORMS:
  urls=ui[platform];assert len(urls)==4;assert all(f'/screenshots/{app_id}/{platform}/' in u for u in urls)
  assets=[a for a in plan['assets'] if Path(a['path']).name.startswith(platform+'_')]
  remote={url:fetch(url) for url in urls}
  for i,a in enumerate(assets):
   path=Path(a['path']);expected=frames(path.read_bytes());matches=[u for u,data in remote.items() if frames(data)==expected];assert matches,f'Public native pixels/timing absent: {path.name}'
   if i==0:assert matches[0]==urls[0],'Animated preview not first'
   results.append({'local':path.name,'public':matches[0],'frames_pixels_and_timing_exact':True,'bytes_exact':hashlib.sha256(remote[matches[0]]).hexdigest()==a['sha256']})
 assert 'World Timer' in html and plan['version'] in html
 assert 'Two cities. One clear view of the day.' in html, 'Public description stale'
 assert 'Previous manual UTC offsets are replaced by explicit city choices.' in html
 proof={'url':receipt['url'],'version':plan['version'],'pbw_exact':True,'pbw_sha256':plan['sha256'],'platforms':list(PLATFORMS),'assets':results,'verified_at':time.time()}
 save(ROOT/'release/combined-update/0.2.0/public-proof.json',proof);receipt['public_verified']=True;save(ROOT/'release/combined-update/0.2.0/store-release.json',receipt);print('PUBLIC VERIFIED',receipt['url'],len(results),'native media assets')
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['prepare','validate','publish','verify']);opt=parser.parse_args()
 if opt.action=='prepare':make_plan();return
 plan=json.loads((STATE/'plan.json').read_text())
 if opt.action=='validate':validate(plan);print('PLAN VALID')
 elif opt.action=='publish':publish(plan)
 else:verify(plan)
if __name__=='__main__':main()
