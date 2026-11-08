"""Apply the source and semantic audit recorded in gametes-rounds12.md.

This is a record of manual review decisions, not an automated medical verifier.
It deliberately leaves banks below the exam threshold locked.
"""
from pathlib import Path
from collections import Counter
import json, hashlib, random

ROOT=Path(__file__).resolve().parents[2]
PATH=ROOT/'content'/'banks'
docs={m:json.loads((ROOT/'content'/f'{m}.json').read_text(encoding='utf-8-sig')) for m in ('m09','m10','m11','m12')}
banks={m:json.loads((PATH/f'{m}.json').read_text(encoding='utf-8-sig')) for m in docs}

def q(m,n): return next(x for x in banks[m]['questions'] if x['id']==f'{m}-q{n:03}')
def group(m,name,nums):
 for n in nums:q(m,n)['conceptId']=m+'-'+name
def levels(m,lv,nums):
 for n in nums:q(m,n)['level']=lv
def textref(m,page,quote):
 text=docs[m]['pages'][page-1]['text']
 assert ' '.join(quote.split()) in ' '.join(text.split()), (m,page,quote)
 return {'page':page,'quote':quote,'type':'text'}
def visualref(page,quote):
 return {'page':page,'quote':quote,'type':'visual','transcriptionVerified':True,'note':'Đã đối chiếu trực tiếp hình gốc; bản thi chỉ hiển thị chữ.'}
def revise(m,n,stem,options,reason,reasons,refs=None,level=None):
 v=q(m,n);v.update(stem=stem,options=options,answer=0,explanation=reason,optionExplanations=[reason]+reasons)
 if refs is not None:v['sources']=refs
 if level:v['level']=level

# Lượt 1: correct excerpt completeness, limit original-source assertions.
noan_caption='(A) Immature, germinal vesicle-intact stage. The chromatin is arrested in prophase of meiosis I; meiotic maturation has not begun. (B) Germinal vesicle breakdown stage. Meiosis I has resumed, with breakdown of the germinal vesicle; the chromatin is progressing through the remainder of meiosis I. (C) Mature oocyte. The first polar body has been emitted, and the remaining chromatin is arrested in metaphase of meiosis II.'
for v in banks['m09']['questions']:
 for ref in v['sources']:
  if ref['page']==12:ref.update(visualref(12,noan_caption))
  elif ref.get('type')=='visual':ref['transcriptionVerified']=True
for v in banks['m10']['questions']:
 for ref in v['sources']:
  if ref.get('type')=='visual':ref['transcriptionVerified']=True

# A before-I cell could be spermatogonium without the primary-cell condition.
revise('m10',32,'Trong mô hình theo dõi hai nhóm tinh bào: A gồm tinh bào I chưa bắt đầu giảm phân I; B đã hoàn thành giảm phân I nhưng chưa bắt đầu II. Ghép giai đoạn và bộ NST nào đúng theo sơ đồ?',
 ['A là tinh bào I 2n; B là tinh bào II n','A là tinh bào I n; B là tinh bào II 2n','A là tinh tử n; B là tinh bào I 2n','A và B đều là tinh tử n'],
 'Từ chính điều kiện ban đầu và các nhãn trên slide 5, A ở trước lần I với 2n; B ở sau lần I với n và là tinh bào II.',
 ['Đảo bộ NST giữa hai giai đoạn.','A chưa qua giảm phân còn B đã qua lần I, không phù hợp hai tên này.','Cả hai nhóm đều chưa hoàn tất giảm phân II để thành tinh tử.'])

# Lượt 2: group semantic duplicates across levels, not merely matching strings.
for name,nums in {
 'phanbiet-noan-va-nang':[1,31], 'dung-giam-phan':[3,12,13,18,38],
 'apoptosis':[4,34], 'mot-hang-det-vuong':[6,14,15,24,28],
 'zona-khoi-dau':[7], 'thu-cap-nhieu-hang':[8,16,21],
 'noan1-qua-cac-nang':[9,25,35,36,40], 'lh-va-noan2':[10,23,32],
 'noanchin-thutinh':[20,39], 'hoc-chua-du':[22,33],
 'gv-nguyenvẹn':[29], 'gvbd':[30]
}.items():group('m09',name,nums)
levels('m09','understand',[11,12,13,18,20,23,24,27,29,30,34,37,39])
levels('m09','apply',[31,35,36,38,40])
# Remaining analyze require evaluating sufficiency or integrating a trajectory.
for name,nums in {
 'tythe-doangiua':[2,16], 'sinh-tinh-thu-tu':[4],
 'giamphan-I':[5,11,12], 'giamphan-II':[6,13],
 'sertoli-che-tiet':[8,19], 'sertoli-thucbao':[9,18],
 'biet-hoa-khong-doi-n':[24,31], 'khoang-ke':[25,37],
 'muc-to-chuc':[30,36], 'phan-bao-vs-biet-hoa':[34],
 'phan-biet-sinh-va-van-chuyen':[39]
}.items():group('m10',name,nums)
levels('m10','understand',[11,12,14,15,18,19,20,21,22,25,26,27,28,29,30,37,38,40])
levels('m10','apply',[34,35,36,39])

