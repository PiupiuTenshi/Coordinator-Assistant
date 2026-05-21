# Giai đoạn 8 - Triển khai MVP

Phase 8 chuẩn bị bản MVP có thể chạy local hoặc Docker.

## Local

Backend:

```bash
python -m pip install -r requirements-backend.txt
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Không dùng lệnh `--port $PORT` khi chạy local bằng PowerShell nếu bạn chưa tự set biến `PORT`. `$PORT` là biến môi trường do nền tảng deploy như Render cấp.

Frontend:

```bash
python -m http.server 5173 -d frontend
```

Smoke test:

```bash
python scripts/smoke_mvp.py
```

## Docker Compose

```bash
docker compose up --build
```

URLs:

- Frontend: `http://127.0.0.1:5173`
- Backend: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

## QR

Tạo SVG QR-style placeholder:

```bash
python scripts/generate_qr.py --url http://127.0.0.1:5173 --output frontend/public/qr-mvp.svg
```

Khi deploy thật, đổi URL thành domain public của frontend, ví dụ:

```bash
python scripts/generate_qr.py --url https://your-frontend.onrender.com --output frontend/public/qr-mvp.svg
```

QR hiện được hiển thị trong phần đầu của frontend qua mục `Hiển thị QR mở form`.

## Deploy free gợi ý

### Phương án dễ nhất: Render

Render có free web service và static site, nhưng web service miễn phí có thể sleep sau một thời gian không có request. Phù hợp demo/MVP, không phù hợp production y tế.

1. Đẩy repo lên GitHub.
2. Tạo backend:
   - Render Dashboard -> New -> Web Service.
   - Connect repo.
   - Runtime: Python.
   - Build command:
     ```bash
     pip install -r requirements-backend.txt
     ```
   - Start command:
     ```bash
     uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
     ```
   - Lưu lại URL backend, ví dụ:
     ```text
     https://medical-symptom-api.onrender.com
     ```
3. Tạo frontend:
   - New -> Static Site.
   - Root/Publish directory: `frontend`.
   - Build command: để trống.
4. Sửa file `frontend/config.js` trước khi deploy frontend:
   ```js
   window.APP_CONFIG = {
     API_BASE: "https://medical-symptom-api.onrender.com/api"
   };
   ```
5. Sau khi có URL frontend public, tạo lại QR:
   ```bash
   python scripts/generate_qr.py --url https://medical-symptom-frontend.onrender.com --output frontend/public/qr-mvp.svg
   ```
6. Commit/push lại `frontend/config.js` và `frontend/public/qr-mvp.svg`.
7. Render sẽ tự redeploy khi bạn push lên GitHub.

### Deploy bằng Blueprint

Repo có sẵn `render.yaml`, có thể dùng Render Blueprint để tạo cả backend và frontend. Sau khi backend được tạo, vẫn cần sửa `frontend/config.js` sang URL backend public và push lại.

### Phương án tách frontend/backend

- Frontend static: Vercel, Netlify, Cloudflare Pages hoặc Render Static Site.
- Backend FastAPI: Render Web Service hoặc Railway.

Nếu dùng tài khoản miễn phí, cần kiểm tra quota/cold start trước khi demo.

## Release checklist

- [ ] `python safety/run_safety_suite.py` pass.
- [ ] `python -m pytest backend/tests` pass.
- [ ] `python scripts/smoke_mvp.py` pass.
- [ ] Frontend mở được trên điện thoại.
- [ ] Nút gọi 115, gọi bệnh viện, Google Maps hoạt động.
- [ ] API `/api/health` trả `ok`.
- [ ] Response emergency không hiển thị đặt lịch thường.
- [ ] Có disclaimer y khoa trên kết quả.
- [ ] QR trỏ đúng domain production.
- [ ] Không dùng dữ liệu cá nhân để train nếu chưa có đồng ý rõ ràng.

## Theo dõi sau deploy

- Theo dõi lỗi API 4xx/5xx.
- Theo dõi thời gian phản hồi `/api/symptom/analyze`.
- Review feedback `unsafe`.
- Bổ sung red flag case mới vào `data/safety/red_flag_cases.jsonl`.
- Cập nhật dataset/model định kỳ sau review chuyên môn.
