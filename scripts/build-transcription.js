import {MODEL_SPEC} from '../model-spec.js';
import {build} from 'esbuild';
import {readFile,writeFile,mkdir,copyFile,readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../',import.meta.url),dest=new URL('vendor/',root),modules=new URL('node_modules/',root);
for(const path of ['','model/','wasm/','licenses/'])await mkdir(new URL(path,dest),{recursive:true});
await build({entryPoints:[new URL('transcription-worker.js',root).pathname],outfile:new URL('transcription-worker.js',dest).pathname,bundle:true,format:'iife',platform:'browser',target:['es2020'],minify:true,legalComments:'external'});
const files={};
for(const path of ['model.json','group1-shard1of1.bin']){
 const src=new URL(`@spotify/basic-pitch/model/${path}`,modules);await copyFile(src,new URL(`model/${path}`,dest));const b=await readFile(src);files[path]={bytes:b.length,sha256:createHash('sha256').update(b).digest('hex')};
}
for(const path of ['tfjs-backend-wasm.wasm','tfjs-backend-wasm-simd.wasm'])await copyFile(new URL(`@tensorflow/tfjs-backend-wasm/dist/${path}`,modules),new URL(`wasm/${path}`,dest));
if(JSON.stringify(files)!==JSON.stringify(MODEL_SPEC.files))throw Error('Upstream-Modell entspricht nicht den geprüften SHA-256-Werten.');
const manifest={provider:'spotify-basic-pitch',packageVersion:'1.0.1',model:'ICASSP 2022',tensorflow:'3.21.0',license:'Apache-2.0',files};
await writeFile(new URL('model-manifest.json',dest),JSON.stringify(manifest,null,2)+'\n');
const licenses=[];
async function scan(folder){for(const entry of await readdir(folder,{withFileTypes:true})){
 if(!entry.isDirectory()||entry.name.startsWith('.'))continue;
 const dir=new URL(entry.name+'/',folder);
 if(entry.name.startsWith('@')){await scan(dir);continue;}
 let pkg;try{pkg=JSON.parse(await readFile(new URL('package.json',dir),'utf8'));}catch{continue;}
 const notices=(await readdir(dir)).filter(n=>/^(licen[sc]e|notice|copying)(\.|$)/i.test(n));
 for(const name of notices){const text=await readFile(new URL(name,dir),'utf8');const filename=`${pkg.name.replaceAll('/','_').replaceAll('@','')}-${name}`;await writeFile(new URL(filename,new URL('licenses/',dest)),text);licenses.push({package:pkg.name,version:pkg.version,license:pkg.license,file:filename});}
 }}
await scan(modules);await writeFile(new URL('licenses/index.json',dest),JSON.stringify(licenses,null,2)+'\n');
console.log(JSON.stringify(manifest,null,2));
