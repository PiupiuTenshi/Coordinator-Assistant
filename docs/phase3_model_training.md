# Giai đoạn 3 - Huấn luyện PhoBERT

Phase 3 fine-tune hai mô hình:

- PhoBERT token classification cho nhận diện triệu chứng.
- PhoBERT sequence classification cho phân loại mức độ xử trí.

## Chuẩn bị

Chạy phase 1 và phase 2 trước:

```bash
python phase1_pipeline.py --demo
python phase2_pipeline.py
```

Cài dependencies:

```bash
pip install -r requirements.txt
```

## Kiểm tra dữ liệu không cần tải model

```bash
python phase3_pipeline.py --validate-only
```

Lệnh này đọc các file:

- `data/annotated/train.bio`
- `data/annotated/valid.bio`
- `data/annotated/test.bio`
- `data/annotated/triage_train.csv`
- `data/annotated/triage_valid.csv`
- `data/annotated/triage_test.csv`

Nếu valid/test đang trống với dữ liệu demo nhỏ thì vẫn validate được, nhưng trainer thật sẽ chặn để tránh huấn luyện sai.

## Train NER

```bash
python training/train_ner.py
```

Output:

```text
models/symptom_ner/
```

## Train triage classifier

```bash
python training/train_triage.py
```

Output:

```text
models/triage_classifier/
```

## Train cả hai task

```bash
python phase3_pipeline.py
```

## Lưu ý

- Mặc định dùng model `vinai/phobert-base`.
- Lần train đầu tiên cần mạng để tải model/tokenizer từ Hugging Face.
- Dữ liệu gán nhãn tự động ở Phase 2 chỉ là seed, cần review thủ công trước khi huấn luyện nghiêm túc.
- Với dữ liệu thật, cần có validation split khác 0 để tính F1/Recall.
- Nhóm `EMERGENCY` cần ưu tiên recall hơn accuracy tổng.
