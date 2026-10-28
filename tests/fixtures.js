import {vlq} from '../midi.js';
export function smf(tracks,format=1,ppq=480){const out=[77,84,104,100,0,0,0,6,0,format,0,tracks.length,ppq>>8,ppq&255];for(const ev of tracks){let prev=0;const data=[];for(const [at,...bytes]of ev){data.push(...vlq(at-prev),...bytes);prev=at;}out.push(77,84,114,107,0,0,data.length>>8,data.length&255,...data);}return new Uint8Array(out);}
export const fixture=()=>smf([
 [[0,255,81,3,7,161,32],[240,255,81,3,6,26,128],[480,255,81,3,9,39,192],[960,255,47,0]],
 [[0,255,3,4,84,101,115,116],[0,192,0],[0,176,64,127],[0,176,7,100],[0,240,3,1,2,247],[0,144,60,80],[240,128,60,45],[240,144,64,90],[480,128,64,50],[720,176,64,0],[960,255,47,0]]
]);
