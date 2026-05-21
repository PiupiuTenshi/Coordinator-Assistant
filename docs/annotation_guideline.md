# Annotation guideline - Phase 2

Tài liệu này dùng cho bộ dữ liệu gán nhãn triệu chứng và phân luồng mức độ xử trí.

## Mục tiêu

- Tạo dữ liệu BIO để fine-tune PhoBERT token classification.
- Tạo dữ liệu phân loại câu để fine-tune PhoBERT sequence classification.
- Ưu tiên an toàn: không bỏ sót các câu có dấu hiệu nguy hiểm.

## Nhãn BIO

| Nhãn | Ý nghĩa |
|---|---|
| `B-SYMPTOM` | Token đầu của triệu chứng |
| `I-SYMPTOM` | Token tiếp theo của cùng triệu chứng |
| `B-BODY_PART` | Token đầu của bộ phận cơ thể |
| `I-BODY_PART` | Token tiếp theo của bộ phận cơ thể |
| `B-DURATION` | Token đầu của thời gian xuất hiện |
| `I-DURATION` | Token tiếp theo của thời gian xuất hiện |
| `B-SEVERITY` | Token đầu của mức độ nặng/nhẹ |
| `I-SEVERITY` | Token tiếp theo của mức độ |
| `B-FREQUENCY` | Token đầu của tần suất |
| `I-FREQUENCY` | Token tiếp theo của tần suất |
| `B-RISK_FACTOR` | Token đầu của yếu tố nguy cơ |
| `I-RISK_FACTOR` | Token tiếp theo của yếu tố nguy cơ |
| `O` | Không thuộc nhóm cần nhận diện |

Code hiện tại tự gợi ý `B-SYMPTOM/I-SYMPTOM` bằng từ điển triệu chứng seed. Các nhãn còn lại để người gán nhãn bổ sung thủ công ở vòng sau.

## Quy tắc gán triệu chứng

- Gán toàn bộ cụm triệu chứng, ví dụ `đau ngực`, `khó thở`, `vã mồ hôi`.
- Nếu triệu chứng có mức độ đi kèm, tách mức độ sang `SEVERITY` khi có annotation thủ công, ví dụ `đau đầu dữ dội`: `đau đầu` là `SYMPTOM`, `dữ dội` là `SEVERITY`.
- Không gán tên bệnh chắc chắn là triệu chứng nếu câu đang nói về chẩn đoán, ví dụ `viêm phổi` không tự động là `SYMPTOM`.
- Nếu một cụm vừa có triệu chứng vừa bộ phận cơ thể, ưu tiên span triệu chứng phổ biến, ví dụ `đau bụng` là `SYMPTOM`.

## Nhãn triage

| Nhãn | Ý nghĩa |
|---|---|
| `SELF_CARE` | Có thể theo dõi và chăm sóc tạm thời nếu nhẹ |
| `BOOK_APPOINTMENT` | Nên đặt lịch khám |
| `URGENT_CARE` | Nên đi khám sớm trong ngày |
| `EMERGENCY` | Cần cấp cứu hoặc đến cơ sở y tế gần nhất ngay |

## Quy tắc an toàn

- Nếu câu có dấu hiệu nguy hiểm như `đau ngực + khó thở`, `liệt`, `méo miệng`, `nói khó`, `co giật`, `ngất`, `chảy máu nhiều`, ưu tiên `EMERGENCY`.
- Trẻ nhỏ, phụ nữ mang thai, người cao tuổi hoặc người có bệnh nền nên được review tăng mức cảnh báo khi triệu chứng nặng.
- Không dùng nhãn tự động làm khuyến nghị y khoa cuối cùng nếu chưa có review chuyên môn.

## File đầu ra

- `data/annotated/train.bio`
- `data/annotated/valid.bio`
- `data/annotated/test.bio`
- `data/annotated/triage_train.csv`
- `data/annotated/triage_valid.csv`
- `data/annotated/triage_test.csv`
