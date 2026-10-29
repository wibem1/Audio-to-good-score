"""Browser adapter: JSON data only, no executable model output, no network."""
import base64,hashlib,io,json,math
from pathlib import Path
from collections import Counter
from .contracts import validate_analysis,validate_plan,digest,require,ContractError
from .analysis import migrate_02,alternatives
from .compact import unpack,pack

def preliminary(m):
 import mido
 raw=base64.b64decode(m['midi']);mid=mido.MidiFile(file=io.BytesIO(raw));require(mid.type in [0,1] and mid.ticks_per_beat>0,'Only PPQ SMF 0/1');start,end=m['range'];require(0<=start<end and end-start<=60,'Choose 0.1 to 60 seconds');events=[];at=0
 for e in mid:
  at+=e.time
  if e.type=='note_on' and e.velocity>0 and start<=at<end:events.append((at,e.note,e.velocity))
 require(len(events)<=10000,'Too many notes');source_id='s1';sections=[]
 for i in range(max(1,math.ceil((end-start)/10))):sections.append({'id':f'g{i+1}','source_id':source_id,'range_s':[start+i*10,min(end,start+(i+1)*10)],'development':'Musikalische Entwicklung noch nicht beurteilt; keine automatische Musterfortsetzung.'})
 obs=[]
 for i,(t,p,v) in enumerate(events):obs.append({'id':f'o{i+1}','source_id':source_id,'time_s':t,'section_id':sections[min(int((t-start)//10),len(sections)-1)]['id'],'slot':i,'candidate_relation':'unresolved','candidates':[{'pitch_midi':p,'velocity':v}],'pitch_certainty':'low','rhythm_certainty':'undetermined','reason':'Aus MIDI bzw. lokalem Notendetektor gelesen. Musikalische Absicht, Notenwert und Stimme sind nicht verifiziert.'})
 a={'format':'MusicCraft-Analysis-Handoff','version':'0.3','analysis_id':'analysis-'+m['sha256'][:12],'revision':1,'sources':[{'id':source_id,'kind':m['kind'],'sha256':m['sha256'],'range_s':[start,end]}],'source_access_allowed':False,'content':{'summary':f'Lokale Voranalyse: {len(obs)} Notenanschläge in {end-start:.1f} Sekunden. Tonmaterial und Einsätze erfasst; Tonart, Taktart, Form und musikalische Rollen benötigen eine musikalische KI-Analyse oder Nutzerprüfung.','findings':[{'id':'pitch-material','feature':'Tonmaterial','value':sorted(set(p for _,p,_ in events)),'certainty':'low','reason':'Beobachtete Tonhöhen, keine verifizierte Melodie oder Harmonie.','basis':'observation','depends_on':[]}],'sections':sections,'observations':obs},'style':{'findings':[]},'timing_hypotheses':[],'open_questions':[{'id':'q-music','section_id':sections[0]['id'],'question':'Tonart, Metrum, Melodieführung, Begleitung und Veränderungen musikalisch analysieren.'}],'suitability':{'forecast':'free','reason':'Nur technische Voranalyse; Vorlagennähe noch nicht seriös beurteilbar.'},'provenance':{'method':'Lokale Ereignis-Voranalyse; keine generative KI','limitations':['Keine vollständige musikalische Analyse.','MIDI-Speichertempo nicht als musikalischen Puls verwenden.','Leere Kandidaten sind keine Pausen.']}}
 return validate_analysis(a)

def dispatch(m):
 action=m['action']
 if action=='hash':return {'sha256':hashlib.sha256(base64.b64decode(m['data'])).hexdigest()}
 if action=='ready':return {'ready':True,'version':'0.1.0-beta.2','core':'0.3'}
 if action=='analysis_request':
  from .analysis_exchange import request
  return request(m['analysis'],m.get('hints'))
 if action=='analysis_merge':
  from .analysis_exchange import merge
  return merge(m['analysis'],m['document'])
 if action=='analysis_context':
  from .analysis_exchange import context
  return context(m['analysis'])
 if action=='preliminary':return preliminary(m)
 if action=='analysis':
  a=m['document']
  if a.get('format')=='MusicCraft-Compact':a=unpack(a)
  if a.get('version')=='0.2':a=migrate_02(a)
  validate_analysis(a);return {'analysis':a,'sha256':digest(a),'alternatives':alternatives(a)}
 if action=='plan':
  from .exporter import export_plan
  p=m['document']
  if p.get('format')=='MusicCraft-Compact':p=unpack(p)
  a=m.get('analysis') if p.get('source_analysis') else None;validate_plan(p,a);out=Path('/tmp/musiccraft-web-export');report=export_plan(p,out,a)
  result={'plan':p,'midi':base64.b64encode((out/'composition.mid').read_bytes()).decode(),'musicxml':(out/'composition.musicxml').read_text(),'report':report}
  return result
 if action=='schemas':
  root=Path(__file__).resolve().parent.parent/'protocol';return {name:json.loads((root/(name+'.schema.json')).read_text()) for name in ['analysis','composition']}
 if action=='pack':return pack(m['document'])
 raise ContractError('Unknown action')
