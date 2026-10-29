"""Reproducible static site staging, never includes user music or credentials."""
from pathlib import Path
import shutil,zipfile,argparse
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=root/'dist')
dest=parser.parse_args().output.resolve();dest.mkdir(parents=True,exist_ok=True)
for p in (root/'web').iterdir():
 if p.is_file() and p.suffix in ['.html','.css','.js']:shutil.copy2(p,dest/p.name)
with zipfile.ZipFile(dest/'core.zip','w',zipfile.ZIP_DEFLATED) as z:
 for folder in ['musiccraft','protocol']:
  for p in (root/folder).iterdir():
   if p.suffix in ['.py','.json']:z.write(p,str(p.relative_to(root)))
for name in ['midi.js','player.js','transcription.js'] :shutil.copy2(root/name,dest/name)
shutil.copytree(root/'vendor',dest/'vendor',dirs_exist_ok=True)
shutil.copy2(root/'tests/fixtures/composition-plan.json',dest/'example-plan.json')
for name in ['analysis','composition']:shutil.copy2(root/'protocol'/f'{name}.schema.json',dest/f'{name}.schema.json')
print('Static files staged:',dest)
