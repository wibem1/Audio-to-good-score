import {tickToSeconds} from './midi.js';
export function analyzePassage(midi,notes,section){
  const active=notes.filter(n=>!n.muted),local=active.filter(n=>n.start>=section[0]&&n.end<=section[1]),proposals=[];
  const context=active.filter(n=>n.end>=Math.max(0,section[0]-midi.ppq*8)&&n.start<=section[1]+midi.ppq*8);
  const classes=Array(12).fill(0);for(const n of context)classes[n.pitch%12]+=n.end-n.start;
  const summary={noteCount:local.length,contextNotes:context.length,pitchClasses:classes,bass:context.length?Math.min(...context.map(n=>n.pitch)):null,peak:context.length?Math.max(...context.map(n=>n.pitch)):null,uncertainty:'Heuristische Kontextbeschreibung, keine bestätigte Harmonie- oder Stimmenanalyse.'};
  const onsets=[...new Set(local.map(n=>n.start))].sort((a,b)=>a-b);
  const intervals=onsets.slice(1).map((t,i)=>tickToSeconds(midi,t)-tickToSeconds(midi,onsets[i])).filter(t=>t>.08&&t<3).sort((a,b)=>a-b);
  summary.medianOnsetGapSeconds=intervals.length?intervals[Math.floor(intervals.length/2)]:null;
  summary.harmonyHypotheses=onsets.slice(0,100).map(t=>{const sounding=context.filter(n=>n.start<=t&&n.end>t),pcs=new Set(sounding.map(n=>n.pitch%12));const labels=[];for(let root=0;root<12;root++)for(const [name,steps]of [['Dur',[0,4,7]],['Moll',[0,3,7]],['vermindert',[0,3,6]]])if(steps.every(i=>pcs.has((root+i)%12)))labels.push({rootPitchClass:root,quality:name});return {tick:t,labels,uncertainty:'Tonklassen-Muster, keine bestätigte Akkordfunktion'};}).filter(c=>c.labels.length);
  const top=onsets.map(t=>Math.max(...local.filter(n=>n.start===t).map(n=>n.pitch))),motifs=new Map();
  for(let i=0;i+3<top.length;i++){const key=[top[i+1]-top[i],top[i+2]-top[i+1],top[i+3]-top[i+2]].join(',');const positions=motifs.get(key)||[];positions.push(onsets[i]);motifs.set(key,positions);}
  summary.repeatedIntervalMotifs=[...motifs].filter(([,ticks])=>ticks.length>1).map(([intervals,ticks])=>({intervals,ticks,uncertainty:'Oberste Anschlagstöne als einfache Melodiehypothese'}));
  const seen=new Set();
  for(const upper of local){
    const lower=context.find(n=>n.id!==upper.id&&upper.pitch-n.pitch===12&&Math.abs(tickToSeconds(midi,upper.start)-tickToSeconds(midi,n.start))<.04&&n.end>=upper.end-midi.ppq*.15);
    if(lower){proposals.push({id:upper.id,patch:{muted:true},before:structuredClone(upper),hypothesis:`Möglicher zusätzlicher Oktavton zu ${lower.id}; ebenso kann eine beabsichtigte Oktavverdopplung vorliegen.`,uncertainty:'hoch – nur nach Audio-/B-C-Vergleich entscheiden',context:[lower.id],section:[...section]});seen.add(upper.id);}
  }
  const melody=[...local].sort((a,b)=>a.start-b.start||b.pitch-a.pitch).filter((n,i,a)=>i===0||n.start-a[i-1].start>midi.ppq*.1);
  for(let i=1;i<melody.length-1;i++){
    const n=melody[i],a=melody[i-1],b=melody[i+1];if(seen.has(n.id)||a.end>n.start||n.end>b.start)continue;
    for(const delta of [-12,12]){const pitch=n.pitch+delta;if(pitch<21||pitch>108)continue;
      if(Math.abs(n.pitch-a.pitch)+Math.abs(n.pitch-b.pitch)-Math.abs(pitch-a.pitch)-Math.abs(pitch-b.pitch)>=20){proposals.push({id:n.id,patch:{pitch},before:structuredClone(n),hypothesis:`Isolierter Oktavsprung zwischen ${a.id} und ${b.id}; bewusster Sprung bleibt möglich.`,uncertainty:'hoch – kein verifizierter Tonhöhenfehler',context:[a.id,b.id],section:[...section]});break;}
    }
  }
  const snapshot=JSON.stringify(notes);return {summary,proposals:proposals.slice(0,200).map(p=>({...p,snapshot}))};
}
export function applyProposal(session,proposal,reason){
  const current=session.notes.find(n=>n.id===proposal.id);
  if(proposal.snapshot!==JSON.stringify(session.notes))throw Error('Vorschlag ist veraltet. Kontext neu analysieren.');
  if(JSON.stringify(current)!==JSON.stringify(proposal.before))throw Error('Vorschlag ist veraltet. Diagnose neu ausführen.');
  if(!reason.trim())throw Error('Bitte eigene Prüfbegründung angeben.');
  session.edit(proposal.id,proposal.patch,proposal.section,`${proposal.hypothesis} Unsicherheit: ${proposal.uncertainty}. Entscheidung: ${reason}`);
}
// Neural audio candidates inform pitch hypotheses; never infer deletions from missing model notes.
export function compareAudioCandidates(midi,notes,section,predicted,audioStart,offset){
  const local=notes.filter(n=>!n.muted&&n.start>=section[0]&&n.end<=section[1]),snapshot=JSON.stringify(notes),proposals=[];
  const on=n=>tickToSeconds(midi,n.start),end=n=>tickToSeconds(midi,n.end);
  const candidates=predicted.filter(n=>Number.isFinite(n.startTimeSeconds)&&Number.isFinite(n.durationSeconds)&&Number.isInteger(n.pitchMidi)).map(n=>({...n,time:audioStart+n.startTimeSeconds-offset,end:audioStart+n.startTimeSeconds+n.durationSeconds-offset}));
  for(const n of local){const nearby=candidates.filter(c=>Math.abs(c.time-on(n))<=.12&&Math.min(c.end,end(n))-Math.max(c.time,on(n))>Math.min(c.durationSeconds,end(n)-on(n))*.5);
    if(nearby.some(c=>c.pitchMidi===n.pitch))continue;
    const alternatives=nearby.filter(c=>Math.abs(c.pitchMidi-n.pitch)===12&&!local.some(o=>o.id!==n.id&&o.pitch===c.pitchMidi&&Math.abs(on(o)-c.time)<.12));
    if(alternatives.length!==1)continue;const c=alternatives[0];
    proposals.push({id:n.id,patch:{pitch:c.pitchMidi},before:structuredClone(n),snapshot,section:[...section],context:local.filter(o=>o.id!==n.id).slice(0,8).map(o=>o.id),hypothesis:`Lokales Basic-Pitch-Audiomodell schlägt Ton ${c.pitchMidi} statt ${n.pitch} vor; Einsatz und Dauer überlappen.`,uncertainty:'hoch – Modell kann Oktaven verwechseln; Originalaudio anhören',modelEvidence:{pitch:c.pitchMidi,onset:c.time,end:c.end,activation:c.amplitude,activationIsCalibratedProbability:false}});
  }return proposals.slice(0,200);
}
