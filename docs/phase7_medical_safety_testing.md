# Giai đoạn 7 - Kiểm thử an toàn y khoa

Phase 7 thêm bộ kiểm thử tình huống nguy hiểm và báo cáo an toàn.

## Chạy safety suite

```bash
python safety/run_safety_suite.py
```

Output:

```text
data/reports/phase7_safety_report.md
```

## Chạy toàn bộ backend tests

```bash
python -m pytest backend/tests
```

## Dữ liệu test

Các case nằm ở:

```text
data/safety/red_flag_cases.jsonl
```

Mỗi case có thể định nghĩa:

- `symptom_text`
- `age`
- `discomfort_level`
- `risk_groups`
- `dangerous_symptoms`
- `expected_triage`
- `expected_not_triage`
- `must_not_recommend_doctor`

## Điều kiện pass

- Red flag phải trả `EMERGENCY`.
- Emergency không được trả danh sách bác sĩ/đặt lịch thường.
- Emergency phải có bệnh viện có cấp cứu.
- Response phải có disclaimer.
- Case phủ định như `không kèm khó thở` không bị đẩy nhầm sang `EMERGENCY`.
