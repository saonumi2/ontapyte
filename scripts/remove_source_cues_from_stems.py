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

def clean(stem: str) -> str:
    text = PREFIX.sub('', stem)
    text = LOCATION.sub('', text)
    text = LEADING.sub('', text)
    text = DOC_PREFIX.sub('', text)
    text = DOC_INLINE.sub('', text)
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
for path in sorted((ROOT / 'content' / 'banks').glob('m[0-9][0-9].json')):
    bank = json.loads(path.read_text(encoding='utf-8-sig'))
    for question in bank['questions']:
        if question['id'] in rewrites:
            question['stem'] = rewrites[question['id']]
    path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
