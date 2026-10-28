import {parseMidi,exportMidi,tickToSeconds,secondsToTick,midiDuration} from './midi.js';
import {Session,inputPath} from './model.js';
import {Player} from './player.js';
import {demoMidi} from './demo.js';
import {LocalTranscriber,TRANSCRIPTION_PARAMETERS,audioRange,candidateMidi,resamplePassage} from './transcription.js';
import {MODEL_SPEC} from './model-spec.js';
const $=id=>document.getElementById(id), NS='http://www.w3.org/2000/svg';
let session=null,audio=null,audioBytes=null,audioName='',midiName='',context,player,selected='',duration=4,drag=null,loadBusy=false;
const transcriber=new LocalTranscriber();let transcribing=false,pendingCandidate=null,provenance=null,sourceEpoch=0,inferenceLog=[];
function ctx(){if(!context){context=new AudioContext();player=new Player(context);}return context;}
function status(message,error=false){$('status').textContent=message;$('status').classList.toggle('error',error);}
function action(id,fn,event='click'){$(id).addEventListener(event,async e=>{try{await fn(e);}catch(error){status(error.message,true);}});}
function number(id){const v=$(id).valueAsNumber;if(!Number.isFinite(v))throw Error('Bitte gültige Zahlen eingeben.');return v;}
function section(){const from=number('from'),to=number('to');if(from<0||to<=from||to>duration+0.001)throw Error('Passage muss innerhalb des Stücks liegen und eine positive Länge haben.');return [from,to];}
function stop(){player?.stop();}
function confirmReplace(){return !session?.history.length||confirm('Neue Quelle ersetzt die aktuelle MIDI-Bearbeitung. Projekt zuvor gespeichert?');}
function installMidi(bytes,name){const midi=parseMidi(bytes);invalidateTranscription();provenance=null;session=new Session(midi);midiName=name;selected=midi.notes[0]?.id||'';stop();resetRange();render();status('MIDI geladen; Original und expressive Zeiten erhalten.');}
function resetRange(){duration=Math.max(audio?audio.duration-number('offset'):0,session?midiDuration(session.midi,session.notes):0,0.01);$('from').value=0;$('to').value=duration.toFixed(4);$('seek').max=duration;$('seek').value=0;}
function svgNode(tag,attrs,parent,text){const node=document.createElementNS(NS,tag);for(const [k,v]of Object.entries(attrs))node.setAttribute(k,v);if(text!==undefined)node.textContent=text;parent.append(node);return node;}
function draw(){
  const roll=$('roll');roll.replaceChildren();const left=50,width=1140,ys=p=>20+(108-p)*5.7;
  for(let pitch=21;pitch<=108;pitch++){svgNode('rect',{x:left,y:ys(pitch),width,height:5.7,fill:[1,3,6,8,10].includes(pitch%12)?'#122028':'#1c2f37'},roll);if(pitch%12===0)svgNode('text',{x:5,y:ys(pitch)+6,fill:'#9bb8bb','font-size':10},roll,`C${pitch/12-1}`);}
  const step=Math.max(0.5,10**Math.floor(Math.log10(duration/10)));
  for(let s=0;s<=duration;s+=step){const x=left+s/duration*width;svgNode('line',{x1:x,x2:x,y1:14,y2:530,stroke:'#344951','stroke-width':.5},roll);svgNode('text',{x,y:12,fill:'#92b0b4','font-size':10},roll,`${+s.toFixed(2)}s`);}
  let range;try{range=section();}catch{range=[0,0];}
  svgNode('rect',{x:left+range[0]/duration*width,y:15,width:(range[1]-range[0])/duration*width,height:515,fill:'#5dc3ad','fill-opacity':.08,stroke:'#60bca8'},roll);
  if(session){
    const originals=new Map(session.midi.notes.map(n=>[n.id,n]));
    const plot=(n,original)=>{const start=tickToSeconds(session.midi,n.start),end=tickToSeconds(session.midi,n.end);const changed=JSON.stringify(n)!==JSON.stringify(originals.get(n.id));
      const y=Math.max(17,Math.min(527,ys(n.pitch)));const node=svgNode('rect',{x:left+start/duration*width,y,width:Math.max(2,(end-start)/duration*width),height:5.2,fill:original?'#78dbca':changed?'#f1b266':'#64c6b0','fill-opacity':original?.28:n.muted?.12:.9,'stroke-dasharray':n.muted?'2 2':'none',stroke:n.id===selected&&!original?'white':'none','data-id':n.id},roll);
      svgNode('title',{},node,`${n.id} · MIDI ${n.pitch} · ${start.toFixed(3)}–${end.toFixed(3)} s`);
    };session.midi.notes.forEach(n=>plot(n,true));session.notes.forEach(n=>plot(n,false));
  }
  svgNode('line',{id:'playhead',x1:50,x2:50,y1:15,y2:535,stroke:'#fff','stroke-width':1.5,'pointer-events':'none'},roll);
  const wave=$('wave');wave.replaceChildren();if(audio){const data=audio.getChannelData(0),points=[];for(let i=0;i<1140;i++){const t=i/1140*duration+number('offset');let peak=0;const a=Math.floor(t*audio.sampleRate),b=Math.min(data.length,a+Math.ceil(duration*audio.sampleRate/1140));for(let j=Math.max(0,a);j<b;j+=Math.max(1,Math.floor((b-a)/50)))peak=Math.max(peak,Math.abs(data[j]));points.push(`M${i+50},${35-peak*30}v${peak*60}`);}svgNode('path',{d:points.join(''),stroke:'#78c6d0','stroke-width':1},wave);}
}
function render(){
  const path=provenance?'audio-only':inputPath(audio,session);$('sources').textContent=`Audio: ${audioName||'—'} · MIDI: ${midiName||'—'}`;
  $('path').textContent=path==='audio-only'?(provenance?'Eingang: Audio allein → lokaler MIDI-Kandidat. Zum Prüfen A/B/C vergleichen.':'Eingang: Audio allein. Markierte Passage lokal transkribieren und Kandidat prüfen.'):`Eingang: ${path}`;
  for(const id of ['originalMidi','export'])$(id).disabled=!session; $('originalAudio').disabled=!audio;
  $('undo').disabled=!session?.history.length;$('redo').disabled=!session?.future.length;
  $('note').replaceChildren();for(const n of session?.notes||[]){const option=document.createElement('option');option.value=n.id;option.textContent=`Spur ${n.track+1} · Kanal ${n.channel+1} · ${n.id} · Ton ${n.pitch}${n.muted?' (ausgeblendet)':''} · ${tickToSeconds(session.midi,n.start).toFixed(3)} s`;$('note').append(option);}
  $('note').value=selected;$('apply').disabled=!session?.notes.length;
  $('changes').textContent=session?`${session.history.length} aktive Änderungen · ${session.future.length} wiederherstellbar · keine automatische Quantisierung.`:'';
  fillNote();draw();diagnose();updateTranscriptionControls();
}
function fillNote(){const n=session?.notes.find(n=>n.id===selected);for(const id of ['pitch','velocity','start','end'])$(id).value=n?.[id]??'';$('timing').checked=false;$('muted').checked=!!n?.muted;
  const o=session?.midi.notes.find(n=>n.id===selected);$('before').textContent=o?`Original: Ton ${o.pitch}, Velocity ${o.velocity}, Start ${o.start}, Ende ${o.end} Ticks. Zeitbasis ${session.midi.ppq} Ticks/Viertel; Tempokurve bleibt unverändert.`:'';
}
function download(bytes,name,type){const url=URL.createObjectURL(new Blob([bytes],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),10000);}
function b64(bytes){let s='';for(let i=0;i<bytes.length;i+=16384)s+=String.fromCharCode(...bytes.slice(i,i+16384));return btoa(s);}
function unb64(text){return Uint8Array.from(atob(text),c=>c.charCodeAt(0));}
async function hash(bytes){if(!bytes)return null;return [...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(n=>n.toString(16).padStart(2,'0')).join('');}
function diagnose(){const list=$('findings');list.replaceChildren();const findings=session?.diagnose()||[];
  const messages=[...findings,{kind:'Prüfstatus',message:'Technische Prüfungen siehe TEST_RESULTS.md. Musikalische Hörfreigabe und Referenztest „Graziler Tanz“ fehlen.'},{kind:'Wiedergabe',message:'MIDI-Vergleich mit Tonhöhe, Velocity, Tempokurve und CC64-Pedal. Programmwechsel, Pitchbend und weitere Controller sind im Export erhalten, im einfachen Synthesizer nicht klanggetreu dargestellt.'}];
  if(provenance)messages.push({kind:'Transkriptionsunsicherheit',message:'Basic Pitch ist instrumentenübergreifend. Keine Pedalerkennung, keine musikalische Tempokurve; Modell-Amplituden sind keine kalibrierten Vertrauenswerte. Jeder Ton bleibt ein ungeprüfter Kandidat.'});
  if(!audio)messages.push({kind:'Unsicherheit',message:'Kein Referenzaudio: vermutete Tonhöhenfehler nicht verifizierbar.'});
  for(const f of messages){const li=document.createElement('li');if(f.id){const b=document.createElement('button');b.textContent=f.id;b.onclick=()=>{selected=f.id;$('note').value=selected;fillNote();draw();};li.append(b);}li.append(document.createTextNode(`${f.kind}: ${f.message}`));list.append(li);}
  return findings;
}
async function play(from){if(loadBusy)throw Error('Quelle wird noch geladen.');const [a,b]=section(),mode=$('mode').value;if((mode==='audio'||mode==='mix')&&!audio)throw Error('Bitte Audio laden.');if(mode!=='audio'&&!session)throw Error('Bitte MIDI laden.');ctx();await player.play({from:Math.max(a,Math.min(from,b-0.001)),end:b,mode,buffer:audio,offset:number('offset'),midi:session?.midi,notes:mode==='original'?session?.midi.notes:session?.notes});status('Wiedergabe läuft. Hörvergleich ist keine automatische Freigabe.');}
action('midi',async e=>{const f=e.target.files[0];e.target.value='';if(!f||!confirmReplace())return;if(f.size>10*1024*1024)throw Error('MIDI maximal 10 MiB.');installMidi(await f.arrayBuffer(),f.name);},'change');
action('audio',async e=>{const f=e.target.files[0];e.target.value='';if(!f)return;if(!/\.(wav|mp3)$/i.test(f.name))throw Error('Bitte WAV oder MP3 wählen.');if(f.size>50*1024*1024)throw Error('Audio maximal 50 MiB im Prototyp.');invalidateTranscription();loadBusy=true;stop();try{const bytes=new Uint8Array(await f.arrayBuffer()),decoded=await ctx().decodeAudioData(bytes.slice().buffer);if(provenance)provenance={...provenance,referenceAudioChanged:true};audioBytes=bytes;audio=decoded;audioName=f.name;resetRange();render();status('Audio vollständig dekodiert. Versatz bei Bedarf manuell einstellen.');}finally{loadBusy=false;updateTranscriptionControls();}},'change');
action('demo',()=>{if(confirmReplace())installMidi(demoMidi(),'Synthetische Tonfolge.mid');});
action('note',()=>{selected=$('note').value;fillNote();draw();},'change');
action('apply',()=>{if(!session)return;stop();const [a,b]=section();session.edit(selected,{...Object.fromEntries(['pitch','velocity','start','end'].map(id=>[id,number(id)])),...($('muted').checked?{muted:true}:session.notes.find(n=>n.id===selected)?.muted?{muted:false}:{})},[secondsToTick(session.midi,a),secondsToTick(session.midi,b)],$('reason').value,$('timing').checked);render();status('Änderung übernommen. Bitte B/C vergleichen; musikalisch noch ungeprüft.');});
action('undo',()=>{stop();session?.undo();render();status('Änderung rückgängig.');});action('redo',()=>{stop();session?.redo();render();status('Änderung wiederhergestellt.');});
action('play',()=>play(section()[0]));action('pause',()=>{stop();status('Wiedergabe pausiert.');});action('resume',()=>play(player?.position??section()[0]));
action('mode',async()=>{if(player?.running)await play(player.position);},'change');
action('seek',async()=>{const at=number('seek');if(player?.running)await play(at);else if(player)player.position=at;},'input');
for(const id of ['from','to'])action(id,()=>{section();stop();draw();},'change');
action('offset',()=>{number('offset');stop();resetRange();draw();},'change');action('all',()=>{stop();resetRange();draw();});
action('export',()=>{if(session)download(exportMidi(session.midi,session.notes),'bearbeitung.mid','audio/midi');});
action('originalMidi',()=>download(new Uint8Array(session.midi.original),'original.mid','audio/midi'));
action('originalAudio',()=>download(audioBytes,audioName,'application/octet-stream'));action('diagnose',()=>{diagnose();status('Diagnose aktualisiert; Hinweise führen zu keiner automatischen Änderung.');});
action('report',async()=>{const report={schema:1,mode:'Musikalisch ausgewogen',input:provenance?'audio-only':inputPath(audio,session),transcription:provenance,localInference:inferenceLog,sources:{audio:{name:audioName,sha256:await hash(audioBytes)},midi:{name:midiName,sha256:await hash(session?new Uint8Array(session.midi.original):null)}},offset:number('offset'),section:section(),changes:session?.history||[],redo:session?.future||[],findings:diagnose(),ai:{calls:0,scope:'external services',paidCalls:0,cost:0,provider:null,localModelRuns:inferenceLog.length},validation:{musicalApproval:false,humanListeningApproval:false,technical:'See TEST_RESULTS.md; per-edit SMF round-trip validation enabled',tempo:'Original tempo map retained',quantization:'none'}};download(JSON.stringify(report,null,2),'diagnose.json','application/json');});
action('save',()=>{const project={schema:3,transcription:provenance,localInference:inferenceLog,audio:audioBytes?{name:audioName,base64:b64(audioBytes)}:null,midi:session?{name:midiName,base64:b64(new Uint8Array(session.midi.original)),history:session.history,future:session.future}:null,offset:number('offset'),section:section()};download(JSON.stringify(project),'audio-to-good-score.projekt.json','application/json');status('Projektdatei zum Speichern erstellt; enthält Originalquellen und Änderungsverlauf.');});
action('project',async e=>{const f=e.target.files[0];e.target.value='';if(!f||!confirmReplace())return;if(f.size>85*1024*1024)throw Error('Projekt zu groß.');invalidateTranscription();loadBusy=true;stop();try{
  const p=JSON.parse(await f.text());if(![1,2,3].includes(p.schema)||!Number.isFinite(p.offset)||!Array.isArray(p.section)||p.section.length!==2||!p.section.every(Number.isFinite))throw Error('Ungültiges Projekt.');
  let s=null,ab=null,decoded=null;if(p.midi){s=new Session(parseMidi(unb64(p.midi.base64)));const replay=c=>{s.edit(c.id,{pitch:c.after.pitch,velocity:c.after.velocity,start:c.after.start,end:c.after.end,...(c.after.muted!==undefined?{muted:c.after.muted}:{})},[0,Number.MAX_SAFE_INTEGER],c.reason,true);if(s.history.length&&typeof c.at==='string')s.history.at(-1).at=c.at;};for(const c of p.midi.history)replay(c);const active=s.history.length;for(const c of [...p.midi.future].reverse())replay(c);while(s.history.length>active)s.undo();}
  if(p.audio){ab=unb64(p.audio.base64);if(ab.length>50*1024*1024)throw Error('Audio zu groß.');decoded=await ctx().decodeAudioData(ab.slice().buffer);}
  const total=Math.max(decoded?decoded.duration-p.offset:0,s?midiDuration(s.midi,s.notes):0,.01);if(p.section[0]<0||p.section[1]<=p.section[0]||p.section[1]>total+.001)throw Error('Ungültige Projektpassage.');
  if(p.transcription&&(!s||!decoded||p.transcription.provider!==MODEL_SPEC.provider||p.transcription.packageVersion!==MODEL_SPEC.packageVersion||!Array.isArray(p.transcription.audioRange)||!p.transcription.audioRange.every(Number.isFinite)))throw Error('Ungültige Transkriptionsherkunft.');
  if(p.transcription&&p.transcription.candidateMidiSha256!==await hash(new Uint8Array(s.midi.original)))throw Error('Transkriptionsherkunft passt nicht zum gespeicherten MIDI-Kandidaten.');
  provenance=p.transcription?{...p.transcription,referenceAudioChanged:p.transcription.referenceAudioChanged||p.transcription.sourceAudioSha256!==await hash(ab)}:null;inferenceLog=Array.isArray(p.localInference)?p.localInference.slice(-100):[];session=s;audioBytes=ab;audio=decoded;audioName=p.audio?.name||'';midiName=p.midi?.name||'';$('offset').value=p.offset;selected=s?.notes[0]?.id||'';resetRange();$('from').value=p.section[0];$('to').value=p.section[1];render();status('Projekt einschließlich Originalen und Undo/Redo-Verlauf geladen.');
}finally{loadBusy=false;updateTranscriptionControls();}},'change');

function invalidateTranscription(){sourceEpoch++;transcriber.cancel();pendingCandidate=null;$('transcriptionProgress').value=0;$('transcriptionStatus').textContent='Quelle gewechselt; kein aktiver Kandidat.';updateTranscriptionControls();}
function updateTranscriptionControls(){
  $('transcribe').disabled=!audio||!!session||transcribing||loadBusy;
  $('cancelTranscription').disabled=!transcribing;
  $('candidate').hidden=!pendingCandidate;
  $('acceptCandidate').disabled=transcribing||!pendingCandidate?.noteCount;
  $('originalMidi').textContent=provenance?'Unbearbeiteten Kandidaten sichern':'Original-MIDI sichern';$('mode').querySelector('[value=original]').textContent=provenance?'B · Unbearbeiteter Kandidat':'B · Ausgangs-MIDI';
  if(provenance&&!transcribing&&!pendingCandidate)$('transcriptionStatus').textContent='Kandidat im Projekt. Musikalische Prüfung steht aus.';
  $('provenance').textContent=provenance?`Kandidat: Basic Pitch ${provenance.packageVersion} · ${provenance.noteCount} Noten · Ursprung Audio allein · musikalisch ungeprüft.${provenance.referenceAudioChanged?' Referenzaudio wurde gewechselt; Zuordnung erneut prüfen.':''}`:'';
  for(const id of ['audio','midi','project','demo','from','to','offset','all','save'])$(id).disabled=transcribing;
  if(transcribing)for(const id of ['apply','undo','redo'])$(id).disabled=true;
}
action('transcribe',async()=>{
  if(!audio||session||loadBusy||transcribing)throw Error('Transkription benötigt einen Audio-only-Arbeitsbereich.');
  const range=audioRange(section(),number('offset'),audio.duration),epoch=sourceEpoch,source=audio,sourceBytes=audioBytes;
  stop();transcribing=true;pendingCandidate=null;updateTranscriptionControls();$('transcriptionProgress').value=0;
  const run={provider:MODEL_SPEC.provider,model:MODEL_SPEC,parameters:{...TRANSCRIPTION_PARAMETERS},audioRange:range,startedAt:new Date().toISOString(),state:'preparing',cost:0,remoteCalls:0};inferenceLog.push(run);inferenceLog=inferenceLog.slice(-100);const start=performance.now();
  try{
    $('transcriptionStatus').textContent='Audio vorbereiten …';
    const samples=await resamplePassage(source,range);if(epoch!==sourceEpoch||!transcribing)throw new DOMException('Transkription abgebrochen.','AbortError');
    run.sourceAudioSha256=await hash(sourceBytes);if(epoch!==sourceEpoch)throw new DOMException('Transkription abgebrochen.','AbortError');run.state='running';
    const result=await transcriber.run(samples,p=>{$('transcriptionProgress').value=p.value;$('transcriptionStatus').textContent=`${p.phase} · ${Math.round(p.value*100)} %`;});
    if(epoch!==sourceEpoch)throw new DOMException('Quelle wurde gewechselt.','AbortError');
    const candidate=candidateMidi(result.notes,range[0],range[1]-range[0]);run.candidateMidiSha256=await hash(candidate.bytes);
    Object.assign(run,{state:'completed',elapsedMs:Math.round(performance.now()-start),backend:result.backend,tensorBytes:result.tensorBytes,noteCount:candidate.noteCount,clipped:candidate.clipped,overlapChannels:candidate.overlapChannels});
    pendingCandidate={...candidate,provenance:{...run,packageVersion:MODEL_SPEC.packageVersion,uncertainty:'Ungeprüfte Modellhypothese; Amplituden nicht als Wahrscheinlichkeit kalibriert.',noteActivations:result.notes}};
    $('candidateInfo').textContent=`${candidate.noteCount} vorgeschlagene Noten für Audio ${range[0].toFixed(2)}–${range[1].toFixed(2)} s. ${candidate.clipped} Notengrenzen an den Analyseabschnitt angepasst. Kein Pedal rekonstruiert. Mit Übernehmen wird der Kandidat zur bearbeitbaren Vergleichsversion; das Audio bleibt unverändert.`;
    $('transcriptionStatus').textContent=candidate.noteCount?'Kandidat bereit. Vor musikalischer Freigabe anhören und prüfen.':'Keine Noten erkannt. Quelle bleibt unverändert; anderen Abschnitt prüfen.';
    status('Lokale Transkription abgeschlossen; Kandidat noch nicht übernommen.');
  }catch(error){run.state=error.name==='AbortError'?'cancelled':'failed';run.message=error.message;run.elapsedMs=Math.round(performance.now()-start);$('transcriptionStatus').textContent=error.message;status(error.message,error.name!=='AbortError');}
  finally{transcribing=false;updateTranscriptionControls();}
});
action('cancelTranscription',()=>{sourceEpoch++;transcriber.cancel();updateTranscriptionControls();$('cancelTranscription').disabled=true;$('transcriptionStatus').textContent='Transkription abgebrochen. Quellen unverändert.';});
action('acceptCandidate',()=>{
  if(!pendingCandidate?.noteCount||transcribing)throw Error('Kein Notenkandidat vorhanden.');
  const candidate=pendingCandidate,parsed=parseMidi(candidate.bytes);
  session=new Session(parsed);provenance=structuredClone(candidate.provenance);midiName=`${audioName} – MIDI-Kandidat.mid`;selected=parsed.notes[0]?.id||'';pendingCandidate=null;
  stop();$('offset').value=0;resetRange();$('from').value=provenance.audioRange[0];$('to').value=provenance.audioRange[1];$('mode').value='edited';render();
  $('transcriptionStatus').textContent='Kandidat übernommen. Musikalische Prüfung steht aus.';
  status('MIDI-Kandidat übernommen. A: Originalaudio · B: unbearbeiteter Kandidat · C: manuelle Bearbeitung. Bitte anhören.');
});
action('discardCandidate',()=>{pendingCandidate=null;updateTranscriptionControls();$('transcriptionStatus').textContent='Kandidat verworfen. Originalaudio unverändert.';});

const timeAt=e=>{const r=$('roll').getBoundingClientRect();return Math.max(0,Math.min(duration,((e.clientX-r.left)/r.width*1200-50)/1140*duration));};
$('roll').addEventListener('pointerdown',e=>{if(transcribing)return;drag={x:e.clientX,at:timeAt(e),id:e.target.dataset.id};$('roll').setPointerCapture(e.pointerId);});
$('roll').addEventListener('pointerup',e=>{if(!drag)return;if(Math.abs(e.clientX-drag.x)<5&&drag.id){selected=drag.id;$('note').value=selected;fillNote();}else if(Math.abs(e.clientX-drag.x)>=5){stop();$('from').value=Math.min(drag.at,timeAt(e)).toFixed(4);$('to').value=Math.max(drag.at,timeAt(e)).toFixed(4);}drag=null;draw();});
$('roll').addEventListener('pointercancel',()=>{drag=null;});
window.addEventListener('beforeunload',e=>{if(session?.history.length||audio){e.preventDefault();e.returnValue='';}});
function frame(){if(player){const pos=player.position;$('clock').value=`${pos.toFixed(2)} s`;$('seek').value=pos;const line=$('playhead');if(line){const x=50+pos/duration*1140;line.setAttribute('x1',x);line.setAttribute('x2',x);}}requestAnimationFrame(frame);}render();frame();
