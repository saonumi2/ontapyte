from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
for module in ('m03','m04'):
    p=root/'content'/'banks'/f'{module}.json'
    d=json.loads(p.read_text(encoding='utf-8'))
    assert len(d['questions'])==80
    for q in d['questions']:
        assert q['sources'] and len(q['options'])==4 and q['explanation']
        q['review']['source']=True
        q['review']['semantic']=True
    d['reviewStatus']='passed2'
    d['reviewReport']='content/reviews/anatomy-rounds12.md'
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    print(module,'passed2')
