export const MUSICAL_FEATURES=['tonality','meter','tempo','bar_count','style','form','melody','harmony','bass','accompaniment','rhythm','expression'];
export function analysisStage(a){return a&&MUSICAL_FEATURES.every(k=>a.content.findings.some(f=>f.feature===k))?'interpretation':'preliminary';}
export function stageText(a,attempt){const kind=analysisStage(a);if(attempt?.status==='failed')return 'KI-Analyse fehlgeschlagen – '+(kind==='preliminary'?'nur Voranalyse vorhanden.':'vorherige musikalische Analyse erhalten.');return kind==='preliminary'?'Lokale Voranalyse – musikalische Deutung steht noch aus.':'Musikalische Analyse vorhanden – Sicherheiten und offene Stellen prüfen.';}
export async function interpret({base,hints,core,request,guard=()=>{}}){
 const exchange=await core('analysis_request',{analysis:base,hints});guard();
 if(exchange.stats.text_chars>60000)throw Error('Die Befundmenge ist für einen einzelnen KI-Auftrag zu groß. Bitte einen kürzeren Abschnitt wählen; es wurde kein KI-Auftrag gesendet.');
 const text=await request(exchange);guard();let delta;
 try{let s=text.trim();if(s.startsWith('```'))s=s.replace(/^```(?:json)?\s*/i,'').replace(/\s*```$/,'');delta=JSON.parse(s);}catch{throw Error('KI-Analyse ist kein vollständiges JSON. Bisherige Analyse bleibt erhalten. Keine automatische Wiederholung.');}
 const result=await core('analysis_merge',{analysis:base,document:delta});guard();return result;
}