# m11: only read-off caption used, never infer clinical mechanisms from mislabeled image.
cap='Tinh trùng được bọc bởi các chất ngăn khả năng thụ tinh. Trong quá trình di chuyển, tinh trùng va chạm với cấu trúc lưới của chất nhầy cổ tử cung và các hoạt chất khác, dẫn đến dỡ bỏ các chất ức chế'
for v in banks['m11']['questions']:
 for i,ref in enumerate(v['sources']):
  if ref['page']==5:v['sources'][i]=visualref(5,cap)
  elif ref['page']==6:v['sources'][i]=textref('m11',6,'Vài chục tinh trùng quanh noãn\nXuyên thủng lớp tế bào hạt quanh noãn\nXuyên qua màng trong suốt')
# Exclude source wording that conflates capacitation/acrosomal reaction.
banks['m11']['questions']=[v for v in banks['m11']['questions'] if v['id']!='m11-q028']
revise('m11',2,'Hiện tượng nào được liệt kê trong mục “Từ âm đạo đến vòi trứng” của bài?',
 ['Ly giải tinh dịch','Phôi thoát màng trong suốt','Tạo hồ huyết ở nội mạc','Hình thành hoàng thể thai kỳ'],
 'Slide 3 liệt kê ly giải tinh dịch. Danh sách không được dùng để khẳng định mọi hiện tượng xảy ra nối tiếp hoàn toàn.',
 ['Không được liệt kê trong mục hành trình tinh trùng này.','Không được liệt kê trong mục hành trình tinh trùng này.','Không được liệt kê trong mục hành trình tinh trùng này.'])
revise('m11',23,'Một tóm tắt chỉ ghi đường đi âm đạo–tử cung–vòi trứng và các biến đổi của tinh trùng, nhưng chưa nêu biến đổi của tinh dịch. Mục nào từ slide 3 cần bổ sung?',
 ['Ly giải tinh dịch','Phôi thoát màng','Hình thành hồ huyết','Hình thành hoàng thể thai kỳ'],
 'Mục về tinh dịch trên slide 3 là ly giải tinh dịch; không suy diễn thứ tự tuyệt đối chỉ từ cách xếp dòng.',
 ['Đây không phải biến đổi tinh dịch được hỏi.','Đây không phải biến đổi tinh dịch được hỏi.','Đây không phải biến đổi tinh dịch được hỏi.'])
revise('m11',38,'Một bản tóm tắt “thụ tinh chính danh” mới ghi tiền nhân đực. Nhóm bổ sung nào cùng được slide 10 nêu?',
 ['Tiền nhân cái, hoàn tất phân bào II và hai cực cầu','Tiền nhân cái nhưng noãn chưa hoàn tất phân bào II và không có cực cầu','Hai tiền nhân đực và bốn cực cầu','Chỉ có một tiền nhân, không có phân bào của noãn'],
 'Slide 10 nêu tiền nhân cái và đực, hoàn tất phân bào II, hai cực cầu. Câu chỉ hỏi nhóm sự kiện, không khẳng định đã liệt kê hết slide.',
 ['Trái với hoàn tất phân bào II và hai cực cầu.','Sai nguồn gốc tiền nhân và số cực cầu.','Bỏ các sự kiện có mặt trong nguồn.'],level='understand')
