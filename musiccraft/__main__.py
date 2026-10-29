"""Optional local CLI. Never sends audio, calls AI or modifies originals."""
import argparse,json
from pathlib import Path
from .contracts import validate_analysis,validate_plan
from .analysis import migrate_02,alternatives

def main():
 p=argparse.ArgumentParser(description='MusicCraft contracts and shared export core');sub=p.add_subparsers(dest='cmd',required=True)
 for name in ['validate-analysis','alternatives','migrate-02','pack','unpack']:
  s=sub.add_parser(name);s.add_argument('input');
  if name in ['migrate-02','pack','unpack']:s.add_argument('output')
 for name in ['validate-plan','export']:
  s=sub.add_parser(name);s.add_argument('input');s.add_argument('--analysis');
  if name=='export':s.add_argument('output')
 args=p.parse_args();data=json.loads(Path(args.input).read_text());analysis=json.loads(Path(args.analysis).read_text()) if getattr(args,'analysis',None) else None
 if args.cmd in ['pack','unpack']:
  from .compact import pack,unpack
  result=pack(data) if args.cmd=='pack' else unpack(data)
  with Path(args.output).open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,separators=(',',':'))
 elif args.cmd=='migrate-02':
  target=Path(args.output);result=migrate_02(data)
  with target.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
 elif args.cmd=='validate-analysis':validate_analysis(data);print('Analysis valid; no composition generated.')
 elif args.cmd=='alternatives':print(json.dumps(alternatives(data),ensure_ascii=False,indent=2))
 elif args.cmd=='validate-plan':validate_plan(data,analysis);print('Composition plan valid.')
 else:
  from .exporter import export_plan
  print(json.dumps(export_plan(data,args.output,analysis),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
