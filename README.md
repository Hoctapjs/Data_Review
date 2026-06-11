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

Tìm `REVIEWER_NAMES` (khoảng dòng 420):

```python
REVIEWER_NAMES = [
    "Emily", "Jessica", "Ashley", "Lauren", ...
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

Review được tạo theo kiểu **kể chuyện** — ghép các mảnh từ nhiều ngân hàng câu toàn cục, theo thứ tự tự nhiên như người thật viết. Mỗi ngân hàng dùng chung cho cả hai sắc thái Positive và Neutral.

| Ngân hàng | Vị trí trong code | Vai trò | Xác suất xuất hiện |
|---|---|---|---|
| `LIFE_EVENTS` | ~dòng 308 | Lý do mua / dịp sử dụng | ~80% |
| `HAIR_SITUATIONS` | ~dòng 320 | Tình trạng tóc của người dùng | Luôn có |
| `PRODUCT_DETAILS` | ~dòng 330 | Chi tiết sản phẩm đã chọn (màu, độ dài) | ~70% |
| `BODY_BANK[sentiment]["quality"]` | ~dòng 43 | Nhận xét về chất lượng | Luôn có |
| `BODY_BANK[sentiment]["color"]` | ~dòng 43 | Nhận xét về màu sắc | ~80% |
| `BODY_BANK[sentiment]["fit_usage"]` | ~dòng 43 | Nhận xét về cách đeo / sử dụng | ~60% |
| `MINOR_CONS` | ~dòng 340 | Nhược điểm nhỏ (Positive: 35%, Neutral: luôn có) | 35–100% |
| `RESULTS` | ~dòng 352 | Kết quả sau khi dùng | Luôn có |
| `RECOMMENDATIONS` | ~dòng 362 | Câu kết / khuyến nghị | Luôn có |

Thêm câu mới vào bất kỳ ngân hàng nào theo cú pháp:
```python
"Câu mới của bạn.",
```

Dấu phẩy ở cuối mỗi câu là bắt buộc (trừ câu cuối cùng trong danh sách).

---

### Review ngắn (một câu)

Tìm `SHORT_BODIES` (khoảng dòng 194). Khoảng 12% review sẽ được chọn ngẫu nhiên từ đây thay vì ghép nhiều phần.

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
| `body` | text | "I bought these for my wedding..." |
| `rating` | số (1–5) | 5 |
| `review_date` | ngày (YYYY-MM-DD) | "2025-03-14" |
| `reviewer_name` | text | "Emily" |
| `reviewer_email` | text hoặc rỗng | "emily123@example.com" |
| `sentiment` | Positive / Neutral | "Positive" |
