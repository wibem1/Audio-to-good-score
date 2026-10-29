"""Conservative migration and bounded alternatives; no automatic composition."""
from copy import deepcopy
from .contracts import validate_analysis,ContractError,require

def migrate_02(old):
 require(old.get('format')=='MusicCraft-Analysis-Handoff' and old.get('version')=='0.2','Expected explicit 0.2 handoff')
 c={'summary':old['summary'],'findings':[],'sections':[],'observations':[]};style={'findings':[]}
 certainty=lambda x:'undetermined' if x in ['not-determined','undetermined'] else x
 for feature,f in old['global_findings'].items():
  item={'id':'global-'+feature,'feature':feature,'value':deepcopy(f.get('value',f.get('value_seconds'))),'certainty':certainty(f['confidence']) if f.get('reason') else 'undetermined','reason':f.get('reason') or 'Legacy handoff has no supporting reason; certainty downgraded','basis':'interpretation','depends_on':[]}
  (style['findings'] if feature in ['style','expression'] else c['findings']).append(item)
 for g in old['groups']:
  sid='group-'+str(g['provisional_group']);c['sections'].append({'id':sid,'source_id':'source','range_s':g['range_seconds'],'development':g['phrase_observation'],'provisional_bar':g['provisional_group']})
  for k in ['harmony_hypothesis','salient_pitch_material','bass_octave_hypothesis']:
   c['findings'].append({'id':sid+'-'+k,'feature':k,'value':deepcopy(g[k]),'certainty':'medium','reason':g['basis'],'basis':'interpretation','depends_on':[]})
 for i,(row,conf) in enumerate(zip(old['observations']['rows'],old['observations']['confidence'])):
  candidates=[]
  for entry in row[3]:
   candidates.append({'pitch_midi':entry[0],**({'strength':entry[1]} if old['source']['kind']=='audio' else {'velocity':entry[1],'offset_s':entry[2]})})
  c['observations'].append({'id':f'observation-{i}','source_id':'source','time_s':row[0],'section_id':'group-'+str(row[1]),'slot':row[2],'candidate_relation':'alternatives' if old['source']['kind']=='audio' else 'unresolved','candidates':candidates,'pitch_certainty':certainty(conf[0]),'rhythm_certainty':certainty(conf[1]),'reason':conf[2]})
 require(len(c['observations'])==len(old['observations']['rows'])==len(old['observations']['confidence']),'Confidence table length mismatch')
 a={'format':'MusicCraft-Analysis-Handoff','version':'0.3','analysis_id':old['analysis_id'],'revision':old['revision']+1,'sources':[{'id':'source','kind':old['source']['kind'],'sha256':old['source']['sha256'],'range_s':old['source']['range_seconds']}],'source_access_allowed':old['access_policy']['composition_may_read_source'],'content':c,'style':style,'timing_hypotheses':[{k:v for k,v in {**h,'certainty':certainty(h['confidence'])}.items() if k not in ['status','confidence']} for h in old['timing']['metric_hypotheses']],'open_questions':[{'id':f'question-{i}','section_id':'group-'+str(f['group']),'question':f['issue']} for i,f in enumerate(old['open_questions'])],'suitability':{'forecast':'similar','reason':old['suitability']['reason']},'provenance':{'method':'Explicit 0.2 migration; measurements unchanged','limitations':old['uncertainties']+[old['experiment_limit']]}}
 return validate_analysis(a)

def alternatives(a,limit=3):
 """Propose one-position alternatives, not scores or automatically approved edits."""
 validate_analysis(a);require(type(limit)==int and 1<=limit<=3,'At most three alternatives')
 out=[]
 for o in a['content']['observations']:
  if o['pitch_certainty']=='high' or o['candidate_relation']=='simultaneous':continue
  pitches=list(dict.fromkeys(c['pitch_midi'] for c in o['candidates'] if c['pitch_midi'] is not None))
  if len(pitches)>1:
   for p in pitches[:limit]:out.append({'observation_id':o['id'],'section_id':o['section_id'],'pitch_midi':p,'status':'requires_musical_review','reason':'Alternative from an uncertain observation, not a correction or probability'})
   break
 return out
