"""Library-backed export from one verified composition plan."""
from fractions import Fraction as F
from pathlib import Path
import json,math,platform
from collections import defaultdict
import mido
from music21 import stream,note,chord,meter,clef,tempo,layout,metadata,instrument,tie,converter
from .contracts import q,validate_plan,require,ContractError,digest

def seconds_at(p,at):
 at=F(at);total=F(0);ts=p['tempos']
 for i,t in enumerate(ts):
  start=q(t['at_q']);stop=q(ts[i+1]['at_q']) if i+1<len(ts) else at
  if at>start:total+=(min(at,stop)-start)*60/(q(t['per_minute'])*q(t['reference_q']))
  if at<=stop:break
 return total

def q_at_seconds(p,value):
 value=F(str(value));total=F(0);ts=p['tempos']
 for i,t in enumerate(ts):
  start=q(t['at_q']);rate=60/(q(t['per_minute'])*q(t['reference_q']))
  if i+1==len(ts):return start+(value-total)/rate
  length=(q(ts[i+1]['at_q'])-start)*rate
  if value<=total+length:return start+(value-total)/rate
  total+=length

def resolution(p):
 d=480
 for e in p['notes']+p['rests']:
  for k in ['onset_q','duration_q']:d=math.lcm(d,q(e[k]).denominator)
 for b in p['bars']:
  for k in ['start_q','length_q']:d=math.lcm(d,q(b[k]).denominator)
 for t in p['tempos']:d=math.lcm(d,q(t['at_q']).denominator)
 require(d<=32767,'Rhythm requires excessive MIDI resolution');return d

def write_midi(p,path,ppq):
 mid=mido.MidiFile(type=1,ticks_per_beat=ppq);con=mido.MidiTrack();mid.tracks.append(con);events=[]
 for t in p['tempos']:
  micros=round(F(60000000)/(q(t['per_minute'])*q(t['reference_q'])));require(1<=micros<=0xffffff,'Tempo outside MIDI range');events.append((int(q(t['at_q'])*ppq),mido.MetaMessage('set_tempo',tempo=micros)))
 for b in p['bars']:events.append((int(q(b['start_q'])*ppq),mido.MetaMessage('time_signature',numerator=b['meter'][0],denominator=b['meter'][1])))
 end=int((q(p['bars'][-1]['start_q'])+q(p['bars'][-1]['length_q']))*ppq);prev=0
 for at,msg in sorted(events,key=lambda e:e[0]):con.append(msg.copy(time=at-prev));prev=at
 con.append(mido.MetaMessage('end_of_track',time=end-prev));performance=[]
 for v in p['voices']:
  tr=mido.MidiTrack();mid.tracks.append(tr);tr.append(mido.MetaMessage('track_name',name=v['id']));tr.append(mido.Message('program_change',channel=v['channel'],program=0));events=[];active_intervals=defaultdict(list)
  for n in p['notes']:
   if n['voice_id']!=v['id']:continue
   a=q(n['onset_q']);z=a+q(n['duration_q'])
   if 'performance' in n:
    a=q_at_seconds(p,n['performance']['onset_s']);z=q_at_seconds(p,F(str(n['performance']['onset_s']))+F(str(n['performance']['duration_s'])))
   require(z<=q_at_seconds(p,seconds_at(p,F(end,ppq))+10),'Performance tail exceeds supported 10 seconds');at,off=round(a*ppq),round(z*ppq);require(off>at,'Performance note collapses at MIDI resolution')
   for x,y in active_intervals[n['pitch_midi']]:require(off<=x or at>=y,'Performance introduces same-pitch overlap')
   active_intervals[n['pitch_midi']].append((at,off));events.extend([(at,mido.Message('note_on',channel=v['channel'],note=n['pitch_midi'],velocity=n['velocity'])),(off,mido.Message('note_off',channel=v['channel'],note=n['pitch_midi'],velocity=0))]);performance.append({'id':n['id'],'channel':v['channel'],'pitch':n['pitch_midi'],'start_tick':at,'end_tick':off,'velocity':n['velocity']})
  prev=0
  for at,msg in sorted(events,key=lambda e:(e[0],e[1].type!='note_off')):tr.append(msg.copy(time=at-prev));prev=at
  tr.append(mido.MetaMessage('end_of_track',time=max(end,prev)-prev))
 mid.save(path);return performance

