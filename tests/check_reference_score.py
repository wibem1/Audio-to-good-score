"""Usage: python tests/check_reference_score.py SOURCE.mid MAPPING.json SCORE.musicxml [ROUNDTRIP.musicxml]
External test dependencies: mido 1.3.3, music21 9.9.1. User music stays outside the repository.
"""
import sys,json,hashlib
from pathlib import Path
from collections import Counter
from fractions import Fraction
import xml.etree.ElementTree as ET
import mido
from music21 import converter,chord
source,mapping_path,score_path=map(Path,sys.argv[1:4]);mapping=json.loads(mapping_path.read_text());original=mido.MidiFile(source)
pitches=Counter(e.note for track in original.tracks for e in track if e.type=='note_on' and e.velocity>0)
# Planned score note times are expressed in quarter notes independently of MIDI seconds.
plan=Counter()
for hand in mapping['voices']:
    for voice in hand:
        for g in voice:
            for n in g['notes']:plan[(n['pitch'],Fraction(g['start'],4),Fraction(g['end']-g['start'],4),g['staff'])]+=1
results=[]
for path in [score_path,*map(Path,sys.argv[4:])]:
    s=converter.parse(path);actual=Counter()
    assert len(s.parts)==2
    for staff,part in enumerate(s.parts,1):
        for n in part.stripTies().flatten().notes:
            for p in (n.pitches if isinstance(n,chord.Chord) else [n.pitch]):actual[(p.midi,Fraction(str(n.offset)),Fraction(str(n.duration.quarterLength)),staff)]+=1
    assert actual==plan,(path,'score timing/pitch mismatch')
    assert Counter({p:sum(v for (pitch,_,_,_),v in actual.items() if pitch==p) for p in pitches})==pitches
    x=ET.parse(path);assert x.find('.//sound').get('tempo') is not None
    divisions=1
    for part in x.findall('./part'):
        for measure in part.findall('measure'):
            divisions=int(measure.findtext('./attributes/divisions',str(divisions)));totals=Counter()
            for n in measure.findall('note'):
                if n.find('chord') is None:totals[n.findtext('voice','1')]+=Fraction(n.findtext('duration'))/divisions
            assert all(v==Fraction(mapping['bar'],4) for v in totals.values()),(path,measure.get('number'),totals)
    results.append({'file_role':'generated' if path==score_path else 'native_roundtrip','note_attacks_after_tie_join':sum(actual.values()),'all_pitches_staves_notated_starts_durations_equal_plan':True})
result={'passed':True,'source_midi_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_note_attacks':sum(pitches.values()),'cases':results,'performance_midi_modified':False,'human_listening_approval':False}
print(json.dumps(result,indent=2))
