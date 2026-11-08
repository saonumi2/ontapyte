"""Compile manually authored TSV into draft banks. Does not certify any review."""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
TOPICS = {
 'm03': {'phoi':'Phôi thai học','giaiphau':'Giải phẫu','mohoc':'Mô học','chucnang':'Chức năng','hinhanh':'Hình ảnh học','udich':'Viêm tắc, ứ dịch vòi trứng','apxe':'Áp xe phần phụ','nangcanh':'Nang nước cạnh vòi trứng','tntc':'Thai ngoài tử cung'},
 'm04': {'giaiphau':'Giải phẫu','phoi':'Phôi thai học','mohoc':'Mô học và nang noãn','hoangthe':'Hoàng thể','chucnang':'Chức năng','nangconang':'Nang cơ năng','lacnoimac':'Nang lạc nội mạc tử cung','utan':'U tân sinh','pcos':'Hội chứng buồng trứng đa nang'},
 'm14': {'dinhnghia':'Định nghĩa','vitri':'Vị trí làm tổ','nguyco':'Yếu tố nguy cơ','coche':'Cơ chế bệnh sinh','giaiphaubenh':'Giải phẫu bệnh','lamsang':'Lâm sàng','thaioobung':'Thai trong ổ bụng','cls':'Cận lâm sàng','chandoan':'Chẩn đoán','xutri':'Xử trí','tienluong':'Tiên lượng','phongngua':'Phòng ngừa'},
 'm11': {'ditruyen':'Di chuyển tinh trùng','khananghoa':'Khả năng hóa','tiepxucnoan':'Tiếp xúc với noãn','thutinh':'Thụ tinh chính danh','hopty':'Di chuyển hợp tử'},
 'm12': {'noimac':'Nội mạc tiền làm tổ','cuaso':'Cửa sổ làm tổ','phoi':'Phôi tiền làm tổ','doithoai':'Đối thoại phôi–nội mạc','hcg':'hCG và thai sớm','phattrien':'Phát triển phôi thai'},
}
for module, topics in TOPICS.items():
    doc = json.loads((ROOT/'content'/f'{module}.json').read_text(encoding='utf-8-sig'))
    questions=[]
    for line_no,line in enumerate((ROOT/'content'/f'{module}-authoring.tsv').read_text(encoding='utf-8-sig').splitlines(),1):
        if not line.strip(): continue
        bits=line.split('|')
        if len(bits)!=10: raise ValueError(f'{module}:{line_no}: expected 10 fields, got {len(bits)}')
        level,topic,page_list,concept,stem,*rest=bits
        correct,w1,w2,w3,explanation=rest
        refs=[]
        for page_no in [int(x) for x in page_list.split(',')]:
            raw=doc['pages'][page_no-1]['text']
            if not raw.strip(): raise ValueError(f'{module}:{line_no}: blank page {page_no}')
            # Keep the complete page as the exact audit excerpt; it preserves qualifications.
            refs.append({'page':page_no,'quote':raw.strip()})
        questions.append({'id':f'{module}-q{len(questions)+1:03}','topicId':topic,'conceptId':concept,
            'level':level,'stem':stem,'options':[correct,w1,w2,w3],'answer':0,
            'explanation':explanation,'optionExplanations':[explanation]+[f'Không khớp mô tả ở trang {page_list}: {explanation}' for _ in range(3)],
            'sources':refs,'review':{'source':False,'semantic':False,'coverage':False}})
    out={'moduleId':module,'title':doc['title'],'topics':[{'id':k,'title':v,'pages':sorted({s['page'] for q in questions if q['topicId']==k for s in q['sources']})} for k,v in topics.items()], 'questions':questions}
    path=ROOT/'content'/'banks'/f'{module}.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(module,len(questions),{l:sum(q['level']==l for q in questions) for l in ('understand','apply','analyze')})
