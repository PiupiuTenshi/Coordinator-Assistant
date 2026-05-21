# MVP release checklist

## Data

- [ ] Dataset Phase 1/2 đã được review quyền sử dụng.
- [ ] Không có dữ liệu định danh cá nhân trong dữ liệu training.

## Safety

- [ ] Safety suite pass.
- [ ] Emergency seed recall đạt 100% trên bộ case MVP.
- [ ] Disclaimer hiển thị trên frontend.
- [ ] Red flag không đi qua luồng đặt lịch thường.

## Backend

- [ ] `/api/health` hoạt động.
- [ ] `/api/symptom/analyze` trả response dưới 2 giây với rule fallback.
- [ ] `/api/hospitals/nearby` trả map URL.
- [ ] Swagger docs mở được.

## Frontend

- [ ] Form dùng tốt trên mobile.
- [ ] Nút gọi 115 luôn dễ thấy.
- [ ] Bản đồ và chỉ đường hoạt động.
- [ ] Feedback gửi được.

## Deploy

- [ ] Domain/HTTPS đã cấu hình.
- [ ] QR code trỏ đúng URL public.
- [ ] Log runtime không commit vào git.
- [ ] Có kế hoạch rollback.