for name,nums in {
 'duong-di':[1,12], 'ly-giai':[2,23], 'chon-loc':[3,27],
 'kha-nang-hoa':[4,13,14,32], 'lop-quanh-noan':[5,6,16,24,31],
 'hoan-tat-II':[7,30], 'tien-nhan':[8,18], 'dong-dac-ZP':[9,19],
 'E2-nhu-dong':[10,26], 'du-tru-co-tu-cung':[11],
 'nhieu-co-che-van-chuyen':[29,36,40], 'su-kien-thu-tinh':[25,38]
}.items():group('m11',name,nums)
levels('m11','understand',list(range(11,28))+[29,30,32,33,34,36,37,38,40])
levels('m11','apply',[12,16,31,35,39])

# Replace repetitive boilerplate with the reason each alternative is excluded.
wrong11={
 1:['Đảo hướng và thứ tự đường đi của tinh trùng.','Thêm niệu đạo, không phải đường đi nêu ở slide3.','Thêm bàng quang, không thuộc trình tự slide3.'],
 3:['Nang Graaf không được liệt kê là sản phẩm của tinh trùng.','Noãn bào I không được liệt kê là sản phẩm trong tinh trùng.','Bài phân biệt hành trình tinh trùng với hợp tử sau thụ tinh.'],
 4:['Đó là cấu trúc khác, không đối tượng của khả năng hóa được mô tả.','Đó là tế bào khác, không tinh trùng.','Đó là biến đổi nội mạc, không khả năng hóa tinh trùng.'],
 5:['Cơ vòi không phải lớp quanh noãn được hỏi.','Thanh mạc tử cung không phải lớp quanh noãn.','Hạch bạch huyết không phải lớp quanh noãn.'],
 6:['Bài nêu màng trong suốt, không màng trắng buồng trứng.','Không phải lớp tiếp theo trong slide6.','Không phải lớp tiếp theo trong slide6.'],
 7:['Không phải sự kiện giảm phânII đang được hỏi.','Noãn đã ở tiến trình hoàn tất lầnII, không tạo bàoI lần đầu.','Không phải sự kiện thụ tinh chính danh trong bài.'],
 8:['Bài nêu một tiền nhân đực và một cái.','Bài nêu một tiền nhân đực và một cái.','Không phải hai tiền nhân được nêu.'],
 9:['Không có biến đổi ZP thành hoàng thể trong bài.','Không có biến đổi ZP thành tử cung trong bài.','Bài mô tả ZP đông đặc, không luôn biến mất trước tinh trùng.'],
 10:['Slide12 gắn nhu động với E2, không chỉ FSH.','Slide12 gắn nhu động với E2, không chỉ prolactin.','Slide12 gắn nhu động với E2, không chỉ inhibin.'],
 11:['Không phải chức năng tuyến cổ tử cung được liệt kê.','Không phải chức năng tuyến cổ tử cung được liệt kê.','Không phải chức năng tuyến cổ tử cung được liệt kê.'],
 12:['Niệu quản không nằm trong trình tự slide3.','Slide3 ghi vòi trứng tiếp theo tử cung.','Tuyến tiền liệt không nằm trong trình tự slide3.'],
 13:['Không có tạo Sertoli trong đầu tinh trùng theo chú thích.','Không có biến đổi nhân tinh trùng thành noãn theo chú thích.','Trái với sự dỡ bỏ chất ức chế được mô tả.'],
 14:['Không được chú thích gắn với khả năng hóa.','Không có hàng rào máu–tinh hoàn ở tử cung trong mô tả.','Không được chú thích gắn với khả năng hóa.'],
 15:['Không đúng mức vài chục được nguồn nêu.','Trái với nguồn có vài chục tinh trùng quanh noãn.','Nguồn không giới hạn chính xác hai.'],
 16:['Cơ tử cung không phải lớp kế tiếp quanh noãn.','Không phải màng được slide6 nêu.','Không phải lớp được slide6 nêu.'],
 17:['Nguồn nêu có hai cực cầu.','Nguồn nêu hai, không bốn.','Nguồn nêu hai, không tám.'],
 18:['Bỏ tiền nhân cái có trong nguồn.','Không phải tiền nhân của phía noãn.','Không phải tiền nhân của phía noãn.'],
 19:['Không phải hậu quả được slide10 mô tả.','Không phải hậu quả được slide10 mô tả.','Không phải hậu quả được slide10 mô tả.'],
 20:['Sertoli không được slide12 liệt kê.','Hạch không phải yếu tố bề mặt được slide12 liệt kê.','Màng trắng không được slide12 liệt kê.'],
 21:['Không đúng hướng đến buồng tử cung.','Không đúng đường luồng dịch trong nguồn.','Không đúng đường luồng dịch trong nguồn.'],
 22:['Thấp không đồng nghĩa bằng không.','Nguồn ghi thấp và liệt kê nhiều yếu tố khác.','P4 có được liệt kê ở slide12.'],
 24:['Thêm ống sinh tinh không có trong đường qua lớp quanh noãn.','Thay hai lớp quanh noãn bằng cấu trúc khác.','Không phải chuỗi lớp quanh noãn.'],
 25:['Không phải hai sự kiện slide10 liệt kê.','Không phải hai sự kiện slide10 liệt kê.','Không phải hai sự kiện slide10 liệt kê.'],
 26:['Không phải yếu tố slide12 nối với nhu động.','Không phải yếu tố slide12 nối với nhu động.','Không phải yếu tố slide12 nối với nhu động.'],
 27:['Không phải quá trình ở quần thể tinh trùng của slide3.','Không phải mục thay đổi quần thể tinh trùng của slide3.','Không phải mục thay đổi quần thể tinh trùng của slide3.'],
 29:['Không phải nhóm yếu tố của slide12.','Đây là cấu trúc hệ sinh dục nam, không nhóm của slide12.','Không phải các yếu tố vận chuyển được slide12 liệt kê.'],
 30:['Nguồn không mô tả quay lại nguyên bào.','Nguồn nêu hoàn tất lầnII, không lặp lại lầnI.','Không phải sự kiện của noãn được mô tả.'],
 31:['Bài không nêu tinh trùng quay lại tinh hoàn.','Bàng quang không nằm trong hành trình được mô tả.','Bỏ thụ tinh và trộn với làm tổ.'],
 32:['Không có nội dung tinh trùng hình thành từ noãn.','Không có nội dung buồng trứng sinh tinh.','Slide3 nêu tinh trùng ngay trong hành trình.'],
 33:['Ly giải tinh dịch không phải hai sự kiện này.','Làm tổ không phải hai sự kiện này.','Các sự kiện được mô tả trong tiếp xúc tinh trùng–noãn.'],
 34:['Đảo mối liên hệ với vỡ tiểu thể dưới màng.','Slide6 nêu rõ xuyên qua ZP.','ZP là màng quanh noãn, không tuyến cổ tử cung.'],
 35:['Đảo hướng và không đúng cả hai mô tả.','Không phải đường của hợp tử trong nguồn.','Không phải sự kiện được bài mô tả cho tinh trùng.'],
 36:['P4 được slide12 liệt kê.','Slide12 có mục di chuyển hợp tử.','Các mục trên không phải thuốc cản quang.'],
 37:['Không phải chức năng được nêu của tuyến cổ tử cung.','Không phải chức năng được nêu của tuyến cổ tử cung.','Không có khẳng định thay thế vòi trứng trong bài.'],
 39:['Đặt hợp tử trước gặp tinh trùng là đảo trình tự.','Trộn làm tổ và tạo tinh trùng, không chuỗi bài.','Đảo trình tự tinh trùng đến và hoàn tất thụ tinh.'],
 40:['Không phải yếu tố được slide12 nêu.','Nguồn nêu cơ vòi, vi nhung mao và luồng dịch, không chỉ tuyến cổ tử cung.','Slide12 chính là mục về vận chuyển.']}
