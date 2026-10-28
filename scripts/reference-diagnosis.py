"""Offline reference diagnosis; user music is an external input, never a repository fixture.
Usage: python scripts/reference-diagnosis.py AUDIO.wav SOURCE.mid OUT.json
Test-only dependencies: numpy, scipy, mido. No model/API call, no automatic edit.
"""
import json,sys,wave,hashlib
from pathlib import Path
import numpy as np
from scipy import signal
import mido
audio,midi,out=map(Path,sys.argv[1:4])
with wave.open(str(audio)) as w:
    if w.getsampwidth()!=2:raise ValueError('This diagnostic expects signed 16-bit PCM WAV.')
    sr=w.getframerate();duration=w.getnframes()/sr
    x=np.frombuffer(w.readframes(min(w.getnframes(),sr*61)),dtype='<i2').reshape(-1,w.getnchannels()).mean(axis=1)/32768
x=signal.resample_poly(x,16000,sr);sr=16000
_,t,z=signal.stft(x,fs=sr,nperseg=1024,noverlap=896,boundary=None)
mag=np.log1p(100*np.abs(z));flux=np.maximum(0,np.diff(mag,axis=1)).mean(axis=0);times=t[1:]
peaks,props=signal.find_peaks(flux,distance=12,prominence=np.percentile(flux,80)*.35);onsets=times[peaks];strength=props['prominences']
if not len(onsets):raise ValueError('No usable audio onset peaks.')
start=0;note_times=[]
for event in mido.MidiFile(midi):
    start+=event.time
    if event.type=='note_on' and event.velocity>0:note_times.append(start)
errors=np.array([min(abs(onsets-v)) for v in note_times]);windows=[]
for begin,end in [(0,15),(15,30),(30,45),(45,60)]:
    select=(onsets>=begin)&(onsets<end);ot=onsets[select];weight=strength[select]
    if not len(ot):continue
    best=(0,0)
    for step in np.arange(.15,.21,.0001):
        coherence=abs(np.sum(weight*np.exp(ot*2j*np.pi/step))/sum(weight))
        if coherence>best[0]:best=(float(coherence),float(step))
    windows.append({'range_seconds':[begin,end],'audio_peak_count':len(ot),'period_seconds':best[1],'periodicity_not_a_probability':best[0]})
result={'audio_duration_seconds':duration,'midi_duration_seconds':start,'note_attacks':len(note_times),'audio_analysis_limit_seconds':61,'audio_hop_seconds':.008,'audio_windows':windows,'nearest_audio_peak_errors_seconds':dict(zip(['p25','median','p75','p90','p95'],np.percentile(errors,[25,50,75,90,95]).tolist())),'attacks_over_50ms_from_detected_peak':int(sum(errors>.05)),'warning':'Global audio peaks are not pitch-specific ground truth. An unmatched MIDI attack is not a confirmed error.','input_sha256':{'audio':hashlib.sha256(audio.read_bytes()).hexdigest(),'midi':hashlib.sha256(midi.read_bytes()).hexdigest()},'performance_modified':False,'human_listening_approval':False}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
