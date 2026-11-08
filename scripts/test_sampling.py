"""Test the actual sampling constraints across repeated random seeds."""
from pathlib import Path
import json, random, sys

ROOT=Path(__file__).resolve().parents[1]
ok=True
for f in sorted((ROOT/'content'/'banks').glob('m[0-9][0-9].json')):
    bank=json.loads(f.read_text(encoding='utf-8-sig'))
    if bank.get('reviewStatus') != 'passed2':
        print(f.stem,'SKIP (chưa được phát hành)')
        continue
    topics={t['id'] for t in bank['topics']}
    failures=[]
    for seed in range(100):
        rng=random.Random(seed); found=False
        for _ in range(500):
            covered=set(); picks=[]
            for level,n in [('hard',20),('veryHard',10),('easy',10)]:
                for i in range(n):
                    candidates=[q for q in bank['questions'] if q['difficulty']==level and q not in picks]
                    rng.shuffle(candidates)
                    if not candidates:break
                    pick=next((q for q in candidates if q['topicId'] not in covered),candidates[0]);picks.append(pick);covered.add(pick['topicId'])
            if len(picks)==40 and topics<=covered:found=True;break
        if not found:failures.append(seed)
    print(f.stem,'PASS' if not failures else 'FAIL',f'{100-len(failures)}/100 sample seeds')
    ok &= not failures
sys.exit(0 if ok else 1)
