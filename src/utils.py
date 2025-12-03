"""
Các hàm tiện ích chung
"""
import os
import yaml
import logging

def setup_logging():
    """Cấu hình logging cho dự án"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('process.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def load_config(config_path='config/config.yaml'):
    """Đọc file cấu hình"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def create_directories(config):
    """Tạo các thư mục cần thiết"""
    dirs = [
        os.path.dirname(config['paths']['output_images']),
        config['paths']['output_images'],
        os.path.dirname(config['paths']['raw_text'])
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

def save_text(text, filepath):
    """Lưu văn bản ra file với encoding UTF-8"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
def load_text(filepath):
    """Đọc văn bản từ file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()