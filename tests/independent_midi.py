"""Independent export check. pip install mido==1.3.3; run after browser.cjs."""
import json
import os
from pathlib import Path
import mido

root = Path(os.environ.get('TEST_OUTPUT_DIR', '/tmp/ags-browser-results'))
a = mido.MidiFile(root / 'source.mid')
b = mido.MidiFile(root / 'edited.mid')
assert a.ticks_per_beat == b.ticks_per_beat

def events(file):
    output = []
    for track in file.tracks:
        tick = 0
        for event in track:
            tick += event.time
            output.append((tick, event))
    return output

original, edited = events(a), events(b)
assert len(original) == len(edited)
changes = []
for (tick_a, event_a), (tick_b, event_b) in zip(original, edited):
    assert tick_a == tick_b
    if event_a != event_b:
        assert event_a.type in ('note_on', 'note_off')
        assert event_a.note == 60 and event_b.note == 62
        assert event_a.copy(note=62) == event_b
        changes.append(event_a.type)
assert changes == ['note_on', 'note_off']
assert list(mido.merge_tracks(a.tracks)) != list(mido.merge_tracks(b.tracks))
assert a.length == b.length
result = {'parser': 'mido 1.3.3', 'passed': True, 'events': len(original), 'changed_events': changes, 'all_absolute_ticks_unchanged': True, 'duration_seconds': b.length}
(root / 'independent-midi-results.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))

# A second fixture exercises actual tempo changes, CC64, multiple tracks and SysEx.
import subprocess
subprocess.run(['node', str(Path(__file__).with_name('generate-fixtures.js'))], check=True)
ta, tb = mido.MidiFile(root / 'tempo-original.mid'), mido.MidiFile(root / 'tempo-edited.mid')
assert ta.length == tb.length
for track_a, track_b in zip(ta.tracks, tb.tracks):
    assert len(track_a) == len(track_b)
    tick_a = tick_b = 0
    for event_a, event_b in zip(track_a, track_b):
        tick_a += event_a.time
        tick_b += event_b.time
        assert tick_a == tick_b
        if event_a.type in ('note_on', 'note_off') and event_a.note == 60:
            assert event_b.note == 61
            assert event_b.velocity == (72 if event_a.type == 'note_on' else event_a.velocity)
        else:
            assert event_a == event_b
# Mido iteration independently integrates the tempo map into seconds.
absolute_a = absolute_b = 0.0
for event_a, event_b in zip(ta, tb):
    absolute_a += event_a.time
    absolute_b += event_b.time
    assert abs(absolute_a - absolute_b) < 1e-12
result['variable_tempo_duration_seconds'] = tb.length
result['tempo_pedal_sysex_tracks_preserved'] = True
result['independent_seconds_equal'] = True
(root / 'independent-midi-results.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
