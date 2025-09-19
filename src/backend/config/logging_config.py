"""
Logging Configuration - Configuración de logging
"""

import logging
import os
from datetime import datetime

def setup_logging(log_level=logging.INFO, log_dir="logs"):
    """"""Configura el sistema de logging""""""
    
    # Crear directorio de logs si no existe
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configurar formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configurar handler para archivo
    log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Configurar handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configurar logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger
