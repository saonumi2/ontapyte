"""Add source checked questions for omitted concepts; rerunnable without duplicates."""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
items = [
 ('m04','m04-q081','phoi','m04-follicle-reserve-birth','easy',14,
  'Đến lúc sinh, buồng trứng bé gái có khoảng bao nhiêu nang noãn?',
  ['Khoảng 1 triệu','Khoảng 30.000','Khoảng 8.000','Khoảng 400–500'],
  'Nguồn ghi khoảng 1 triệu nang noãn lúc sinh; các con số còn lại thuộc những mốc khác.',
  'Đến lúc sinh, buồng trứng bé gái sẽ có khoảng 1 triệu nang noãn'),
 ('m04','m04-q082','phoi','m04-follicle-reserve-puberty','hard',14,
  'Đến tuổi dậy thì, số nang noãn còn lại được nêu xấp xỉ bao nhiêu?',
  ['30.000','1 triệu','8.000','400–500'],
  'Mốc dậy thì là khoảng 30.000 nang noãn; 1 triệu thuộc lúc sinh.',
  'Đến lúc dậy thì còn khoảng 30.000 nang noãn'),
 ('m04','m04-q083','phoi','m04-lifetime-ovulations','veryHard',14,
  'Trong số nang noãn có từ đầu đời, khoảng bao nhiêu nang tiến triển đến trưởng thành và phóng noãn?',
  ['400–500','Khoảng 1 triệu','Khoảng 30.000','Khoảng 8.000'],
  'Nguồn nêu chỉ một số ít, khoảng 400–500 nang, tiến triển đến trưởng thành và phóng noãn.',
  'Chỉ một số ít 400-500 nang noãn tiến triển đến trưởng thành và\nphóng noãn'),
 ('m08','m08-q081','contraception','m08-fsh-negative-feedback','hard',16,
  'Estrogen ngoại sinh tạo phản hồi âm lên tuyến yên và ức chế FSH dẫn tới hệ quả nào?',
  ['Không có nang noãn vượt trội','Tăng đỉnh LH','Tăng phóng noãn','Tăng tiết FSH'],
  'Nguồn nối phản hồi âm, ức chế FSH với chu kỳ không có nang noãn vượt trội.',
  'ức chế hoàn toàn sự tiết FSH → chu kỳ không có nang noãn vượt trội'),
 ('m08','m08-q082','contraception','m08-lasds-differences','veryHard',25,
  'Vì sao các hệ phóng thích steroid tác dụng dài có thể khác nhau về cơ chế tránh thai?',
  ['Lượng progestogen phóng thích hằng ngày và hoạt tính của chất khác nhau','Mọi hệ luôn có cùng liều và hoạt tính','Chỉ do vị trí đặt, không liên quan hoạt chất','Chỉ do estrogen được phóng thích hằng ngày'],
  'Nguồn nêu khác biệt về lượng phóng thích hằng ngày và hoạt tính progestogenic của hoạt chất.',
  'khác nhau trong liều lượng phóng thích progestogen hàng ngày cũng như các hoạt tính progestogenic'),
 ('m08','m08-q083','contraception','m08-lh-negative-feedback','hard',16,
  'Progestogen ngoại sinh ngăn đỉnh LH qua phản hồi âm dẫn đến hệ quả nào?',
  ['Chu kỳ không phóng noãn','FSH tăng tạo nang vượt trội','Luôn xuất hiện hai đỉnh LH','Estrogen nội sinh mất hoàn toàn'],
  'Nguồn nối phản hồi âm lên hạ đồi và tuyến yên, ngăn đỉnh LH, với chu kỳ không phóng noãn.',
  'ngăn chặn sự xuất hiện của đỉnh LH nhờ phản hồi âm lên hạ đồi & tuyến yên → chu kỳ không có phóng noãn'),
 ('m08','m08-q084','contraception','m08-lng-iud-dual-mechanism','veryHard',25,
  'Ngoài tác dụng của progestogen, LNG-IUD còn có tác dụng của loại dụng cụ nào?',
  ['Dụng cụ tử cung trơ','Que cấy dưới da','Vòng âm đạo phối hợp','Thuốc uống phối hợp'],
  'Nguồn ghi LNG-IUD còn có tác dụng của dụng cụ tử cung trơ.',
  'LNG-IUD còn có tác dụng của IUD trơ'),
]
for mid, ident, topic, concept, difficulty, page, stem, options, explanation, quote in items:
    path=root/'content'/'banks'/f'{mid}.json'
    bank=json.loads(path.read_text(encoding='utf-8-sig'))
    if any(q['id']==ident for q in bank['questions']): continue
    doc=json.loads((root/'content'/f'{mid}.json').read_text(encoding='utf-8-sig'))
    assert quote in doc['pages'][page-1]['text']
    bank['questions'].append({
      'id':ident,'topicId':topic,'conceptId':concept,'level':'understand',
      'difficulty':difficulty,'stem':stem,'options':options,'answer':0,
      'explanation':explanation,'optionExplanations':[explanation]+['Không khớp mốc hoặc cơ chế được nêu ở nguồn.']*3,
      'sources':[{'page':page,'quote':quote,'type':'text'}],
      'review':{'source':True,'semantic':True,'coverage':False}})
    path.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
