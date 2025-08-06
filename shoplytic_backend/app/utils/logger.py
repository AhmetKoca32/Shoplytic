import logging
import sys
from typing import Optional

def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Logger oluştur ve yapılandır"""
    logger = logging.getLogger(name)
    
    # Eğer logger zaten handler'lara sahipse, yeni handler ekleme
    if logger.handlers:
        return logger
    
    # Log seviyesini ayarla
    if level is None:
        level = logging.INFO
    logger.setLevel(level)
    
    # Console handler oluştur
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Formatter oluştur
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Handler'ı logger'a ekle
    logger.addHandler(console_handler)
    
    return logger

def setup_logging(level: int = logging.INFO):
    """Ana logging yapılandırması"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
