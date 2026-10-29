import json,tempfile,unittest,copy
from pathlib import Path
from fractions import Fraction as F
from musiccraft.contracts import validate_plan,validate_analysis,ContractError,pair,digest
from musiccraft.exporter import export_plan,seconds_at
from musiccraft.analysis import alternatives
ROOT=Path(__file__).resolve().parents[1]
def fixture():return json.loads((ROOT/'tests/fixtures/composition-plan.json').read_text())
def analysis():
 return {'format':'MusicCraft-Analysis-Handoff','version':'0.3','analysis_id':'a1','revision':1,'sources':[{'id':'s1','kind':'audio','sha256':'0'*64,'range_s':[0,3]}],'source_access_allowed':False,'content':{'summary':'Synthetic uncertain phrase','findings':[{'id':'f1','feature':'harmony','value':'C','certainty':'medium','reason':'synthetic test','basis':'interpretation','depends_on':[]}],'sections':[{'id':'g1','source_id':'s1','range_s':[0,3],'development':'Second phrase changes direction'}],'observations':[{'id':'o1','source_id':'s1','time_s':.1,'section_id':'g1','slot':0,'candidate_relation':'alternatives','candidates':[{'pitch_midi':60,'strength':.7},{'pitch_midi':64,'strength':.5}],'pitch_certainty':'low','rhythm_certainty':'medium','reason':'ambiguous synthetic observation'}]},'style':{'findings':[]},'timing_hypotheses':[{'id':'h1','meter':[6,8],'pulse_duration_s':[89,500],'pulse_duration_q':[1,4],'tempo_reference_q':[3,2],'tempo_per_minute':[5000,89],'certainty':'medium'}],'open_questions':[{'id':'q1','section_id':'g1','question':'Which pitch?'}],'suitability':{'forecast':'similar','reason':'Synthetic case'},'provenance':{'method':'synthetic fixture','limitations':['not a recognition test']}}
def longnotes(p,length):
 p['notes']=[{'id':v['id'],'voice_id':v['id'],'pitch_midi':72 if v['staff']==1 else 48,'onset_q':[0,1],'duration_q':pair(length),'velocity':65,'decision_id':'d1'} for v in p['voices']];p['rests']=[];return p
class Contracts(unittest.TestCase):
 def test_analysis_unknown_is_not_rest(self):
  a=analysis();a['content']['observations'][0]['candidates']=[];self.assertIs(validate_analysis(a),a)
 def test_content_style_separate(self):
  a=analysis();a['style']['findings']=[{'id':'s2','feature':'character','value':'flowing','certainty':'medium','reason':'synthetic','basis':'interpretation','depends_on':['f1']}];validate_analysis(a)
 def test_bad_tempo_reference(self):
  a=analysis();a['timing_hypotheses'][0]['tempo_per_minute']=[84,1]
  with self.assertRaises(ContractError):validate_analysis(a)
 def test_source_range(self):
  a=analysis();a['content']['observations'][0]['time_s']=10
  with self.assertRaises(ContractError):validate_analysis(a)
 def test_cycle(self):
  a=analysis();a['content']['findings'][0]['depends_on']=['f1']
  with self.assertRaises(ContractError):validate_analysis(a)
 def test_alternatives_no_mutation(self):
  a=analysis();old=copy.deepcopy(a);v=alternatives(a);self.assertEqual([x['pitch_midi'] for x in v],[60,64]);self.assertEqual(a,old)
 def test_simultaneous_not_alternatives(self):
  a=analysis();a['content']['observations'][0]['candidate_relation']='simultaneous';self.assertEqual(alternatives(a),[])
 def test_alternatives_limit(self):
  with self.assertRaises(ContractError):alternatives(analysis(),4)
 def test_free_composition(self):validate_plan(fixture())
 def test_bound_analysis_and_stale(self):
  a=analysis();p=fixture();p['request']['mode']='imitation';p['source_analysis']={'id':'a1','revision':1,'sha256':digest(a)};validate_plan(p,a);a['revision']=2
  with self.assertRaises(ContractError):validate_plan(p,a)
 def test_imitation_needs_analysis(self):
  p=fixture();p['request']['mode']='imitation'
  with self.assertRaises(ContractError):validate_plan(p)
 def test_gap(self):
  p=fixture();p['notes'].pop(0)
  with self.assertRaises(ContractError):validate_plan(p)
 def test_overlap(self):
  p=fixture();p['notes'][1]['pitch_midi']=p['notes'][0]['pitch_midi'];p['notes'][0]['duration_q']=[1,2]
  with self.assertRaises(ContractError):validate_plan(p)
 def test_fraction_not_reduced(self):
  p=fixture();p['notes'][0]['onset_q']=[0,2]
  with self.assertRaises(ContractError):validate_plan(p)
 def test_zero_duration(self):
  p=fixture();p['notes'][0]['duration_q']=[0,1]
  with self.assertRaises(ContractError):validate_plan(p)
 def test_no_nan(self):
  a=analysis();a['content']['observations'][0]['time_s']=float('nan')
  with self.assertRaises(ContractError):validate_analysis(a)
 def test_dependent_certainty(self):
  a=analysis();a['style']['findings']=[{'id':'s2','feature':'character','value':'flowing','certainty':'high','reason':'synthetic','basis':'interpretation','depends_on':['f1']}]
  with self.assertRaises(ContractError):validate_analysis(a)
 def test_unknown_field(self):
  p=fixture();p['bpm']=84
  with self.assertRaises(ContractError):validate_plan(p)
