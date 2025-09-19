"""
Backend Configuration - Configuración del backend
"""

try:
    from .settings import Settings
    __all__ = ['Settings']
except ImportError:
    __all__ = []
