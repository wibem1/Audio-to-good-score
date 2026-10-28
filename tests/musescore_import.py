"""Actual MuseScore CLI test, not a substitute parser. Run musescore-fixtures.js first.
MUSESCORE_EXECUTABLE points to a real installation; QT_QPA_PLATFORM=offscreen for headless.
"""
import os,json,subprocess,hashlib,re
from pathlib import Path
from fractions import Fraction
from collections import Counter
import xml.etree.ElementTree as ET
root=Path(os.environ.get('TEST_OUTPUT_DIR','/tmp/ags-musescore-results'))
exe=os.environ.get('MUSESCORE_EXECUTABLE','musescore3');env={**os.environ};env.setdefault('QT_QPA_PLATFORM','offscreen')
version=subprocess.run([exe,'--version'],env=env,capture_output=True,text=True,check=True,timeout=30)
logs=[];results=[]
def read_notes(path):
    xml=ET.parse(path);notes=[]
    for part in xml.findall('./part'):
        measure_start=Fraction(0);divisions=1;pending={}
        for measure in part.findall('measure'):
            at=Fraction(0);furthest=Fraction(0);last=Fraction(0)
            for element in measure:
                if element.tag=='attributes':divisions=int(element.findtext('divisions',str(divisions)))
                elif element.tag=='backup':at-=Fraction(element.findtext('duration'))/divisions
                elif element.tag=='forward':at+=Fraction(element.findtext('duration'))/divisions;furthest=max(at,furthest)
                elif element.tag=='note':
                    if element.find('grace') is not None:continue
                    duration=Fraction(element.findtext('duration'))/divisions
                    if element.find('chord') is None:last=at;at+=duration;furthest=max(at,furthest)
                    pitch=element.find('pitch')
                    if pitch is None:continue
                    midi=12*(int(pitch.findtext('octave'))+1)+{'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[pitch.findtext('step')]+int(pitch.findtext('alter','0'))
                    staff=int(element.findtext('staff','1'));voice=element.findtext('voice','1');ties={t.attrib['type'] for t in element.findall('tie')};key=(midi,staff,voice)
                    if 'stop' in ties:
                        index=pending.pop(key);old=notes[index];assert old[1]+old[2]==measure_start+last
                        notes[index]=(midi,old[1],old[2]+duration,staff)
                    else:index=len(notes);notes.append((midi,measure_start+last,duration,staff))
                    if 'start' in ties:pending[key]=index
            measure_start+=furthest
        assert not pending
    return Counter(notes)
for name in json.loads((root/'cases.json').read_text()):
    source=root/f'{name}.musicxml';native=root/f'{name}.mscx';exported=root/f'{name}-roundtrip.musicxml'
    for before,after in [(source,native),(native,exported)]:
        proc=subprocess.run([exe,'-o',str(after),str(before)],env=env,capture_output=True,text=True,timeout=60)
        logs.append({'case':name,'output':after.name,'returncode':proc.returncode,'stderr':proc.stderr,'stdout':proc.stdout})
        assert proc.returncode==0 and after.stat().st_size>0,proc.stderr
    expected=read_notes(source);actual=read_notes(exported);assert actual==expected,(name,expected,actual)
    native_tree=ET.parse(native);assert len(native_tree.findall('./Score/Part/Staff'))==2
    results.append({'case':name,'notes_after_tie_rejoin':sum(expected.values()),'all_pitches_onsets_durations_staves_equal':True,'native_format_saved_and_reopened':True,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
proc=subprocess.run([exe,'-o',str(root/'musescore-render.png'),str(root/'piano.mscx')],env=env,capture_output=True,text=True,timeout=60);assert proc.returncode==0
logs.append({'case':'render','returncode':proc.returncode,'stderr':proc.stderr});assert list(root.glob('musescore-render*.png'))
result={'passed':True,'engine':version.stdout.strip() or version.stderr.strip(),'cases':results,'rendered_png':True,'human_listening_approval':False,'dorico_tested':False,'musescore4_tested':bool(re.search(r'MuseScore4\s+4\.',version.stdout+version.stderr))}
(root/'musescore-validation.json').write_text(json.dumps(result,indent=2));(root/'musescore-log.json').write_text(json.dumps(logs,indent=2));print(json.dumps(result,indent=2))