class Migration(unittest.TestCase):
 def legacy(self):
  return {'format':'MusicCraft-Analysis-Handoff','version':'0.2','analysis_id':'legacy','revision':2,'source':{'kind':'audio','sha256':'0'*64,'range_seconds':[0,3]},'access_policy':{'composition_may_read_source':False},'summary':'Synthetic legacy analysis','global_findings':{'expression':{'value':'unknown','confidence':'low'}},'groups':[{'provisional_group':1,'range_seconds':[0,3],'phrase_observation':'A new phrase','harmony_hypothesis':'C','salient_pitch_material':[60],'bass_octave_hypothesis':[36,48],'basis':'synthetic inference'}],'observations':{'rows':[[.1,1,0,[[60,.8],[64,.2]]]],'confidence':[['low','medium','synthetic ambiguity']]},'timing':{'metric_hypotheses':[]},'open_questions':[],'suitability':{'reason':'Synthetic only'},'uncertainties':[],'experiment_limit':'Not a recording test'}
 def test_preserve_candidates_and_downgrade_unsupported_certainty(self):
  from musiccraft.analysis import migrate_02
  old=self.legacy();before=copy.deepcopy(old);a=migrate_02(old);self.assertEqual(a['style']['findings'][0]['certainty'],'undetermined');self.assertEqual(a['content']['observations'][0]['candidates'],[{'pitch_midi':60,'strength':.8},{'pitch_midi':64,'strength':.2}]);self.assertEqual(old,before)
 def test_reject_truncated_confidence(self):
  from musiccraft.analysis import migrate_02
  old=self.legacy();old['observations']['confidence']=[]
  with self.assertRaises(ContractError):migrate_02(old)
class Compact(unittest.TestCase):
 def test_analysis_lossless_unknown(self):
  from musiccraft.compact import pack,unpack
  a=analysis();a['content']['observations'][0]['candidates'].append({'pitch_midi':None});self.assertEqual(unpack(pack(a)),a)
 def test_plan_lossless_optional(self):
  from musiccraft.compact import pack,unpack
  p=fixture();p['notes'][0]['spelling']='C5';self.assertEqual(unpack(pack(p)),p)
 def test_forbid_injected_table_path(self):
  from musiccraft.compact import pack,unpack
  p=pack(fixture());p['tables'][0]['path']=['request']
  with self.assertRaises(ContractError):unpack(p)
