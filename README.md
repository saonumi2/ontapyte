# Ôn tập Module Sản

Web trắc nghiệm tiếng Việt theo từng tài liệu trong thư mục cha. Mỗi lượt thi có 40 câu chữ (A–B–C–D), xáo trộn câu **trong từng mức độ** và đi theo thứ tự 10 thông hiểu, 20 vận dụng, 10 vận dụng cao. Sau khi chọn đáp án, web báo đúng/sai ngay và mở được giải thích cùng trang/slide gốc.

## Tình trạng nội dung

Không thể xem ngân hàng là đã duyệt chỉ vì trang web chạy. `content/banks/*.json` lưu câu hỏi và dấu kiểm tra. `scripts/build_site.py` **chỉ phát hành** một phần khi mọi câu trong phần đó đã qua hai lượt nguồn và ngữ nghĩa, đủ 10/20/10 câu với concept không trùng, và `reviewStatus` của phần là `passed2`. Những phần còn lại hiển thị “Đang kiểm duyệt”. Xem `content/REVIEW_POLICY.md`, `content/source-issues.json` và `content/reviews/` trước khi mở khóa một phần.

Một số slide có nội dung nằm trong ảnh nên cần đối chiếu ảnh gốc, không thể chỉ kiểm lớp chữ tự động. Có mệnh đề trong nguồn cần xác minh chuyên môn; các trang này bị loại khỏi câu hỏi. Nguồn học có thể chứa các mốc hoặc phác đồ không còn phù hợp thực hành hiện nay; trang web là công cụ học theo nguồn, không dùng để chỉ định điều trị.

## Chạy và kiểm tra

Yêu cầu Python 3.10+. Không cần npm hoặc API key. Từ thư mục dự án:

```bash
python scripts/audit_banks.py
python scripts/test_sampling.py
python scripts/build_site.py
python -m http.server 8000 --directory dist
```

Mở `http://localhost:8000`. Mở trực tiếp `index.html` bằng `file://` sẽ không tải được JSON do quy tắc bảo mật trình duyệt.

## Đẩy lên GitHub và deploy

Repo này có `.github/workflows/pages.yml`: mỗi lần push `main`, GitHub Actions kiểm ngân hàng, build thư mục `dist/`, rồi deploy GitHub Pages. Trong GitHub repository, chọn **Settings → Pages → Build and deployment → Source: GitHub Actions**. Repo có thể là GitHub Pages project site; các đường dẫn của web là tương đối nên chạy được dưới `/<ten-repo>/`.

```bash
git init
git add .
git commit -m "Add Module San quiz site and source-backed banks"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

Thay `USERNAME/REPOSITORY` bằng repo của bạn. Chỉ push khi quyền phát hành tài liệu được bảo đảm: tài liệu gốc và PDF slide nằm trong `public/sources` để người học mở nguồn ngay sau mỗi câu.

## Cấu trúc

- `content/mNN.json`: văn bản trích xuất theo trang/slide, hash của tài liệu nguồn.
- `content/banks/mNN.json`: ngân hàng câu hỏi theo từng phần.
- `content/source-issues.json`: các chỗ nguồn cần xác minh, không dùng làm đáp án.
- `src/`: giao diện và logic trộn đề, phản hồi tức thì.
- `scripts/`: trích xuất, kiểm, build.
- `public/sources/`: PDF nguồn và bản PDF xuất từ slide để mở nguồn trong trình duyệt.

Khi sửa đáp án, giải thích hoặc nguồn của bất kỳ câu nào, đặt lại hai dấu duyệt `source` và `semantic` của câu đó và `reviewStatus` của phần trước khi build lại; xem thay đổi như một bản câu hỏi mới cần duyệt.
