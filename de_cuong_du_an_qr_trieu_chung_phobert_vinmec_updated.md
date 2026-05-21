# Đề cương dự án: Website QR nhận biết triệu chứng bằng PhoBERT từ dữ liệu y khoa Vinmec

> **Mục tiêu:** xây dựng hệ thống web đơn giản, phản hồi nhanh, cho phép bệnh nhân quét QR, điền triệu chứng, nhận gợi ý xử trí tạm thời, mức độ ưu tiên đi khám và bản đồ/hướng đi đến bệnh viện phù hợp.  
> **Lưu ý y khoa:** hệ thống chỉ hỗ trợ **sàng lọc ban đầu và hướng dẫn tạm thời**, không chẩn đoán bệnh, không thay thế bác sĩ, không kê đơn thuốc.

---

## 1. Bối cảnh và lý do chọn đề tài

Hiện nay quy trình y tế thường gặp các vấn đề như quá tải bệnh viện, thời gian chờ khám lâu, thủ tục phức tạp và trải nghiệm bệnh nhân chưa đồng đều. Vì vậy, cần một giải pháp lấy người bệnh làm trung tâm, ứng dụng AI, biểu mẫu số, phân luồng thông minh và bản đồ hướng dẫn để giảm tải bước tiếp nhận ban đầu.

Dự án này tập trung vào 4 ý chính:

1. **Thu thập tri thức y khoa công khai** từ các bài viết kiến thức y khoa, triệu chứng, bệnh thường gặp.
2. **Tạo dataset tiếng Việt** để huấn luyện PhoBERT nhận diện triệu chứng trong câu mô tả của bệnh nhân.
3. **Xây dựng website QR form** để người già, trẻ em, người ít rành công nghệ vẫn dễ nhập triệu chứng.
4. **Gợi ý xử trí tạm thời và điều hướng bệnh viện** dựa trên mức độ khẩn cấp và vị trí người dùng.

---

## 2. Phạm vi hệ thống

### 2.1. Hệ thống sẽ làm

- Cho bệnh nhân quét QR để mở website.
- Cho phép nhập triệu chứng bằng form đơn giản:
  - Triệu chứng chính.
  - Thời gian xuất hiện.
  - Mức độ đau/khó chịu.
  - Tuổi, giới tính, nhóm nguy cơ.
  - Triệu chứng nguy hiểm nếu có.
- Dùng mô hình NLP tiếng Việt để nhận diện triệu chứng.
- Gợi ý:
  - Chăm sóc tạm thời tại nhà.
  - Khi nào cần đi khám.
  - Khi nào cần cấp cứu ngay.
  - Nên đi khám **khoa nào**.
  - Nên gặp **bác sĩ chuyên môn nào** theo triệu chứng/nhu cầu.
- Phân biệt nhu cầu **khám lần đầu** và **tái khám**.
- Cho phép bệnh nhân chọn bác sĩ, chọn khung giờ khám theo yêu cầu.
- Hiển thị bệnh viện/phòng khám gần nhất.
- Mở hướng đi bằng Google Maps hoặc bản đồ tích hợp.
- Lưu log ẩn danh để cải thiện hệ thống.

### 2.2. Hệ thống không làm

- Không chẩn đoán bệnh chắc chắn.
- Không kê đơn thuốc.
- Không thay thế tư vấn bác sĩ.
- Không tự động xử lý dữ liệu cá nhân nếu chưa có sự đồng ý.
- Không cào dữ liệu nếu website nguồn không cho phép hoặc vi phạm điều khoản sử dụng.

---

## 3. Nguồn dữ liệu

### 3.1. Nguồn dữ liệu chính

Nguồn đề xuất:

- Vinmec - chuyên mục kiến thức y khoa.
- Các bài viết về:
  - Triệu chứng bệnh.
  - Nguyên nhân.
  - Khi nào cần đi khám.
  - Phương pháp xử trí ban đầu.
  - Khoa khám phù hợp.
- Dữ liệu bệnh viện:
  - Tên bệnh viện/phòng khám.
  - Địa chỉ.
  - Số điện thoại.
  - Giờ làm việc.
  - Tọa độ bản đồ.

### 3.2. Nguyên tắc thu thập dữ liệu

Trước khi crawl cần kiểm tra:

- `robots.txt`
- Điều khoản sử dụng website.
- Bản quyền nội dung.
- Chính sách bảo mật dữ liệu.
- Giới hạn tốc độ request.
- Chỉ lấy dữ liệu công khai.
- Ghi rõ URL nguồn cho từng mẫu dữ liệu.
- Không thu thập dữ liệu cá nhân của bệnh nhân từ Vinmec.

### 3.3. Cách crawl an toàn

Nguyên tắc kỹ thuật:

- Dùng `User-Agent` rõ ràng.
- Rate limit: 1 request / 2-5 giây.
- Có retry nhưng không spam.
- Lưu cache HTML để tránh request lặp.
- Chỉ crawl các URL thuộc danh sách cho phép.
- Không bypass captcha, login, paywall hoặc cơ chế chống bot.
- Có thể xin phép hoặc dùng dữ liệu mẫu thủ công nếu làm đồ án/học thuật.

---

## 4. Kiến trúc tổng thể

```text
[QR Code]
    |
    v
[Website Form nhập triệu chứng]
    |
    v
[Backend API]
    |
    +--> [PhoBERT Symptom NER Model]
    |
    +--> [Rule-based Triage Engine]
    |
    +--> [Specialty Recommendation Engine]
    |
    +--> [Doctor Matching & Appointment Service]
    |
    +--> [Knowledge Base từ dữ liệu y khoa]
    |
    +--> [Hospital Map Service]
    |
    v
[Kết quả cho bệnh nhân]
    |
    +--> Triệu chứng nhận diện
    +--> Mức độ ưu tiên
    +--> Gợi ý xử trí tạm thời
    +--> Gợi ý khoa khám
    +--> Gợi ý bác sĩ phù hợp
    +--> Chọn khám lần đầu hoặc tái khám
    +--> Đặt giờ bác sĩ theo yêu cầu
    +--> Bệnh viện gần nhất
    +--> Nút mở hướng đi
```

---

## 5. Thành phần dữ liệu

### 5.1. Raw article schema

