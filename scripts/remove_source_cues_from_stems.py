"""Remove page/slide and document cues from learner-facing question stems.

Sources remain attached to explanations and the in-page source viewer.  This is
an editorial display change only: answers, options, explanations and citations
are left untouched.
"""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]

PREFIX = re.compile(
    r'(?i)\btheo\s+(?:(?:các\s+mốc\s+trong\s+)?(?:mô\s+hình|mô\s+tả|chú\s+thích|bảng|mục)\s+)?(?:slide|trang)\s*\d+\s*,?\s*'
)
LOCATION = re.compile(r'(?i)\s+(?:ở|trong|từ)\s+(?:(?:mô\s+tả|bảng)\s+)?(?:slide|trang)\s*\d+\b')
LEADING = re.compile(r'(?i)^(?:trang|slide)\s*\d+\s+(?:ghi|nêu|mô\s+tả|liệt\s+kê|đặt|chia)\s+')
DOC_PREFIX = re.compile(r'(?i)\btheo\s+(?:các\s+mốc\s+trong\s+)?(?:tài\s+liệu|bài(?:\s+học)?)\s*,?\s*')
DOC_INLINE = re.compile(r'(?i)\s+trong\s+(?:tài\s+liệu|bài(?:\s+học)?)\b')
LESSON_INLINE = re.compile(r'(?i)\s+(?:của|theo|trong)\s+(?:tài\s+liệu|bài(?:\s+học)?)\b')
FRAME_PREFIX = re.compile(r'(?i)\b(?:trong|theo|ở)\s+(?:các\s+)?(?:sơ\s+đồ|bảng|hình(?:\s+chú\s+thích)?|mô\s+hình)(?:\s+(?:của\s+)?bài(?:\s+học)?)?\s*,?\s*')
FRAME_INLINE = re.compile(r'(?i)\s+(?:trong|theo|ở)\s+(?:các\s+)?(?:sơ\s+đồ|bảng|hình(?:\s+chú\s+thích)?)(?:\s+(?:của\s+)?bài(?:\s+học)?)?\b')

def clean(stem: str) -> str:
    text = PREFIX.sub('', stem)
    text = LOCATION.sub('', text)
    text = LEADING.sub('', text)
    text = DOC_PREFIX.sub('', text)
    text = DOC_INLINE.sub('', text)
    text = LESSON_INLINE.sub('', text)
    text = FRAME_PREFIX.sub('', text)
    text = FRAME_INLINE.sub('', text)
    text = re.sub(r'\s+([,?.!;:])', r'\1', text)
    text = re.sub(r'\s{2,}', ' ', text).strip()
    if text:
        text = text[0].upper() + text[1:]
    return text

for path in sorted((ROOT / 'content' / 'banks').glob('m[0-9][0-9].json')):
    bank = json.loads(path.read_text(encoding='utf-8-sig'))
    changed = 0
    for question in bank['questions']:
        revised = clean(question['stem'])
        if revised != question['stem']:
            question['stem'] = revised
            changed += 1
    path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(bank['moduleId'], changed)

