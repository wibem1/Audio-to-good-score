import {vlq} from './midi.js';
export function demoMidi(){
  const events=[{tick:0,data:[255,81,3,7,161,32]},{tick:0,data:[255,88,4,4,2,24,8]}];
  [60,64,67,72,71,67,64,60].forEach((pitch,i)=>{events.push({tick:i*480,data:[144,pitch,82]},{tick:i*480+420,data:[128,pitch,40]});});
  events.push({tick:3840,data:[255,47,0]});events.sort((a,b)=>a.tick-b.tick);const track=[];let at=0;
  for(const e of events){track.push(...vlq(e.tick-at),...e.data);at=e.tick;}
  const len=track.length;return new Uint8Array([77,84,104,100,0,0,0,6,0,0,0,1,1,224,77,84,114,107,len>>>24,len>>>16&255,len>>>8&255,len&255,...track]);
}
