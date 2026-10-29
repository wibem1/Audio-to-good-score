"""Strict structural and semantic validation. Never silently repair music."""
import hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parent.parent
class ContractError(ValueError):pass

def q(value):
 if not isinstance(value,list) or len(value)!=2 or any(type(x)!=int for x in value) or value[1]<=0 or math.gcd(*value)!=1:raise ContractError('Expected reduced rational [numerator, positive denominator]')
 return F(*value)
def pair(v):v=F(v);return [v.numerator,v.denominator]
def digest(data):return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def structure(data,name):
 try:json.dumps(data,allow_nan=False)
 except (ValueError,TypeError) as e:raise ContractError('Non-finite or non-JSON data') from e
 schema=json.loads((ROOT/'protocol'/f'{name}.schema.json').read_text());errors=list(Draft202012Validator(schema).iter_errors(data))
 if errors:raise ContractError('; '.join(f'{list(e.path)}: {e.message}' for e in errors[:5]))
def unique(items):
 ids=[i['id'] for i in items]
 if len(set(ids))!=len(ids):raise ContractError('Duplicate IDs')
 return set(ids)
def require(condition,message):
 if not condition:raise ContractError(message)

def validate_analysis(a):
 structure(a,'analysis');src={s['id']:s for s in a['sources']};require(len(src)==len(a['sources'])>0,'Sources must be unique and nonempty')
 for s in src.values():require(s['range_s'][1]>s['range_s'][0],'Invalid source range')
 sections={s['id']:s for s in a['content']['sections']};unique(a['content']['sections'])
 for s in sections.values():
  require(s['source_id'] in src,'Unknown section source');lo,hi=src[s['source_id']]['range_s'];require(lo<=s['range_s'][0]<s['range_s'][1]<=hi,'Section outside source')
 unique(a['content']['observations'])
 for o in a['content']['observations']:
  require(o['section_id'] in sections,'Unknown observation section');s=sections[o['section_id']];require(o['source_id']==s['source_id'],'Observation source mismatch');require(s['range_s'][0]<=o['time_s']<=s['range_s'][1],'Observation outside section')
 findings=a['content']['findings']+a['style']['findings'];ids=unique(findings)
 dependencies={f['id']:f['depends_on'] for f in findings}
 def visit(n,path):
  require(n not in path,'Cyclic finding dependency')
  for d in dependencies[n]:require(d in ids,'Unknown finding dependency');visit(d,path|{n})
 for f in findings:visit(f['id'],set())
 rank={'undetermined':0,'low':1,'medium':2,'high':3};levels={f['id']:rank[f['certainty']] for f in findings}
 for f in findings:
  for dep in f['depends_on']:require(levels[f['id']]<=levels[dep],'Dependent certainty exceeds its prerequisite')
 for question in a['open_questions']:require(question['section_id'] in sections,'Unknown question section')
 unique(a['open_questions']);unique(a['timing_hypotheses'])
 for h in a['timing_hypotheses']:
  pulse,ps,bpm,ref=[q(h[k]) for k in ['pulse_duration_q','pulse_duration_s','tempo_per_minute','tempo_reference_q']]
  require(min(pulse,ps,bpm,ref)>0,'Positive pulse and tempo required');require(ps==60*pulse/(bpm*ref),'Pulse/tempo reference mismatch')
 return a

def validate_plan(p,analysis=None):
 structure(p,'composition');voices={v['id']:v for v in p['voices']};require(len(voices)==len(p['voices'])>0,'Voices must be unique and nonempty');require(len({v['channel'] for v in voices.values()})==len(voices),'Each voice needs a distinct MIDI channel');require(all(v['channel']!=9 for v in voices.values()),'Percussion channel unsupported')
 require(p['bars'] and p['tempos'],'Bars and tempos required');at=F(0)
 for i,b in enumerate(p['bars']):
  require(b['number']==i+1 and q(b['start_q'])==at,'Bars must be contiguous and numbered from 1');length=q(b['length_q']);full=F(b['meter'][0]*4,b['meter'][1]);require(b['meter'][1] in [1,2,4,8,16,32],'Unsupported meter denominator');require(length>0 and length<=full,'Invalid bar length');require(length==full or bool(b.get('partial_reason')),'Partial bar requires reason');at+=length
 require(at<=2000 and len(p['notes'])<=10000,'Plan exceeds supported size');end=at
 tempos=p['tempos'];positions=[q(t['at_q']) for t in tempos];require(positions[0]==0 and positions==sorted(set(positions)) and positions[-1]<end,'Tempo map must begin at zero and be ordered')
 for t in tempos:require(q(t['per_minute'])>0 and q(t['reference_q'])>0,'Tempo must be positive')
 ids=unique(p['notes']+p['rests']);decisions=unique(p['decisions'])
 if p['request']['mode']=='new':require(p['source_analysis'] is None or analysis is not None,'Analysis reference requires verified input')
 else:require(p['source_analysis'] is not None and analysis is not None,'Source-based composition requires exact analysis')
 if p['source_analysis'] is not None:
  validate_analysis(analysis);r=p['source_analysis'];require((r['id'],r['revision'],r['sha256'])==(analysis['analysis_id'],analysis['revision'],digest(analysis)),'Stale analysis or digest mismatch')
 else:require(analysis is None,'Unexpected analysis input')
 findings=set() if analysis is None else {f['id'] for f in analysis['content']['findings']+analysis['style']['findings']}
 for d in p['decisions']:require(set(d['finding_ids'])<=findings,'Unknown finding in decision')
 intervals={v:{} for v in voices};pitch_intervals={}
 for n in p['notes']+p['rests']:
  require(n['voice_id'] in voices,'Unknown voice');a=q(n['onset_q']);z=a+q(n['duration_q']);require(0<=a<z<=end,'Event outside plan or zero/negative duration')
  is_note='pitch_midi' in n
  if is_note:
   require(n['decision_id'] in decisions,'Every note requires a decision');key=(voices[n['voice_id']]['channel'],n['pitch_midi'])
   for x,y in pitch_intervals.get(key,[]):require(z<=x or a>=y,'Same-pitch overlap')
   pitch_intervals.setdefault(key,[]).append((a,z))
   if 'performance' in n:require(n['performance']['duration_s']>0,'Performance duration must be positive')
  key=(a,z)
  for (x,y),typ in intervals[n['voice_id']].items():require(z<=x or a>=y or (key==(x,y) and typ and is_note),'Overlapping voice events; use another voice for independent durations')
  intervals[n['voice_id']][key]=is_note
 for lane in intervals.values():
  pos=F(0)
  for a,z in sorted(lane):require(a==pos,'Voice has an implicit gap; declare rests');pos=z
  require(pos==end,'Voice does not fill plan')
 return p
