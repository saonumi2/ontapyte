from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
p=root/'content'/'banks'/'m11.json';d=json.loads(p.read_text(encoding='utf-8'))
visual={5:'Slide 5 hình khả năng hóa đầu tinh trùng; câu chữ lấy từ chú thích hình.',7:'Slide 7 hình thụ tinh; nhãn dùng để phân biệt nhân tinh trùng/noãn và zona pellucida.',11:'Slide 11 hình thụ tinh; nhãn polar bodies, pronuclei, zona pellucida.'}
for q in d['questions']:
 for s in q['sources']:
  if s['page'] in visual:
   s['type']='visual';s['transcriptionVerified']=True
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
