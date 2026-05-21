# Giai đoạn 4 - Backend API

Phase 4 tạo backend FastAPI cho MVP.

## Chạy server

```bash
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Health check:

```bash
curl http://127.0.0.1:8000/api/health
```

## Endpoint chính

- `POST /api/symptom/analyze`
- `GET /api/specialties/recommend`
- `GET /api/doctors/recommend`
- `GET /api/doctors/{id}/available-slots`
- `POST /api/appointments/book`
- `GET /api/appointments/{id}`
- `POST /api/appointments/{id}/cancel`
- `POST /api/appointments/{id}/reschedule`
- `POST /api/hospitals/nearby`
- `GET /api/hospitals/{id}/directions`
- `POST /api/feedback`
- `GET /api/health`

## Request mẫu

```json
{
  "age": 45,
  "gender": "male",
  "patient_type": "first_visit",
  "symptom_text": "Tôi bị đau ngực, khó thở và vã mồ hôi từ 30 phút trước.",
  "duration": "30 phút",
  "discomfort_level": 9,
  "risk_groups": [],
  "dangerous_symptoms": [],
  "location": {
    "lat": 10.7769,
    "lng": 106.7009
  },
  "consent": false
}
```

## Thiết kế hiện tại

- Nhận diện triệu chứng bằng `data/dictionaries/symptom_seed.txt`.
- Phân loại triage bằng rule engine trong `backend/app/rules/triage_rules.py`.
- Nếu có red flag, luôn ưu tiên `EMERGENCY`.
- Gợi ý bác sĩ bị ẩn khi kết quả là `EMERGENCY`; API ưu tiên bệnh viện có cấp cứu.
- Model PhoBERT Phase 3 được để qua adapter `backend/app/services/model_adapter.py` để cắm sau.

## Test nhanh

```bash
pytest backend/tests
```

## Docker

```bash
docker build -f backend/Dockerfile -t medical-symptom-api .
docker run --rm -p 8000:8000 medical-symptom-api
```
