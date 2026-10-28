import {parseMidi,vlq} from './midi.js';
export const TRANSCRIPTION_PARAMETERS=Object.freeze({onsetThreshold:0.5,frameThreshold:0.3,minimumNoteFrames:11});
export const TRANSCRIPTION_LIMIT_SECONDS=60;
export function audioRange(section,offset,audioDuration){
  if(![...section,offset,audioDuration].every(Number.isFinite)||section.length!==2)throw Error('Ungültiger Audioabschnitt.');
  const from=Math.max(0,section[0]+offset),to=Math.min(audioDuration,section[1]+offset);
  if(to-from<0.1)throw Error('Bitte mindestens 0,1 Sekunden hörbares Audio markieren.');
  if(to-from>TRANSCRIPTION_LIMIT_SECONDS+1e-6)throw Error('Bitte höchstens 60 Sekunden für einen Transkriptionslauf markieren.');
  return [from,to];
}
// Candidate times are seconds, not inferred score beats. 120 BPM only encodes time.
export function candidateMidi(events,startSeconds,durationSeconds){
  if(!Number.isFinite(startSeconds)||startSeconds<0||!Number.isFinite(durationSeconds)||durationSeconds<=0||durationSeconds>60.000001)throw Error('Ungültiger Kandidatenabschnitt.');
  if(!Array.isArray(events)||events.length>10000)throw Error('Zu viele Modellnoten.');
  const sorted=events.map(n=>({...n})).sort((a,b)=>a.startTimeSeconds-b.startTimeSeconds||a.pitchMidi-b.pitchMidi);
  const sequence=[{tick:0,data:[255,81,3,7,161,32],priority:0}],channels=new Map();let clipped=0,overlapChannels=0;
  for(const n of sorted){
    if(![n.startTimeSeconds,n.durationSeconds,n.pitchMidi,n.amplitude].every(Number.isFinite)||!Number.isInteger(n.pitchMidi)||n.pitchMidi<21||n.pitchMidi>108||n.durationSeconds<=0)throw Error('Ungültige Modellnote. Kandidat wurde verworfen.');
    const a=Math.max(0,n.startTimeSeconds),b=Math.min(durationSeconds,n.startTimeSeconds+n.durationSeconds);
    if(a!==n.startTimeSeconds||b!==n.startTimeSeconds+n.durationSeconds)clipped++;
    if(b<=a)continue;
    const on=Math.round((startSeconds+a)*2000),off=Math.max(on+1,Math.round((startSeconds+b)*2000));
    const active=channels.get(n.pitchMidi)||Array(16).fill(-1),channel=active.findIndex(end=>end<=on);
    if(channel<0)throw Error('Mehr als 16 überlappende gleiche Töne: Kandidat nicht sicher als MIDI darstellbar.');
    if(channel)overlapChannels++;active[channel]=off;channels.set(n.pitchMidi,active);
    sequence.push({tick:on,data:[144+channel,n.pitchMidi,Math.max(1,Math.min(127,Math.round(n.amplitude*127)))],priority:2},{tick:off,data:[128+channel,n.pitchMidi,0],priority:1});
  }
  sequence.sort((a,b)=>a.tick-b.tick||a.priority-b.priority);
  const end=Math.max(Math.round((startSeconds+durationSeconds)*2000),sequence.at(-1).tick);sequence.push({tick:end,data:[255,47,0],priority:3});
  const track=[];let previous=0;for(const e of sequence){track.push(...vlq(e.tick-previous),...e.data);previous=e.tick;}
  const len=track.length,bytes=new Uint8Array([77,84,104,100,0,0,0,6,0,0,0,1,3,232,77,84,114,107,len>>>24&255,len>>>16&255,len>>>8&255,len&255,...track]);
  const parsed=parseMidi(bytes);return {bytes,noteCount:parsed.notes.length,clipped,overlapChannels};
}
export class LocalTranscriber {
  constructor(workerFactory=()=>new Worker(new URL('./vendor/transcription-worker.js',import.meta.url))){this.workerFactory=workerFactory;this.running=null;}
  run(samples,onProgress=()=>{}){
    if(this.running)throw Error('Eine Transkription läuft bereits.');
    if(!(samples instanceof Float32Array)||samples.length<2205||samples.length>60*22050)throw Error('Transkription unterstützt 0,1 bis 60 Sekunden Audio.');
    if(!samples.every(Number.isFinite))throw Error('Ungültige Audio-Abtastwerte.');
    const worker=this.workerFactory();
    return new Promise((resolve,reject)=>{
      let settled=false;
      const finish=(error,value)=>{if(settled)return;settled=true;clearTimeout(timer);worker.terminate();this.running=null;error?reject(error):resolve(value);};
      const timer=setTimeout(()=>finish(Error('Zeitlimit von fünf Minuten erreicht. Bitte kürzere Passage wählen.')),300000);
      this.running={cancel:()=>finish(new DOMException('Transkription abgebrochen.','AbortError'))};
      worker.onmessage=({data})=>{
        if(!this.running)return;
        if(data.type==='progress')onProgress(data);
        else if(data.type==='error')finish(Error(`Lokale Transkription fehlgeschlagen: ${data.message}`));
        else if(data.type==='result')finish(null,data);
      };
      worker.onerror=()=>finish(Error('Transkriptionsmodul konnte nicht geladen werden. Modelldateien und WebAssembly-Unterstützung prüfen.'));
      try{worker.postMessage({samples,parameters:TRANSCRIPTION_PARAMETERS},[samples.buffer]);}catch(error){finish(error);}
    });
  }
  cancel(){this.running?.cancel();}
}
export async function resamplePassage(audio,range){
  const from=Math.floor(range[0]*audio.sampleRate),to=Math.min(audio.length,Math.ceil(range[1]*audio.sampleRate));
  const offline=new OfflineAudioContext(1,Math.round((to-from)/audio.sampleRate*22050),22050);
  const mono=offline.createBuffer(1,to-from,audio.sampleRate),out=mono.getChannelData(0);
  for(let ch=0;ch<audio.numberOfChannels;ch++){const data=audio.getChannelData(ch);for(let i=0;i<out.length;i++)out[i]+=data[from+i]/audio.numberOfChannels;}
  const source=offline.createBufferSource();source.buffer=mono;source.connect(offline.destination);source.start();const rendered=await offline.startRendering();return rendered.getChannelData(0).slice();
}