class Exports(unittest.TestCase):
 def export(self,p):
  with tempfile.TemporaryDirectory() as d:
   report=export_plan(p,d);self.assertEqual(report['xml_independent_timing_type_staff'],'passed');self.assertEqual(report['musicxml_pitch_onset_duration'],'passed');self.assertEqual(report['human_listening'],'not_run');return report
 def test_single_hand(self):
  p=fixture();p['voices']=[p['voices'][1]];p['notes']=[n for n in p['notes'] if n['voice_id']=='LH'];self.export(p)
 def test_independent_checker_rejects_gemini_classes(self):
  from musiccraft.xmlcheck import check_xml
  import xml.etree.ElementTree as E
  p=fixture()
  with tempfile.TemporaryDirectory() as d:
   export_plan(p,d);path=Path(d)/'composition.musicxml';original=path.read_bytes()
   tree=E.parse(path);tree.find('.//note/type').text='eighth';tree.write(path)
   with self.assertRaises(ContractError):check_xml(path,p)
   path.write_bytes(original);tree=E.parse(path);tree.find('.//sound').set('tempo','126');tree.write(path)
   with self.assertRaises(ContractError):check_xml(path,p)
 def test_sixteenth_68(self):self.assertEqual(self.export(fixture())['ppq'],480)
 def test_triplets(self):
  p=fixture();p['notes']=[n for n in p['notes'] if n['voice_id']=='LH'];template={'voice_id':'RH','duration_q':[1,3],'velocity':70,'decision_id':'d1'}
  for i in range(9):p['notes'].append({**template,'id':f't{i}','pitch_midi':60+i,'onset_q':pair(F(i,3))})
  self.export(p)
 def test_dotted(self):self.export(longnotes(fixture(),3))
 def test_tie_across_bars(self):
  p=fixture();p['bars'].append({'number':2,'start_q':[3,1],'length_q':[3,1],'meter':[6,8]});self.export(longnotes(p,6))
 def test_tempo_change(self):
  p=fixture();p['tempos'].append({'at_q':[3,2],'per_minute':[100,1],'reference_q':[1,1]});self.export(p);self.assertEqual(seconds_at(p,3),F(89,125)*F(3,2)+F(3,5)*F(3,2))
 def test_meter_change(self):
  p=fixture();p['bars'][0]['meter']=[3,4];p['bars'].append({'number':2,'start_q':[3,1],'length_q':[4,1],'meter':[4,4]});self.export(longnotes(p,7))
 def test_pickup(self):
  p=fixture();p['bars'][0]['length_q']=[1,1];p['bars'][0]['partial_reason']='pickup';self.export(longnotes(p,1))
 def test_explicit_rests(self):
  p=longnotes(fixture(),3);p['notes'][0]['duration_q']=[1,1];p['rests']=[{'id':'r','voice_id':'RH','onset_q':[1,1],'duration_q':[2,1]}];self.export(p)
 def test_performance_gate(self):
  p=fixture();p['notes'][0]['performance']={'onset_s':0,'duration_s':.16};self.export(p)
 def test_reject_performance_overlap(self):
  p=fixture();p['notes'][0]['performance']={'onset_s':0,'duration_s':1.5}
  with self.assertRaises(ContractError):self.export(p)
 def test_reject_insufficient_resolution(self):
  p=fixture();p['tempos'].append({'at_q':[1,103],'per_minute':[80,1],'reference_q':[1,1]})
  with self.assertRaises(ContractError):self.export(p)
 def test_rejected_export_preserves_existing(self):
  p=fixture();p['notes'][0]['spelling']='C1'
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'composition.mid';f.write_bytes(b'previous')
   with self.assertRaises(ContractError):export_plan(p,d)
   self.assertEqual(f.read_bytes(),b'previous');self.assertFalse((Path(d)/'composition.musicxml').exists())
 def test_input_not_mutated(self):
  p=fixture();before=copy.deepcopy(p);self.export(p);self.assertEqual(p,before)
if __name__=='__main__':unittest.main()
