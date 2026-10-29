"""Independent XML timing/type/staff reader, separate from music21 export."""
from fractions import Fraction as F
import xml.etree.ElementTree as E
from .contracts import require,q
TYPES={'maxima':32,'long':16,'breve':8,'whole':4,'half':2,'quarter':1,'eighth':F(1,2),'16th':F(1,4),'32nd':F(1,8),'64th':F(1,16),'128th':F(1,32),'256th':F(1,64),'512th':F(1,128),'1024th':F(1,256)}
def check_xml(path,p):
 root=E.parse(path).getroot();events=[];tempos=[];open_ties={};bar_count=0
 for pi,part in enumerate(root.findall('part')):
  divisions=None;absolute=F(0)
  for i,m in enumerate(part.findall('measure')):
   require(i<len(p['bars']),'Extra XML bar');b=p['bars'][i];bar=q(b['length_q']);cursor=F(0);last=F(0);lanes={};bar_count+=1
   for e in m:
    if e.tag=='attributes':
     if e.find('divisions') is not None:divisions=int(e.findtext('divisions'));require(divisions>0,'Invalid divisions')
    elif e.tag in ('backup','forward'):cursor+=(1 if e.tag=='forward' else -1)*F(int(e.findtext('duration')),divisions);require(cursor>=0,'Negative XML cursor')
    elif e.tag=='direction':
     sound=e.find('sound')
     if sound is not None and sound.get('tempo') is not None:tempos.append((absolute+cursor+F(int(e.findtext('offset','0')),divisions),float(sound.get('tempo'))))
    elif e.tag=='note':
     require(e.find('grace') is None,'Grace timing not implemented');duration=F(int(e.findtext('duration')),divisions);require(duration>0,'Zero XML duration')
     at=last if e.find('chord') is not None else cursor
     if e.find('chord') is None:last=at;cursor+=duration
     require(at>=0 and at+duration<=bar,'MusicXML bar over/under boundary')
     typ=e.findtext('type')
     if typ:
      require(typ in TYPES,'Unknown note type');dots=len(e.findall('dot'));expected=F(TYPES[typ])*sum((F(1,2)**i for i in range(dots+1)),F(0));tm=e.find('time-modification')
      if tm is not None:expected*=F(int(tm.findtext('normal-notes')),int(tm.findtext('actual-notes')))
      require(expected==duration,'MusicXML numeric duration disagrees with type/dots/tuplet')
     staff=int(e.findtext('staff',str(pi+1)));voice=e.findtext('voice','1');lane=lanes.setdefault((staff,voice),set());lane.add((at,at+duration))
     pitch=e.find('pitch')
     if pitch is not None:
      midi=(int(pitch.findtext('octave'))+1)*12+{'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[pitch.findtext('step')]+int(pitch.findtext('alter','0'));key=(pi,staff,voice,midi);ties={t.get('type') for t in e.findall('tie')};begin=absolute+at
      if 'stop' in ties:
       require(key in open_ties,'Tie stop without start');old,d=open_ties.pop(key);require(old+d==begin,'Noncontiguous tie');begin,duration=old,d+duration
      if 'start' in ties:require(key not in open_ties,'Overlapping tie');open_ties[key]=(begin,duration)
      else:events.append((staff,midi,begin,duration))
   for intervals in lanes.values():
    pos=F(0)
    for a,z in sorted(intervals):require(a==pos,'XML voice gap or overlap');pos=z
    require(pos==bar,'XML voice does not fill bar')
   absolute+=bar
  require(i+1==len(p['bars']),'Missing XML bar')
 require(not open_ties,'Unclosed ties');voices={v['id']:v for v in p['voices']};expected=sorted((voices[n['voice_id']]['staff'],n['pitch_midi'],q(n['onset_q']),q(n['duration_q'])) for n in p['notes']);require(sorted(events)==expected,'Independent XML staff/pitch/timing mismatch')
 expected_tempos=[(q(t['at_q']),float(q(t['per_minute'])*q(t['reference_q']))) for t in p['tempos']];require(len(tempos)==len(expected_tempos),'XML tempo count mismatch')
 for (a,x),(b,y) in zip(tempos,expected_tempos):require(a==b and abs(x-y)<1e-6,'XML playback tempo mismatch')
 return {'xml_independent_timing_type_staff':'passed','xml_tempo_map':'passed','xml_bars_checked':bar_count}
