"""Render every PDF page to mobile friendly JPEG previews."""
from pathlib import Path
import json, subprocess, shutil

root=Path(__file__).resolve().parents[1]
out=root/'public'/'page-previews'
out.mkdir(exist_ok=True)
renderer=shutil.which('pdftoppm')
if not renderer:raise SystemExit('pdftoppm is required to render cited pages')
for doc_path in sorted((root/'content').glob('m[0-9][0-9].json')):
    doc=json.loads(doc_path.read_text(encoding='utf-8-sig'))
    mid=doc['id']
    pdf=root/'public'/'sources'/f'{mid}.pdf'
    pages=range(1,len(doc['pages'])+1)
    for page in pages:
        stem=out/f'{mid}-p{page:03}'
        image=stem.with_suffix('.jpg')
        if image.exists():continue
        subprocess.run([renderer,'-f',str(page),'-l',str(page),'-scale-to','1400',
                        '-singlefile','-jpeg','-jpegopt','quality=82',str(pdf),str(stem)],check=True,
                       stdout=subprocess.DEVNULL)
        if not image.exists():raise RuntimeError(f'No preview for {mid} page {page}')
    print(mid,len(pages))
