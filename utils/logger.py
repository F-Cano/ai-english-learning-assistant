"""
Logging configuration and utilities
"""
import logging
import os
from config import config


def setup_logger(name: str = __name__) -> logging.Logger:
    """Setup and configure logger"""
    
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Set level from config
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    log_level = level_map.get(config.LOGGING_CONFIG['level'], logging.INFO)
    logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(config.LOGGING_CONFIG['format'])
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # File handler (if enabled)
    if config.LOGGING_CONFIG['file_enabled']:
        log_dir = os.path.dirname(config.LOGGING_CONFIG['file_path'])
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(config.LOGGING_CONFIG['file_path'])
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Global logger instance
logger = setup_logger('ia_assistant')