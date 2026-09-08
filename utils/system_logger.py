import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def setup_system_logger():
    """Configurar logger central do sistema"""
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'logs'
    )
    os.makedirs(log_dir, exist_ok=True)
    
    # Logger principal
    logger = logging.getLogger('Sentinel')
    logger.setLevel(logging.INFO)
    
    # Handler para arquivo
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'sentinel.log'),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Adicionar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Singleton
system_logger = setup_system_logger()
