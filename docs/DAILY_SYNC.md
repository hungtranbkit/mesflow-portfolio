# Đồng bộ dự án portfolio hằng ngày

Workflow: `.github/workflows/daily-portfolio-sync.yml`
Lịch: **08:17 mỗi ngày theo giờ Việt Nam** (`17 1 * * *` UTC).
Nguồn công khai: https://hungtranbkit.github.io/mesflow-portfolio/

## Hoạt động
1. GitHub Actions liệt kê repo của `hungtranbkit`.
2. Bỏ qua repo fork, lưu trữ, bản thử nghiệm, repo trống, tên bị loại trừ và những repo đã có trong portfolio.
3. Với repo **public** có README đủ nội dung, tự tạo metadata ở `data/projects.json`, trang case study, demo minh họa và sitemap.
4. Giữ nguyên toàn bộ nội dung dự án đã được biên tập thủ công (không đổi tên, trạng thái, nội dung, URL cũ).
5. Chạy unit test, kiểm tra routes, JavaScript; chỉ commit nếu có dự án mới; triển khai GitHub Pages trong cùng workflow.
6. Công khai **chỉ các file thuộc website** qua `scripts/build_site.py`, không xuất bản `.git`, `scripts`, file cấu hình nội bộ hoặc secrets.

## Private repository
**Mặc định không công bố repo private.** GitHub Actions chỉ nhìn được repo public bằng `GITHUB_TOKEN` trong repository portfolio.

Nếu muốn đọc repo private, chủ repo tự thêm GitHub Actions secret có tên `PORTFOLIO_SYNC_TOKEN` (token chỉ có quyền *read-only* trên những repository được chọn). Không paste token vào chat, không in ra log.

Sau đó, trong từng repo private muốn giới thiệu, tạo file `portfolio.public.json` với thông tin **được phép công bố**. Ví dụ:

```json
{
  "publish": true,
  "name": "Tên sản phẩm được phép công khai",
  "summary": "Tóm tắt an toàn, không chứa URL hay dữ liệu nội bộ.",
  "category": "ai",
  "phase": "development",
  "tagline": "Giá trị chính của sản phẩm.",
  "stack": ["Python", "React"],
  "capabilities": ["Năng lực một", "Năng lực hai", "Năng lực ba"],
  "steps": ["Chuẩn bị dữ liệu", "Tải dữ liệu mẫu", "Chạy mô phỏng", "Xem kết quả"],
  "sample": "Dữ liệu demo hoàn toàn giả lập"
}
```

Repo private **không được đọc nội dung README** để tự viết nội dung. Chỉ dữ liệu đã được ghi trong manifest `publish:true` được phép đưa vào danh mục. Không hiện link repository private. Repo không có manifest sẽ bị bỏ qua.

## Tùy chỉnh
Repo public cũng có thể tạo `portfolio.public.json` nếu muốn kiểm soát nội dung, trạng thái hoặc bỏ qua với `{"publish":false}`. Thuộc tính `featured` không tự bật; những dự án nổi bật vẫn do chủ portfolio chọn thủ công.

Trạng thái mặc định của dự án tự phát hiện là **Đang phát triển**. Từ README có cảnh báo thử nghiệm sẽ gắn **Prototype**. Không tự gán **Đang vận hành**. Hệ thống **không tự tạo demo backend**; demo là luồng thao tác mô phỏng local, không gửi dữ liệu.

## Chạy kiểm tra
```bash
python3 -m unittest discover -s scripts -p test_repo_sync.py -v
python3 scripts/sync_repos.py --owner hungtranbkit
python3 scripts/check_site.py
python3 scripts/build_site.py
node --check assets/app.js
```
Bỏ `--apply` để chạy thử; thêm `--apply` để ghi ra project mới. Chạy lại không tạo trùng.

## Chạy ngay
Vào GitHub **Actions → Daily portfolio discovery and publish → Run workflow**. Kết quả và số project mới hiển thị trong Job Summary. Nếu chưa có dự án phù hợp sẽ không tạo commit, nhưng vẫn triển khai bản hiện hành.

**Không tự publish thư mục làm việc, log vận hành, đường dẫn SSH, token, dữ liệu khách hàng hay thông tin chưa được chủ dự án xác nhận.**