```json
{
  "source": "vinmec",
  "url": "https://www.vinmec.com/...",
  "title": "Đau đầu là triệu chứng của bệnh gì?",
  "category": "Kiến thức y khoa",
  "specialty": "Thần kinh",
  "published_date": "YYYY-MM-DD",
  "updated_date": "YYYY-MM-DD",
  "content_raw": "...",
  "content_clean": "...",
  "symptom_candidates": ["đau đầu", "buồn nôn", "chóng mặt"],
  "red_flags": ["đau đầu dữ dội đột ngột", "yếu liệt tay chân"],
  "temporary_advice": ["nghỉ ngơi", "uống đủ nước", "theo dõi triệu chứng"],
  "when_to_see_doctor": "Nếu triệu chứng kéo dài hoặc nặng lên...",
  "hospital_department": "Khoa Thần kinh"
}
```

### 5.2. Dataset huấn luyện PhoBERT

Dự án nên dùng 2 loại dataset:

#### Loại 1: Token-level NER dataset

Dùng để nhận diện triệu chứng trong câu.

Ví dụ câu:

```text
Tôi bị đau đầu, sốt nhẹ và buồn nôn từ hôm qua.
```

Gán nhãn BIO:

```text
Tôi        O
bị         O
đau_đầu    B-SYMPTOM
,          O
sốt_nhẹ    B-SYMPTOM
và         O
buồn_nôn   B-SYMPTOM
từ         O
hôm_qua    B-DURATION
.          O
```

Nhãn đề xuất:

| Nhãn | Ý nghĩa |
|---|---|
| `B-SYMPTOM` | Bắt đầu một triệu chứng |
| `I-SYMPTOM` | Phần tiếp theo của triệu chứng |
| `B-BODY_PART` | Bộ phận cơ thể |
| `I-BODY_PART` | Phần tiếp theo của bộ phận |
| `B-DURATION` | Thời gian xuất hiện |
| `I-DURATION` | Phần tiếp theo của thời gian |
| `B-SEVERITY` | Mức độ nặng/nhẹ |
| `I-SEVERITY` | Phần tiếp theo của mức độ |
| `B-FREQUENCY` | Tần suất |
| `I-FREQUENCY` | Phần tiếp theo của tần suất |
| `B-RISK_FACTOR` | Yếu tố nguy cơ |
| `I-RISK_FACTOR` | Phần tiếp theo của yếu tố nguy cơ |
| `O` | Không thuộc nhóm cần nhận diện |

#### Loại 2: Sentence-level triage dataset

Dùng để phân loại mức độ cần xử trí.

```json
{
  "text": "Tôi bị đau ngực dữ dội, khó thở và vã mồ hôi.",
  "symptoms": ["đau ngực", "khó thở", "vã mồ hôi"],
  "triage_label": "EMERGENCY",
  "suggested_action": "Gọi cấp cứu hoặc đến cơ sở y tế gần nhất ngay."
}
```

Nhãn phân loại:

| Nhãn | Ý nghĩa |
|---|---|
| `SELF_CARE` | Có thể theo dõi và chăm sóc tạm thời |
| `BOOK_APPOINTMENT` | Nên đặt lịch khám |
| `URGENT_CARE` | Nên đi khám sớm trong ngày |
| `EMERGENCY` | Cần cấp cứu/nguy cơ cao |

---

## 6. Pipeline tạo dataset

### 6.1. Bước 1 - Crawl dữ liệu

```text
Input: Danh sách URL bài viết Vinmec
Output: raw_articles.jsonl
```

Trường cần lấy:

- URL
- Tiêu đề
- Chuyên mục
- Nội dung chính
- Ngày đăng/cập nhật nếu có
- Tác giả/chuyên môn nếu có
- Các đoạn có từ khóa triệu chứng

### 6.2. Bước 2 - Làm sạch dữ liệu

Loại bỏ:

- Menu
- Footer
- Quảng cáo
- Breadcrumb
- Nội dung trùng lặp
- Ký tự thừa
- Đoạn quá ngắn

Chuẩn hóa:

- Unicode tiếng Việt.
- Viết thường nếu cần.
- Chuẩn hóa dấu câu.
- Chuẩn hóa khoảng trắng.
- Tách câu.
- Tách từ tiếng Việt.

### 6.3. Bước 3 - Sinh ứng viên triệu chứng

Có thể kết hợp:

- Từ điển triệu chứng thủ công.
- Regex.
- Keyword matching.
- Embedding similarity.
- Annotation thủ công.

Ví dụ từ điển ban đầu:

```text
sốt
ho
đau đầu
đau bụng
khó thở
đau ngực
buồn nôn
nôn
tiêu chảy
chóng mặt
phát ban
mệt mỏi
mất ngủ
đau họng
sổ mũi
```

### 6.4. Bước 4 - Gán nhãn thủ công

Công cụ đề xuất:

- Label Studio.
- Doccano.
- Prodigy nếu có kinh phí.
- Google Sheet cho bản demo nhỏ.

Quy trình:

1. Sinh câu ứng viên từ bài viết.
2. Gợi ý nhãn tự động bằng từ điển.
3. Người gán nhãn kiểm tra.
4. Bác sĩ/sinh viên y khoa review mẫu nhạy cảm.
5. Xuất dataset BIO.

### 6.5. Bước 5 - Chia tập dữ liệu

Tỷ lệ đề xuất:

```text
Train: 70%
Validation: 15%
Test: 15%
```

Nguyên tắc chia:

- Không để cùng một bài viết xuất hiện ở cả train và test.
- Chia theo `article_id`, không chia ngẫu nhiên từng câu đơn lẻ.
- Đảm bảo mỗi nhãn có đủ mẫu.
- Test set nên có câu bệnh nhân tự viết, không chỉ câu từ bài y khoa.

---

## 7. Mô hình PhoBERT

### 7.1. Bài toán 1 - Nhận diện triệu chứng

Mô hình:

```text
PhoBERT + Token Classification Head
```

Input:

```text
Tôi bị đau đầu và buồn nôn từ sáng nay
```

Output:

```json
{
  "symptoms": ["đau đầu", "buồn nôn"],
  "duration": ["sáng nay"],
  "severity": [],
  "body_part": []
}
```

### 7.2. Bài toán 2 - Phân loại mức độ

Mô hình:

```text
PhoBERT + Sequence Classification Head
```

Input:

```text
Tôi bị đau ngực dữ dội và khó thở.
```

Output:

```json
{
  "triage_label": "EMERGENCY",
  "confidence": 0.94
}
```