for n,reasons in wrong11.items():
 v=q('m11',n);v['optionExplanations']=[v['explanation']]+reasons

# m12: remove the internally unclear 'no pregnancy, day11 after fertilization' phrase.
banks['m12']['questions']=[v for v in banks['m12']['questions'] if v['id'] not in ('m12-q028','m12-q029')]
revise('m12',38,'Một lịch dùng ngày chu kỳ để ghi cửa sổ làm tổ; lịch khác ghi ngày sau thụ tinh; slide17 lại tính tuần thai từ kỳ kinh cuối. Trước khi so sánh các mốc, cần làm gì?',
 ['Xác định rõ điểm bắt đầu của từng cách đếm, không xem các con số ngày và tuần là cùng một mốc','Coi ngày6 sau thụ tinh là ngày6 của chu kỳ trong mọi trường hợp','Coi tuần4 luôn là ngày thứ4 sau thụ tinh','Coi ngày18 chu kỳ luôn là tuần18 thai kỳ'],
 'Slide6 dùng ngày chu kỳ, slide9 dùng ngày sau thụ tinh, slide17 dùng tuần thai từ ngày bắt đầu kỳ kinh cuối. Phải nhận biết điểm gốc trước khi đối chiếu; bài không đủ để tự suy ra một phép đổi chính xác cho mọi chu kỳ.',
 ['Đồng nhất hai điểm bắt đầu khác nhau.','Đồng nhất đơn vị tuần và ngày, đồng thời đổi điểm bắt đầu.','Đồng nhất ngày chu kỳ với tuần thai.'],
 refs=[textref('m12',6,'Cửa sổ làm tổ thường được mở ra ở ngày thứ 18 và đóng lại vào ngày thứ 23 của chu kỳ'),textref('m12',9,'Ngày thứ 6 sau khi thụ tinh'),textref('m12',17,'Thai kỳ bình thường có độ dài 40 tuần (280 ngày) kêt từ ngày bắt đầu của kỳ kinh cuối cùng')],level='analyze')