def write_xml(p,path):
 score=stream.Score();score.metadata=metadata.Metadata(title=p['title'],composer='MusicCraft - interpreted composition')
 parts={}
 for staff in [1,2]:
  part=stream.PartStaff(id='staff'+str(staff));part.insert(0,instrument.Piano());parts[staff]=part
  for i,b in enumerate(p['bars']):
   measure=stream.Measure(number=b['number']);a=q(b['start_q']);z=a+q(b['length_q']);measure.timeSignature=meter.TimeSignature(f"{b['meter'][0]}/{b['meter'][1]}")
   if i==0:measure.insert(0,clef.TrebleClef() if staff==1 else clef.BassClef())
   if q(b['length_q'])<F(b['meter'][0]*4,b['meter'][1]):measure.paddingLeft=float(F(b['meter'][0]*4,b['meter'][1])-q(b['length_q']))
   for v in [v for v in p['voices'] if v['staff']==staff]:
    voice=stream.Voice(id=v['id']);groups=defaultdict(list)
    for n in p['notes']:
     if n['voice_id']==v['id'] and q(n['onset_q'])<z and q(n['onset_q'])+q(n['duration_q'])>a:groups[(q(n['onset_q']),q(n['duration_q']))].append(n)
    for (at,duration),ns in sorted(groups.items()):
     stop=at+duration;lo=max(a,at);hi=min(z,stop);items=[]
     for n in ns:
      item=note.Note(n.get('spelling',n['pitch_midi']));require(item.pitch.midi==n['pitch_midi'],'Spelling changes pitch');item.volume.velocity=n['velocity'];items.append(item)
     obj=items[0] if len(items)==1 else chord.Chord(items);obj.duration.quarterLength=hi-lo
     if lo>at or hi<stop:obj.tie=tie.Tie('continue' if lo>at and hi<stop else 'stop' if lo>at else 'start')
     voice.insert(lo-a,obj)
    for rest in p['rests']:
     if rest['voice_id']!=v['id']:continue
     lo=max(a,q(rest['onset_q']));hi=min(z,q(rest['onset_q'])+q(rest['duration_q']))
     if hi>lo:voice.insert(lo-a,note.Rest(quarterLength=hi-lo))
    measure.insert(0,voice)
   if staff==min(parts):
    for t in p['tempos']:
     at=q(t['at_q'])
     if a<=at<z:measure.insert(at-a,tempo.MetronomeMark(number=float(q(t['per_minute'])),referent=note.Note(quarterLength=q(t['reference_q'])).duration))
   if not any(v['staff']==staff for v in p['voices']):measure.insert(0,note.Rest(quarterLength=z-a))
   measure.makeNotation(inPlace=True);part.insert(a,measure)
  score.insert(0,part)
 if len(parts)==2:score.insert(0,layout.StaffGroup(list(parts.values()),name='Piano',symbol='brace',barTogether=True))
 score.write('musicxml',fp=path)
 # Text tempo avoids missing metronome glyphs in SVG/PDF renderers. Playback
 # retains the library's full-precision quarter-note sound tempo.
 import xml.etree.ElementTree as E
 tree=E.parse(path)
 for direction in tree.findall('.//direction'):
  sound=direction.find('sound')
  if sound is None or sound.get('tempo') is None:continue
  for dt in direction.findall('direction-type'):
   for mark in dt.findall('metronome'):
    dt.remove(mark);E.SubElement(dt,'words').text='Viertel = '+format(float(sound.get('tempo')),'.2f')
 tree.write(path,encoding='utf-8',xml_declaration=True)

def verify(p,midi_path,xml_path,performance,ppq):
 # Re-read using libraries; compare against plan, never trust model test prose.
 imported=mido.MidiFile(midi_path);actual=[];tempos=[]
 for tr in imported.tracks:
  t=0;active={}
  for e in tr:
   t+=e.time
   if e.type=='set_tempo':tempos.append((t,e.tempo))
   if e.type=='note_on' and e.velocity:
    require((e.channel,e.note) not in active,'MIDI overlap');active[(e.channel,e.note)]=(t,e.velocity)
   elif e.type=='note_off' or e.type=='note_on' and not e.velocity:
    require((e.channel,e.note) in active,'Orphan note-off');at,vel=active.pop((e.channel,e.note));actual.append((e.channel,e.note,at,t,vel))
  require(not active,'Open MIDI notes')
 expected=sorted((e['channel'],e['pitch'],e['start_tick'],e['end_tick'],e['velocity']) for e in performance);require(sorted(actual)==expected,'MIDI event roundtrip differs')
 expected_tempos=sorted((int(q(t['at_q'])*ppq),round(F(60000000)/(q(t['per_minute'])*q(t['reference_q'])))) for t in p['tempos']);require(sorted(tempos)==expected_tempos,'MIDI tempo mismatch')
 parsed=converter.parse(str(xml_path));parsed.stripTies(inPlace=True);actual_score=[]
 # Original staff/voice identities are retained in the separate mapping report;
 # imported voice numbering can be normalised by the notation library.
 for part in parsed.parts:
  for n in part.flatten().notes:
   for pitch in n.pitches:actual_score.append((pitch.midi,F(n.offset),F(n.quarterLength)))
 expected_score=sorted((n['pitch_midi'],q(n['onset_q']),q(n['duration_q'])) for n in p['notes']);require(sorted(actual_score)==expected_score,'MusicXML note/pitch/duration roundtrip differs')
 from .xmlcheck import check_xml
 independent = check_xml(xml_path,p)
 return {**independent,'midi_events':'passed','midi_tempo_map':'passed','musicxml_pitch_onset_duration':'passed','notation_engine_visual':'not_run','human_listening':'not_run','ppq':ppq,'midi_tempo_rounding_us_per_quarter_max':.5,'performance_tick_rounding_max':.5,'notes':len(p['notes']),'python':platform.python_version(),'music21':__import__('music21').__version__,'mido':'1.3.3'}

def export_plan(p,out,analysis=None):
 validate_plan(p,analysis);out=Path(out);out.mkdir(parents=True,exist_ok=True)
 # Stage all files before replacing any result. Rejections preserve old outputs.
 import tempfile,os
 with tempfile.TemporaryDirectory(dir=out) as d:
  stage=Path(d);ppq=resolution(p);performance=write_midi(p,stage/'composition.mid',ppq);write_xml(p,stage/'composition.musicxml');report=verify(p,stage/'composition.mid',stage/'composition.musicxml',performance,ppq);report['plan_sha256']=digest(p);report['performance_mapping']=performance
  (stage/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
  for name in ['composition.mid','composition.musicxml','validation.json']:os.replace(stage/name,out/name)
 return report
