let runtime,queue=Promise.resolve();
async function init(){
 const progress=message=>self.postMessage({progress:message});
 progress('Verarbeitungskern wird geladen. Beim ersten Start kann das etwa eine Minute dauern.');
 importScripts('https://cdn.jsdelivr.net/pyodide/v0.29.1/full/pyodide.js');
 const py=await loadPyodide({indexURL:'https://cdn.jsdelivr.net/pyodide/v0.29.1/full/'});
 await py.loadPackage('micropip');
 progress('Musikbibliotheken werden lokal im Browser vorbereitet …');
 await py.runPythonAsync("import micropip\nawait micropip.install(['music21==9.9.1','mido==1.3.3','jsonschema==4.26.0'])");
 const response=await fetch(new URL('./core.zip',self.location.href));if(!response.ok)throw Error('Kernpaket nicht erreichbar.');
 py.unpackArchive(await response.arrayBuffer(),'zip',{extractDir:'/musiccraft'});
 py.runPython("import sys,json\nsys.path.insert(0,'/musiccraft')\nfrom musiccraft.web_bridge import dispatch");
 return py;
}
self.onmessage=({data:m})=>{queue=queue.catch(()=>{}).then(async()=>{try{
 runtime??=init();const py=await runtime;py.globals.set('mc_request',JSON.stringify(m));
 const result=JSON.parse(await py.runPythonAsync('json.dumps(dispatch(json.loads(mc_request)),ensure_ascii=False,allow_nan=False)'));
 self.postMessage({id:m.id,result});
 }catch(e){self.postMessage({id:m.id,error:String(e).slice(-5000)});}});};
