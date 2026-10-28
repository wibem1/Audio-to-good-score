"""Run after browser.cjs; checks grouped passage export with independent mido."""
import os,json,mido
from pathlib import Path
root=Path(os.environ.get('TEST_OUTPUT_DIR','/tmp/ags-browser-results'))
a=mido.MidiFile(root/'passage-source.mid');b=mido.MidiFile(root/'batch-edited.mid')
def notes(m):
    out=[]
    for track in m.tracks:
        tick=0
        for e in track:
            tick+=e.time
            if e.type in ('note_on','note_off'):out.append((tick,e.type,e.note,e.velocity,e.channel))
    return out
assert notes(b)==[n for n in notes(a) if n[2] not in (72,74)]
assert (root/'batch-restored.mid').read_bytes()==(root/'passage-source.mid').read_bytes()
r={'parser':'mido 1.3.3','passed':True,'selected_octaves_removed':2,'remaining_event_times_and_velocities_unchanged':True,'single_undo_restores_original_bytes':True}
(root/'batch-validation.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
