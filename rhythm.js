import {tickToSeconds} from './midi.js';
// Periodicity is evidence for a subdivision, not a verified beat, meter or tempo.
export function suggestNotationPulse(midi,notes){
  const times=[...new Set(notes.filter(n=>!n.muted).map(n=>tickToSeconds(midi,n.start)))].sort((a,b)=>a-b);
  if(times.length<12||times.at(-1)-times[0]<2)throw Error('Zu wenig Einsätze für einen Pulsvorschlag.');
  const sampled=times.filter((_,i)=>i%Math.max(1,Math.ceil(times.length/2000))===0);let best=null;
  for(let i=400;i<=2000;i++){const step=i/5000;let re=0,im=0;for(const t of sampled){const a=t*2*Math.PI/step;re+=Math.cos(a);im+=Math.sin(a);}const coherence=Math.hypot(re,im)/sampled.length;
    if(!best||coherence>best.coherence+.0001)best={step,coherence,origin:((Math.atan2(im,re)*step/(2*Math.PI))%step+step)%step};
  }
  const errors=times.map(t=>Math.abs(t-best.origin-Math.round((t-best.origin)/best.step)*best.step)).sort((a,b)=>a-b);
  return {...best,bpm:60/(best.step*4),alternatives:[60/(best.step*4),60/(best.step*2)],medianResidualSeconds:errors[Math.floor(errors.length/2)],noteOnsets:times.length,uncertainty:'Unterteilungshypothese aus MIDI-Einsätzen; Halb-/Doppeltempo, Auftakt, Taktart und Tempodrift selbst prüfen.'};
}
