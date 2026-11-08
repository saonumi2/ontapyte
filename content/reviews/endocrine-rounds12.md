# Đối chiếu nội dung m05–m08: lượt 1 và lượt 2

Phạm vi: 300 câu chữ, 4 lựa chọn, một đáp án; m05 60 câu, m06/m07/m08 mỗi bài 80 câu. Đây chưa phải mục tiêu 100 câu/bài và chưa phải xác nhận qua đủ ba lượt. `review.coverage` của tất cả câu vẫn là `false` để reviewer độc lập kiểm tra lượt 3.

## Lượt 1 — căn cứ trong đúng tài liệu

- Đọc trọn phần chữ m05, m07, m08; giữ nguyên nguồn theo trang/slide của chính từng bài.
- m06: xem ảnh trang 3–48 (8 contact sheets), đối chiếu bản OCR với ảnh và chép các đoạn sử dụng vào `content/banks/_m06-verified-excerpts.json`. Không dùng OCR sai dấu làm trích dẫn. Mọi nguồn này được đánh dấu `type: visual`, `transcriptionVerified: true`.
- m08: xem trực tiếp trang 10–15. Phần WHO và bảng nguyên nhân vô kinh ở 12–15 được chép riêng vào `_m08-verified-excerpts.json`. Các bảng được chuyển thành chữ, không đưa hình vào đề.
- Một số khái niệm có mặt trong cả m05 và m06. Câu tương ứng được đối chiếu lại ở m06 và thay hoàn toàn căn cứ bằng trang/hình m06; không lấy trích dẫn m05 làm căn cứ cho m06.
- Không dùng m06 trang 33 có cụm “tiền kỳ (metaphase)”. Điểm dừng meiosis II dùng trang 34 rõ nghĩa. Không hỏi con số 36 giờ ở trang đang bị treo.
- Không dùng khái quát LASDS ở m08 trang 24, liều/thời điểm tránh thai khẩn cấp ở 30/31/34. Trang 29 chỉ sử dụng mô tả riêng vòng EE–etonogestrel.
- Các trích dẫn lớp chữ giữ đoạn toàn trang để không đánh mất điều kiện. Các trích dẫn hình là bản chép phần liên quan, không phải nội dung ngoài bài. Các con số được giữ trong phạm vi bài, không gộp giữa những bài có mốc khác nhau.

Kết quả lượt 1 đối với 300 câu hiện lưu: đạt đối chiếu căn cứ trong phạm vi tài liệu đã sử dụng. Đây không xác nhận mọi phát biểu của tài liệu gốc là hướng dẫn lâm sàng hiện hành.

## Lượt 2 — tự giải lại và biên tập câu hỏi

Đã kiểm từng stem, đáp án khóa, bốn lựa chọn, phần giải thích và điều kiện áp dụng. Chỉ suy luận trực tiếp từ các mệnh đề nguồn; không thêm phác đồ, liều thuốc hoặc chẩn đoán bệnh chắc chắn từ mẫu xét nghiệm đơn độc.

Các sửa chữa quan trọng:

1. Hạ mức các câu chỉ gọi tên cấu trúc/hormone/gene/dạng thuốc, dù trước đó có mở đầu “một sơ đồ”, “một tế bào”. Ví dụ ESR1/ESR2, PGR, thành phần que cấy, nhãn WHO trong sơ đồ không được giữ là vận dụng chỉ vì cách diễn đạt.
2. Viết lại các câu m05 về gián đoạn di trú, ngừng nguyên phân, gián đoạn xung GnRH, chặn bước thơm hóa, phản hồi E2, giảm phân sau LH và nguồn cholesterol thành câu có tình huống cần áp dụng quan hệ. Không suy mất một nguồn cung đồng nghĩa mọi hormone bằng không.
3. Dùng cùng `conceptId` cho các câu hỏi gần như cùng ý để bộ chọn đề không lấy cả hai. Ví dụ hỏi tác dụng E2 lên FSH và hỏi chiều biến thiên FSH; kiểu chất nhầy và hormone giải thích; mẫu WHO với bài tập xếp nhóm tương ứng.
4. m08-q078 đã thay hoàn toàn: phân tích việc không thể suy cơ chế chỉ từ đường đặt vòng âm đạo. Câu này không sử dụng khái quát sai ở trang 24.
5. Không kết luận phóng noãn đồng nghĩa đã thụ tinh/hoàn tất giảm phân II. Không kết luận ra máu lần đầu chứng minh phóng noãn đều. Không biến sơ đồ WHO II thành tiêu chuẩn chẩn đoán chắc chắn PCOS.

Phân bố sau sửa:

| Bài | Thông hiểu | Vận dụng | Vận dụng cao | Tổng |
|---|---:|---:|---:|---:|
| m05 | 26 | 20 | 14 | 60 |
| m06 | 29 | 32 | 19 | 80 |
| m07 | 33 | 29 | 18 | 80 |
| m08 | 32 | 30 | 18 | 80 |

Kết quả lượt 2: đạt kiểm tra đáp án duy nhất và mức độ trong phạm vi các câu đang lưu. Các câu vận dụng cao yêu cầu nối cơ chế, phân biệt điều kiện/giai đoạn, hoặc đánh giá suy luận khái quát; không dùng độ dài để gán mức độ.

## Kiểm tra cơ học kèm theo, không thay thế lượt 3

Đã chạy `scripts/audit_banks.py` sau biên tập: m05, m06, m07 và m08 đều PASS cơ học (4 lựa chọn không trùng, đáp án hợp lệ, nguồn trong đúng tài liệu hoặc bản chép hình đã xác minh, đủ số mức độ tối thiểu). Chạy chương trình này không được tính thành một lượt duyệt chuyên môn khác.

## Hạn chế phải giữ khi bàn giao

- Chưa đạt 100 câu mỗi bài. Không nhân bản câu hoặc làm câu hỏi về liều chưa rõ để tăng số.
- m05 hiện có đúng 20 câu vận dụng: đề 10/20/10 sẽ sử dụng toàn bộ nhóm vận dụng này mỗi lượt. Chỉ các nhóm khác và thứ tự/đáp án có thể thay đổi; cần bổ sung câu vận dụng có nội dung mới nếu muốn thay đổi cả tập câu ở mức này.
- Nguồn m08 có các đoạn bị treo; chưa thể tuyên bố bao quát cả liều và thời điểm của tránh thai khẩn cấp. Không dùng các sơ đồ hình thiếu giải thích để tự tạo bệnh sinh mới.
- Nguồn hình không có text layer; kiểm tra substring không đủ. Bản chép và số trang được giữ để người khác đọc lại ảnh.
- Lượt 3 cần kiểm tra toàn phần, độ bao quát các mục, trùng ý và việc lấy 40 câu. Chưa set cờ đó, chưa gọi ngân hàng “chính thức đã duyệt chuyên môn”.

## Tái lập

Các file `_m05_author.py`, `_m06_author.py`, `_m07_author.py`, `_m08_author.py` là bản soạn lần đầu. Chạy theo thứ tự đó, sau đó chạy `_round2_endocrine.py` đúng một lần để áp dụng biên tập lượt 2 và nhóm concept. Các JSON `m05.json`–`m08.json` hiện tại là phiên bản sau lượt 2; không chạy lại bản soạn đầu đơn độc rồi coi đó là bản cuối.
