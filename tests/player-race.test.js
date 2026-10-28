import {test} from 'node:test';
import assert from 'node:assert/strict';
import {Player} from '../player.js';
function setup(){
 const pending=[],starts=[];
 const node=()=>({gain:{value:0,setValueAtTime(){},linearRampToValueAtTime(){},setTargetAtTime(){}},frequency:{value:0},connect(){},disconnect(){},start(...args){starts.push(args);},stop(){}});
 const context={currentTime:2,destination:{},createGain:node,createDynamicsCompressor:node,createBufferSource:node,createOscillator:node,resume(){return new Promise(resolve=>pending.push(resolve));}};
 return {player:new Player(context),pending,starts};
}
const request={from:0,end:2,mode:'audio',buffer:{duration:5}};
test('pause during pending audio activation prevents a late restart',async()=>{
 const {player,pending,starts}=setup();const playing=player.play(request);player.stop();pending[0]();
 try{assert.equal(await playing,false);assert.equal(player.running,false);assert.equal(starts.length,0);}finally{player.stop();}
});
test('latest play wins even when older audio activation resolves last',async()=>{
 const {player,pending,starts}=setup();const older=player.play(request),newer=player.play({...request,from:1});
 pending[1]();try{assert.equal(await newer,true);pending[0]();assert.equal(await older,false);assert.equal(starts.length,1);assert.equal(starts[0][1],1);assert.equal(player.from,1);}finally{pending[0]();await older;player.stop();}
});