### 7.3. Kết hợp AI và luật an toàn

Không nên chỉ dựa vào AI. Cần thêm rule-based engine để bắt các dấu hiệu nguy hiểm.

Ví dụ rule:

```python
RED_FLAGS = [
    ["đau ngực", "khó thở"],
    ["liệt", "méo miệng", "nói khó"],
    ["sốt cao", "co giật"],
    ["đau đầu dữ dội", "cứng gáy"],
    ["chảy máu nhiều"],
    ["bất tỉnh"],
    ["khó thở nặng"]
]
```

Nếu phát hiện red flag:

```text
Luôn ưu tiên EMERGENCY dù model dự đoán thấp hơn.
```

---

## 8. Crawler mẫu

> Chỉ dùng sau khi đã kiểm tra điều khoản sử dụng, robots.txt và phạm vi được phép.

```python
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "MedicalEducationResearchBot/1.0 contact: your_email@example.com"
}

def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    time.sleep(3)
    return response.text

def parse_article(url: str, html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1")
    title_text = title.get_text(" ", strip=True) if title else ""

    paragraphs = soup.find_all(["p", "li"])
    content = "\n".join(
        p.get_text(" ", strip=True)
        for p in paragraphs
        if len(p.get_text(" ", strip=True)) > 30
    )

    return {
        "url": url,
        "title": title_text,
        "content_raw": content
    }

def save_jsonl(records, path="raw_articles.jsonl"):
    with open(path, "w", encoding="utf-8") as f:
        for item in records:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    urls = [
        "https://www.vinmec.com/vie/..."
    ]

    records = []
    for url in urls:
        html = fetch_html(url)
        article = parse_article(url, html)
        records.append(article)

    save_jsonl(records)
```

---

## 9. Tiền xử lý tiếng Việt cho PhoBERT

PhoBERT thường cần văn bản tiếng Việt đã được tách từ.

Ví dụ:

```text
Tôi bị đau đầu và buồn nôn.
```

Sau tách từ:

```text
Tôi bị đau_đầu và buồn_nôn .
```

Pipeline:

```text
Raw text
  -> Normalize Unicode
  -> Sentence segmentation
  -> Vietnamese word segmentation
  -> BIO alignment
  -> PhoBERT tokenizer
  -> Train model
```

Thư viện có thể dùng:

- `underthesea`
- `pyvi`
- `VnCoreNLP`
- `transformers`
- `datasets`
- `seqeval`
- `scikit-learn`

---

## 10. Backend API

### 10.1. Công nghệ đề xuất

| Thành phần | Công nghệ |
|---|---|
| API | FastAPI |
| Model serving | PyTorch + Transformers |
| Database | PostgreSQL |
| Cache | Redis |
| Search kiến thức | Elasticsearch hoặc PostgreSQL full-text |
| Map | Google Maps API hoặc OpenStreetMap |
| Deploy | Docker + Nginx |

### 10.2. API endpoints

```text
POST /api/symptom/analyze
GET  /api/specialties/recommend
GET  /api/doctors/recommend
GET  /api/doctors/{id}/available-slots
POST /api/appointments/book
GET  /api/appointments/{id}
POST /api/appointments/{id}/cancel
POST /api/appointments/{id}/reschedule
GET  /api/hospitals/nearby
GET  /api/hospitals/{id}/directions
POST /api/feedback
GET  /api/health
```

### 10.3. Request mẫu

```json
{
  "age": 45,
  "gender": "male",
  "symptom_text": "Tôi bị đau ngực, khó thở và vã mồ hôi từ 30 phút trước.",
  "duration": "30 phút",
  "location": {
    "lat": 10.7769,
    "lng": 106.7009
  }
}
```

### 10.4. Response mẫu

```json
{
  "recognized_symptoms": ["đau ngực", "khó thở", "vã mồ hôi"],
  "triage_label": "EMERGENCY",
  "risk_level": "high",
  "message": "Triệu chứng có dấu hiệu nguy hiểm. Vui lòng gọi cấp cứu hoặc đến cơ sở y tế gần nhất ngay.",
  "temporary_advice": [
    "Ngừng vận động mạnh.",
    "Ngồi hoặc nằm ở tư thế dễ thở.",
    "Không tự lái xe nếu đang khó thở hoặc đau ngực nặng.",
    "Gọi người thân hoặc cấp cứu hỗ trợ."
  ],
  "nearest_hospitals": [
    {
      "name": "Vinmec Central Park",
      "address": "720A Điện Biên Phủ, TP. Hồ Chí Minh",
      "distance_km": 4.2,
      "phone": "028 3622 1166",
      "map_url": "https://www.google.com/maps/dir/?api=1&destination=..."
    }
  ],
  "disclaimer": "Thông tin chỉ mang tính tham khảo, không thay thế chẩn đoán và điều trị của bác sĩ."
}
```

---

## 11. Frontend QR form

### 11.1. Mục tiêu giao diện

Giao diện phải phù hợp cho mọi lứa tuổi:

- Chữ lớn.
- Ít bước.
- Nút bấm rõ.
- Có biểu tượng minh họa.
- Có màu cảnh báo dễ hiểu.
- Có nút gọi cấp cứu.
- Có thể dùng trên điện thoại cấu hình thấp.
- Phản hồi dưới 2 giây với cache/model tối ưu.

### 11.2. Luồng người dùng

```text
Bước 1: Quét QR
Bước 2: Mở form
Bước 3: Chọn/ngõ triệu chứng
Bước 4: Nhấn "Kiểm tra nhanh"
Bước 5: Xem kết quả
Bước 6: Mở bản đồ hoặc gọi bệnh viện
```

### 11.3. Form đề xuất

Trường bắt buộc:

- Loại nhu cầu: **Khám lần đầu** hoặc **Tái khám**.
- Triệu chứng chính.
- Thời gian xuất hiện.
- Mức độ khó chịu: 1-10.
- Tuổi.
- Khoa mong muốn nếu người bệnh đã biết.
- Bác sĩ mong muốn nếu người bệnh đã biết.
- Khung giờ mong muốn.
- Vị trí hiện tại hoặc chọn bệnh viện gần nhất.

Trường tùy chọn:

