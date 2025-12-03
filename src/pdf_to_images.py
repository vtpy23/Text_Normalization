"""
Module chuyển đổi PDF sang ảnh
"""
from pdf2image import convert_from_path
import os
from src.utils import setup_logging

logger = setup_logging()

class PDFToImageConverter:
    def __init__(self, dpi=300):
        """
        Khởi tạo converter
        
        Args:
            dpi (int): Độ phân giải ảnh (300 DPI khuyến nghị cho OCR)
        """
        self.dpi = dpi
        
    def convert(self, pdf_path, output_dir):
        """
        Chuyển đổi PDF sang ảnh
        
        Args:
            pdf_path (str): Đường dẫn file PDF
            output_dir (str): Thư mục lưu ảnh
            
        Returns:
            list: Danh sách đường dẫn các file ảnh
        """
        logger.info(f"Bắt đầu chuyển đổi PDF: {pdf_path}")
        logger.info(f"DPI: {self.dpi}")
        
        try:
            # Chuyển PDF sang ảnh
            pages = convert_from_path(pdf_path, dpi=self.dpi)
            logger.info(f"Tổng số trang: {len(pages)}")
            
            # Tạo thư mục output nếu chưa có
            os.makedirs(output_dir, exist_ok=True)
            
            # Lưu từng trang
            image_paths = []
            for i, page in enumerate(pages, start=1):
                image_path = os.path.join(output_dir, f"page_{i}.png")
                page.save(image_path, "PNG")
                image_paths.append(image_path)
                logger.info(f"Đã lưu trang {i}: {image_path}")
            
            logger.info(f"Hoàn thành chuyển đổi {len(image_paths)} trang")
            return image_paths
            
        except Exception as e:
            logger.error(f"Lỗi khi chuyển đổi PDF: {str(e)}")
            raise