for name,nums in {
 'estrogen-chuanbi':[1], 'progesterone-che-tiet':[2],
 'cua-so-thoi-gian':[4,26], 'hatching-nhu-cau':[15,16],
 'dong-bo-cua-so':[12,32], 'doi-thoai-hoa-hoc':[9,27],
 'lif-egf':[17,33], 'tuan3-tuan4':[23,39],
 'hcg-hoangthe':[21,37], 'hcg-sinhhoa':[22],
 'giao-dien-mach-mau':[20,40]
}.items():group('m12',name,nums)
levels('m12','understand',[13,14,15,16,17,18,19,20,21,23,24,25,30,33,34,37,39])
levels('m12','apply',[27,31,32,35,40])
for v in banks['m12']['questions']:
 # Explicit source frame matters for historical/teaching timelines.
 if v['id'] in ['m12-q004','m12-q015','m12-q019','m12-q020','m12-q023','m12-q024','m12-q025','m12-q026','m12-q030','m12-q035'] and not v['stem'].startswith('Theo'):
  v['stem']='Theo các mốc trong tài liệu, '+v['stem'][0].lower()+v['stem'][1:]

# Keep only the evidence needed. This avoids displaying the excluded source sentence in explanations.
for v in banks['m12']['questions']:
 # The loop may append a second citation. Iterate a snapshot so that citation
 # cannot be revisited and appended again indefinitely.
 for i,ref in enumerate(list(v['sources'])):
  if ref['page']==13:
   v['sources'][i]=textref('m12',13,'N10 sau thụ tinh, các hội bào nuôi của phôi phá vỡ được các mạch máu xoắn ốc của NMTC, tạo ra các hồ huyết sơ khai.\nKể từ thời điểm này, phôi chính thức được nhận dưỡng chất và trao đổi khí trực tiếp với mẹ\nhCG được phóng thích vào máu mẹ\nhCG có hoạt tính tương đương LH nên chuyển hoàng thể chu kỳ thành hoàng thể thai kỳ')
   if v['id'] in ['m12-q022','m12-q036','m12-q040']:
    v['sources'].append(textref('m12',13,'Hiện diện hCG trong máu mẹ là bằng chứng của hiện tượng thai đã làm tổ, được coi như là thai sinh hóa'))

