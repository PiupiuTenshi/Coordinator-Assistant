# Chính sách an toàn y khoa MVP

Hệ thống chỉ hỗ trợ sàng lọc ban đầu và điều hướng người bệnh. Không chẩn đoán bệnh, không kê đơn, không thay thế bác sĩ.

## Nguyên tắc bắt buộc

- Nếu có dấu hiệu nguy hiểm, luôn ưu tiên `EMERGENCY` dù model AI dự đoán mức thấp hơn.
- Với `EMERGENCY`, không gợi ý đặt lịch thường hoặc chọn bác sĩ như luồng khám thông thường.
- Với `EMERGENCY`, response phải có bệnh viện có cấp cứu và nút gọi cấp cứu trên frontend.
- Response phải có disclaimer y khoa.
- Dữ liệu người dùng nhập trong MVP không được dùng để train nếu chưa có đồng ý rõ ràng.

## Red flags tối thiểu

- Đau ngực kèm khó thở hoặc vã mồ hôi.
- Méo miệng, nói khó, yếu/liệt tay chân.
- Co giật, bất tỉnh, ngất.
- Sốt cao ở trẻ nhỏ kèm li bì hoặc co giật.
- Đau đầu dữ dội đột ngột, cứng gáy.
- Chảy máu nhiều hoặc không cầm.
- Khó thở nặng, tím tái.

## Release gate

Trước khi demo hoặc deploy MVP phải chạy:

```bash
python safety/run_safety_suite.py
python -m pytest backend/tests
```

Không release nếu có bất kỳ case emergency nào fail.
