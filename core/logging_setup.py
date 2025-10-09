"""
Logging setup for the IA English Assistant application
"""
import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from config import config


def setup_logging(log_level: Optional[str] = None) -> None:
    """Setup logging configuration"""
    # Get log level from config or parameter
    level = log_level or config.LOGGING_CONFIG.get('level', 'INFO')
    log_format = config.LOGGING_CONFIG.get('format', 
                                           '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Convert string level to logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Console handler (if enabled)
    if config.LOGGING_CONFIG.get('console_enabled', True):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(numeric_level)
        root_logger.addHandler(console_handler)
    
    # File handler (if enabled)
    if config.LOGGING_CONFIG.get('file_enabled', True):
        try:
            # Ensure logs directory exists
            log_dir = Path(config.get_log_file_path()).parent
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # Rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                filename=config.get_log_file_path(),
                maxBytes=config.LOGGING_CONFIG.get('max_file_size', 10 * 1024 * 1024),
                backupCount=config.LOGGING_CONFIG.get('backup_count', 5),
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(numeric_level)
            root_logger.addHandler(file_handler)
            
        except Exception as e:
            # If file logging fails, at least log to console
            print(f"Warning: Could not setup file logging: {e}")
    
    # Configure specific loggers
    _configure_app_loggers(numeric_level)
    
    # Log initial message
    logger = logging.getLogger('logging_setup')
    logger.info(f"Logging initialized - Level: {level}")
    logger.debug(f"Log file: {config.get_log_file_path()}")


def _configure_app_loggers(level: int) -> None:
    """Configure application-specific loggers"""
    app_loggers = [
        'main',
        'ia_assistant',
        'ui.app',
        'ui.components',
        'core.services',
        'core.events',
        'core.app_state'
    ]
    
    for logger_name in app_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        # Don't add handlers here - they inherit from root


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance"""
    return logging.getLogger(name)


def set_log_level(level: str) -> None:
    """Change log level at runtime"""
    try:
        numeric_level = getattr(logging, level.upper())
        logging.getLogger().setLevel(numeric_level)
        
        # Update all handlers
        for handler in logging.getLogger().handlers:
            handler.setLevel(numeric_level)
            
        logger = logging.getLogger('logging_setup')
        logger.info(f"Log level changed to: {level}")
        
    except AttributeError:
        logger = logging.getLogger('logging_setup')
        logger.error(f"Invalid log level: {level}")


def disable_debug_logging() -> None:
    """Disable debug logging for production"""
    set_log_level('INFO')


def enable_debug_logging() -> None:
    """Enable debug logging for development"""
    set_log_level('DEBUG')


# Default setup when module is imported
if __name__ != "__main__":
    # Auto-setup when imported
    try:
        setup_logging()
    except Exception as e:
        print(f"Warning: Could not auto-setup logging: {e}")