# All m12 alternatives re-solved against the supplied slide. Keep narrow conclusions.
wrong12={
 1:['hCG không là hormone gây pha tăng sinh được slide5 nêu.','FSH không là hormone trực tiếp được slide5 gắn với nội mạc dày lên.','AMH không là hormone được slide5 gắn với tác động đó.'],
 2:['Nguồn mô tả chế tiết, không mất mọi tế bào.','Không phải tác động lên nội mạc đã chuẩn bị.','Nguồn không gắn progesterone với việc lập tức làm phôi thoát màng.'],
 3:['Không phải vị trí pinopode được slide5 nêu.','Không phải vị trí pinopode được slide5 nêu.','Không phải vị trí pinopode được slide5 nêu.'],
 4:['Không đúng khoảng ngày nguồn nêu.','Không đúng khoảng ngày nguồn nêu.','Không đúng khoảng ngày nguồn nêu.'],
 5:['Nguồn nêu progesterone, không AMH.','Nguồn nêu progesterone, không inhibinB.','Nguồn nêu progesterone, không androgen.'],
 6:['Không phải giai đoạn phôi đến buồng tử cung.','Tinh bào là đối tượng khác, không phôi.','Hoàng thể không là một giai đoạn phôi.'],
 7:['Đây không phải hai khối tế bào phôi nang.','Đây là các tế bào nang noãn, không hai khối của phôi nang.','Không phải hai khối được slide7 nêu.'],
 8:['Không phải ba tên PGT được slide8 liệt kê.','Đây là các hormone, không tên xét nghiệm PGT.','Đây là các ký hiệu steroid, không tên xét nghiệm PGT.'],
 9:['Không phải nhóm phân tử trong đối thoại hóa học được nguồn nêu.','Không phải nhóm phân tử trong đối thoại hóa học được nguồn nêu.','Không phải nhóm phân tử trong đối thoại hóa học được nguồn nêu.'],
 10:['Đây không phải các tế bào miễn dịch được slide12 nêu.','Đây không phải các tế bào miễn dịch được slide12 nêu.','Đây không phải các tế bào miễn dịch được slide12 nêu.'],
 11:['Đảo hormone chuẩn bị nội mạc và thêm AMH không có trong chuỗi.','Không đúng hai hormone và thứ tự của slide5.','Không đúng hai hormone và thứ tự của slide5.'],
 12:['Bỏ qua yêu cầu đồng bộ của cửa sổ tiếp nhận.','Nguồn ghi cửa sổ có giới hạn, không vô hạn.','hCG là hormone, không kết cục phôi biến thành.'],
 13:['Trái nội dung có thể di dời cửa sổ.','Nguồn nêu nhiều yếu tố nội/ngoại sinh, không chỉ noãn.','Nguồn không nêu tinh trùng quyết định hoàn toàn.'],
 14:['Sertoli không phải lớp ngoại bì lá nuôi của phôi.','Bài nêu lấy tế bào phôi, không chỉ nội mạc mẹ.','Nguồn khẳng định có thể lấy tế bào ngoại bì lá nuôi.'],
 15:['Không phải mục đích thoát màng được slide9 mô tả.','Không phải mục đích thoát màng được slide9 mô tả.','Không phải mục đích thoát màng được slide9 mô tả.'],
 16:['Trái mô tả nhu cầu oxygen tăng của phôi.','Không phải lý do được slide9 nêu.','Không có nội dung zona tiết oxygen quá mức.'],
 17:['Không phải cặp tín hiệu của giao diện được slide11 nêu.','Không phải cặp tín hiệu của giao diện được slide11 nêu.','Không phải cặp tín hiệu của giao diện được slide11 nêu.'],
 18:['Nguồn gọi bán dị ghép, không tự thân hoàn toàn.','Không đúng cách gọi bán dị ghép của nguồn.','Không phù hợp đối tượng phôi sống mà nguồn đang mô tả.'],
 19:['Không phải mạch hội bào nuôi tiếp cận được slide12 nêu.','Không phải mạch hội bào nuôi tiếp cận được slide12 nêu.','Không phải mạch hội bào nuôi tiếp cận được slide12 nêu.'],
 20:['Không phải sự kiện ngày10 được mô tả.','Nguồn mô tả hCG hỗ trợ hoàng thể, không làm thoái triển hoàn toàn.','Không phải sự kiện ngày10 được mô tả.'],
 21:['Cấu trúc được chuyển là hoàng thể chu kỳ, không nang nguyên thủy.','Sertoli không phải cấu trúc được chuyển trong đoạn này.','Zona không phải cấu trúc được chuyển trong đoạn này.'],
 22:['Có hCG không đồng nghĩa đã quan sát được trên siêu âm.','Dữ kiện này không chứng minh sống đủ tháng.','Dữ kiện này không chứng minh đã hoàn tất tạo cơ quan.'],
 23:['Đảo thứ tự hai sự kiện so với slide17.','Không đúng thứ tự mốc của slide17.','Không phải cặp sự kiện được slide17 gắn hai tuần này.'],
 24:['Không đúng tuần nguồn nêu.','Nguồn gắn tuần3 với thụ tinh.','Không đúng thời điểm bắt đầu được nguồn nêu.'],
 25:['Sai đơn vị: nguồn ghi ngày.','Không đúng thời gian tồn tại được nguồn ghi.','Không đúng thời gian tồn tại được nguồn ghi.'],
 26:['Nguồn thường mở ngày18, không ngày24.','Trái khoảng mở có giới hạn trong nguồn.','Nguồn gắn progesterone với mở cửa sổ.'],
 27:['Không bác bỏ mô tả phôi đã thoát màng có đối thoại hóa học.','Sertoli không nằm trong giao diện tương tác được nêu.','Trái nội dung slide11 nêu tương tác.'],
 30:['Không đúng độ dài nguồn ghi.','37 tuần không tương đương100 ngày và không phải cặp số nguồn.','Không đúng độ dài nguồn ghi.'],
 31:['Đảo thứ tự hormone trong slide5.','Nguồn mô tả estrogen chuẩn bị trước làm tổ.','Bài nêu rõ tác động cả hai hormone.'],
 32:['Không phải điều kiện đồng bộ được bài nêu.','Không phải điều kiện đồng bộ được bài nêu.','Không phải điều kiện đồng bộ được bài nêu.'],
 33:['Không phải quá trình ở giao diện phôi–nội mạc.','Không phải quá trình ở giao diện phôi–nội mạc.','Không phải quá trình ở giao diện phôi–nội mạc.'],
 34:['Bỏ các tín hiệu hóa học và thành phần miễn dịch.','LH và HSG không là hai cơ chế mô tả ở slide11–12.','Bài đang mô tả tiến trình làm tổ sớm.'],
 35:['Không có mốc tạo Sertoli trong tiến trình này.','Không đúng mốc thụ tinh và tạo noãn.','Trộn ngày chu kỳ với ngày sau thụ tinh.'],
 36:['Đảo thứ tự hai mốc được mô tả.','Bài phân biệt rõ sinh hóa với thấy thai trên siêu âm.','Siêu âm là căn cứ thai lâm sàng trong slide14.'],
 37:['Không phải tác dụng hCG được slide13 nêu.','Không phải tác dụng hCG được slide13 nêu.','Không phải tác dụng hCG được slide13 nêu.'],
 39:['Trái thứ tự được ghi trong nguồn.','Không đúng hai mốc của nguồn.','Nguồn có ghi rõ hai mốc.'],
 40:['Không phải trình tự của slide13.','Hồ huyết ở giao diện nội mạc, không từ nang noãn.','Thai sinh hóa được nguồn gắn hCG trong máu mẹ sớm.']}
