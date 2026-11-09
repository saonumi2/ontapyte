"""Add distinct facts from previously uncited pages of the short modules."""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
items=[
 ('m12','m12-q043','phoi','m12-day3-laser-hatching','hard',10,
  'Kỹ thuật nào được nêu để hỗ trợ phôi ngày 3 thoát màng?',
  ['Laser','Siêu âm Doppler','Nội soi ổ bụng','Chọc dò Douglas'],
  'Trang nguồn ghi hỗ trợ phôi ngày 3 thoát màng bằng laser; không suy ra chỉ định cho từng phôi.',
  'Hỗ trợ phôi thoát màng đối với phôi ngày 3 bằng laser'),
 ('m14','m14-q049','nguyco','m14-cervical-pregnancy-history','hard',5,
  'Những tiền sử nào được liên hệ với thai ở cổ tử cung?',
  ['Nạo thai và mổ lấy thai','Chỉ viêm ruột thừa và sỏi thận','Chỉ nang noãn và u xơ','Chỉ đau đầu và tăng huyết áp'],
  'Trang nguồn liên hệ thể thai ở cổ tử cung với tiền sử nạo thai, mổ lấy thai; đây là yếu tố liên quan, không phải dấu xác nhận.',
  'Loại TNTC này có liên quan đến tiền sử nạo thai, mổ lấy thai'),
]
for mid,ident,topic,concept,difficulty,page,stem,options,explanation,quote in items:
    path=root/'content'/'banks'/f'{mid}.json'
    bank=json.loads(path.read_text(encoding='utf-8-sig'))
    if any(q['id']==ident for q in bank['questions']):continue
    doc=json.loads((root/'content'/f'{mid}.json').read_text(encoding='utf-8-sig'))
    assert quote in doc['pages'][page-1]['text'],ident
    assert topic in {t['id'] for t in bank['topics']},ident
    bank['questions'].append({'id':ident,'topicId':topic,'conceptId':concept,'level':'understand',
      'difficulty':difficulty,'stem':stem,'options':options,'answer':0,'explanation':explanation,
      'optionExplanations':[explanation]+['Không phù hợp với chi tiết được dẫn nguồn.']*3,
      'sources':[{'page':page,'quote':quote,'type':'text'}],
      'review':{'source':True,'semantic':True,'coverage':False}})
    path.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
