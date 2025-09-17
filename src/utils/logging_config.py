"""
Centralized logging configuration
"""
import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from ..config.settings import Settings


def setup_logging(settings: Settings, level: str = "INFO") -> logging.Logger:
    """
    Configura el sistema de logging de manera centralizada
    
    Args:
        settings: Configuración de la aplicación
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Logger configurado
    """
    # Crear directorio de logs si no existe
    settings.paths.logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Configurar formato
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configurar logging básico
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=[
            # Handler para archivo
            logging.handlers.RotatingFileHandler(
                settings.paths.logs_dir / "assistant.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            ),
            # Handler para consola
            logging.StreamHandler()
        ]
    )
    
    # Configurar loggers específicos para diferentes niveles
    loggers_config = {
        'transformers': logging.WARNING,  # Reduce noise from transformers
        'torch': logging.WARNING,         # Reduce noise from PyTorch
        'whisper': logging.INFO,
        'src': logging.INFO,
    }
    
    for logger_name, log_level in loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
    
    # Retornar logger principal
    return logging.getLogger(__name__)


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger con el nombre especificado
    
    Args:
        name: Nombre del logger
    
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)