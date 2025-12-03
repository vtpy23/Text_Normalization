"""
Module phân đoạn văn bản thành các đơn vị nhỏ (câu hoặc đoạn)
"""
import re
import nltk
from src.utils import setup_logging

logger = setup_logging()

# Download NLTK data nếu chưa có
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class TextSegmenter:
    def __init__(self, method='sentence', min_length=10):
        """
        Khởi tạo text segmenter
        
        Args:
            method (str): Phương pháp phân đoạn ('sentence' hoặc 'paragraph')
            min_length (int): Độ dài tối thiểu của một đoạn
        """
        self.method = method
        self.min_length = min_length
        
    def segment_by_sentence(self, text):
        """
        Chia văn bản thành các câu
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            list: Danh sách các câu
        """
        logger.info("Phân đoạn văn bản theo câu...")
        
        # Sử dụng regex để chia câu theo dấu câu tiếng Việt
        # Dấu kết thúc câu: . ! ? ; 
        sentences = re.split(r'[.!?;]\s+', text)
        
        # Lọc câu quá ngắn
        sentences = [s.strip() for s in sentences if len(s.strip()) >= self.min_length]
        
        logger.info(f"Đã chia thành {len(sentences)} câu")
        return sentences
    
    def segment_by_paragraph(self, text):
        """
        Chia văn bản thành các đoạn
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            list: Danh sách các đoạn
        """
        logger.info("Phân đoạn văn bản theo đoạn...")
        
        # Chia theo 2 newline trở lên
        paragraphs = re.split(r'\n\s*\n+', text)
        
        # Lọc đoạn quá ngắn
        paragraphs = [p.strip() for p in paragraphs if len(p.strip()) >= self.min_length]
        
        logger.info(f"Đã chia thành {len(paragraphs)} đoạn")
        return paragraphs
    
    def segment(self, text):
        """
        Phân đoạn văn bản theo phương pháp đã chọn
        
        Args:
            text (str): Văn bản đầu vào
            
        Returns:
            list: Danh sách các đoạn văn bản
        """
        if self.method == 'sentence':
            return self.segment_by_sentence(text)
        elif self.method == 'paragraph':
            return self.segment_by_paragraph(text)
        else:
            logger.warning(f"Phương pháp không hợp lệ: {self.method}. Sử dụng mặc định 'sentence'")
            return self.segment_by_sentence(text)
    
    def save_segments(self, segments, filepath):
        """
        Lưu các đoạn văn bản ra file
        
        Args:
            segments (list): Danh sách các đoạn
            filepath (str): Đường dẫn file đích
        """
        logger.info(f"Lưu {len(segments)} đoạn vào file: {filepath}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for segment in segments:
                f.write(segment + '\n')