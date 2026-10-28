"""Independent SMF and provenance validation after transcription-browser.cjs."""
import hashlib
import json
import os
from pathlib import Path
import mido

root = Path(os.environ.get('TEST_OUTPUT_DIR', '/tmp/ags-transcription-results'))
original = mido.MidiFile(root / 'candidate.mid')
edited = mido.MidiFile(root / 'edited.mid')
assert original.type == edited.type == 0
assert original.ticks_per_beat == edited.ticks_per_beat == 1000
assert len(original.tracks) == len(edited.tracks) == 1
assert len(original.tracks[0]) == len(edited.tracks[0])
changes = 0
for a, b in zip(original.tracks[0], edited.tracks[0]):
    assert a.time == b.time
    if a != b:
        assert a.type == b.type == 'note_on'
        assert a.copy(velocity=70) == b
        changes += 1
assert changes == 1
assert original.length == edited.length
report = json.loads((root / 'diagnosis.json').read_text())
assert report['transcription']['candidateMidiSha256'] == hashlib.sha256((root / 'candidate.mid').read_bytes()).hexdigest()
assert report['transcription']['sourceAudioSha256'] == hashlib.sha256((root / 'polyphonic.wav').read_bytes()).hexdigest()
assert report['ai']['calls'] == report['ai']['paidCalls'] == report['ai']['cost'] == 0
assert report['validation']['humanListeningApproval'] is False
result = {'parser':'mido 1.3.3','passed':True,'note_count':sum(n.type=='note_on' and n.velocity>0 for n in original.tracks[0]),'changed_note_on_velocities':changes,'unchanged_absolute_times':True,'unchanged_tempo':True,'original_audio_and_candidate_hashes_verified':True,'duration_seconds':original.length}
(root / 'independent-transcription-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
