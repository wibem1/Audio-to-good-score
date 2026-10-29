"""Real exports through the browser JSON dispatcher."""
import base64,io,json,unittest
from pathlib import Path
import mido
from musiccraft.web_bridge import dispatch
from musiccraft.compact import pack
from musiccraft.contracts import ContractError
ROOT=Path(__file__).resolve().parents[1]
class WebBridge(unittest.TestCase):
 def plan(self):return json.loads((ROOT/'tests/fixtures/composition-plan.json').read_text())
 def test_real_export(self):
  r=dispatch({'action':'plan','document':self.plan()});m=mido.MidiFile(file=io.BytesIO(base64.b64decode(r['midi'])))
  self.assertEqual(sum(e.type=='note_on' and e.velocity>0 for t in m.tracks for e in t),len(r['plan']['notes']))
  self.assertIn('<score-partwise',r['musicxml']);self.assertTrue(r['report'])
 def test_compact_free_plan(self):
  r=dispatch({'action':'plan','document':pack(self.plan()),'analysis':{'unrelated':'unused'}});self.assertEqual(r['plan'],self.plan())
 def test_bad_rhythm(self):
  p=self.plan();p['notes'].pop(0)
  with self.assertRaises(ContractError):dispatch({'action':'plan','document':p})
 def test_preanalysis_uncertainty(self):
  r=dispatch({'action':'plan','document':self.plan()})
  a=dispatch({'action':'preliminary','midi':r['midi'],'range':[0,1],'kind':'midi','sha256':'a'*64})
  self.assertEqual(a['sources'][0]['sha256'],'a'*64);self.assertTrue(a['content']['observations'])
  self.assertTrue(all(o['pitch_certainty']=='low' for o in a['content']['observations']));self.assertEqual(a['timing_hypotheses'],[])
  self.assertEqual(dispatch({'action':'analysis','document':pack(a)})['analysis'],a)
 def test_bad_range(self):
  r=dispatch({'action':'plan','document':self.plan()})
  with self.assertRaises(ContractError):dispatch({'action':'preliminary','midi':r['midi'],'range':[0,61],'kind':'midi','sha256':'a'*64})
 def test_sha256_fallback(self):
  self.assertEqual(dispatch({'action':'hash','data':'YWJj'})['sha256'],'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
 def test_no_code_execution(self):
  with self.assertRaises(ContractError):dispatch({'action':'exec','code':'print(1)'})
if __name__=='__main__':unittest.main()
