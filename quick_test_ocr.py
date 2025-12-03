"""
Test nhanh OCR cho 1 trang
"""
import pytesseract
from PIL import Image
import os

# CẤU HÌNH (THAY ĐỔI NẾU CẦN)
TESSERACT_PATH = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
TEST_IMAGE = "output/images/page_6.png"  # Ảnh để test

# Set đường dẫn Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def quick_test():
    print("="*60)
    print("QUICK OCR TEST")
    print("="*60)
    
    # Kiểm tra file ảnh
    if not os.path.exists(TEST_IMAGE):
        print(f"✗ File không tồn tại: {TEST_IMAGE}")
        print("\nGợi ý:")
        print("1. Chạy bước chuyển PDF sang ảnh trước")
        print("2. Hoặc thay đổi TEST_IMAGE trong code")
        return
    
    print(f"Test file: {TEST_IMAGE}")
    
    try:
        # Mở ảnh
        img = Image.open(TEST_IMAGE)
        print(f"✓ Image size: {img.size}")
        print(f"✓ Image mode: {img.mode}")
        
        # Chạy OCR
        print("\nĐang chạy OCR...")
        text = pytesseract.image_to_string(img, lang='vie', config='--psm 6')
        
        # Kết quả
        print(f"\n✓ OCR THÀNH CÔNG!")
        print(f"✓ Số ký tự: {len(text)}")
        print(f"✓ Số dòng: {len(text.splitlines())}")
        
        # Hiển thị nội dung
        print("\n" + "="*60)
        print("NỘI DUNG (1000 ký tự đầu):")
        print("="*60)
        print(text[:1000])
        print("="*60)
        
        # Lưu ra file
        output_file = "quick_test_result.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        print(f"\n✓ Đã lưu toàn bộ nội dung vào: {output_file}")
        print("\n🎉 TEST THÀNH CÔNG!")
        
    except pytesseract.TesseractNotFoundError:
        print("\n✗ LỖI: Không tìm thấy Tesseract!")
        print(f"Đường dẫn hiện tại: {TESSERACT_PATH}")
        print("\nGiải pháp:")
        print("1. Kiểm tra Tesseract đã cài đặt chưa")
        print("2. Thay đổi TESSERACT_PATH trong code")
        
    except Exception as e:
        print(f"\n✗ LỖI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_test()