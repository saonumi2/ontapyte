"""Render cited PDF pages to mobile friendly JPEG previews."""
from pathlib import Path
import json, subprocess, shutil

root=Path(__file__).resolve().parents[1]
out=root/'public'/'page-previews'
out.mkdir(exist_ok=True)
renderer=shutil.which('pdftoppm')
if not renderer:raise SystemExit('pdftoppm is required to render cited pages')
for bank_path in sorted((root/'content'/'banks').glob('m[0-9][0-9].json')):
    bank=json.loads(bank_path.read_text(encoding='utf-8-sig'))
    mid=bank['moduleId']
    pdf=root/'public'/'sources'/f'{mid}.pdf'
    pages=sorted({source['page'] for q in bank['questions'] for source in q['sources']})
    for page in pages:
        stem=out/f'{mid}-p{page:03}'
        image=stem.with_suffix('.jpg')
        if image.exists():continue
        subprocess.run([renderer,'-f',str(page),'-l',str(page),'-scale-to','1400',
                        '-singlefile','-jpeg','-jpegopt','quality=82',str(pdf),str(stem)],check=True,
                       stdout=subprocess.DEVNULL)
        if not image.exists():raise RuntimeError(f'No preview for {mid} page {page}')
    print(mid,len(pages))
