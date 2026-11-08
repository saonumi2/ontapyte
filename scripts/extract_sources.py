from pathlib import Path
import json, re, shutil, hashlib, zipfile
from pypdf import PdfReader
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT.parent
OUT = ROOT / 'public' / 'sources'
OUT.mkdir(parents=True, exist_ok=True)
(ROOT / 'content').mkdir(exist_ok=True)
catalog = []
for f in sorted(INPUT.iterdir(), key=lambda p: int(re.match(r'\d+', p.name)[0]) if re.match(r'\d+', p.name) else 999):
    if f.suffix.lower() not in ('.pdf', '.pptx', '.ppt'): continue
    num = int(f.name.split('.')[0])
    ident = f'm{num:02}'
    pages = []
    fmt = f.suffix.lower()[1:]
    if fmt == 'pdf':
        for i, p in enumerate(PdfReader(f).pages):
            pages.append({'page': i+1, 'text': p.extract_text() or ''})
    elif zipfile.is_zipfile(f) and 'ppt/presentation.xml' in zipfile.ZipFile(f).namelist():
        def texts(shapes):
            result = []
            for shape in shapes:
                if shape.has_text_frame: result.append(shape.text)
                if shape.has_table:
                    result.extend(' | '.join(c.text for c in r.cells) for r in shape.table.rows)
                if shape.shape_type == 6: result.extend(texts(shape.shapes))
            return result
        prs = Presentation(f)
        for i, s in enumerate(prs.slides):
            pages.append({'page': i+1, 'text': '\n'.join(texts(s.shapes))})
        fmt = 'pptx'
    else:
        print('LEGACY', f.name, f.read_bytes()[:12].hex())
    name = f'{ident}.{fmt}'
    shutil.copy2(f, OUT / name)
    doc = {'id':ident,'title':f.stem.split('. ',1)[-1], 'original':f.name,'file':f'sources/{name}', 'format':fmt,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'pages':pages}
    (ROOT/'content'/f'{ident}.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'content'/f'{ident}.txt').write_text('\n\n'.join(f'=== {p["page"]} ===\n{p["text"]}' for p in pages), encoding='utf-8')
    catalog.append({k:v for k,v in doc.items() if k != 'pages'} | {'pageCount':len(pages),'textCharacters':sum(len(p['text']) for p in pages)})
    print(ident, len(pages), sum(len(p['text']) for p in pages), f.name)
(ROOT/'content'/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
