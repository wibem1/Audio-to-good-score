"""pip install music21==9.9.1 verovio==5.7.0; run after generate-score.js."""
from pathlib import Path
import json,os
from collections import Counter
import xml.etree.ElementTree as ET
import music21,verovio
root=Path(os.environ.get('TEST_OUTPUT_DIR','/tmp/ags-finish-results'))
score=json.loads((root/'score.json').read_text());xml=ET.parse(root/'piano.musicxml');bar=score['bar']
for measure in xml.findall('.//part/measure'):
    at=0;positions={};durations={}
    for child in measure:
        if child.tag=='backup':at-=int(child.findtext('duration'));assert at==0
        elif child.tag=='note':
            duration=int(child.findtext('duration'));voice=child.findtext('voice')
            if child.find('chord') is None:positions[voice]=at;at+=duration;durations[voice]=durations.get(voice,0)+duration
            assert 0<=positions[voice] and at<=bar
    assert durations and all(v==bar for v in durations.values())
parsed=music21.converter.parse(str(root/'piano.musicxml')).stripTies()
actual=[]
for part in parsed.parts:
    for element in part.flatten().notes:
        for pitch in element.pitches:actual.append((pitch.midi,round(float(element.offset)*4),round(float(element.duration.quarterLength)*4)))
expected=[]
for hand in score['voices']:
    for voice in hand:
        for group in voice:
            for note in group['notes']:expected.append((note['pitch'],group['start'],group['end']-group['start']))
assert Counter(actual)==Counter(expected),(actual,expected)
toolkit=verovio.toolkit();toolkit.setOptions({'inputFrom':'musicxml','pageWidth':1600,'pageHeight':2200,'adjustPageHeight':True})
assert toolkit.loadFile(str(root/'piano.musicxml'));assert toolkit.getPageCount()>0
svg=toolkit.renderToSVG(1);assert '<svg' in svg and 'note' in svg
(root/'score.svg').write_text(svg)
result={'passed':True,'parser':'music21 9.9.1','renderer':toolkit.getVersion(),'notes_after_tie_rejoin':len(actual),'all_quantized_pitches_onsets_durations_equal':True,'all_voice_measures_filled':True,'staves':len(parsed.parts),'rendered_pages':toolkit.getPageCount(),'dorico_import':False,'musescore_import':False,'human_musical_approval':False}
(root/'score-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
