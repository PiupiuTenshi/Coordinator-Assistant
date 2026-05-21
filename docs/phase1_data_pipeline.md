# Giai đoạn 1 - Thu thập và làm sạch dữ liệu

Phần code này tạo các đầu ra đúng theo đề cương:

- `data/raw/raw_articles.jsonl`
- `data/clean/clean_articles.jsonl`
- `data/dictionaries/symptom_dictionary.csv`
- `data/reports/phase1_quality_report.md`

## Cài thư viện

```bash
pip install -r requirements.txt
```

## Chạy với dữ liệu crawl thật

1. Thêm URL bài viết công khai vào `data/input/sample_urls.txt`.
2. Kiểm tra điều khoản sử dụng và robots.txt của nguồn dữ liệu.
3. Chạy pipeline:

```bash
python phase1_pipeline.py --urls data/input/sample_urls.txt
```

Crawler có:

- User-Agent rõ ràng trong `crawler/config.py`.
- Allowlist domain Vinmec.
- Kiểm tra `robots.txt`.
- Cache HTML ở `data/cache/html`.
- Rate limit mặc định 3 giây/request.

## Chạy demo offline

Khi chưa có URL thật, có thể dùng dữ liệu mẫu:

```bash
python phase1_pipeline.py --demo
```

## Mở rộng từ điển triệu chứng

Sửa file `data/dictionaries/symptom_seed.txt`, mỗi dòng một triệu chứng. Sau đó chạy lại:

```bash
python phase1_pipeline.py --skip-crawl
```

## Lưu ý an toàn

Pipeline chỉ phục vụ thu thập và chuẩn bị dữ liệu ban đầu. Không crawl dữ liệu cá nhân, không bypass đăng nhập/captcha/paywall, và cần review thủ công chất lượng nội dung trước khi dùng cho gán nhãn hoặc huấn luyện.