- Bệnh nền.
- Dị ứng thuốc.
- Đang mang thai.
- Đã dùng thuốc gì.
- Triệu chứng đi kèm.
- Mã bệnh nhân nếu tái khám.
- Bác sĩ đã khám trước đó nếu tái khám.
- Hồ sơ/kết quả xét nghiệm cũ nếu cần tải lên.
- Nhu cầu hỗ trợ đặc biệt: xe lăn, người cao tuổi, trẻ em, phiên dịch.

### 11.4. Màu hiển thị mức độ

| Mức | Màu | Ý nghĩa |
|---|---|---|
| Xanh | Nhẹ | Có thể theo dõi |
| Vàng | Trung bình | Nên đặt lịch khám |
| Cam | Cần chú ý | Nên đi khám sớm |
| Đỏ | Nguy hiểm | Cần cấp cứu |

---

## 12. Bản đồ bệnh viện và hướng đi

### 12.1. Dữ liệu bệnh viện

```json
{
  "id": "vinmec-central-park",
  "name": "Vinmec Central Park",
  "address": "720A Điện Biên Phủ, Phường Thạnh Mỹ Tây, TP. Hồ Chí Minh",
  "phone": "028 3622 1166",
  "lat": 10.7941,
  "lng": 106.7218,
  "emergency": true,
  "working_hours": "07:30-17:00"
}
```

### 12.2. Tính bệnh viện gần nhất

Công thức Haversine:

```python
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)

    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
```

### 12.3. Link mở Google Maps

```text
https://www.google.com/maps/dir/?api=1&destination={lat},{lng}
```

---

## 13. Module gợi ý khoa khám, bác sĩ và đặt lịch

Module này giúp hệ thống chuyển từ mức “tư vấn triệu chứng” sang “điều phối khám thông minh”, giúp bệnh nhân biết nên đi khoa nào, gặp bác sĩ nào và đặt lịch theo nhu cầu.

### 13.1. Gợi ý nên đi khoa nào

Sau khi PhoBERT nhận diện triệu chứng, hệ thống ánh xạ triệu chứng sang chuyên khoa phù hợp.

Ví dụ:

| Triệu chứng chính | Khoa gợi ý | Mức ưu tiên |
|---|---|---|
| Đau ngực, khó thở, vã mồ hôi | Cấp cứu / Tim mạch | Rất cao |
| Đau đầu kéo dài, chóng mặt, tê yếu tay chân | Thần kinh | Cao |
| Ho, sốt, đau họng, khó thở nhẹ | Hô hấp / Tai Mũi Họng | Trung bình |
| Đau bụng, buồn nôn, tiêu chảy | Tiêu hóa | Trung bình |
| Phát ban, ngứa, nổi mề đay | Da liễu | Trung bình |
| Đau khớp, đau lưng, hạn chế vận động | Cơ xương khớp | Trung bình |
| Trẻ sốt cao, bỏ bú, co giật | Nhi khoa / Cấp cứu | Rất cao |
| Phụ nữ mang thai đau bụng, ra máu | Sản phụ khoa / Cấp cứu | Rất cao |

Cách xử lý:

```text
Triệu chứng người dùng
    -> PhoBERT NER nhận diện triệu chứng
    -> Rule kiểm tra dấu hiệu nguy hiểm
    -> Specialty Recommendation Engine
    -> Gợi ý khoa khám phù hợp
```

Schema đề xuất:

```json
{
  "symptom": "đau ngực",
  "specialty_candidates": [
    {
      "specialty": "Tim mạch",
      "priority": 0.92,
      "reason": "Đau ngực có thể liên quan đến bệnh lý tim mạch."
    },
    {
      "specialty": "Cấp cứu",
      "priority": 0.98,
      "reason": "Đau ngực kèm khó thở là dấu hiệu nguy hiểm."
    }
  ]
}
```

### 13.2. Gợi ý bác sĩ chuyên môn theo nhu cầu

Sau khi xác định chuyên khoa, hệ thống đề xuất bác sĩ dựa trên:

- Chuyên khoa phù hợp.
- Triệu chứng hoặc nhóm bệnh nghi ngờ.
- Độ tuổi bệnh nhân.
- Nhu cầu khám:
  - Khám tổng quát.
  - Khám chuyên sâu.
  - Khám trẻ em.
  - Khám người cao tuổi.
  - Khám thai/sản phụ khoa.
  - Tư vấn sau điều trị.
- Vị trí bệnh nhân.
- Lịch trống của bác sĩ.
- Ngôn ngữ hỗ trợ nếu cần.
- Hình thức khám:
  - Khám trực tiếp.
  - Tư vấn từ xa.
  - Tái khám.

Ví dụ dữ liệu bác sĩ:

```json
{
  "doctor_id": "bs-nguyen-van-a",
  "full_name": "BS. Nguyễn Văn A",
  "degree": "Thạc sĩ, Bác sĩ",
  "specialty": "Tim mạch",
  "sub_specialties": ["đau ngực", "tăng huyết áp", "rối loạn nhịp tim"],
  "hospital_id": "vinmec-central-park",
  "experience_years": 12,
  "consultation_types": ["first_visit", "follow_up", "telemedicine"],
  "available_slots": [
    "2026-05-22T08:00:00+07:00",
    "2026-05-22T09:30:00+07:00"
  ],
  "rating": 4.8
}
```

Response gợi ý bác sĩ:

```json
{
  "recommended_specialty": "Tim mạch",
  "recommended_doctors": [
    {
      "doctor_name": "BS. Nguyễn Văn A",
      "specialty": "Tim mạch",
      "reason": "Phù hợp với triệu chứng đau ngực và khó thở.",
      "next_available_slot": "2026-05-22T08:00:00+07:00",
      "hospital_name": "Vinmec Central Park"
    }
  ]
}
```

### 13.3. Đặt giờ bác sĩ theo yêu cầu

Người bệnh có thể chọn:

- Bác sĩ mong muốn.
- Ngày khám.
- Buổi khám:
  - Sáng.
  - Chiều.
  - Tối nếu bệnh viện hỗ trợ.
- Hình thức:
  - Khám trực tiếp.
  - Tư vấn online.
- Loại lịch:
  - Khám lần đầu.
  - Tái khám.
- Cơ sở khám.
- Nhu cầu đặc biệt:
  - Người cao tuổi cần hỗ trợ.
  - Trẻ em.
  - Người khuyết tật.
  - Cần xe lăn.
  - Cần phiên dịch/người hỗ trợ.

Luồng đặt lịch:

