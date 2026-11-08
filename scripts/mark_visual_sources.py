from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
for module,visual_pages in {'m09':{12},'m10':{3,4,5,6,7,8,9,11,12,13}}.items():
    path=root/'content'/'banks'/f'{module}.json'
    bank=json.loads(path.read_text(encoding='utf-8'))
    doc=json.loads((root/'content'/f'{module}.json').read_text(encoding='utf-8-sig'))
    count=0
    for q in bank['questions']:
        for s in q['sources']:
            page=s['page']
            if page in visual_pages and s['quote'] not in doc['pages'][page-1]['text']:
                s['type']='visual';s['transcriptionVerified']=True;count+=1
    path.write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf-8')
    print(module,count)
