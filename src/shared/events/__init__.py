"""
Event System - Sistema de eventos
"""

try:
    from .event_bus import EventBus
    __all__ = ['EventBus']
except ImportError:
    __all__ = []
