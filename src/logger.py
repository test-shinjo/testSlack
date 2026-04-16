import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_level: str = None) -> logging.Logger:
    """ロギング設定"""
    if log_level is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    # ログディレクトリ作成
    os.makedirs('logs', exist_ok=True)
    
    # ハンドラ設定
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # ファイルハンドラ
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # コンソールハンドラ
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