```text
Bước 1: Người bệnh nhập triệu chứng
Bước 2: Hệ thống gợi ý khoa khám
Bước 3: Hệ thống hiển thị danh sách bác sĩ phù hợp
Bước 4: Người bệnh chọn bác sĩ hoặc chọn "bác sĩ sớm nhất"
Bước 5: Người bệnh chọn khám lần đầu/tái khám
Bước 6: Người bệnh chọn khung giờ
Bước 7: Xác nhận thông tin
Bước 8: Nhận mã lịch hẹn/QR lịch khám
```

API đề xuất:

```text
GET  /api/specialties/recommend
GET  /api/doctors/recommend
GET  /api/doctors/{id}/available-slots
POST /api/appointments/book
GET  /api/appointments/{id}
POST /api/appointments/{id}/cancel
POST /api/appointments/{id}/reschedule
```

Request đặt lịch mẫu:

```json
{
  "patient_type": "first_visit",
  "doctor_id": "bs-nguyen-van-a",
  "specialty": "Tim mạch",
  "hospital_id": "vinmec-central-park",
  "appointment_time": "2026-05-22T08:00:00+07:00",
  "symptom_summary": "Đau ngực và khó thở từ 30 phút trước.",
  "contact_phone": "Ẩn hoặc mã hóa nếu lưu",
  "need_support": ["wheelchair_support"]
}
```

Response đặt lịch mẫu:

```json
{
  "appointment_id": "APT-20260522-0001",
  "status": "pending_confirmation",
  "message": "Lịch hẹn đang chờ xác nhận từ bệnh viện.",
  "qr_checkin_url": "https://example.com/checkin/APT-20260522-0001",
  "doctor_name": "BS. Nguyễn Văn A",
  "specialty": "Tim mạch",
  "appointment_time": "2026-05-22T08:00:00+07:00",
  "hospital_address": "720A Điện Biên Phủ, TP. Hồ Chí Minh"
}
```

### 13.4. Phân chia khám lần đầu và tái khám

Hệ thống cần hỏi bệnh nhân ngay từ đầu:

```text
Bạn muốn đăng ký:
[ ] Khám lần đầu
[ ] Tái khám
```

#### Khám lần đầu

Dành cho người bệnh:

- Chưa từng khám vấn đề này.
- Chưa có hồ sơ tại bệnh viện.
- Có triệu chứng mới xuất hiện.
- Chưa biết nên khám khoa nào.

Form nên hỏi:

- Triệu chứng chính.
- Thời gian xuất hiện.
- Mức độ nặng.
- Tuổi/giới tính.
- Bệnh nền quan trọng.
- Thuốc đang dùng nếu có.
- Vị trí hiện tại.

Kết quả ưu tiên:

- Gợi ý khoa khám.
- Gợi ý bác sĩ phù hợp.
- Gợi ý bệnh viện gần nhất.
- Chọn khung giờ khám.
- Nhắc mang giấy tờ cần thiết.

#### Tái khám

Dành cho người bệnh:

- Đã từng khám cùng vấn đề.
- Có lịch hẹn tái khám.
- Cần xem lại kết quả xét nghiệm.
- Cần theo dõi sau điều trị.
- Cần gặp lại đúng bác sĩ cũ.

Form nên hỏi:

- Mã bệnh nhân hoặc số điện thoại đã đăng ký.
- Chuyên khoa đã khám.
- Bác sĩ đã khám trước đó nếu nhớ.
- Ngày khám gần nhất.
- Lý do tái khám:
  - Theo lịch hẹn.
  - Triệu chứng nặng hơn.
  - Có tác dụng phụ.
  - Cần đọc kết quả xét nghiệm.
  - Cần đổi thuốc/tư vấn tiếp.
- Có kết quả xét nghiệm/hồ sơ cần tải lên không.

Kết quả ưu tiên:

- Gợi ý gặp lại bác sĩ cũ nếu còn lịch.
- Nếu bác sĩ cũ không có lịch, gợi ý bác sĩ cùng chuyên khoa.
- Cho phép chọn lại giờ khám.
- Cho phép tải lên kết quả xét nghiệm.
- Nhắc mang toa thuốc/cận lâm sàng cũ.

### 13.5. Logic điều phối khám lần đầu/tái khám

```text
Nếu patient_type = first_visit:
    Ưu tiên xác định triệu chứng -> chuyên khoa -> bác sĩ phù hợp -> lịch trống

Nếu patient_type = follow_up:
    Ưu tiên tìm hồ sơ/lịch sử khám -> bác sĩ cũ -> chuyên khoa cũ -> lịch tái khám

Nếu có red flag:
    Bỏ qua đặt lịch thông thường
    Hiển thị cảnh báo cấp cứu
    Gợi ý cơ sở có cấp cứu gần nhất
```

### 13.6. Bổ sung dữ liệu cần lưu

Bảng `specialties`:

```sql
CREATE TABLE specialties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    emergency_supported BOOLEAN DEFAULT FALSE
);
```

Bảng `doctors`:

```sql
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    degree VARCHAR(255),
    specialty_id INT REFERENCES specialties(id),
    hospital_id INT,
    experience_years INT,
    bio TEXT,
    is_active BOOLEAN DEFAULT TRUE
);
```

Bảng `doctor_slots`:

```sql
CREATE TABLE doctor_slots (
    id SERIAL PRIMARY KEY,
    doctor_id INT REFERENCES doctors(id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'available'
);
```

Bảng `appointments`:

