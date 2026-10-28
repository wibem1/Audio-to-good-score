import {writeFileSync,mkdirSync} from 'node:fs';
import {join} from 'node:path';
import {fixture} from './fixtures.js';
import {parseMidi,exportMidi} from '../midi.js';
import {Session} from '../model.js';
const out=process.env.TEST_OUTPUT_DIR||'/tmp/ags-browser-results';mkdirSync(out,{recursive:true});
const bytes=fixture(),m=parseMidi(bytes),s=new Session(m);
s.edit(s.notes[0].id,{pitch:61,velocity:72},[0,960],'Synthetischer Test mit Tempowechseln');
writeFileSync(join(out,'tempo-original.mid'),bytes);writeFileSync(join(out,'tempo-edited.mid'),exportMidi(m,s.notes));
