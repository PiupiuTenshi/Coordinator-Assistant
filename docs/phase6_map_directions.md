# Giai đoạn 6 - Bản đồ và hướng đi

Phase 6 mở rộng phần bệnh viện gần nhất và chỉ đường. Bản mới ưu tiên **sơ đồ nội viện tới khoa** thay vì chỉ mở bản đồ ngoài.

## Backend

`POST /api/hospitals/nearby`

Request:

```json
{
  "location": {
    "lat": 10.7769,
    "lng": 106.7009
  },
  "emergency_only": true,
  "limit": 3
}
```

Response mỗi bệnh viện có:

- `lat`, `lng`
- `distance_km`
- `has_emergency`
- `opening_hours`
- `map_url` cho Google Maps Directions
- `osm_url` cho OpenStreetMap
- `embed_map_url` để nhúng bản đồ
- `department_route` gồm khoa, tòa, tầng, phòng, tuyến đường nội viện và các bước đi

`GET /api/hospitals/{id}/directions?lat=...&lng=...`

Trả URL chỉ đường Google Maps và URL OpenStreetMap cho bệnh viện.

## Frontend

Trang kết quả hiển thị:

- Danh sách 3 bệnh viện gần nhất.
- Ưu tiên bệnh viện có cấp cứu khi triage là `EMERGENCY`.
- Khoảng cách tính theo Haversine nếu có vị trí người dùng.
- Sơ đồ nội viện từ cổng/sảnh chính tới khoa được gợi ý.
- Nút `Chỉ đường tới khoa`, `Gọi bệnh viện`.

## Chạy kiểm tra

```bash
python -m pytest backend/tests
```

Frontend:

```bash
python -m http.server 5173 -d frontend
```
