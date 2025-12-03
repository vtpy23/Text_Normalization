"""
Module chuẩn hóa và làm sạch văn bản
"""
import re
import unicodedata
from src.utils import setup_logging

logger = setup_logging()

class TextCleaner:
    def __init__(self, config):
        """
        Khởi tạo text cleaner
        
        Args:
            config (dict): Cấu hình từ config.yaml
        """
        self.config = config
        self.remove_patterns = config['cleaning']['remove_patterns']
        self.unicode_form = config['cleaning']['unicode_form']
        
    def remove_headers_footers(self, text):
        """
        Loại bỏ header, footer, số trang
        
        Args:
            text (str): Văn bản gốc
            
        Returns:
            str: Văn bản sau khi loại bỏ
        """
        logger.info("Loại bỏ header, footer, số trang...")
        
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Kiểm tra từng pattern
            should_remove = False
            for pattern in self.remove_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    should_remove = True
                    break
            
            if not should_remove:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def remove_special_characters(self, text):
        """
        Loại bỏ ký tự đặc biệt, ký tự rác
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            str: Văn bản đã làm sạch
        """
        logger.info("Loại bỏ ký tự đặc biệt...")
        
        # Loại bỏ BOM và các ký tự không mong muốn
        text = text.replace('\ufeff', '')
        text = text.replace('\x0c', '')
        
        # Loại bỏ URL
        text = re.sub(r'http\S+|www\.\S+', '', text)
        
        return text
    
    def normalize_unicode(self, text):
        """
        Chuẩn hóa Unicode theo form NFC (yêu cầu DAISY)
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            str: Văn bản đã chuẩn hóa Unicode
        """
        logger.info(f"Chuẩn hóa Unicode theo form {self.unicode_form}...")
        return unicodedata.normalize(self.unicode_form, text)
    
    def normalize_whitespace(self, text):
        """
        Chuẩn hóa khoảng trắng
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            str: Văn bản đã chuẩn hóa khoảng trắng
        """
        logger.info("Chuẩn hóa khoảng trắng...")
        
        # Chuyển nhiều space thành 1 space
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Xóa khoảng trắng đầu/cuối mỗi dòng
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        # Giới hạn số dòng trống liên tiếp
        max_newlines = self.config['cleaning']['max_consecutive_newlines']
        pattern = r'\n\s*\n'
        replacement = '\n' * max_newlines
        text = re.sub(f'({pattern})+', replacement, text)
        
        return text
    
    def clean(self, text):
        """
        Thực hiện toàn bộ quy trình làm sạch văn bản
        
        Args:
            text (str): Văn bản gốc
            
        Returns:
            str: Văn bản đã chuẩn hóa hoàn chỉnh
        """
        logger.info("=== BẮT ĐẦU QUY TRÌNH LÀM SẠCH VĂN BẢN ===")
        
        # Bước 1: Loại bỏ header/footer
        text = self.remove_headers_footers(text)
        
        # Bước 2: Loại bỏ ký tự đặc biệt
        text = self.remove_special_characters(text)
        
        # Bước 3: Chuẩn hóa Unicode
        text = self.normalize_unicode(text)
        
        # Bước 4: Chuẩn hóa khoảng trắng
        text = self.normalize_whitespace(text)
        
        logger.info("=== HOÀN THÀNH LÀM SẠCH VĂN BẢN ===")
        logger.info(f"Độ dài văn bản sau khi làm sạch: {len(text)} ký tự")
        
        return text