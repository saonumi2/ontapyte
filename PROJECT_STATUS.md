# Trạng thái thực tế

Ngày ghi nhận: 08/11/2026 (Asia/Saigon).

Đã có giao diện tĩnh và workflow GitHub Pages. Theo yêu cầu cập nhật của người dùng ngày 08/11/2026, điều kiện phát hành đổi thành hai lượt nội dung (nguồn và ngữ nghĩa), cộng kiểm tra cơ học khả năng tạo đề. `scripts/build_site.py` hiện mở **9/14 phần**: m03–m08, m13, m15, m16.

Đã trích xuất 14 tài liệu và tạo câu hỏi cho 12 phần: m03 80, m04 80, m05 60, m06 80, m07 80, m08 80, m09 40, m10 40, m13 80, m14 48, m15 80, m16 80. m11 có file tác giả hóa nháp chưa biên dịch/duyệt; m12 chưa có ngân hàng. Hiện các phần có 2 lượt được mở là m03–m08, m13, m15, m16. Mục tiêu khoảng 100 câu/phần chưa đạt. Bài ngắn cần nội dung bổ sung hoặc chấp nhận giới hạn câu hỏi để tránh lặp ý và gắn nhãn độ khó sai.

`scripts/audit_banks.py` kiểm cấu trúc, trang nguồn, một đáp án theo chỉ số và số ý theo mức; hiện các bank đã biên dịch PASS **cơ học**. `scripts/test_sampling.py` chạy 100 hạt giống/phần và hiện PASS với ràng buộc 10/20/10 và tất cả chủ đề. Hai phép kiểm này không chứng nhận đúng y khoa.

m05–m08 và m13/m15/m16 có báo cáo hai lượt nguồn/ngữ nghĩa trong `content/reviews/`. m03/m04 vừa được ghi nhận hai lượt. m09/m10/m14 vẫn là nháp chưa duyệt. Review độc lập trước đó của m14 chỉ ra câu hỏi tự lộ đáp án, độ khó bị gán cao, thiếu chủ đề và lặp ý; bản sửa 48 câu chưa được duyệt lại. `content/source-issues.json` và `content/reviews/early-source-issues.json` liệt kê các vùng nguồn chưa rõ/bất nhất bị loại. Hai lượt không khẳng định bao quát tuyệt đối hoặc không sai sót.

Nếu nội dung được sửa, dấu duyệt cũ không tự bảo toàn. Build chỉ phát hành phần có `reviewStatus: passed2`, đủ concept 10/20/10 và mọi câu có `source`/`semantic` true. Không phát hành các câu nháp chỉ để có trang web chạy.

Để tiếp tục: (1) hoàn thiện m11/m12 và duyệt m09/m10/m14, (2) kiểm giao diện trên trình duyệt, (3) gắn remote GitHub rồi push và xác nhận deploy Pages. Thư mục hiện chưa có remote.
