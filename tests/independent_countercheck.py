"""Independent event check after browser.cjs local neural countercheck."""
from pathlib import Path
import os,json,mido
root=Path(os.environ.get('TEST_OUTPUT_DIR','/tmp/ags-browser-results'))
a=mido.MidiFile(root/'counter-original.mid');b=mido.MidiFile(root/'counter-edited.mid');assert len(a.tracks)==len(b.tracks)==1
changes=0
for x,y in zip(a.tracks[0],b.tracks[0]):
    assert x.time==y.time
    if x!=y:
        assert x.type in ('note_on','note_off') and x.note==72 and y.note==60
        assert x.copy(note=60)==y;changes+=1
assert len(a.tracks[0])==len(b.tracks[0]) and changes==2 and a.length==b.length
result={'passed':True,'parser':'mido 1.3.3','changed_pitch_events':changes,'all_event_times_unchanged':True,'duration_seconds':b.length}
(root/'countercheck-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