```sql
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    appointment_code VARCHAR(50) UNIQUE NOT NULL,
    patient_type VARCHAR(50) NOT NULL,
    doctor_id INT REFERENCES doctors(id),
    specialty_id INT REFERENCES specialties(id),
    hospital_id INT,
    appointment_time TIMESTAMP NOT NULL,
    symptom_summary TEXT,
    status VARCHAR(50) DEFAULT 'pending_confirmation',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 13.7. Giao diện bổ sung

Trang kết quả nên hiển thị theo thứ tự dễ hiểu:

```text
1. Mức độ cần xử trí
2. Triệu chứng hệ thống nhận diện
3. Khoa khám gợi ý
4. Bác sĩ phù hợp
5. Chọn khám lần đầu hoặc tái khám
6. Chọn ngày giờ khám
7. Bệnh viện gần nhất và hướng đi
8. Lưu ý chuẩn bị trước khi đi khám
```

Thiết kế cho người lớn tuổi/trẻ em:

- Nút “Khám lần đầu” và “Tái khám” thật lớn.
- Có biểu tượng minh họa:
  - Ống nghe: khám lần đầu.
  - Lịch sử: tái khám.
  - Bản đồ: chỉ đường.
  - Điện thoại: gọi bệnh viện.
- Có nút “Tôi không biết chọn khoa nào” để hệ thống tự gợi ý.
- Có lựa chọn “Bác sĩ sớm nhất” nếu bệnh nhân không biết chọn bác sĩ.
- Có lựa chọn “Bệnh viện gần nhất có cấp cứu”.

### 13.8. Quy tắc an toàn khi gợi ý bác sĩ/lịch khám

- Nếu triệu chứng nguy hiểm, không ưu tiên đặt lịch thường; phải khuyến nghị cấp cứu.
- Không cam kết bác sĩ chắc chắn phù hợp 100%.
- Không hiển thị thông tin bác sĩ nếu chưa được phép công khai.
- Không tự động đặt lịch nếu bệnh viện chưa xác nhận.
- Không lưu thông tin định danh bệnh nhân nếu chưa có đồng ý.
- Tái khám cần xác thực người bệnh trước khi truy xuất hồ sơ cũ.
- Nếu bệnh nhân là trẻ em, phụ nữ mang thai, người cao tuổi hoặc có bệnh nền nặng, tăng mức ưu tiên cảnh báo.

---

## 14. Tối ưu tốc độ phản hồi

Mục tiêu:

```text
Thời gian phản hồi API: < 2 giây
Thời gian tải trang lần đầu: < 3 giây trên 4G
```

Giải pháp:

- Dùng model `vinai/phobert-base` thay vì large cho bản MVP.
- Quantization model nếu cần.
- Cache kết quả triệu chứng phổ biến.
- Tách service AI riêng.
- Dùng Redis cache.
- Tải map sau khi có kết quả, không tải ngay từ đầu.
- Lazy loading frontend.
- Dùng CDN cho static assets.
- Nén JSON response.
- Giới hạn độ dài input triệu chứng.

---

## 15. Bảo mật và dữ liệu cá nhân

### 15.1. Nguyên tắc

- Chỉ thu thập dữ liệu thật sự cần thiết.
- Có checkbox đồng ý xử lý dữ liệu.
- Không lưu tên/số điện thoại nếu không bắt buộc.
- Mã hóa dữ liệu nhạy cảm.
- Ẩn danh log huấn luyện.
- Cho phép người dùng xóa dữ liệu.
- Không dùng dữ liệu bệnh nhân để train nếu chưa có đồng ý rõ ràng.

### 15.2. Dữ liệu nên lưu

```json
{
  "session_id": "anonymous_uuid",
  "symptom_text_hash": "...",
  "recognized_symptoms": ["sốt", "ho"],
  "triage_label": "BOOK_APPOINTMENT",
  "timestamp": "2026-05-21T10:00:00+07:00",
  "feedback": "useful"
}
```

### 15.3. Dữ liệu không nên lưu ở MVP

- Họ tên.
- Số CCCD.
- Số bảo hiểm y tế.
- Địa chỉ nhà chi tiết.
- Hồ sơ bệnh án đầy đủ.
- Ảnh giấy tờ.
- File xét nghiệm cá nhân.

---

## 16. Đánh giá mô hình

### 16.1. Với NER triệu chứng

Metric:

- Precision.
- Recall.
- F1-score.
- Entity-level F1.

Mục tiêu MVP:

```text
F1 >= 0.80 trên test set nội bộ
```

### 16.2. Với phân loại mức độ

Metric:

- Accuracy.
- Macro F1.
- Recall cho nhóm EMERGENCY.
- Confusion matrix.

Ưu tiên:

```text
Không bỏ sót ca nguy hiểm.
Recall của EMERGENCY quan trọng hơn accuracy tổng.
```

---

## 17. Kế hoạch triển khai theo giai đoạn

## Giai đoạn 0 - Khảo sát và xác định phạm vi

Thời gian đề xuất: 1 tuần

Công việc:

- Xác định chuyên khoa ưu tiên:
  - Hô hấp.
  - Tiêu hóa.
  - Tim mạch.
  - Thần kinh.
  - Nhi khoa.
- Liệt kê 50-100 triệu chứng phổ biến.
- Kiểm tra pháp lý nguồn dữ liệu.
- Xác định bệnh viện/phòng khám hiển thị trên bản đồ.
- Viết tài liệu yêu cầu hệ thống.

Kết quả:

- Danh sách triệu chứng.
- Danh sách nguồn dữ liệu.
- Tài liệu phạm vi MVP.
- Checklist pháp lý/bảo mật.

---

## Giai đoạn 1 - Thu thập và làm sạch dữ liệu

Thời gian đề xuất: 2-3 tuần

Công việc:

- Crawl thử 100-300 bài viết công khai.
- Làm sạch HTML.
- Tách đoạn, tách câu.
- Gắn URL nguồn.
- Loại bỏ dữ liệu trùng.
- Tạo từ điển triệu chứng ban đầu.

Kết quả:

- `raw_articles.jsonl`
- `clean_articles.jsonl`
- `symptom_dictionary.csv`
- Báo cáo chất lượng dữ liệu.

---

## Giai đoạn 2 - Gán nhãn dataset

Thời gian đề xuất: 3-4 tuần

Công việc:

- Chọn 3.000-10.000 câu y khoa.
- Gán nhãn BIO cho triệu chứng.
- Gán nhãn phân loại mức độ.
- Review bởi người có kiến thức y khoa.
- Chia train/validation/test.

Kết quả:

- `train.bio`
- `valid.bio`
- `test.bio`
- `triage_train.csv`
- `triage_valid.csv`
- `triage_test.csv`
- Annotation guideline.

---

## Giai đoạn 3 - Huấn luyện PhoBERT

Thời gian đề xuất: 2-3 tuần

Công việc:

- Fine-tune PhoBERT cho NER.
- Fine-tune PhoBERT cho triage classification.
- Đánh giá F1, Recall, confusion matrix.
- Test với câu bệnh nhân tự nhập.
- Xuất model phục vụ backend.

Kết quả:

- `symptom_ner_phobert.pt`
- `triage_classifier_phobert.pt`
- Báo cáo đánh giá model.
- Demo notebook.

---

## Giai đoạn 4 - Xây dựng backend

Thời gian đề xuất: 2 tuần

Công việc:

- Xây API FastAPI.
- Tích hợp model PhoBERT.
- Xây triage rule engine.
- Tạo API bệnh viện gần nhất.
- Tích hợp cache Redis.
- Viết test API.

Kết quả:

- Backend chạy bằng Docker.
- Swagger API docs.
- API nhận diện triệu chứng.
- API gợi ý bệnh viện.

---

## Giai đoạn 5 - Xây dựng frontend QR form

Thời gian đề xuất: 2 tuần

Công việc:

- Thiết kế giao diện đơn giản.
- Tạo form nhập triệu chứng.
- Hiển thị kết quả bằng màu cảnh báo.
- Thêm nút gọi bệnh viện.
- Thêm nút mở bản đồ.
- Tối ưu mobile.

Kết quả:

- Website responsive.
- QR code dẫn vào website.
- Giao diện thân thiện cho người già/trẻ em.

---

## Giai đoạn 6 - Tích hợp bản đồ và hướng đi

Thời gian đề xuất: 1-2 tuần

Công việc:

- Lưu danh sách bệnh viện.
- Tính khoảng cách.
- Tích hợp Google Maps hoặc OpenStreetMap.
- Hiển thị tuyến đường.
- Ưu tiên bệnh viện có cấp cứu 24/7 khi nguy hiểm.

Kết quả:

- Map hiển thị bệnh viện.
- Nút chỉ đường.
- Gợi ý bệnh viện phù hợp.

---

## Giai đoạn 7 - Kiểm thử an toàn y khoa

Thời gian đề xuất: 2-3 tuần

Công việc:

- Tạo bộ test tình huống nguy hiểm.
- Test các ca red flag:
  - Đau ngực + khó thở.
  - Liệt nửa người.
  - Co giật.
  - Bất tỉnh.
  - Chảy máu nhiều.
  - Sốt cao ở trẻ nhỏ.
- Review nội dung khuyến nghị.
- Kiểm thử bảo mật dữ liệu.
- Kiểm thử tải hệ thống.

Kết quả:

- Báo cáo an toàn.
- Báo cáo bảo mật.
- Danh sách lỗi và cách sửa.
- Phiên bản beta.

---

## Giai đoạn 8 - Triển khai MVP

Thời gian đề xuất: 1-2 tuần

Công việc:

- Deploy backend.
- Deploy frontend.
- Gắn domain.
- Tạo QR code.
- Theo dõi log lỗi.
- Thu feedback người dùng.
- Cập nhật dataset/model định kỳ.

Kết quả:

- MVP hoạt động.
- QR code dùng được.
- Dashboard theo dõi.
- Kế hoạch cải tiến phiên bản 2.

---

## 18. Cấu trúc thư mục dự án

```text
medical-symptom-qr-ai/
├── data/
│   ├── raw/
│   ├── clean/
│   ├── annotated/
│   └── dictionaries/
├── crawler/
│   ├── crawl_vinmec.py
│   ├── parse_article.py
│   └── robots_check.py
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_annotation_analysis.ipynb
│   └── 03_model_training.ipynb
├── models/
│   ├── symptom_ner/
│   └── triage_classifier/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── services/
│   │   │   ├── symptom_service.py
│   │   │   ├── specialty_service.py
│   │   │   ├── doctor_service.py
│   │   │   └── appointment_service.py
│   │   ├── models/
│   │   └── rules/
│   ├── tests/
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/
│   ├── annotation_guideline.md
│   ├── api_spec.md
│   └── safety_policy.md
└── README.md
```

---

## 19. Nhân sự đề xuất

| Vai trò | Nhiệm vụ |
|---|---|
| Project Manager | Quản lý tiến độ, phạm vi |
| Data Engineer | Crawl, làm sạch, lưu dữ liệu |
| NLP Engineer | Huấn luyện PhoBERT |
| Backend Developer | API, model serving, database |
| Frontend Developer | QR form, giao diện, map |
| Medical Reviewer | Kiểm tra nội dung y khoa |
| QA Tester | Test chức năng, test an toàn |

---

## 20. Rủi ro và cách giảm thiểu

| Rủi ro | Ảnh hưởng | Giải pháp |
|---|---|---|
| Dữ liệu crawl vi phạm điều khoản | Cao | Kiểm tra quyền sử dụng, xin phép, giới hạn crawl |
| Nội dung y khoa sai/nguy hiểm | Rất cao | Medical reviewer, disclaimer, rule red flag |
| Model bỏ sót ca nguy hiểm | Rất cao | Ưu tiên recall, rule engine, test case khẩn cấp |
| Giao diện khó dùng với người lớn tuổi | Trung bình | Font lớn, ít bước, nút rõ |
| Phản hồi chậm | Trung bình | Cache, model base, tối ưu backend |
| Lộ dữ liệu cá nhân | Rất cao | Ẩn danh, mã hóa, tối thiểu hóa dữ liệu |
| Dataset thiếu cân bằng | Trung bình | Bổ sung mẫu hiếm, phân tích phân phối nhãn |

---

## 21. MVP đề xuất

Phiên bản MVP nên làm nhỏ nhưng hoàn chỉnh:

### Chuyên khoa MVP

- Hô hấp.
- Tiêu hóa.
- Tim mạch.
- Thần kinh.

### Tính năng MVP

- QR mở website.
- Form nhập triệu chứng.
- Phân chia **khám lần đầu** và **tái khám**.
- Nhận diện triệu chứng bằng PhoBERT.
- Rule phát hiện dấu hiệu nguy hiểm.
- Gợi ý xử trí tạm thời.
- Gợi ý khoa khám phù hợp.
- Gợi ý bác sĩ chuyên môn theo nhu cầu.
- Đặt giờ bác sĩ theo yêu cầu.
- Hiển thị 3 bệnh viện gần nhất.
- Nút mở Google Maps.
- Gửi feedback.

### Dataset MVP

- 100-300 bài viết y khoa công khai.
- 3.000-5.000 câu đã gán nhãn.
- 50-100 triệu chứng phổ biến.
- 4 nhãn triage.

---

## 22. README mẫu cho GitHub

```md
# Medical Symptom QR AI

