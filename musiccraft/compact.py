"""Lossless column tables inspired by symbolic event representations.
No MidiTok/REMI code copied. Uncertainty and unknown values are retained.
"""
from copy import deepcopy
from .contracts import require,validate_analysis,validate_plan

def pack(document):
 require(document.get('format') in ['MusicCraft-Composition-Plan','MusicCraft-Analysis-Handoff'] and document.get('version')=='0.3','Unknown document format');d=deepcopy(document);tables=[]
 paths=[['notes'],['rests']] if d['format']=='MusicCraft-Composition-Plan' else [['content','observations']]
 for path in paths:
  parent=d
  for key in path[:-1]:parent=parent[key]
  rows=parent.pop(path[-1]);columns=sorted({key for row in rows for key in row});values=[]
  for row in rows:
   # Explicit presence mask preserves absent fields versus explicit null.
   present=[i for i,k in enumerate(columns) if k in row];values.append([present,[row[columns[i]] for i in present]])
  tables.append({'path':path,'columns':columns,'rows':values})
 return {'format':'MusicCraft-Compact','version':'0.3','body':d,'tables':tables}

def unpack(packed):
 require(packed.get('format')=='MusicCraft-Compact' and packed.get('version')=='0.3','Unknown compact format');d=deepcopy(packed['body']);expected=[['notes'],['rests']] if d['format']=='MusicCraft-Composition-Plan' else [['content','observations']]
 require([t['path'] for t in packed['tables']]==expected,'Unexpected table paths')
 for t in packed['tables']:
  cols=t['columns'];require(len(cols)==len(set(cols)),'Duplicate columns');rows=[]
  for present,values in t['rows']:
   require(len(present)==len(values) and len(present)==len(set(present)) and all(type(i)==int and 0<=i<len(cols) for i in present),'Invalid table row');rows.append({cols[i]:v for i,v in zip(present,values)})
  parent=d
  for key in t['path'][:-1]:parent=parent[key]
  require(t['path'][-1] not in parent,'Conflicting table and body');parent[t['path'][-1]]=rows
 return d
