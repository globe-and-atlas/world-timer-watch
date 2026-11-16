"""Publishing must never repeat an ambiguous write or silently create a duplicate."""
from pathlib import Path
import importlib.util,json,tempfile,unittest
from unittest.mock import patch,Mock
import requests
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('store_pub',ROOT/'execution/publish_store.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class GuardTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.state=self.root/'state';self.state.mkdir()
  (self.root/'media/store').mkdir(parents=True);(self.root/'media/store/description.txt').write_text('Test description')
  self.artifact=self.root/'test.pbw';self.artifact.write_bytes(b'unit fixture')
  self.plan={'uuid':mod.UUID,'version':'0.2.0','sha256':'fixture','artifact':str(self.artifact),'app_id':'unit-app','assets':[],'release_notes':'test'}
  self.patches=[patch.object(mod,'ROOT',self.root),patch.object(mod,'STATE',self.state),patch.object(mod,'validate'),patch.object(mod,'account_mapping',return_value=('test-auth-placeholder',{})),patch.object(mod,'mapping_id',return_value='unit-app'),patch.object(mod.requests,'post')]
  self.mocks=[p.start() for p in self.patches];self.post=self.mocks[-1]
 def tearDown(self):
  for p in reversed(self.patches):p.stop()
  self.tmp.cleanup()
 def test_receipt_skips_post(self):
  (self.root/'release/combined-update/0.2.0').mkdir(parents=True);(self.root/'release/combined-update/0.2.0/store-release.json').write_text('{}');mod.publish(self.plan);self.post.assert_not_called()
 def test_inflight_blocks_post(self):
  (self.state/'inflight.json').write_text('{}')
  with self.assertRaisesRegex(RuntimeError,'Ambiguous'):mod.publish(self.plan)
  self.post.assert_not_called();self.assertTrue((self.state/'inflight.json').exists())
 def test_mapping_change_blocks_post(self):
  with patch.object(mod,'mapping_id',return_value='already-exists'):
   with self.assertRaisesRegex(AssertionError,'mapping changed'):mod.publish(self.plan)
  self.post.assert_not_called()
 def test_timeout_keeps_guard_no_retry(self):
  self.post.side_effect=requests.Timeout()
  with self.assertRaisesRegex(RuntimeError,'outcome ambiguous'):mod.publish(self.plan)
  self.assertEqual(self.post.call_count,1);self.assertTrue((self.state/'inflight.json').exists());self.assertFalse((self.root/'release/combined-update/0.2.0/store-release.json').exists())
 def test_rejected_write_keeps_guard(self):
  self.post.return_value=Mock(ok=False,status_code=400,text='test rejection')
  with self.assertRaisesRegex(RuntimeError,'HTTP400'):mod.publish(self.plan)
  self.assertEqual(self.post.call_count,1);self.assertTrue((self.state/'inflight.json').exists())
 def test_success_writes_receipt_and_clears_guard(self):
  response=Mock(ok=True);response.json.return_value={'app':{'id':'unit-app'}};self.post.return_value=response
  with patch.object(mod.PublishCommand,'_extract_app_id',return_value='unit-app'):mod.publish(self.plan)
  receipt=json.loads((self.root/'release/combined-update/0.2.0/store-release.json').read_text());self.assertEqual(receipt['app_id'],'unit-app');self.assertFalse((self.state/'inflight.json').exists())
  self.assertEqual(self.post.call_count,1);self.assertEqual(self.post.call_args.kwargs['data']['isPublished'],'true')
  mod.publish(self.plan);self.assertEqual(self.post.call_count,1)
if __name__=='__main__':unittest.main()
