import {exportMidi,parseMidi,tickToSeconds} from './midi.js';
export class Session {
  constructor(midi){this.midi=midi;this.notes=structuredClone(midi.notes);this.history=[];this.future=[];}
  edit(id,patch,section,reason,allowTiming=false){
    const old=this.notes.find(n=>n.id===id);if(!old)throw Error('Note fehlt.');
    if(!reason.trim())throw Error('Bitte die musikalische Begründung angeben.');
    const next={...old,...patch};
    if(next.muted!==undefined&&typeof next.muted!=='boolean')throw Error('Ungültiger Ausblendstatus.');
    for(const k of Object.keys(patch))if(!['pitch','velocity','start','end','muted'].includes(k))throw Error('Nicht erlaubte Änderung.');
    if(![next.pitch,next.velocity,next.start,next.end].every(Number.isInteger)||next.pitch<0||next.pitch>127||next.velocity<1||next.velocity>127||next.start<0||next.end<=next.start)throw Error('Ungültige Notenwerte.');
    if(old.start<section[0]||old.end>section[1]||next.start<section[0]||next.end>section[1])throw Error('Die ganze Note muss im gewählten Abschnitt liegen.');
    if((old.start!==next.start||old.end!==next.end)&&!allowTiming)throw Error('Zeitänderung muss ausdrücklich freigegeben werden.');
    const overlaps=(a,b)=>!a.muted&&!b.muted&&a.channel===b.channel&&a.pitch===b.pitch&&a.start<b.end&&b.start<a.end;
    for(const other of this.notes)if(other.id!==id&&overlaps(next,other)&&!overlaps(old,other))throw Error('Neue Überlappung gleicher Tonhöhe: Änderung abgelehnt.');
    const after=this.notes.map(n=>n.id===id?next:n);
    // Round-trip verifies note pairing and protects every untouched note's timing.
    const parsed=parseMidi(exportMidi(this.midi,after));
    const signature=ns=>ns.filter(n=>!n.muted).map(n=>[n.track,n.channel,n.pitch,n.velocity,n.start,n.end].join(':')).sort();
    if(JSON.stringify(signature(parsed.notes))!==JSON.stringify(signature(after)))throw Error('Export würde Notenpaarung verändern; Änderung abgelehnt.');
    if(JSON.stringify(old)===JSON.stringify(next))return;
    this.history.push({id,before:structuredClone(old),after:structuredClone(next),reason:reason.trim(),uncertainty:'manuelle Hypothese, musikalisch ungeprüft',at:new Date().toISOString()});
    this.notes=after;this.future=[];
  }
  undo(){const c=this.history.pop();if(!c)return;this.notes=this.notes.map(n=>n.id===c.id?structuredClone(c.before):n);this.future.push(c);}
  redo(){const c=this.future.pop();if(!c)return;this.notes=this.notes.map(n=>n.id===c.id?structuredClone(c.after):n);this.history.push(c);}
  diagnose(){
    const findings=this.midi.warnings.map(message=>({kind:'Import',message,certainty:'technisch'}));
    const add=f=>{if(findings.length<200)findings.push(f);};
    const groups=new Map();
    for(const n of this.notes.filter(n=>!n.muted)){const length=tickToSeconds(this.midi,n.end)-tickToSeconds(this.midi,n.start);
      if(length<0.04) add({id:n.id,kind:'Länge',message:'Sehr kurze Note (<40 ms); Ornament oder Fehler?',certainty:'unsicher'});
      if(n.pitch<21||n.pitch>108)add({id:n.id,kind:'Tonhöhe',message:'Außerhalb des üblichen Klavierumfangs.',certainty:'unsicher'});
      const key=`${n.channel}:${n.pitch}`,group=groups.get(key)||[];group.push(n);groups.set(key,group);
    }
    for(const group of groups.values()){
      group.sort((a,b)=>a.start-b.start);let previous=null;
      for(const n of group){if(previous&&n.start<previous.end)add({id:n.id,kind:'Timing',message:`Gleiche Tonhöhe auf Kanal ${n.channel+1} überlappt mit ${previous.id}; Pedal/Artikulation prüfen.`,certainty:'unsicher'});if(!previous||n.end>previous.end)previous=n;}
    }
    if(findings.length>=200)findings.push({kind:'Umfang',message:'Anzeige auf die ersten 200 Hinweise begrenzt.',certainty:'technisch'});
    return findings;
  }
}
// Shared input contract: audio-only is a first-class source, never a fake MIDI result.
export function inputPath(audio,midi){return audio?(midi?'audio+midi':'audio-only'):(midi?'midi-only':'empty');}
