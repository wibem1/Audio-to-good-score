"""Bounded musical interpretation exchange. Original measurements never go on an output roundtrip."""
from copy import deepcopy
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from .contracts import validate_analysis,digest,require,ContractError
FEATURES=['tonality','meter','tempo','bar_count','style','form','melody','harmony','bass','accompaniment','rhythm','expression']
def dumps(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'),allow_nan=False)
def table(rows):
 columns=sorted({k for r in rows for k in r});defaults={};dictionary={}
 for col in columns:
  vals=[r.get(col) for r in rows];unique={dumps(v):v for v in vals}
  if len(unique)==1 and all(col in r for r in rows):defaults[col]=vals[0]
  elif len(unique)<len(vals):
   lookup={key:i for i,key in enumerate(unique)};indices=[lookup[dumps(v)] for v in vals]
   if len(dumps(list(unique.values())))+len(dumps(indices))<len(dumps(vals)):dictionary[col]=list(unique.values())
 columns=[c for c in columns if c not in defaults];out=[];presence={}
 for index,r in enumerate(rows):
  present=[i for i,k in enumerate(columns) if k in r]
  if len(present)!=len(columns):presence[str(index)]=present
  out.append([next(i for i,v in enumerate(dictionary[k]) if dumps(v)==dumps(r.get(k))) if k in dictionary else r.get(k) for k in columns])
 return {'columns':columns,'defaults':defaults,'dictionary':dictionary,'presence':presence,'rows':out}
def context(a):
 validate_analysis(a);b=deepcopy(a);obs=b['content'].pop('observations');candidate_columns=sorted({k for o in obs for c in o['candidates'] for k in c})
 if all(set(c)==set(candidate_columns) for o in obs for c in o['candidates']):
  for o in obs:o['candidates']=[[c[k] for k in candidate_columns] for c in o['candidates']]
 else:candidate_columns=None
 return {'analysis':b,'observations_table':table(obs),'candidate_columns':candidate_columns,'table_rule':'Rows are column-ordered values. Apply defaults to each row. dictionary columns store zero-based indices; other values are literal. presence, if listed for a row index, names present column indices (missing differs from null). If candidate_columns is non-null, each candidate is an array in that order. Exact source seconds, no quantization.'}
def schema():return json.loads((Path(__file__).resolve().parent.parent/'protocol/analysis-interpretation.schema.json').read_text())
def request(a,hints=None):
 validate_analysis(a);reference={'id':a['analysis_id'],'revision':a['revision'],'sha256':digest(a)}
 prompt=('Analysiere die Musik gründlich; keine Komposition oder Partitur. Antworte ausschließlich als MusicCraft-Analysis-Interpretation JSON. '
 'Die vollständigen lokalen Messdaten bleiben lokal erhalten. Gib sie NICHT erneut aus. Liefere musikalische Deutung mit Sicherheit und Begründung für jedes Pflichtkriterium. '
 'Ein unbekannter Befund ist zulässig und ausdrücklich als undetermined zu begründen, nicht zu erraten. Kandidaten sind unsicher, Obertöne möglich, unknown ist keine Pause. '
 'Prüfe jede Phrase auf Änderungen und Richtungswechsel; kein blindes Fortsetzen. Tempo immer mit Bezugsnotenwert in Viertelnoten-Einheiten; keine erfundene Taktzahl. '
 'Verwende vollständige Originalsekunden, der Audioclip beginnt bei sources.range_s[0]. Mehrere Quellen sind nicht automatisch ausgerichtet. '
 'Abschnitte nur ersetzen, wenn sie sämtliche vorhandenen Beobachtungen abdecken. sections=[] behält vorläufige Zeitgruppen; dann offene Fragen auf deren IDs beziehen. '
 'observation_updates ist nur für gezielte begründete Ergänzungen/Korrekturen, keine Vollabschrift; [] ist ausdrücklich erlaubt. '
 'Jedes Update benennt eine vorhandene Beobachtungs-ID. Behalte Tonalternativen. Keine neuen Messungen als sicher ausgeben. '
 'Schreibweise: ausgeschriebene deutsche musikalische Werte in findings.value, kurze konkrete Gründe. Ziel etwa 1500 bis 3000 Ausgabetokens, keine Wiederholung identischer Gründe. '
 'depends_on darf nur auf neue Befunde oder beibehaltene lokale IDs verweisen: '+dumps([f['id'] for f in a['content']['findings'] if f['basis']=='user_hint' or f['id']=='pitch-material'])+'. '
 'Pflichtkriterien (findings.feature exakt): '+','.join(FEATURES)+'. '
 'Timing-Hypothesen nur bei begründbarer exakter Puls-/Tempo-Gleichung; sonst Timing in findings erklären. base muss exakt '+dumps(reference)+' sein.\n'
 'Ausgabeschema:'+dumps(schema())+'\nBefunde:'+dumps(context(a))+'\nNutzerhinweise:'+dumps(hints or []))
 return {'text':prompt,'base':reference,'stats':{'text_chars':len(prompt),'observations':len(a['content']['observations']),'schema_chars':len(dumps(schema()))}}
def merge(a,delta):
 validate_analysis(a);require(len(dumps(delta))<=100000,'Musikalische Ergänzung überschreitet die zulässige Größe.');errors=list(Draft202012Validator(schema()).iter_errors(delta));require(not errors,'Ungültige musikalische Ergänzung: '+('; '.join(e.message for e in errors[:2])))
 require(delta['base']=={'id':a['analysis_id'],'revision':a['revision'],'sha256':digest(a)},'Veraltete Analysegrundlage; Ergänzung nicht übernommen.')
 features=[f['feature'] for f in delta['findings']];require(set(FEATURES)<=set(features),'Musikalische Pflichtkriterien fehlen.');require(len(features)==len(set(features)),'Doppelte musikalische Kriterien.')
 b=deepcopy(a);b['revision']+=1;b['content']['summary']=delta['summary'];b['content']['findings']=[f for f in b['content']['findings'] if f['basis']=='user_hint' or f['id']=='pitch-material']+deepcopy(delta['findings']);b['style']['findings']=deepcopy(delta['style_findings'])
 if delta['sections']:
  sections=deepcopy(delta['sections']);by_source={s['id']:s for s in a['sources']}
  for s in sections:
   require(s['source_id'] in by_source,'Unbekannte Abschnittsquelle.');lo,hi=by_source[s['source_id']]['range_s'];require(lo<=s['range_s'][0]<s['range_s'][1]<=hi,'Abschnitt außerhalb der Quelle.')
  for i,s in enumerate(sections):
   for t in sections[i+1:]:require(s['source_id']!=t['source_id'] or s['range_s'][1]<=t['range_s'][0] or t['range_s'][1]<=s['range_s'][0],'Überlappende Analyseabschnitte.')
  for o in b['content']['observations']:
   matches=[s for s in sections if s['source_id']==o['source_id'] and (s['range_s'][0]<=o['time_s']<s['range_s'][1] or o['time_s']==s['range_s'][1]==by_source[o['source_id']]['range_s'][1])]
   require(len(matches)==1,'Analyseabschnitte lassen Beobachtungen unzugeordnet.');o['section_id']=matches[0]['id']
  b['content']['sections']=sections
 obs={o['id']:o for o in b['content']['observations']};seen=set()
 for update in delta['observation_updates']:
  oid=update['id'];require(oid in obs and oid not in seen,'Unbekannte oder doppelte Beobachtungs-ID.');seen.add(oid);obs[oid].update(deepcopy(update))
 b['timing_hypotheses']=deepcopy(delta['timing_hypotheses']);b['open_questions']=deepcopy(delta['open_questions']);b['suitability']=deepcopy(delta['suitability'])
 b['provenance']={'method':'Musikalische KI-Deutung mit lokal zusammengeführten Messbefunden (Analysis Interpretation 1).','limitations':list(dict.fromkeys(a['provenance']['limitations']+delta['limitations']+['Unveränderte Rohbefunde bleiben unsichere Detektorbefunde; keine vollständige KI-Verifikation jeder Note.']))}
 # Superseded local-only limitation must not label a successful interpretation as local-only.
 b['provenance']['limitations']=[x for x in b['provenance']['limitations'] if x!='Keine vollständige musikalische Analyse.']
 return validate_analysis(b)
