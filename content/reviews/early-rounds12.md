# Kiểm tra lượt 1–2: m13, m15, m16

## Phạm vi

240 câu chữ: mỗi bài 80 câu. Chưa gọi là ngân hàng 100 câu/bài. Không chèn ảnh vào đề. Không bổ sung kiến thức từ các bài khác hoặc từ Internet. Phần trích nguồn thuộc đúng tài liệu của từng câu.

Đã đọc toàn bộ lớp chữ trích xuất của ba PDF. Đã render toàn bộ ba PDF và xem các trang hình có nội dung thêm: m13 trang14/17/24/26/33; m15 trang3/9/13/15/16/20/24/26; m16 trang3/7/9/10/11/12/13/17/20/21/22. Không diễn giải ảnh siêu âm thiếu tiêu chuẩn thành câu chẩn đoán chắc chắn. Các câu đều là văn bản dù một số bằng chứng là bảng trong hình.

## Lượt 1: đối chiếu nguồn

Đã kiểm từng câu khi soạn: m13-q001–q080; m15-q001–q080; m16-q001–q080. Mỗi câu có nguồn số trang, giữ chữ của tài liệu trong quote; phần bảng hình có `type: visual`, `transcriptionVerified: true` sau khi xem bản render. Đây là bản chép nội dung hình, không phải OCR tự động đã được mặc định tin cậy.

Các dữ kiện tính toán dùng đúng công thức/phạm vi ở nguồn: m13 CRL10–30mm và cộng42 ngày; m15 hCG48giờ, nhóm ban đầu dưới1500,1500–3000,trên3000 với49%,40%,33%. Không dùng trường hợp đúng ranh giới gây mơ hồ. Kết quả tính không được biến thành xác nhận vị trí thai.

Loại vùng nguồn nghi vấn được ghi tại `early-source-issues.json`. Không diễn giải mốc hCG>100000 thành điều kiện cần cho mọi thai trứng; các câu liên quan dùng bảng phân biệt trang12 và nhắc vai trò xác nhận của GPB. Không dùng ngoại lệ hút nạo ở m16p20 làm chỉ định điều trị. Không sử dụng các nhánh xử trí can thiệp ở m15p26.

Kết quả lượt1: đạt đối chiếu cho240 câu đã giữ lại. Không đồng nghĩa toàn bộ tài liệu không có lỗi; những vùng bị loại làm hạn chế tuyên bố bao quát tuyệt đối.

## Lượt 2: tự giải lại và kiểm tra cấu trúc câu

Đã đọc lại bản JSON xuất ra của cả240 câu, gồm stem, cả4 lựa chọn và vị trí đáp án sau xoay. Tự kiểm phép tính62/52/72 ngày;1490/2800/5320 IU/L;20%/30%/50% và các ngưỡng tương ứng. Kiểm rằng một dấu hiệu gợi ý không được nâng thành chẩn đoán chắc chắn, một đặc điểm điển hình không bị biến thành điều kiện cần/đủ, và một hướng xử trí được liệt kê không thành chỉ định cho mọi người.

Lỗi tìm và sửa:

- Sửa lỗi gõ `tha ilưu`, `phôi/tha i`.
- Thêm khoảng trắng quanh số để câu đọc được; giữ nguyên ký hiệu p57KIP2 và kiểu nhiễm sắc thể.
- Hạ mức độ ở các câu thực chất chỉ nhắc lại bảng/thuật ngữ dù có vỏ tình huống. Không giữ tỷ lệ20/40/20 bằng cách gán nhãn cao giả.
- Một số câu tính toán/đọc bảng gần nhau được gắn chung `conceptId` để không lấy đồng thời trong một đề40 câu. Ngân hàng chứa các cách kiểm khác nhau của cùng ý nhưng số ý độc lập thấp hơn số câu; cần bộ chọn đề tránh trùng ý.
- Xác minh `answer` vẫn trỏ đúng phương án sau khi xoay các lựa chọn; không dựa vào vị trí A mặc định.

Phân bố sau chỉnh mức độ:

| Bài | Thông hiểu | Vận dụng | Phân tích/vận dụng cao | Tổng |
|---|---:|---:|---:|---:|
|m13|27|37|16|80|
|m15|29|33|18|80|
|m16|42|24|14|80|

Mức cao trong các bài này chủ yếu là tích hợp bằng chứng, phân biệt điều kiện áp dụng, đối chiếu nhiều đặc điểm hoặc phân tích lỗi suy luận. Không tuyên bố đây là bộ tình huống điều trị chuyên sâu vì nguồn không đủ điều kiện/phác đồ để soạn an toàn.

Kết quả lượt2: đạt kiểm tra nội dung/đáp án của bản đã sửa. Chưa có chứng nhận bác sĩ độc lập. Lời giải từng phương án viện lại cùng căn cứ đúng, không thêm cơ chế hoặc khuyến nghị ngoài tài liệu.

## Lượt 3 còn chờ

`review.coverage` vẫn false. Cần reviewer khác kiểm bao quát theo chủ đề, mức độ, trùng ý còn sót và chạy bộ chọn40 câu10/20/10 với ràng buộcconceptId. Không được ghi ba lượtPASS trước bước này. Những vùng nguồn bị loại phải tiếp tục được công khai trong phạm vi bao quát.
