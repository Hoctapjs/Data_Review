# Review Data Generator

Công cụ tạo dữ liệu review sản phẩm giả lập bằng tiếng Anh (chủ đề hair extensions).
Chạy trên trình duyệt, không cần biết code để sử dụng.

---

## Cách chạy

### Bước 1 — Cài Python

Tải Python tại [python.org](https://www.python.org/downloads/) (chọn phiên bản 3.10 trở lên).
Khi cài, tick vào ô **"Add Python to PATH"**.

### Bước 2 — Cài thư viện

Mở terminal (Command Prompt hoặc PowerShell), chạy:

```
pip install -r requirements.txt
```

### Bước 3 — Khởi chạy app

```
streamlit run app.py
```

Trình duyệt sẽ tự mở tại `http://localhost:8501`.

---

## Cách dùng

Giao diện có thanh điều khiển bên trái. Chỉnh các thông số rồi bấm **"Sinh dữ liệu"**.

| Thông số | Ý nghĩa |
|---|---|
| **Số dòng** | Bao nhiêu review cần tạo (ví dụ: 10.000) |
| **Positive / Neutral** | Loại review muốn sinh — tích/bỏ tích để bật/tắt |
| **Trọng số** | Tỉ lệ mỗi loại (ví dụ Positive 70, Neutral 30 → 70% review tích cực) |
| **Sinh email giả** | Bật nếu muốn cột `reviewer_email` có dữ liệu |
| **Từ ngày / Đến ngày** | Khoảng thời gian ngẫu nhiên cho `review_date` |
| **Cố định seed** | Bật để mỗi lần bấm sinh ra kết quả giống hệt nhau (tiện cho test) |

Sau khi sinh xong, tải file về bằng nút **Tải CSV** hoặc **Tải JSON**.

---

## Tùy chỉnh nội dung review

Toàn bộ nội dung review được lắp ghép từ các "ngân hàng câu" trong file [app.py](app.py).
Không cần hiểu code — chỉ cần tìm đúng chỗ và sửa văn bản trong dấu ngoặc kép.

### Tên người review

Tìm dòng có `REVIEWER_NAMES` (khoảng dòng 247):

```python
REVIEWER_NAMES = [
    "Amazon Customer", "RyB", "Andres Alomia", "Bella", ...
]
```

Thêm, xóa hoặc đổi tên tùy ý. Mỗi tên là một chuỗi trong dấu ngoặc kép, cách nhau bằng dấu phẩy.

---

### Tiêu đề review (Title)

Tìm `TITLE_TEMPLATES` (khoảng dòng 22). Có hai nhóm:

- **Positive** — dùng cho review 4–5 sao
- **Neutral** — dùng cho review 3 sao

```python
"Positive": [
    "Perfect color match for me",
    "Best extensions I've ever tried, no joke",
    ...
],
```

Thêm dòng mới theo đúng định dạng:
```python
"Câu tiêu đề mới của bạn",
```

> Nếu muốn chèn tính từ ngẫu nhiên vào tiêu đề, dùng `{adj1}` hoặc `{adj2}` trong câu.
> Ví dụ: `"These are {adj1} and so {adj2}"` → sẽ tự điền tính từ từ danh sách `POS_ADJ`.

Danh sách tính từ Positive ở `POS_ADJ` (dòng 20), tính từ Neutral ở `NEU_MILD_ADJ` (dòng 39).

---

### Nội dung review (Body)

Tìm `BODY_BANK` (khoảng dòng 43). Mỗi nhóm sentiment có các phần sau, mỗi phần được chọn ngẫu nhiên theo xác suất riêng:

| Phần | Vai trò | Xác suất xuất hiện |
|---|---|---|
| `opener` | Câu mở đầu | Luôn có |
| `shipping` | Nhận xét về giao hàng | ~25% |
| `support` | Nhận xét về hỗ trợ khách hàng | ~20% |
| `quality` | Nhận xét về chất lượng | ~90% |
| `color` | Nhận xét về màu sắc | ~60% |
| `fit_usage` | Nhận xét về cách đeo / sử dụng | ~70% |
| `results` | Nhận xét về kết quả sau khi dùng | ~80% |
| `extra` | Chi tiết thêm / cảm xúc cá nhân | ~25% |
| `value` | Nhận xét về giá trị / giá cả | ~35% |
| `closer` | Câu kết | Luôn có |

Thêm câu mới vào bất kỳ phần nào theo cú pháp:
```python
"Câu mới của bạn.",
```

Dấu phẩy ở cuối mỗi câu là bắt buộc (trừ câu cuối cùng trong danh sách).

Để thay đổi xác suất xuất hiện của một phần, tìm `BODY_SECTIONS` (khoảng dòng 283) và chỉnh số thập phân tương ứng (0.0 = không bao giờ, 1.0 = luôn luôn):
```python
BODY_SECTIONS = [
    ("shipping",  0.25),
    ("quality",   0.90),
    ...
]
```

---

### Review ngắn (một câu)

Tìm `SHORT_BODIES` (khoảng dòng 194). Khoảng 10% review sẽ được chọn ngẫu nhiên từ đây thay vì ghép nhiều phần.

```python
"Positive": [
    "Super thick and great quality.",
    "Perfect",
    ...
],
```

Thêm hoặc xóa câu tương tự như trên.

---

## Cấu trúc dữ liệu đầu ra

Mỗi dòng trong file CSV/JSON có các cột sau:

| Cột | Kiểu | Ví dụ |
|---|---|---|
| `title` | text | "Perfect color match for me" |
| `body` | text | "Okay I'm obsessed with these..." |
| `rating` | số (1–5) | 5 |
| `review_date` | ngày (YYYY-MM-DD) | "2025-03-14" |
| `reviewer_name` | text | "Emily R." |
| `reviewer_email` | text hoặc rỗng | "emily123@example.com" |
| `sentiment` | Positive / Neutral | "Positive" |
