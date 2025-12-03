"""
Module trích xuất văn bản từ ảnh bằng OCR
"""
import pytesseract
from PIL import Image
from src.utils import setup_logging
import os

logger = setup_logging()

# ====== THÊM DÒNG NÀY ======
# Chỉ định đường dẫn đến tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
# ===========================

class OCRExtractor:
    def __init__(self, language='vie', config='--psm 6'):
        """
        Khởi tạo OCR extractor
        
        Args:
            language (str): Ngôn ngữ nhận dạng ('vie' cho tiếng Việt)
            config (str): Cấu hình Tesseract
        """
        self.language = language
        self.config = config
        
        # Kiểm tra xem Tesseract có hoạt động không
        self._verify_tesseract()
        
    def _verify_tesseract(self):
        """Kiểm tra Tesseract có hoạt động không"""
        try:
            version = pytesseract.get_tesseract_version()
            logger.info(f"Tesseract version: {version}")
            
            # Kiểm tra ngôn ngữ
            langs = pytesseract.get_languages()
            logger.info(f"Available languages: {langs}")
            
            if self.language not in langs:
                logger.warning(f"Language '{self.language}' not found. Available: {langs}")
                
        except Exception as e:
            logger.error(f"Cannot verify Tesseract: {str(e)}")
            raise Exception(
                "Tesseract not found! Please check:\n"
                f"1. Tesseract installed at: {pytesseract.pytesseract.tesseract_cmd}\n"
                "2. PATH environment variable is set correctly"
            )
        
    def extract_from_image(self, image_path):
        """
        Trích xuất văn bản từ một ảnh
        
        Args:
            image_path (str): Đường dẫn file ảnh
            
        Returns:
            str: Văn bản trích xuất được
        """
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(
                img, 
                lang=self.language,
                config=self.config
            )
            return text
        except Exception as e:
            logger.error(f"Lỗi OCR cho file {image_path}: {str(e)}")
            return ""
    
    def extract_from_images(self, image_paths):
        """
        Trích xuất văn bản từ nhiều ảnh
        
        Args:
            image_paths (list): Danh sách đường dẫn ảnh
            
        Returns:
            str: Toàn bộ văn bản trích xuất
        """
        logger.info(f"Bắt đầu OCR cho {len(image_paths)} ảnh")
        
        full_text = ""
        for i, image_path in enumerate(image_paths, start=1):
            logger.info(f"Đang xử lý trang {i}/{len(image_paths)}")
            
            page_text = self.extract_from_image(image_path)
            
            if page_text.strip():  # Chỉ thêm nếu có nội dung
                full_text += page_text + "\n\n"
                logger.info(f"Trang {i}: Trích xuất được {len(page_text)} ký tự")
            else:
                logger.warning(f"Trang {i}: Không trích xuất được văn bản")
        
        logger.info(f"Hoàn thành OCR. Tổng {len(full_text)} ký tự")
        return full_text