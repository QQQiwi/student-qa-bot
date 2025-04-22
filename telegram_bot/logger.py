import logging
from pathlib import Path

def setup_logger(name: str = __name__):
    """Настройка логгера с выводом в файл и консоль"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Файловый обработчик
    file_handler = logging.FileHandler(
        filename=logs_dir / 'bot.log',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Очистка старых обработчиков
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Инициализация глобального логгера
logger = setup_logger()