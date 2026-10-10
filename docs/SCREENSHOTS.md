# Ảnh giao diện trong Portfolio

Ngày 10/10/2026: 16 ảnh giao diện đã xem và kiểm tra trên 13/27 dự án. 14 dự án khác sẽ hiện rõ “Chưa có ảnh giao diện công khai” thay cho dashboard giả lập.

## Nguồn ảnh

- public_demo: ảnh chụp trực tiếp từ website công khai hoặc trang demo. Không mặc định là production.
- test_evidence: ảnh chụp từ bộ kiểm thử UI hoặc showcase của chính dự án, thường sử dụng dữ liệu giả lập.
- Trường screenshots[] trong data/projects.json lưu src, caption, source, kind và note; ảnh đặt ở assets/screenshots/*.png.
- Người dùng nhấn ảnh ở trang chi tiết để mở bản gốc; thumbnail được crop bằng CSS, không làm mất ảnh nguồn.

## An toàn trước khi đưa ảnh lên website

1. Kiểm tra ảnh bằng mắt, xác nhận đúng sản phẩm và đúng phạm vi, không ghép ảnh ứng dụng khác.
2. Chỉ dùng dữ liệu demo hoặc đã được phép công khai. Loại bỏ hình chứa tài khoản riêng, email/số điện thoại khách hàng, token, khóa truy cập, mật khẩu, URL nội bộ nhạy cảm hoặc cuộc trò chuyện thật.
3. Không đi vòng Cloudflare Access hoặc màn hình đăng nhập để chụp nội dung bảo vệ. Với BĐS Đắk Nông, sử dụng ảnh public demo kiểm thử đã rà soát, không công bố nội dung phía sau Access.
4. Caption phải nói rõ đó là website công khai, demo hay ảnh kiểm thử. Không khẳng định phiên bản test là sản phẩm production hiện hành.
5. Dùng PNG đã kiểm tra và giới hạn assets/screenshots/; thêm nguồn/ghi chú qua data/projects.json. Chạy python3 scripts/check_site.py và node --check assets/app.js.

## Các dự án đã có ảnh

MESFlow; NovaRetail; PropertyIQ; Hint; NovaFactory; AI Gateway (module Hội đồng thiết kế); BĐS Đắk Nông; Customer AI; JobRadar; Chọn Đồ Thông Minh; MESFlow QA Center; Sales Radar; OfflinePOS.

## Các dự án còn thiếu ảnh

NovaMaint; QR Restaurant; Gia Phả; MESFlow ESP32 Kiosk; AI QC Agent; MESFlow Deploy Agent; AI Design Council; ProjectFlow Workspace; ServerHub; OpenClaw Ops; Filament Winding CAD; RepoPort; MESFlow Kiosk Runtime v2; Terminal MCP.

Các dự án firmware, CLI, nghiên cứu hoặc chỉ có mã nguồn không tự động được dựng thành UI screenshot. Có bản demo an toàn mới bổ sung ảnh.

GitHub Actions quét repo mỗi ngày để phát hiện dự án mới; workflow này không tự động chụp hoặc công bố screenshot riêng tư.
