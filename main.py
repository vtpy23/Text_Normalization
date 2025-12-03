"""
File chính để chạy toàn bộ quy trình
"""
import sys
import os
from src.utils import setup_logging, load_config, create_directories, save_text, load_text
from src.pdf_to_images import PDFToImageConverter
from src.ocr_extraction import OCRExtractor
from src.text_cleaner import TextCleaner
from src.text_segmenter import TextSegmenter

logger = setup_logging()

def main():
    """Hàm chính chạy toàn bộ pipeline"""
    try:
        logger.info("="*60)
        logger.info("DAISY PART 2 - TEXT NORMALIZATION PIPELINE")
        logger.info("="*60)
        
        # Bước 1: Load cấu hình
        logger.info("\n[BƯỚC 1] Đọc file cấu hình...")
        config = load_config()
        create_directories(config)
        
        # Lấy cấu hình execution
        exec_config = config.get('execution', {})
        skip_pdf_to_images = exec_config.get('skip_pdf_to_images', False)
        skip_ocr = exec_config.get('skip_ocr_extraction', False)
        skip_cleaning = exec_config.get('skip_text_cleaning', False)
        skip_segmentation = exec_config.get('skip_text_segmentation', False)
        
        # Bước 2: Chuyển PDF sang ảnh
        if skip_pdf_to_images:
            logger.info("\n[BƯỚC 2] ⏭️  BỎ QUA - Chuyển đổi PDF sang ảnh (đã có sẵn)")
            # Kiểm tra xem thư mục ảnh có tồn tại không
            if not os.path.exists(config['paths']['output_images']):
                logger.error(f"✗ Thư mục ảnh không tồn tại: {config['paths']['output_images']}")
                logger.error("Vui lòng chạy bước này trước hoặc set skip_pdf_to_images = false")
                return 1
            image_files = [f for f in os.listdir(config['paths']['output_images']) if f.endswith('.png')]
            logger.info(f"  Sử dụng {len(image_files)} ảnh có sẵn")
        else:
            logger.info("\n[BƯỚC 2] 🔄 Chuyển đổi PDF sang ảnh...")
            converter = PDFToImageConverter(dpi=config['ocr']['dpi'])
            image_paths = converter.convert(
                pdf_path=config['paths']['input_pdf'],
                output_dir=config['paths']['output_images']
            )
        
        # Bước 3: OCR - Trích xuất văn bản
        if skip_ocr:
            logger.info("\n[BƯỚC 3] ⏭️  BỎ QUA - Trích xuất văn bản bằng OCR (đã có sẵn)")
            # Kiểm tra file raw_text có tồn tại không
            if not os.path.exists(config['paths']['raw_text']):
                logger.error(f"✗ File văn bản gốc không tồn tại: {config['paths']['raw_text']}")
                logger.error("Vui lòng chạy bước OCR trước hoặc set skip_ocr_extraction = false")
                return 1
            raw_text = load_text(config['paths']['raw_text'])
            logger.info(f"  Đã load văn bản gốc: {len(raw_text)} ký tự")
        else:
            logger.info("\n[BƯỚC 3] 🔄 Trích xuất văn bản bằng OCR...")
            # Lấy danh sách ảnh
            image_paths = sorted([
                os.path.join(config['paths']['output_images'], f)
                for f in os.listdir(config['paths']['output_images'])
                if f.endswith('.png')
            ])
            
            ocr = OCRExtractor(
                language=config['ocr']['language'],
                config=config['ocr']['tesseract_config']
            )
            raw_text = ocr.extract_from_images(image_paths)
            
            # Lưu văn bản gốc
            save_text(raw_text, config['paths']['raw_text'])
            logger.info(f"Đã lưu văn bản gốc: {config['paths']['raw_text']}")
        
        # Bước 4: Làm sạch và chuẩn hóa văn bản
        if skip_cleaning:
            logger.info("\n[BƯỚC 4] ⏭️  BỎ QUA - Làm sạch và chuẩn hóa văn bản")
            if not os.path.exists(config['paths']['clean_text']):
                logger.warning("⚠️  File clean_text không tồn tại, sẽ thực hiện làm sạch")
                skip_cleaning = False
            else:
                clean_text = load_text(config['paths']['clean_text'])
                logger.info(f"  Đã load văn bản sạch: {len(clean_text)} ký tự")
        
        if not skip_cleaning:
            logger.info("\n[BƯỚC 4] 🔄 Làm sạch và chuẩn hóa văn bản...")
            cleaner = TextCleaner(config)
            clean_text = cleaner.clean(raw_text)
            
            # Lưu văn bản đã chuẩn hóa
            save_text(clean_text, config['paths']['clean_text'])
            logger.info(f"Đã lưu văn bản chuẩn hóa: {config['paths']['clean_text']}")
        
        # Bước 5: Phân đoạn văn bản
        if skip_segmentation:
            logger.info("\n[BƯỚC 5] ⏭️  BỎ QUA - Phân đoạn văn bản")
            if not os.path.exists(config['paths']['segments']):
                logger.warning("⚠️  File segments không tồn tại, sẽ thực hiện phân đoạn")
                skip_segmentation = False
        
        if not skip_segmentation:
            logger.info("\n[BƯỚC 5] 🔄 Phân đoạn văn bản...")
            segmenter = TextSegmenter(
                method=config['segmentation']['method'],
                min_length=config['segmentation']['min_sentence_length']
            )
            segments = segmenter.segment(clean_text)
            segmenter.save_segments(segments, config['paths']['segments'])
        
        # Tổng kết
        logger.info("\n" + "="*60)
        logger.info("✅ HOÀN THÀNH QUY TRÌNH!")
        logger.info("="*60)
        
        # Hiển thị thống kê
        if os.path.exists(config['paths']['raw_text']):
            raw_text_size = len(load_text(config['paths']['raw_text']))
            logger.info(f"✓ Văn bản gốc: {raw_text_size:,} ký tự")
        
        if os.path.exists(config['paths']['clean_text']):
            clean_text_size = len(load_text(config['paths']['clean_text']))
            logger.info(f"✓ Văn bản chuẩn hóa: {clean_text_size:,} ký tự")
        
        if os.path.exists(config['paths']['segments']):
            with open(config['paths']['segments'], 'r', encoding='utf-8') as f:
                num_segments = len(f.readlines())
            logger.info(f"✓ Số đoạn phân tách: {num_segments:,}")
        
        logger.info(f"\nFile đầu ra:")
        logger.info(f"  - {config['paths']['raw_text']}")
        logger.info(f"  - {config['paths']['clean_text']}")
        logger.info(f"  - {config['paths']['segments']}")
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ LỖI: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())