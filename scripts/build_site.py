from pathlib import Path
import json, shutil, sys
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
if DIST.exists(): shutil.rmtree(DIST)
DIST.mkdir()
for item in (ROOT/'src').iterdir():
    shutil.copy2(item,DIST/item.name)
shutil.copytree(ROOT/'public'/'sources',DIST/'sources')
if (ROOT/'public'/'page-previews').exists():
    shutil.copytree(ROOT/'public'/'page-previews',DIST/'page-previews')
(DIST/'data').mkdir()
catalog=[]
for path in sorted((ROOT/'content').glob('m[0-9][0-9].json')):
    doc=json.loads(path.read_text(encoding='utf-8-sig'))
    bank_path=ROOT/'content'/'banks'/path.name
    bank=json.loads(bank_path.read_text(encoding='utf-8-sig')) if bank_path.exists() else None
    q=bank['questions'] if bank else []
    for question in q:
        for source in question['sources']:
            preview=ROOT/'public'/'page-previews'/f'{doc["id"]}-p{source["page"]:03}.jpg'
            if not preview.exists():raise RuntimeError(f'Missing source preview: {preview.name}')
    level_counts=Counter(x.get('difficulty') for x in q)
    all_reviewed=all(all(x.get('review',{}).get(k) is True for k in ('source','semantic')) for x in q)
    enough=all(level_counts[l]>=n for l,n in [('easy',10),('hard',20),('veryHard',10)])
    eligible=bank.get('examEligibility',{}).get('eligible',True)
    ready=bool(q) and all_reviewed and enough and eligible and bank.get('reviewStatus')=='passed2'
    if ready: ready_reason='Đã qua 2 lượt kiểm và đủ điều kiện tạo đề 40 câu.'
    elif bank and bank.get('examEligibility',{}).get('reason'): ready_reason=bank['examEligibility']['reason']
    else: ready_reason='Chưa hoàn tất kiểm nguồn, kiểm câu hỏi, hoặc điều kiện tạo đề 40 câu.'
    file_name=doc.get('viewFile',doc['file'])
    catalog.append({'id':doc['id'],'title':doc['title'],'original':doc['original'],'file':file_name,
                    'pageCount':len(doc['pages']),'questionCount':len(q),'levels':level_counts,'ready':ready,'readyReason':ready_reason})
    if ready:
        public_bank={k:v for k,v in bank.items() if k in ('moduleId','title','topics','questions')}
        (DIST/'data'/path.name).write_text(json.dumps(public_bank,ensure_ascii=False),encoding='utf-8')
(DIST/'data'/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False),encoding='utf-8')
print('Built',DIST,'ready',sum(x['ready'] for x in catalog),'of',len(catalog))
