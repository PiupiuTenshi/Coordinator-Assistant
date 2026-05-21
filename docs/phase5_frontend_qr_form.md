# Giai đoạn 5 - Frontend QR form

Phase 5 tạo giao diện web mobile-first để bệnh nhân nhập triệu chứng và xem kết quả từ backend Phase 4.

## Chạy frontend

Backend cần chạy trước:

```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Frontend static:

```bash
python -m http.server 5173 -d frontend
```

Mở:

```text
http://127.0.0.1:5173
```

## Chức năng đã có

- Chọn `Khám lần đầu` hoặc `Tái khám`.
- Nhập triệu chứng chính, thời gian, tuổi, giới tính, mức khó chịu.
- Chọn nhóm nguy cơ và dấu hiệu nguy hiểm.
- Lấy vị trí bằng Geolocation API.
- Gọi `POST /api/symptom/analyze`.
- Hiển thị mức xử trí bằng màu cảnh báo.
- Hiển thị triệu chứng nhận diện, khoa gợi ý, bác sĩ phù hợp, bệnh viện gần nhất.
- Nút gọi 115, gọi bệnh viện, mở Google Maps.
- Đặt lịch demo qua `POST /api/appointments/book`.
- Gửi feedback qua `POST /api/feedback`.

## Cấu hình API

Mặc định frontend gọi:

```text
http://127.0.0.1:8000/api
```

Có thể đổi trong trình duyệt:

```js
localStorage.setItem("apiBase", "https://your-domain.example/api")
```

## QR code

Khi deploy, tạo QR trỏ tới URL frontend, ví dụ:

```text
https://your-domain.example/
```

Trong môi trường local, QR có thể trỏ tới `http://<IP-máy-tính>:5173` nếu điện thoại và máy tính cùng mạng.
