"""Record the seven banks with documented source and semantic review."""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
approved={'m05':'endocrine-rounds12.md','m06':'endocrine-rounds12.md','m07':'endocrine-rounds12.md','m08':'endocrine-rounds12.md',
          'm13':'early-rounds12.md','m15':'early-rounds12.md','m16':'early-rounds12.md'}
for ident,report in approved.items():
    if not (root/'content'/'reviews'/report).exists():raise RuntimeError(f'Missing review report: {report}')
    path=root/'content'/'banks'/f'{ident}.json'
    bank=json.loads(path.read_text(encoding='utf-8-sig'))
    if not bank['questions'] or not all(q['review']['source'] is True and q['review']['semantic'] is True for q in bank['questions']):
        raise RuntimeError(f'Two reviews incomplete: {ident}')
    bank['reviewStatus']='passed2'
    bank['reviewReport']=f'content/reviews/{report}'
    path.write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf-8')
    print(ident,len(bank['questions']),'passed2')
