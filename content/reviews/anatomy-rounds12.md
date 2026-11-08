# Hai lượt kiểm tra m03 và m04

Nguồn được đọc toàn bộ theo trang của hai PDF. Khi soạn, mỗi câu m03-q001–q080 và m04-q001–q080 được gắn một hoặc nhiều trang nguồn; trích dẫn lưu nguyên văn toàn trang để giữ điều kiện và ngữ cảnh. Không dùng hình không có phần chữ rõ để tạo thêm kết luận. Lượt 1 đối chiếu câu đúng và giải thích với các trang đó; `scripts/audit_banks.py` kiểm tất cả trích dẫn thuộc đúng tài liệu, đúng trang và không chạm trang nguồn bị chặn. Kết quả: không còn lỗi cơ học nguồn.

Lượt 2 đọc lại bốn lựa chọn khi biên soạn và phân biệt đáp án đúng với từng lựa chọn nhiễu. Các câu phân tích nối nhiều trang được ghi nguồn đầy đủ, ví dụ m03-q061 (đoạn bóng và nếp niêm mạc) và m04-q061 (đầu vòi, dây chằng treo, mạch buồng trứng). Điều kiện trong tình huống được giữ, chẳng hạn m03-q034 không dùng việc không thấy vòi trứng để kết luận tắc; m04-q040 chỉ hỏi số tiêu chuẩn PCOS **trong bài** và không thay thế chẩn đoán. `scripts/test_sampling.py` chạy 100 lượt giả lập mỗi phần, đủ 10/20/10, không trùng `conceptId` và có tất cả chủ đề.

Kết quả: hai lượt PASS cho 160 câu ở phiên bản hiện tại. Đây là kiểm tra theo tài liệu được cung cấp, không phải chứng nhận thực hành y khoa hay xác nhận tính cập nhật của tài liệu. Mục tiêu khoảng 100 câu/phần hiện đạt 80 câu/phần; không tạo thêm câu lặp để đủ chỉ tiêu.
