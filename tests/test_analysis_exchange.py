import copy,unittest
from musiccraft.analysis_exchange import request,merge,table,FEATURES
from musiccraft.contracts import digest,ContractError,validate_analysis
from test_composition_core import analysis

def response(a):
 return {'format':'MusicCraft-Analysis-Interpretation','version':'1','base':{'id':a['analysis_id'],'revision':a['revision'],'sha256':digest(a)},'summary':'Synthetic interpretation; not a recognition test.','findings':[{'id':'ai-'+k,'feature':k,'value':'unknown','certainty':'undetermined','reason':'Synthetic uncertainty.','basis':'interpretation','depends_on':[]} for k in FEATURES],'style_findings':[],'sections':[],'timing_hypotheses':[],'open_questions':[],'suitability':{'forecast':'free','reason':'Synthetic test.'},'limitations':['Not musically verified.'],'observation_updates':[]}
class AnalysisExchange(unittest.TestCase):
 def test_table_precision_null_and_missing(self):
  rows=[{'time_s':.123456789012345,'x':None,'reason':'long repeated reason'*5},{'time_s':1.99999999999999,'reason':'long repeated reason'*5}];t=table(rows);out=[]
  for ri,values in enumerate(t['rows']):out.append(dict(t['defaults'],**{t['columns'][i]:(t['dictionary'][t['columns'][i]][values[i]] if t['columns'][i] in t['dictionary'] else values[i]) for i in t['presence'].get(str(ri),range(len(t['columns'])))}))
  self.assertEqual(out,rows)
 def test_no_measurement_rewrite(self):
  a=analysis();old=copy.deepcopy(a);b=merge(a,response(a));self.assertEqual(a,old);self.assertEqual(b['content']['observations'],a['content']['observations']);self.assertEqual(b['revision'],a['revision']+1);validate_analysis(b)
 def test_stale_reference(self):
  a=analysis();d=response(a);d['base']['sha256']='1'*64
  with self.assertRaises(ContractError):merge(a,d)
 def test_missing_criterion(self):
  a=analysis();d=response(a);d['findings'].pop()
  with self.assertRaises(ContractError):merge(a,d)
 def test_update_preserves_time_and_alternatives(self):
  a=analysis();d=response(a);d['observation_updates']=[{'id':'o1','reason':'Synthetic alternative retained.','pitch_certainty':'medium'}];b=merge(a,d);self.assertEqual(b['content']['observations'][0]['time_s'],a['content']['observations'][0]['time_s']);self.assertEqual(len(b['content']['observations'][0]['candidates']),2)
 def test_no_retiming(self):
  a=analysis();d=response(a);d['observation_updates']=[{'id':'o1','time_s':2,'reason':'retime'}]
  with self.assertRaises(ContractError):merge(a,d)
 def test_unknown_update(self):
  a=analysis();d=response(a);d['observation_updates']=[{'id':'missing','reason':'x'}]
  with self.assertRaises(ContractError):merge(a,d)
 def test_section_coverage(self):
  a=analysis();d=response(a);d['sections']=[{'id':'new','source_id':'s1','range_s':[1,2],'development':'Synthetic'}]
  with self.assertRaises(ContractError):merge(a,d)
 def test_new_sections_preserve_all_observations(self):
  a=analysis();d=response(a);d['sections']=[{'id':'new','source_id':'s1','range_s':[0,3],'development':'Synthetic change'}];b=merge(a,d);self.assertEqual(len(b['content']['observations']),len(a['content']['observations']));self.assertEqual(b['content']['observations'][0]['section_id'],'new')
 def test_tempo_consistency(self):
  a=analysis();d=response(a);d['timing_hypotheses']=copy.deepcopy(a['timing_hypotheses']);d['timing_hypotheses'][0]['tempo_per_minute']=[84,1]
  with self.assertRaises(ContractError):merge(a,d)
 def test_no_full_output_table(self):
  a=analysis();d=response(a);d['observations']=a['content']['observations']
  with self.assertRaises(ContractError):merge(a,d)
 def test_request_is_analysis_only(self):
  text=request(analysis())['text'];self.assertIn('observations_table',text);self.assertIn('NICHT erneut',text);self.assertNotIn('Composition-Plan',text)
 def test_context_independently_decoded(self):
  from musiccraft.analysis_exchange import context
  for hetero in [False,True]:
   a=analysis()
   if hetero:a['content']['observations'][0]['candidates'][0]['offset_s']=.0000123456789
   x=context(a);t=x['observations_table'];out=[]
   for ri,values in enumerate(t['rows']):
    row=copy.deepcopy(t['defaults'])
    for i in t['presence'].get(str(ri),range(len(t['columns']))):
     k=t['columns'][i];row[k]=copy.deepcopy(t['dictionary'][k][values[i]] if k in t['dictionary'] else values[i])
    if x['candidate_columns'] is not None:row['candidates']=[dict(zip(x['candidate_columns'],c)) for c in row['candidates']]
    out.append(row)
   self.assertEqual(out,a['content']['observations'])
 def test_user_hint_survives_interpretation(self):
  a=analysis();a['content']['findings'].append({'id':'user-1','feature':'Nutzerhinweis','value':'Schluss kommt von unten.','certainty':'undetermined','reason':'Nutzer','basis':'user_hint','depends_on':[]});b=merge(a,response(a));self.assertIn('user-1',[f['id'] for f in b['content']['findings']])
 def test_duplicate_updates_are_atomic(self):
  a=analysis();before=copy.deepcopy(a);d=response(a);d['observation_updates']=[{'id':'o1','reason':'first'},{'id':'o1','reason':'second'}]
  with self.assertRaises(ContractError):merge(a,d)
  self.assertEqual(a,before)