Website QR hỗ trợ bệnh nhân nhập triệu chứng, nhận diện triệu chứng bằng PhoBERT, gợi ý xử trí tạm thời và hiển thị bản đồ bệnh viện gần nhất.

## Features

- QR symptom form
- Vietnamese symptom NER using PhoBERT
- Triage classification
- Red flag rule engine
- Specialty recommendation
- Doctor recommendation
- First visit / follow-up appointment flow
- Doctor time-slot booking
- Hospital map and directions
- Fast mobile-first UI

## Disclaimer

This system is for educational and triage support only. It does not provide medical diagnosis, prescription, or replacement for professional medical advice.

## Tech Stack

- PhoBERT
- FastAPI
- PostgreSQL
- Redis
- React / Next.js
- Google Maps API or OpenStreetMap
- Docker

## Main Phases

1. Data collection
2. Data cleaning
3. Annotation
4. PhoBERT training
5. Backend API
6. Frontend QR form
7. Map integration
8. Medical safety testing
9. MVP deployment
```

---

## 23. Checklist hoàn thành

### Dữ liệu

- [ ] Có danh sách URL nguồn hợp lệ.
- [ ] Có kiểm tra điều khoản/robots.
- [ ] Có raw dataset.
- [ ] Có clean dataset.
- [ ] Có annotation guideline.
- [ ] Có train/validation/test.

### AI

- [ ] Huấn luyện NER PhoBERT.
- [ ] Huấn luyện triage classifier.
- [ ] Có báo cáo F1.
- [ ] Có kiểm thử red flag.
- [ ] Có fallback rule engine.

### Backend

- [ ] API phân tích triệu chứng.
- [ ] API gợi ý khoa khám.
- [ ] API gợi ý bác sĩ.
- [ ] API lịch trống bác sĩ.
- [ ] API đặt lịch khám.
- [ ] API phân biệt khám lần đầu/tái khám.
- [ ] API bệnh viện gần nhất.
- [ ] API feedback.
- [ ] Có cache.
- [ ] Có Docker.

### Frontend

- [ ] QR mở website.
- [ ] Form dễ dùng.
- [ ] Có lựa chọn khám lần đầu/tái khám.
- [ ] Có gợi ý khoa khám.
- [ ] Có gợi ý bác sĩ phù hợp.
- [ ] Có chọn khung giờ khám.
- [ ] Kết quả rõ ràng.
- [ ] Có màu cảnh báo.
- [ ] Có bản đồ.
- [ ] Có nút gọi/mở chỉ đường.

### An toàn

- [ ] Có disclaimer.
- [ ] Có đồng ý xử lý dữ liệu.
- [ ] Không lưu dữ liệu nhạy cảm không cần thiết.
- [ ] Có mã hóa dữ liệu.
- [ ] Có review y khoa.

---

## 24. Tài liệu tham khảo nên đọc

- Vinmec - trang liên hệ và danh sách cơ sở bệnh viện/phòng khám.
- Vinmec - chính sách bảo vệ dữ liệu cá nhân.
- PhoBERT paper: *PhoBERT: Pre-trained language models for Vietnamese*.
- VinAIResearch/PhoBERT GitHub.
- Google Maps Platform documentation.
- Google Maps Directions API documentation.

---

## 25. Kết luận

Dự án có tính ứng dụng cao vì kết hợp:

- AI tiếng Việt.
- Dữ liệu y khoa.
- QR form dễ dùng.
- Phân luồng bệnh nhân.
- Bản đồ bệnh viện.
- Tối ưu trải nghiệm người bệnh.

Tuy nhiên, vì đây là lĩnh vực y tế, hệ thống cần đặt **an toàn bệnh nhân, bảo mật dữ liệu và tính pháp lý** lên hàng đầu. Phiên bản đầu tiên nên tập trung vào hỗ trợ sàng lọc, phát hiện dấu hiệu nguy hiểm và điều hướng người bệnh đến cơ sở y tế phù hợp, thay vì cố gắng chẩn đoán bệnh.

---

## 26. Cập nhật triển khai theo yêu cầu mới

### 26.1. Bản đồ nội viện thay cho chỉ đường ngoài Google Maps

Luồng bản đồ MVP được điều chỉnh như sau:

```text
Triệu chứng người dùng
  -> Gợi ý chuyên khoa
  -> Chọn bệnh viện phù hợp/gần nhất
  -> Hiển thị sơ đồ nội viện của bệnh viện
  -> Chỉ đường từ cổng/sảnh chính đến khoa được gợi ý
