"""Mechanical audit. Human source/semantic review must be recorded separately."""
from pathlib import Path
from collections import Counter
import json, re, sys, unicodedata

ROOT=Path(__file__).resolve().parents[1]
all_docs={p.stem:json.loads(p.read_text(encoding='utf-8-sig')) for p in (ROOT/'content').glob('m[0-9][0-9].json')}
issues=json.loads((ROOT/'content'/'source-issues.json').read_text(encoding='utf-8'))
blocked={(x['moduleId'],p) for x in issues for p in x['pages']}
results={}
for f in sorted((ROOT/'content'/'banks').glob('m[0-9][0-9].json')):
    d=json.loads(f.read_text(encoding='utf-8-sig'))
    module=d['moduleId']; doc=all_docs[module]; errors=[]
    qs=d['questions']; ids=set(); stems=set(); topics={t['id'] for t in d['topics']}
    for q in qs:
        ident=q.get('id')
        if ident in ids: errors.append(f'duplicate id {ident}')
        ids.add(ident)
        norm=lambda s:' '.join(unicodedata.normalize('NFKC',s).lower().split())
        st=norm(q.get('stem',''))
        if st in stems: errors.append(f'duplicate stem {ident}')
        stems.add(st)
        if q.get('topicId') not in topics: errors.append(f'{ident}: unknown topic')
        if q.get('level') not in ('understand','apply','analyze'):errors.append(f'{ident}: invalid level')
        options=q.get('options',[])
        if len(options)!=4 or len({norm(x) for x in options})!=4: errors.append(f'{ident}: options missing/duplicate')
        if not isinstance(q.get('answer'),int) or q['answer'] not in range(4):errors.append(f'{ident}: invalid answer')
        if not q.get('explanation'): errors.append(f'{ident}: no explanation')
        if len(q.get('optionExplanations',[]))!=4: errors.append(f'{ident}: no 4 option explanations')
        if not q.get('sources'):errors.append(f'{ident}: no sources')
        for ref in q.get('sources',[]):
            page=ref.get('page');quote=ref.get('quote','')
            if not isinstance(page,int) or page<1 or page>len(doc['pages']):errors.append(f'{ident}: invalid page {page}');continue
            if (module,page) in blocked: errors.append(f'{ident}: uses blocked page {page}')
            raw=doc['pages'][page-1]['text']
            if quote and norm(quote) not in norm(raw):
                if ref.get('type')!='visual' or not ref.get('transcriptionVerified'):
                    errors.append(f'{ident}: quote not in text layer page {page}')
    counts=Counter(q['level'] for q in qs)
    threshold_errors=[]
    concepts={level:len({q['conceptId'] for q in qs if q['level']==level}) for level in ('understand','apply','analyze')}
    for level,n in [('understand',10),('apply',20),('analyze',10)]:
        if counts[level]<n or concepts[level]<n: threshold_errors.append(f'insufficient {level}: {counts[level]} questions, {concepts[level]} concepts')
    topic_counts=Counter(q['topicId'] for q in qs)
    if any(topic_counts[t]==0 for t in topics):threshold_errors.append('unrepresented topic')
    published=d.get('reviewStatus') == 'passed2'
    meets_exam_threshold=not errors and not threshold_errors
    publishable=published and meets_exam_threshold
    results[module]={'questions':len(qs),'levels':dict(counts),'concepts':concepts,'topicCounts':dict(topic_counts),'mechanicalPass':not errors,'examThresholdPass':not threshold_errors,'published':published,'publishable':publishable,'errors':errors,'thresholdErrors':threshold_errors}
    label='PASS' if publishable else ('DRAFT' if not published else f'FAIL {len(errors)+len(threshold_errors)}')
    print(module,len(qs),label,dict(counts))
    for err in errors[:15]:print(' ',err)
    for err in threshold_errors[:15]:print(' ',err)
(ROOT/'content'/'reviews'/'mechanical-audit.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
sys.exit(0 if all(v['mechanicalPass'] and (v['examThresholdPass'] or not v['published']) for v in results.values()) else 1)
