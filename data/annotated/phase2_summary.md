# Phase 2 Annotation Dataset Summary

- Total candidate sentences from clean articles: 6
- BIO train/valid/test: 4/0/0
- Triage train/valid/test: 4/0/0

## Outputs

- `data/annotated/train.bio`
- `data/annotated/valid.bio`
- `data/annotated/test.bio`
- `data/annotated/triage_train.csv`
- `data/annotated/triage_valid.csv`
- `data/annotated/triage_test.csv`

## Review Notes

- Các nhãn được tạo tự động bằng từ điển/rule nên chỉ là gợi ý ban đầu.
- Người gán nhãn cần sửa span triệu chứng, thêm duration/severity/body part nếu cần.
- Nhãn `EMERGENCY` phải được review kỹ để tránh bỏ sót ca nguy hiểm.
- Chia tập theo `article_id` để hạn chế rò rỉ cùng bài giữa train và test.