```

Backend cần trả thêm `department_route` cho mỗi bệnh viện:

```json
{
  "department": "Khoa Tim mạch",
  "building": "Tòa A",
  "floor": "Tầng 2",
  "room": "A-205",
  "estimated_walk_minutes": 4,
  "map_points": [[10, 82], [28, 82], [54, 56], [78, 34]],
  "steps": [
    "Vào cổng chính",
    "Đi thẳng tới sảnh A",
    "Rẽ phải tới thang máy",
    "Lên tầng 2",
    "Đi theo biển Khoa Tim mạch đến phòng A-205"
  ]
}
```

Frontend hiển thị sơ đồ nội viện ngay trong trang kết quả. Nút chính là **Chỉ đường tới khoa**, không phụ thuộc vào Google Maps. Link ngoài chỉ là tùy chọn phụ nếu cần định vị bệnh viện từ xa.

### 26.2. QR hiển thị trực tiếp trên frontend

Frontend cần có khu vực **Hiển thị QR mở form** ở đầu trang để người triển khai thấy và in QR. QR được tạo bằng script:

```bash
python scripts/generate_qr.py --url https://your-frontend-domain.example --output frontend/public/qr-mvp.svg
```

Khi chạy local, QR có thể trỏ tới:

```text
http://127.0.0.1:5173
```

Khi deploy thật, phải tạo lại QR theo domain public của frontend.

### 26.3. Deploy miễn phí cho MVP demo

Khuyến nghị dùng Render cho bản demo vì có thể deploy cả backend FastAPI và frontend static:

1. Đẩy source lên GitHub.
2. Tạo Render Web Service cho backend.
3. Build command:
   ```bash
   pip install -r requirements-backend.txt
   ```
4. Start command:
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
   ```
5. Tạo Render Static Site cho thư mục `frontend`.
6. Cập nhật `apiBase` của frontend sang URL backend public.
7. Tạo lại QR bằng URL frontend public.

Lưu ý: free server có thể sleep/cold start, chỉ phù hợp demo/học thuật, không phù hợp vận hành y tế thật.
