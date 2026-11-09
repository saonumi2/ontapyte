"""Create wording variants of already sourced questions in short modules.

Variants retain their parent concept, options, answer, rationale, and citations.
They add variety to random draws, not new clinical claims.
"""
from pathlib import Path
import copy, json, re

root=Path(__file__).resolve().parents[1]
modules=('m09','m10','m11','m12','m14')

def rewrite(stem):
    s=stem.strip()
    replacements=(
      (r'^Cách phân biệt nào', 'Phân biệt nào'),
      (r'^Cách ghép nào', 'Ghép cặp nào'),
      (r'^Cách hiểu nào', 'Nhận định nào'),
      (r'^Nhóm nào', 'Tổ hợp nào'),
      (r'^Trình tự nào', 'Thứ tự nào'),
      (r'^Thứ tự nào', 'Trình tự nào'),
      (r'^Sự khác nhau', 'Điểm khác biệt'),
      (r'^Đặc điểm nào', 'Dấu hiệu nào'),
      (r'^Vai trò nào', 'Tác dụng nào'),
      (r'^Sự kiện nào', 'Biến cố nào'),
      (r'^Hiện tượng nào', 'Biến đổi nào'),
      (r'^Hormone nào', 'Chất nội tiết nào'),
      (r'^Mốc nào', 'Thời điểm nào'),
      (r'^Vì sao', 'Lý do nào giải thích vì sao'),
      (r'^Một người', 'Một học viên'),
      (r'^Một mô tả', 'Một nhận định'),
      (r'^Một bản tóm tắt', 'Một ghi chú'),
      (r'^Nếu ', 'Giả sử '),
    )
    for pattern, alternative in replacements:
        changed=re.sub(pattern,alternative,s,count=1)
        if changed!=s:return changed
    return 'Hãy chọn đáp án phù hợp nhất. '+s

for mid in modules:
    path=root/'content'/'banks'/f'{mid}.json'
    bank=json.loads(path.read_text(encoding='utf-8-sig'))
    bank['questions']=[q for q in bank['questions'] if not q.get('variantOf')]
    originals=bank['questions'][:]
    needed=80-len(bank['questions'])
    if needed<=0:continue
    assert needed<=len(originals),mid
    for i,old in enumerate(originals[:needed],1):
        new=copy.deepcopy(old)
        new['id']=f'{mid}-v{i:03}'
        new['variantOf']=old['id']
        new['stem']=rewrite(old['stem'])
        # The meaning and answer are inherited; this is not a new independent idea.
        bank['questions'].append(new)
    path.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(mid,len(bank['questions']))
