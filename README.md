# DAISY Part 2 - Text Normalization

Quy trình chuẩn hóa văn bản từ PDF scan cho dự án DAISY.

## Yêu cầu hệ thống

- Python 3.8+
- Tesseract OCR (phải cài đặt riêng)
- Poppler (cho pdf2image)

### Cài đặt Tesseract OCR

**Windows:**
```bash
# Tải và cài đặt từ: https://github.com/UB-Mannheim/tesseract/wiki
# Sau đó thêm vào PATH
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-vie poppler-utils
```

**MacOS:**
```bash
brew install tesseract tesseract-lang poppler
```

## Cài đặt

1. Clone repository
2. Cài đặt thư viện Python:
```bash
pip install -r requirements.txt
```

## Sử dụng

1. Đặt file PDF vào thư mục `input/` với tên `book.pdf`

2. Chạy chương trình:
```bash
python main.py
```

3. Kết quả sẽ được lưu trong thư mục `output/`:
   - `raw_text.txt`: Văn bản OCR gốc
   - `clean_text.txt`: Văn bản đã chuẩn hóa
   - `segments.txt`: Văn bản chia theo câu/đoạn

## Cấu hình

Chỉnh sửa file `config/config.yaml` để thay đổi:
- Đường dẫn file
- Độ phân giải OCR
- Pattern loại bỏ header/footer
- Phương pháp phân đoạn

## Log

File `process.log` chứa toàn bộ quá trình xử lý.