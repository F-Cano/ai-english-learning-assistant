"""
Configuration for IA English Assistant
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class Config:
    """Application configuration"""
    
    # Directories
    BASE_DIR = Path(__file__).parent
    LOGS_DIR = BASE_DIR / "logs"
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Window settings
    WINDOW_CONFIG = {
        'title': 'IA English Assistant',
        'width': 1000,
        'height': 700,
        'min_width': 800,
        'min_height': 600,
    }
    
    UI_CONFIG = {
        'padding': 10,
        'header_height': 60,
        'footer_height': 20, 
        'chat_height': 5,
        'input_height': 3,
        'button_width': 25,
        'component_spacing': 10
    }
    
    # Colors (dark theme)
    COLORS = {
        'bg': '#0f0f0f',
        'surface': '#1a1a1a',
        'border': '#2c2c2e',
        'text': '#ffffff',
        'text_secondary': '#a0a0a0',
        'text_muted': '#6c6c6c',
        'primary': '#007aff',
        'primary_dark': '#0056d3',
        'accent': '#5856d6',
        'accent_dark': '#4a49c7',
        'success': '#32d74b',
        'warning': '#ff9f0a',
        'error': '#ff453a',
    }
    
    # Fonts
    FONTS = {
        'text': ('Segoe UI', 10, 'normal'),
        'text_bold': ('Segoe UI', 10, 'bold'),
        'small': ('Segoe UI', 8, 'normal'),
        'small_bold': ('Segoe UI', 9, 'normal'),
        'title': ('Segoe UI', 13, 'bold'),
    }
    
    # Logging
    LOGGING_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file_enabled': True,
        'console_enabled': True,
        'max_file_size': 5 * 1024 * 1024,  # 5MB
        'backup_count': 3
    }
    
    
    @classmethod
    def get_font(cls, font_type: str = 'text') -> Tuple[str, int, str]:
        """Get font tuple for tkinter"""
        return cls.FONTS.get(font_type, cls.FONTS['text'])
    
    @classmethod  
    def get_font_tuple(cls, size: int, weight: str = 'normal', font_type: str = 'text') -> Tuple[str, int, str]:
        """Get font tuple with custom size and weight"""
        base_font = cls.FONTS.get(font_type, cls.FONTS['text'])
        font_family = base_font[0]  # Tomar solo el nombre de la fuente
        return (font_family, size, weight)
    
    # 🔄 MÉTODO DE COLORES (FALTANTE)
    @classmethod
    def get_color_scheme(cls, scheme: str = 'dark') -> Dict[str, str]:
        """Get color scheme dictionary"""
        return cls.COLORS.copy()  # Retorna copia del diccionario de colores
    
    # 🔄 OTROS MÉTODOS NECESARIOS
    @classmethod
    def get_window_geometry(cls) -> str:
        """Get window geometry"""
        w, h = cls.WINDOW_CONFIG['width'], cls.WINDOW_CONFIG['height']
        return f"{w}x{h}"
    
    @classmethod
    def get_log_file_path(cls) -> str:
        """Get log file path"""
        return str(cls.LOGS_DIR / "ia_assistant.log")
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Basic validation"""
        errors = []
        
        if not cls.BASE_DIR.exists():
            errors.append("Base directory missing")
        
        if not os.access(cls.LOGS_DIR, os.W_OK):
            errors.append("Cannot write to logs directory")
            
        return errors


# Global config instance
config = Config()


def validate_environment() -> List[str]:
    """Validate environment"""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append(f"Python 3.8+ required, found {sys.version}")
    
    # Check tkinter
    try:
        import tkinter
    except ImportError:
        issues.append("tkinter not available")
    
    # Check config
    config_errors = config.validate_config()
    if config_errors:
        issues.extend(config_errors)
    
    return issues


def is_environment_valid() -> bool:
    """Check if environment is valid"""
    issues = validate_environment()
    return len(issues) == 0