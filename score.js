import {tickToSeconds} from './midi.js';
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
export function createScore(midi,notes,{beats=4,beatType=4,splitPitch=60,bpm=120,timeBasis='ticks',originSeconds=0,notationStyle='performance',title='Klavier – Prüffassung'}={}){
  if(!Number.isInteger(beats)||beats<1||beats>12||![2,4,8].includes(beatType)||!Number.isInteger(splitPitch)||splitPitch<21||splitPitch>108||!Number.isFinite(bpm)||bpm<20||bpm>300||!['ticks','seconds'].includes(timeBasis)||!Number.isFinite(originSeconds)||originSeconds<0||originSeconds>86400||!['performance','onsets'].includes(notationStyle))throw Error('Ungültige Notationsparameter.');
  const earliest=Math.min(...notes.filter(n=>!n.muted).map(n=>tickToSeconds(midi,n.start)));if(timeBasis==='seconds'&&originSeconds>earliest+60/bpm/8)throw Error('Taktanfang würde frühe Noten abschneiden; Auftakt berücksichtigen.');
  const bar=beats*16/beatType,beat=beatType===8&&beats%3===0?6:16/beatType,voices=[[],[]],groups=new Map(),mapping=[];
  for(const n of notes.filter(n=>!n.muted)){
    if(n.pitch<12)throw Error('Tonhöhe unter C0 ist für diesen MusicXML-Export nicht unterstützt.');
    const scale=t=>timeBasis==='ticks'?t/midi.ppq*4:(tickToSeconds(midi,t)-originSeconds)*bpm/60*4;
    const start=Math.max(0,Math.round(scale(n.start))),end=Math.max(start+1,Math.round(scale(n.end))),staff=n.pitch>=splitPitch?1:2;
    mapping.push({id:n.id,performanceStart:n.start,performanceEnd:n.end,scoreStart:start,scoreEnd:end,staff});
    const key=`${staff}:${start}:${notationStyle==='onsets'?'attack':end}`;let g=groups.get(key);
    if(g?.notes.some(o=>o.pitch===n.pitch))g=null;
    if(!g){g={start,end,staff,notes:[]};groups.set(groups.has(key)?key+':'+n.id:key,g);}g.notes.push(n);
  }
  if(notationStyle==='onsets')for(const staff of [1,2]){
    const attacks=[...groups.values()].filter(g=>g.staff===staff).sort((a,b)=>a.start-b.start);
    for(let i=0;i<attacks.length;i++){const g=attacks[i],next=attacks.slice(i+1).find(n=>n.start>g.start);g.end=next?next.start:Math.max(g.start+1,Math.min(g.end,g.start+bar));for(const n of g.notes){const entry=mapping.find(m=>m.id===n.id);entry.scoreEnd=g.end;entry.durationInterpretation='Anschlag bis zum nächsten Anschlag derselben Hand; keine rekonstruierte Tastendauer.';}}
  }
  for(const g of [...groups.values()].sort((a,b)=>a.start-b.start||b.end-a.end)){
    const hand=voices[g.staff-1];let v=hand.find(v=>v.at(-1).end<=g.start);if(!v){if(hand.length>=8)throw Error('Mehr als acht unabhängige Stimmen pro Hand; Notation manuell vereinfachen.');v=[];hand.push(v);}v.push(g);
  }
  for(const hand of voices)if(!hand.length)hand.push([]);
  const length=Math.max(1,...mapping.map(n=>n.scoreEnd)),measures=Math.ceil(length/bar);if(measures>500)throw Error('Notationsumfang maximal 500 Takte.');
  const tempo=midi.tempos[0]?.data||[7,161,32],playbackBpm=60000000/(tempo[0]*65536+tempo[1]*256+tempo[2]);
  return {voices,mapping,bar,beat,measures,playbackBpm,parameters:{beats,beatType,splitPitch,bpm,timeBasis,originSeconds,notationStyle,title},warnings:[...(notationStyle==='onsets'?['Vereinfachte Anschlagsfassung: Akkorddauern bis zum nächsten Handanschlag. Ausklingen/Pedal sind keine Tastendauer; keine vollständige Stimmenrekonstruktion.']:[]),'Notationsraster: Sechzehntel; keine Triolen oder automatisch erkannten Taktarten.','Handteilung nach gewählter Tonhöhengrenze, keine bestätigte Spielbarkeitsanalyse.','Notationszeiten sind eine separate Darstellung; Performance-MIDI wird nicht verändert.']};
}
function pieces(start,end,group,bar){const result=[];let at=start;while(at<end){const local=at%bar;const len=[24,16,12,8,6,4,3,2,1].find(n=>n<=end-at&&n<=bar-local&&local%([3,6,12,24].includes(n)?n*2/3:n)===0)||1;result.push({start:at,len,group,tieStop:!!group&&at>group.start,tieStart:!!group&&at+len<group.end});at+=len;}return result;}
export function scoreToMusicXML(score){
  const {bar,beat,measures,parameters:p}=score;let xml=`<?xml version="1.0" encoding="UTF-8"?><score-partwise version="4.0"><work><work-title>${esc(p.title)}</work-title></work><identification><creator type="software">Audio to Good Score</creator><encoding><software>Audio to Good Score – ungeprüfte Notation</software></encoding></identification><part-list><score-part id="P1"><part-name>Piano</part-name><part-abbreviation>Pno.</part-abbreviation><score-instrument id="I1"><instrument-name>Piano</instrument-name></score-instrument><midi-instrument id="I1"><midi-channel>1</midi-channel><midi-program>1</midi-program></midi-instrument></score-part></part-list><part id="P1">`;
  const pitches=[['C',0],['C',1],['D',0],['D',1],['E',0],['F',0],['F',1],['G',0],['G',1],['A',0],['A',1],['B',0]];
  for(let m=0;m<measures;m++){
    xml+=`<measure number="${m+1}">`;
    if(m===0)xml+=`<attributes><divisions>4</divisions><key><fifths>0</fifths></key><time><beats>${p.beats}</beats><beat-type>${p.beatType}</beat-type></time><staves>2</staves><clef number="1"><sign>G</sign><line>2</line></clef><clef number="2"><sign>F</sign><line>4</line></clef></attributes><direction placement="above"><direction-type><words>Prüffassung; Notationsraster und Handteilung kontrollieren</words></direction-type><staff>1</staff></direction><direction placement="above"><direction-type><metronome><beat-unit>quarter</beat-unit><per-minute>${Number((p.timeBasis==='seconds'?p.bpm:score.playbackBpm).toFixed(1))}</per-minute></metronome></direction-type><staff>1</staff><sound tempo="${p.timeBasis==='seconds'?p.bpm:score.playbackBpm}"/></direction>`;
    let count=0;
    score.voices.forEach((hand,h)=>hand.forEach((voice,v)=>{
      if(count++)xml+=`<backup><duration>${bar}</duration></backup>`;
      const begin=m*bar,end=begin+bar,segments=[];let at=begin;
      for(const g of voice.filter(g=>g.start<end&&g.end>begin)){
        const a=Math.max(begin,g.start),b=Math.min(end,g.end);if(a>at)segments.push(...pieces(at,a,null,bar));segments.push(...pieces(a,b,g,bar));at=b;
      }if(at<end)segments.push(...pieces(at,end,null,bar));
      segments.forEach((s,i)=>{
        const type={24:'whole',16:'whole',12:'half',8:'half',6:'quarter',4:'quarter',3:'eighth',2:'eighth',1:'16th'}[s.len],voiceId=h*8+v+1;
        const adjacent=(a,b,level)=>a&&b&&a.group&&b.group&&a.start+a.len===b.start&&Math.floor((a.start-begin)/beat)===Math.floor((b.start-begin)/beat)&&a.len<=(level===1?3:1)&&b.len<=(level===1?3:1);
        const beam=[];if(s.group&&s.len<=3)for(let level=1;level<=(s.len===1?2:1);level++){
          const prev=adjacent(segments[i-1],s,level),next=adjacent(s,segments[i+1],level);
          if(prev||next)beam.push(`<beam number="${level}">${prev?(next?'continue':'end'):'begin'}</beam>`);
          else if(level===2&&(adjacent(segments[i-1],s,1)||adjacent(s,segments[i+1],1)))beam.push(`<beam number="2">${adjacent(segments[i-1],s,1)?'backward':'forward'} hook</beam>`);
        }
        (s.group?.notes||[null]).forEach((n,index)=>{
          let content='<rest/>';if(n){const [step,alter]=pitches[n.pitch%12];content=`<pitch><step>${step}</step>${alter?`<alter>${alter}</alter>`:''}<octave>${Math.floor(n.pitch/12)-1}</octave></pitch>`;}
          xml+=`<note>${index?'<chord/>':''}${content}<duration>${s.len}</duration>${n&&s.tieStop?'<tie type="stop"/>':''}${n&&s.tieStart?'<tie type="start"/>':''}<voice>${voiceId}</voice><type>${type}</type>${[3,6,12,24].includes(s.len)?'<dot/>':''}<staff>${h+1}</staff>${index?'':beam.join('')}${n&&(s.tieStop||s.tieStart)?`<notations>${s.tieStop?'<tied type="stop"/>':''}${s.tieStart?'<tied type="start"/>':''}</notations>`:''}</note>`;
        });
      });
    }));xml+='</measure>';
  }return xml+'</part></score-partwise>';
}
