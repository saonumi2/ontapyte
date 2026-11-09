"""Remove references to the lesson itself from question stems."""
from pathlib import Path
import json,re

root=Path(__file__).resolve().parents[1]
for path in sorted((root/'content'/'banks').glob('m[0-9][0-9].json')):
    bank=json.loads(path.read_text(encoding='utf-8-sig'))
    count=0
    for q in bank['questions']:
        s=q['stem']
        manual={
          'm14-q003':'Vì sao thai ở đoạn kẽ khi vỡ có nguy cơ mất máu nặng?',
          'm12-q010':'Phôi được nhận diện sớm bởi thành phần miễn dịch nào?',
          'm09-q012':'Một noãn đang tạm ngưng ở kỳ đầu giảm phân I. Tế bào đó được gọi là gì?',
        }
        s=manual.get(q['id'],s)
        s=re.sub(r'(?i)\bđối chiếu (?:với )?bài(?: học)?\s*,?\s*','',s)
        s=re.sub(r'(?i)\b(?:theo|dựa vào|trong) (?:bài(?: học)?|tài liệu|slide|trang\s*\d+)\s*,?\s*','',s)
        s=re.sub(r'(?i)\bphù hợp (?:với )?bài(?: học)?','phù hợp',s)
        s=re.sub(r'(?i)\bbám (?:đúng )?bài(?: học)?','phù hợp',s)
        s=re.sub(r'(?i)\bđược bài(?: học)?\s+','được ',s)
        s=re.sub(r'(?i)\bbài(?: học)?\s+(?:nêu|ghi|mô tả|nhấn mạnh|giải thích)\b','được nêu',s)
        s=re.sub(r'(?i)^bài(?: học)?\s+','',s)
        s=re.sub(r'(?i)\b(?:của|với) bài(?: học)?\b','',s)
        s=re.sub(r'(?i)\bbài(?: học)?\s+nhắc\b','cần',s)
        s=re.sub(r'(?i)\bbài(?: học)?\s+nói\b','',s)
        s=re.sub(r'(?i)\bbài(?: học)?\b(?!\s+tập)','',s)
        s=re.sub(r'\s+([,?.!;:])',r'\1',s)
        s=re.sub(r'\s{2,}',' ',s).strip()
        if s:s=s[0].upper()+s[1:]
        if s!=q['stem']:q['stem']=s;count+=1
    path.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(bank['moduleId'],count)