# Remaining source-shaped sentences need an editorial rewrite, rather than simple
# removal, to preserve natural Vietnamese and keep the tested knowledge intact.
rewrites = {
 'm03-q035':'Ở bệnh nhân hiếm muộn cần khảo sát thông thương vòi trứng, xét nghiệm nào phù hợp?',
 'm03-q041':'Tiền sử nhiễm Chlamydia gây viêm vùng chậu gợi liên hệ nào?',
 'm05-q019':'Một sơ đồ đặt việc tái tục giảm phân của nhóm nang được chiêu mộ hoàn toàn trước dậy thì. Cách sửa nào phù hợp?',
 'm05-q021':'Một nang đã qua giai đoạn sơ cấp và thứ cấp sớm. Giai đoạn tiếp theo là gì?',
 'm07-q021':'Một nang tiền hốc chưa lệ thuộc gonadotropin. Sản phẩm chính là gì?',
 'm08-q027':'Khi E2 đạt ngưỡng và P4 thấp, phản hồi nào xảy ra?',
 'm08-q038':'FSH/LH thấp và E2 thấp xếp vào nhóm nào?',
 'm08-q040':'FSH/LH cao nhưng E2 thấp thuộc nhóm nào?',
 'm08-q057':'Cơ chế của vòng âm đạo phối hợp tương tự phương pháp nào?',
 'm09-q004':'Apoptosis giúp giải thích đặc điểm nào của quần thể noãn bào 1?',
 'm09-q020':'Sự kiện nào cần có khi chuyển sang mô tả noãn chín?',
 'm09-q029':'Một noãn còn nguyên túi mầm (germinal vesicle), nhiễm sắc chất dừng ở prophase I. Phát biểu nào phù hợp?',
 'm09-q030':'Khi túi mầm đã vỡ và giảm phân I đang tiếp tục, có thể kết luận nào?',
 'm11-q004':'Khả năng hóa chủ yếu liên quan đến đối tượng nào?',
 'm11-q012':'Tinh trùng đang ở tử cung. Vị trí tiếp theo là đâu?',
 'm11-q016':'Tinh trùng đã vượt tế bào hạt quanh noãn. Lớp tiếp theo cần vượt là gì?',
 'm11-q024':'Sắp xếp nào đúng các lớp cần vượt trước khi tinh trùng tiếp xúc noãn?',
 'm11-q027':'Nếu chỉ mô tả số tinh trùng ban đầu mà bỏ quá trình thay đổi quần thể trong đường sinh dục nữ, quá trình nào bị bỏ sót?',
 'm11-q029':'Nhóm nào toàn là yếu tố vận chuyển hợp tử?',
 'm11-q038':'Một bản tóm tắt “thụ tinh chính danh” mới ghi tiền nhân đực. Nhóm bổ sung nào cần có?',
 'm11-q041':'Nhóm nào gồm ba yếu tố vận chuyển hợp tử?',
 'm12-q004':'Cửa sổ làm tổ thường mở ở khoảng ngày nào của chu kỳ?',
 'm12-q025':'Pinopode xuất hiện và tồn tại trong khoảng bao lâu?',
 'm12-q027':'Một mô tả cho rằng phôi không tác động lên nội mạc trước khi bám. Phôi tạo phản hồi nào lên nội mạc?',
 'm12-q038':'Một lịch dùng ngày chu kỳ để ghi cửa sổ làm tổ; lịch khác ghi ngày sau thụ tinh; tuổi thai lại tính từ kỳ kinh cuối. Trước khi so sánh các mốc, cần làm gì?',
 'm12-q042':'Khi đến buồng tử cung, phôi nang có bao nhiêu khối tế bào chính?',
 'm13-q024':'Dùng công thức đã cho, CRL 20 mm tương ứng tuổi thai bao nhiêu ngày?',
 'm13-q026':'CRL 30 mm được quy đổi thành tuổi thai thế nào?',
 'm13-q034':'Khi tiếp cận xuất huyết thai sớm, phương tiện đầu tay để khảo sát vị trí và sinh tồn thai là gì?',
 'm13-q041':'Thai được tống xuất ở 18 tuần vô kinh và chưa có khả năng tự sống. Sự kiện này thuộc định nghĩa nào?',
 'm13-q051':'Khi nghi thai trứng, phương tiện khảo sát đầu tay là gì?',
 'm13-q058':'Một sinh viên ghi cùng một mốc hCG cho đơn thai và song thai. Cần sửa điều gì?',
 'm13-q065':'Một người dùng duy nhất mốc β-hCG cố định để khẳng định vị trí thai, không xét đơn/song thai hay siêu âm. Lập luận nào đúng?',
 'm13-q072':'Có các hướng theo dõi, nội khoa, ngoại khoa và cá thể hóa. Có thể kết luận điều gì?',
 'm15-q020':'Thời gian chảy máu nào được phân loại là kéo dài?',
 'm15-q039':'Cần đánh giá thêm dịch trong ổ bụng. Vai trò nào của siêu âm ngả bụng phù hợp?',
 'm15-q041':'Dấu “viền tăng âm kép” phù hợp với tình trạng nào?',
 'm15-q042':'Cấu trúc vô mạch phù hợp với tình trạng nào?',
 'm15-q045':'Mốc 3000 mUI/ml gắn với bối cảnh nào?',
 'm16-q034':'p57KIP2 âm tính thường hướng về nhóm nào?',
 'm16-q056':'Sau hCG âm tính, TTBP cần được theo dõi tiếp thế nào?',
 'm16-q058':'hCG bình nguyên qua 4 lần đo vào ngày 1, 7, 14 và 21 đáp ứng mô tả nào?',
}
rewrites.update({
 'm03-q026':'Bạch huyết của vòi trứng đổ về vị trí nào?',
 'm04-q059':'Tiêu chuẩn PCOS yêu cầu bao nhiêu trong ba nhóm tiêu chuẩn?',
 'm04-q061':'Đầu bám, dây chằng và mạch đi qua cần được ghép thế nào?',
 'm04-q066':'Chuỗi sản xuất estrogen ở nang có hốc lớn là gì?',
 'm04-q073':'Nang hoàng thể xuất huyết bị xếp vào u tân sinh và áp dụng nguồn gốc tế bào mầm. Sai ở điểm nào?',
 'm05-q019':'Việc tái tục giảm phân của nhóm nang được chiêu mộ diễn ra khi nào?',
 'm05-q036':'Sau đỉnh LH, noãn cần hoàn tất bước nào?',
 'm06-q014':'PTEN tác động theo chiều nào trong quá trình hoạt hóa nang?',
 'm06-q022':'Ngoài E2, hormone buồng trứng nào góp phần kiểm soát FSH trong pha nang?',
 'm06-q027':'Chuỗi nào phù hợp với hoạt hóa nang qua PI3K?',
 'm07-q033':'ESR1 tương ứng với receptor nào?',
 'm07-q034':'ESR2 tương ứng với receptor nào?',
 'm07-q062':'Sau phóng noãn, diễn giải nào đúng về sự hiện diện của E2 và P4?',
 'm08-q041':'Nhóm WHO nào có đặc điểm “no FSH stimulation”?',
 'm08-q042':'Nhóm WHO nào có đặc điểm “advanced follicle maturation arrest”?',
 'm08-q043':'Nhóm WHO nào có đặc điểm “no follicles”?',
 'm08-q044':'Thiếu GnRH đơn độc thuộc nhóm nguyên nhân vô kinh nguyên phát nào?',
 'm08-q045':'Loạn sản tuyến sinh dục thuộc nhóm nguyên nhân vô kinh nguyên phát nào?',
 'm08-q046':'Dính buồng tử cung thuộc nhóm nguyên nhân vô kinh thứ phát nào?',
 'm08-q072':'PCOS thuộc nhóm WHO nào? Có thể chỉ dùng FSH/E2 khoảng bình thường để khẳng định mọi trường hợp là PCOS không?',
 'm09-q034':'Một người kết luận mọi noãn ban đầu đều sẽ trưởng thành. Dữ kiện nào bác bỏ kết luận đó?',
 'm10-q002':'Cụm ty thể của tinh trùng nằm ở vùng nào?',
 'm10-q003':'Bộ máy Golgi tham gia hình thành cấu trúc nào khi tinh tử biệt hóa?',
 'm10-q005':'Giảm phân I xảy ra trong chuyển tiếp nào của dòng tế bào tinh?',
 'm10-q014':'Nhận định “thể cực đầu phủ vùng đầu chứa nhân” được đánh giá thế nào?',
 'm10-q015':'Axoneme thuộc phần nào của tinh trùng?',
 'm10-q019':'Ngoài nâng đỡ và thực bào, Sertoli còn có chức năng nào liên quan tạo dịch, ABP và inhibin?',
 'm10-q020':'Hàng rào máu–tinh hoàn liên quan trực tiếp đến loại tế bào nào?',
 'm10-q022':'Tinh bào I bắt đầu giảm phân vào mốc tuổi nào?',
 'm10-q024':'Tinh tử có cần tăng từ n lên 2n để trở thành tinh trùng không?',
 'm10-q025':'Tế bào Leydig và mạch máu nằm ở vị trí nào so với biểu mô ống sinh tinh?',
 'm10-q028':'Ống dẫn từ mào tinh đi lên vùng chậu được gọi là gì?',
 'm10-q030':'Nhân, thể cực đầu và Sertoli có phải đều là bộ phận của cùng một tinh trùng không?',
 'm10-q035':'Bào tương thừa khi tinh tử biệt hóa được xử lý bởi cơ chế nào?',
 'm11-q011':'Tuyến cổ tử cung có vai trò nào trong hành trình tinh trùng?',
 'm11-q013':'Tinh trùng ban đầu được phủ bởi chất ngăn khả năng thụ tinh. Trong khi di chuyển, biến đổi nào xảy ra?',
 'm11-q020':'Ngoài cơ vòi, yếu tố bề mặt nào góp phần vận chuyển hợp tử?',
 'm11-q026':'Yếu tố nào tạo nhu động cơ vòi trứng khi hợp tử di chuyển?',
 'm11-q037':'Tuyến cổ tử cung có những vai trò nào trong hành trình tinh trùng?',
 'm14-q027':'Người mạch nhanh và huyết áp tụt lại được ghi là huyết động ổn định. Cần sửa điều gì?',
 'm14-q039':'Sau nội soi xác định thai ngoài tử cung, vai trò đánh giá bổ sung nào cần được lưu ý?',
 'm15-q061':'Hai người có hCG ban đầu 1000 và 4000 IU/L, đều tăng 40% sau 48 giờ. Nhận định nào đúng?',
 'm15-q077':'Gán 1500, 3000, 5000 mUI/ml thành “liều điều trị” và dùng 49%, 40%, 33% làm ngưỡng định vị. Sai ở đâu?',
 'm15-q082':'β-core fragment được tìm thấy trong loại mẫu nào?',
 'm16-q004':'Đáp ứng hóa trị của hai nhóm choriocarcinoma khác nhau thế nào?',
 'm16-q022':'Khi phân loại choriocarcinoma ngoài tử cung, phát hiện allele từ cha hướng về nhánh nào?',
 'm16-q023':'Không có allele từ cha hướng về nhánh nào?',
 'm16-q026':'Choriocarcinoma không liên quan thai kỳ có thể có nguồn từ tế bào mầm ngoài sinh dục ở đâu?',
 'm16-q027':'Choriocarcinoma không liên quan thai kỳ có thể có nguồn tế bào soma từ nhóm cơ quan nào?',
 'm16-q031':'Kiểu 46,XX điển hình phù hợp với nhóm nào?',
 'm16-q033':'p57KIP2 dương tính được ghép với nhóm nào?',
 'm16-q038':'Tử cung nhỏ hơn tuổi thai thường gặp ở nhóm nào?',
 'm16-q040':'Nguy cơ GTN tiếp sau của thai trứng bán phần là bao nhiêu?',
 'm16-q062':'Một người cho rằng không có tiền sử thai trứng thì choriocarcinoma không thể liên quan thai kỳ. Phản biện nào đúng?',
 'm16-q064':'Tổ hợp gai nhau phù lan rộng, phôi/thai vắng và p57 âm phù hợp với chẩn đoán nào?',
 'm16-q066':'Kiểu 46,XX điển hình của thai trứng toàn phần. Vì sao không thể suy mọi 46,XX đều là thai trứng toàn phần?',
 'm16-q078':'Nhóm gestational đáp ứng hóa trị tốt và tiên lượng tốt. Sai lầm nào khi suy mọi bệnh nhân chắc chắn khỏi?',
 'm16-q082':'Hai nhánh cùng tạo 46XX: một nhánh từ 23X nhân đôi, một nhánh từ hai bộ 23X. Phân biệt nào đúng?',
 'm16-q083':'Noãn 23X nhận hai bộ 23X tạo ra kết quả nhiễm sắc thể và nhiễm sắc thể giới tính nào?',
})
for path in sorted((ROOT / 'content' / 'banks').glob('m[0-9][0-9].json')):
    bank = json.loads(path.read_text(encoding='utf-8-sig'))
    for question in bank['questions']:
        if question['id'] in rewrites:
            question['stem'] = rewrites[question['id']]
    path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
