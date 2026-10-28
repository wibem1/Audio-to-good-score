// Bundled with pinned, unmodified Apache-2.0 Basic Pitch/TensorFlow dependencies.
import {MODEL_SPEC} from './model-spec.js';
import * as tf from '@tensorflow/tfjs';
import {setWasmPaths} from '@tensorflow/tfjs-backend-wasm';
import {BasicPitch,outputToNotesPoly,noteFramesToTime} from '@spotify/basic-pitch';
self.onmessage=async({data})=>{
  try{
    const {samples,parameters}=data;
    if(!(samples instanceof Float32Array)||samples.length<2205||samples.length>60*22050)throw Error('Transkription benötigt 0,1 bis 60 Sekunden Audio.');
    if(!samples.every(Number.isFinite))throw Error('Audiosignal enthält ungültige Werte.');
    self.postMessage({type:'progress',value:0,phase:'Modell laden'});
    tf.env().set('WASM_HAS_MULTITHREAD_SUPPORT',false);
    setWasmPaths(new URL('./wasm/',self.location.href).href);
    await tf.setBackend('wasm');await tf.ready();
    // TFJS 3.21 signal.frame calls Fill without dtype; WASM lacks the CPU default.
    // Supply float32 only for an omitted dtype. Upstream package files remain unchanged.
    const fill=tf.getKernel('Fill','wasm');
    tf.unregisterKernel('Fill','wasm');
    tf.registerKernel({...fill,kernelFunc:args=>fill.kernelFunc({...args,attrs:{...args.attrs,dtype:args.attrs.dtype??'float32'}})});
    const files={};
    for(const [name,spec]of Object.entries(MODEL_SPEC.files)){
      const response=await fetch(new URL('./model/'+name,self.location.href));
      if(!response.ok)throw Error('Lokale Modelldatei fehlt.');
      const bytes=await response.arrayBuffer(),digest=[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(n=>n.toString(16).padStart(2,'0')).join('');
      if(bytes.byteLength!==spec.bytes||digest!==spec.sha256)throw Error('Modell-Prüfsumme stimmt nicht. Modelldateien neu erstellen.');
      files[name]=bytes;
    }
    const json=JSON.parse(new TextDecoder().decode(files['model.json']));
    const model=tf.loadGraphModel(tf.io.fromMemory({...json,weightSpecs:json.weightsManifest.flatMap(w=>w.weights),weightData:files['group1-shard1of1.bin']}));
    const basicPitch=new BasicPitch(model),frames=[],onsets=[];
    await basicPitch.evaluateModel(samples,(f,o)=>{for(const row of f)frames.push(row);for(const row of o)onsets.push(row);},p=>self.postMessage({type:'progress',value:p,phase:'Audio analysieren'}));
    self.postMessage({type:'progress',value:1,phase:'Notenkandidat bilden'});
    const notes=noteFramesToTime(outputToNotesPoly(frames,onsets,parameters.onsetThreshold,parameters.frameThreshold,parameters.minimumNoteFrames,true,null,null,true));
    self.postMessage({type:'result',notes,backend:tf.getBackend(),model:MODEL_SPEC,tensorBytes:tf.memory().numBytes});
  }catch(error){self.postMessage({type:'error',message:error.message||String(error)});}
};
