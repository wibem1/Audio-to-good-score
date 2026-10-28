// SMF 0/1, PPQ only. Unsupported timebases/formats fail explicitly.
const ascii = bytes => String.fromCharCode(...bytes);
const u16 = n => [n >>> 8 & 255, n & 255];
const u32 = n => [n >>> 24 & 255, n >>> 16 & 255, n >>> 8 & 255, n & 255];
export function vlq(n) {
  if (!Number.isInteger(n) || n < 0 || n > 0x0fffffff) throw Error('MIDI-Zeit außerhalb des SMF-Bereichs.');
  const a = [n & 127]; while (n >>>= 7) a.unshift((n & 127) | 128); return a;
}
export function parseMidi(input) {
  const bytes = new Uint8Array(input); let p = 0, limit = bytes.length;
  if (bytes.length > 10 * 1024 * 1024) throw Error('MIDI maximal 10 MiB.');
  const take = n => { if (p + n > limit) throw Error('Abgeschnittene MIDI-Datei.'); const b = bytes.slice(p, p += n); return b; };
  const num = n => [...take(n)].reduce((s,b) => s * 256 + b, 0);
  const variable = () => { let n=0; for(let i=0;i<4;i++){const b=num(1); n=n*128+(b&127); if(!(b&128)) return n;} throw Error('Ungültige variable MIDI-Länge.'); };
  if(ascii(take(4)) !== 'MThd') throw Error('Kein Standard-MIDI.');
  const hlen=num(4); if(hlen<6) throw Error('Ungültiger MIDI-Header.');
  const format=num(2), count=num(2), ppq=num(2); take(hlen-6);
  if(format>1 || !count || (format===0 && count!==1)) throw Error('Nur SMF Typ 0 und 1 werden unterstützt.');
  if(!ppq || ppq&0x8000) throw Error('SMPTE-Zeitbasis wird noch nicht unterstützt.');
  const tracks=[], notes=[], warnings=[]; let totalEvents=0;
  for(let t=0;t<count;t++){
    if(ascii(take(4))!=='MTrk') throw Error('MIDI-Spur fehlt.');
    const size=num(4), end=p+size; if(end>bytes.length) throw Error('Abgeschnittene MIDI-Spur.'); limit=end;
    let tick=0, running=0, ended=false; const events=[], active=new Map();
    while(p<end){
      tick+=variable(); if(!Number.isSafeInteger(tick)) throw Error('MIDI zu lang.');
      let status=num(1); if(status<128){if(!running) throw Error('Ungültiger Running Status.'); p--; status=running;}
      let data, meta;
      if(status===255){ running=0; meta=num(1); data=[...take(variable())]; if(meta===47){if(data.length)throw Error('Ungültiges Spur-Ende.'); ended=true;} if(meta===81 && (data.length!==3 || !data.some(Boolean))) throw Error('Ungültiges Tempo.'); }
      else if(status===240 || status===247){running=0;data=[...take(variable())];}
      else if(status>=128 && status<240){running=status; data=[...take([12,13].includes(status>>4)?1:2)];if(data.some(b=>b>127)) throw Error('Ungültige MIDI-Daten.');}
      else throw Error('Nicht unterstütztes MIDI-Systemereignis.');
      if(++totalEvents>100000) throw Error('Prototyp unterstützt maximal 100.000 MIDI-Ereignisse.');
      const e={tick,status,data,meta,order:events.length}; events.push(e);
      const kind=status>>4, key=`${status&15}:${data[0]}`;
      if(kind===9 && data[1]>0){const q=active.get(key)||[];if(q.length) warnings.push(`Spur ${t+1}: überlappende gleiche Tonhöhe; Zuordnung FIFO unsicher.`);q.push(e);active.set(key,q);}
      if(kind===8 || (kind===9 && data[1]===0)){
        const q=active.get(key)||[], on=q.shift();
        if(!on) warnings.push(`Spur ${t+1}: Note-off ohne Note-on.`);
        else {const id=`${t}:${on.order}`;notes.push({id,track:t,channel:status&15,pitch:on.data[0],velocity:on.data[1],start:on.tick,end:tick,on:on.order,off:e.order});}
      }
      if(ended && p!==end) throw Error('Daten nach MIDI-Spur-Ende.');
    }
    if(!ended) throw Error('MIDI-Spur-Ende fehlt.');
    for(const q of active.values()) if(q.length) warnings.push(`Spur ${t+1}: ungeschlossene Noten; keine automatische Reparatur.`);
    tracks.push(events);limit=bytes.length;
  }
  if(p!==bytes.length) throw Error('Zusätzliche MIDI-Daten nach letzter Spur.');
  if(notes.length>10000)throw Error('Prototyp unterstützt maximal 10.000 Noten.');
  const tempos=tracks.flatMap((events,track)=>events.filter(e=>e.status===255 && e.meta===81).map(e=>({...e,track}))).sort((a,b)=>a.tick-b.tick||a.track-b.track||a.order-b.order);
  return {format,ppq,tracks,notes,warnings,tempos,original:Array.from(bytes)};
}
export function tickToSeconds(midi,tick){
  let at=0,sec=0,tempo=500000;
  for(const e of midi.tempos){if(e.tick>tick)break;sec+=(e.tick-at)*tempo/midi.ppq/1e6;at=e.tick;tempo=e.data[0]*65536+e.data[1]*256+e.data[2];}
  return sec+(tick-at)*tempo/midi.ppq/1e6;
}
export function secondsToTick(midi,seconds){
  let at=0,sec=0,tempo=500000;
  for(const e of midi.tempos){const next=sec+(e.tick-at)*tempo/midi.ppq/1e6;if(next>seconds)break;sec=next;at=e.tick;tempo=e.data[0]*65536+e.data[1]*256+e.data[2];}
  return Math.max(0,Math.round(at+(seconds-sec)*midi.ppq*1e6/tempo));
}
export function exportMidi(midi,notes=midi.notes){
  if(JSON.stringify(notes)===JSON.stringify(midi.notes)) return new Uint8Array(midi.original);
  const tracks=structuredClone(midi.tracks);
  for(const n of notes){const on=tracks[n.track][n.on],off=tracks[n.track][n.off];on.tick=n.start;on.data=[n.pitch,n.velocity];off.tick=n.end;off.data[0]=n.pitch;}
  const result=[77,84,104,100,...u32(6),...u16(midi.format),...u16(tracks.length),...u16(midi.ppq)];
  for(const events of tracks){
    const eot=events.find(e=>e.status===255&&e.meta===47);
    eot.tick=events.reduce((end,e)=>Math.max(end,e.tick),eot.tick);
    const sorted=events.filter(e=>e!==eot).sort((a,b)=>a.tick-b.tick||a.order-b.order); sorted.push(eot);
    const data=[];let previous=0;
    for(const e of sorted){const prefix=[...vlq(e.tick-previous),e.status];previous=e.tick;
      if(e.status===255) prefix.push(e.meta,...vlq(e.data.length));
      else if(e.status===240||e.status===247)prefix.push(...vlq(e.data.length));
      data.push(...prefix);for(const b of e.data)data.push(b);
    }
    result.push(77,84,114,107,...u32(data.length)); for(const b of data)result.push(b);
  }
  return new Uint8Array(result);
}
export function midiDuration(midi,notes=midi.notes){return Math.max(0,...notes.map(n=>tickToSeconds(midi,n.end)),...midi.tracks.map(t=>tickToSeconds(midi,t.at(-1).tick)));}