for n,reasons in wrong12.items():
 v=q('m12',n);v['optionExplanations']=[v['explanation']]+reasons

for m,b in banks.items():
 for v in b['questions']:
  v['review']={'source':True,'semantic':True,'coverage':False}
  v['reviewNotes']={'source':'Đối chiếu riêng với trang/slide của đúng tài liệu; xem báo cáo gametes-rounds12.md.','semantic':'Đã tự giải lại cả bốn lựa chọn; các câu đồng ý cốt lõi dùng chung conceptId; mức độ đã hạ khi chỉ là đọc/nhận diện.'}
 # Store content state honestly; two checked questions do not make a complete 40-item exam.
 b['reviewStatus']='needs-expansion'
 b['reviewReport']='content/reviews/gametes-rounds12.md'
 counts=Counter(v['level'] for v in b['questions'])
 conceptCounts={lv:len({v['conceptId'] for v in b['questions'] if v['level']==lv}) for lv in ('understand','apply','analyze')}
 b['examEligibility']={'eligible':False,'reason':'Chưa đủ câu khác ý ở mức vận dụng/vận dụng cao cho đề40 theo10/20/10 sau rà soát; không đổi nhãn để bù số.','levels':dict(counts),'distinctConceptsByLevel':conceptCounts,'distinctConcepts':len({v['conceptId'] for v in b['questions']})}
 b['limitations']=[f"Ngân hàng hiện có {len(b['questions'])} câu; còn các biến thể chung concept, không được lấy chung một đề.",'Chỉ những câu hiện có đã qua đối chiếu nguồn và tự giải lựa chọn; điều kiện đề40 chưa đạt.','Chưa có đủ căn cứ để tạo khoảng100 câu độc lập và đủ10/20/10; cần bổ sung tài liệu hoặc đổi cấu hình đề theo quyết định của người dùng.']
 # Shuffle answer position deterministically to avoid authoring-position bias.
 for i,v in enumerate(b['questions']):
  if m in ('m11','m12'):
   order=list(range(4));random.Random(v['id']).shuffle(order)
   old=v['answer'];v['options']=[v['options'][j] for j in order];v['optionExplanations']=[v['optionExplanations'][j] for j in order];v['answer']=order.index(old)
 (PATH/f'{m}.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(m,len(b['questions']),dict(counts),conceptCounts,'distinct',b['examEligibility']['distinctConcepts'])
