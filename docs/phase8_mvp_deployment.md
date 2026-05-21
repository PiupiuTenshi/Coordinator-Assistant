# Giai đoạn 8 - Triển khai MVP

Phase 8 chuẩn bị bản MVP có thể chạy local hoặc Docker.

## Local

Backend:

```bash
python -m pip install -r requirements-backend.txt
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

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
3. Tạo frontend:
   - New -> Static Site.
   - Root/Publish directory: `frontend`.
   - Build command: để trống.
4. Sau khi có backend URL, mở frontend và set:
   ```js
   localStorage.setItem("apiBase", "https://your-backend.onrender.com/api")
   ```
   Hoặc sửa trực tiếp `frontend/app.js` trước khi deploy.
5. Tạo lại QR bằng URL frontend public.

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
