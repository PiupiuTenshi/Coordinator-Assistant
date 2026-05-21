# Medical Symptom QR AI

MVP hỗ trợ bệnh nhân nhập triệu chứng qua QR form, nhận diện triệu chứng tiếng Việt bằng PhoBERT ở các giai đoạn sau, gợi ý phân luồng ban đầu và cơ sở y tế phù hợp.

## Đã scaffold

Giai đoạn 1: thu thập và làm sạch dữ liệu.

```bash
pip install -r requirements.txt
python phase1_pipeline.py --urls data/input/sample_urls.txt
```

Chạy thử bằng dữ liệu mẫu:

```bash
python phase1_pipeline.py --demo
```

Tài liệu chi tiết: `docs/phase1_data_pipeline.md`.

Giai đoạn 2: sinh dữ liệu gợi ý để gán nhãn BIO và triage.

```bash
python phase1_pipeline.py --demo
python phase2_pipeline.py
```

Guideline gán nhãn: `docs/annotation_guideline.md`.

Giai đoạn 3: fine-tune PhoBERT cho NER và triage.

```bash
python phase3_pipeline.py --validate-only
```

Khi đã có dữ liệu train/valid đủ lớn và đã cài dependencies:

```bash
python training/train_ner.py
python training/train_triage.py
```

Tài liệu: `docs/phase3_model_training.md`.

Giai đoạn 4: backend FastAPI.

```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Swagger UI: `http://127.0.0.1:8000/docs`

Tài liệu: `docs/phase4_backend_api.md`.

Giai đoạn 5: frontend QR form.

```bash
python -m http.server 5173 -d frontend
```

Mở: `http://127.0.0.1:5173`

Tài liệu: `docs/phase5_frontend_qr_form.md`.

Giai đoạn 6: bản đồ và hướng đi.

- Backend trả khoảng cách, Google Maps Directions URL, OpenStreetMap URL và map embed URL.
- Frontend hiển thị bản đồ nhúng trong trang kết quả.

Tài liệu: `docs/phase6_map_directions.md`.

Giai đoạn 7: kiểm thử an toàn y khoa.

```bash
python safety/run_safety_suite.py
python -m pytest backend/tests
```

Tài liệu: `docs/phase7_medical_safety_testing.md` và `docs/safety_policy.md`.

Giai đoạn 8: triển khai MVP.

```bash
python scripts/generate_qr.py --url http://127.0.0.1:5173
python scripts/smoke_mvp.py
```

Docker:

```bash
docker compose up --build
```

Tài liệu: `docs/phase8_mvp_deployment.md` và `docs/release_checklist.md`.

Lưu ý deploy: `--port $PORT` chỉ dùng trên Render/Railway hoặc môi trường có biến `PORT`. Chạy local bằng PowerShell dùng `--port 8000`.

Render public URL hiện có thể mở thẳng web ở `/` vì FastAPI serve thư mục `frontend`:

```text
https://coordinator-assistant.onrender.com
```

## Disclaimer

Hệ thống chỉ hỗ trợ sàng lọc ban đầu và chuẩn bị dữ liệu nghiên cứu. Không chẩn đoán bệnh, không kê đơn thuốc, không thay thế tư vấn bác sĩ.
