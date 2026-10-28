import {tickToSeconds} from './midi.js';
export function notePlan(midi,notes){
  const pedals=midi.tracks.flatMap((track,t)=>track.filter(e=>(e.status>>4)===11&&e.data[0]===64).map(e=>({time:tickToSeconds(midi,e.tick),channel:e.status&15,value:e.data[1],track:t,order:e.order}))).sort((a,b)=>a.time-b.time||a.track-b.track||a.order-b.order);
  return notes.filter(n=>!n.muted).map(n=>{
    const start=tickToSeconds(midi,n.start);let end=tickToSeconds(midi,n.end),down=false;
    const beforeOff=p=>p.time<end||(p.time===end&&(p.track<n.track||(p.track===n.track&&p.order<n.off)));
    for(const p of pedals)if(p.channel===n.channel&&beforeOff(p))down=p.value>=64;
    if(down){const up=pedals.find(p=>p.channel===n.channel&&!beforeOff(p)&&p.value<64);end=up?up.time:Math.max(end,...midi.tracks.map(t=>tickToSeconds(midi,t.at(-1).tick)));}
    return {id:n.id,start,end,pitch:n.pitch,velocity:n.velocity};
  }).sort((a,b)=>a.start-b.start);
}
export class Player {
  constructor(context){this.ctx=context;this.nodes=new Set();this.running=false;this.position=0;this.generation=0;
    this.master=context.createGain();this.master.gain.value=0.7;
    const compressor=context.createDynamicsCompressor();this.master.connect(compressor);compressor.connect(context.destination);
  }
  stop(){this.generation++;if(this.running)this.position=Math.min(this.end,this.from+Math.max(0,this.ctx.currentTime-this.anchor));this.running=false;clearInterval(this.timer);for(const n of this.nodes){try{n.stop();}catch{}}this.nodes.clear();}
  async play({from,end,mode,buffer,offset=0,midi,notes}){
    this.stop();const generation=this.generation;await this.ctx.resume();if(generation!==this.generation)return false;this.from=from;this.end=end;this.position=from;this.anchor=this.ctx.currentTime+0.06;this.running=true;
    if((mode==='audio'||mode==='mix')&&buffer){
      const audioAt=from+offset, delay=Math.max(0,-audioAt), start=Math.max(0,audioAt), duration=Math.min(end-from-delay,buffer.duration-start);
      if(duration>0){const src=this.ctx.createBufferSource();src.buffer=buffer;src.connect(this.master);src.start(this.anchor+delay,start,duration);this.nodes.add(src);src.onended=()=>{this.nodes.delete(src);src.disconnect();};}
    }
    const plan=midi&&mode!=='audio'?notePlan(midi,notes).filter(n=>n.end>from&&n.start<end):[];let index=0;
    const schedule=()=>{
      const now=this.ctx.currentTime, horizon=now+0.18;
      while(index<plan.length&&this.anchor+Math.max(0,plan[index].start-from)<horizon){
        const n=plan[index++],start=this.anchor+Math.max(0,n.start-from),finish=this.anchor+Math.min(end,n.end)-from;
        if(finish<=now)continue;
        const osc=this.ctx.createOscillator(),gain=this.ctx.createGain();osc.type='triangle';osc.frequency.value=440*2**((n.pitch-69)/12);
        const at=Math.max(start,now), level=0.075*n.velocity/127;
        gain.gain.setValueAtTime(0,at);gain.gain.linearRampToValueAtTime(level,at+0.005);gain.gain.setTargetAtTime(level*0.35,at+0.03,0.3);gain.gain.setTargetAtTime(0,Math.max(at+0.006,finish),0.018);
        osc.connect(gain);gain.connect(this.master);osc.start(at);osc.stop(Math.max(at+0.1,finish+0.12));this.nodes.add(osc);osc.onended=()=>{this.nodes.delete(osc);osc.disconnect();gain.disconnect();};
      }
      this.position=from+Math.max(0,now-this.anchor);
      if(this.position>=end)this.stop();
    };schedule();this.timer=setInterval(schedule,40);return true;
  }
}
