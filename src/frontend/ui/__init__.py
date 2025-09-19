"""
UI Components - Componentes de interfaz de usuario
"""

try:
    from .main_window import MainWindow
    __all__ = ['MainWindow']
except ImportError:
    __all__ = []
