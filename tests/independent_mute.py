"""Run after browser.cjs; independently verify selective note exclusion."""
import json,os
from pathlib import Path
import mido
root=Path(os.environ.get('TEST_OUTPUT_DIR','/tmp/ags-browser-results'))
def absolute(name):
    result=[]
    for track in mido.MidiFile(root/name).tracks:
        tick=0
        for event in track:
            tick+=event.time
            result.append((tick,event.copy(time=0)))
    return result
original=absolute('source.mid')
expected=[(tick,event) for tick,event in original if not (event.type=='note_on' and event.note==60 and tick==0 or event.type=='note_off' and event.note==60 and tick==420)]
assert absolute('muted.mid')==expected
result={'parser':'mido 1.3.3','passed':True,'removed_events':2,'all_remaining_events_and_absolute_ticks_unchanged':True}
(root/'independent-mute-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
