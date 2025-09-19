# shared/events/event_bus.py
"""
Event Bus - Sistema de eventos para comunicación UI-Backend
"""

import logging
from typing import Dict, Any, Callable, List
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Event:
    """Evento del sistema"""
    type: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "unknown"

class EventBus:
    """📡 Bus de eventos para comunicación entre componentes"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger(__name__)
    
    def subscribe(self, event_type: str, callback: Callable):
        """🔔 Suscribirse a un tipo de evento"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        self._subscribers[event_type].append(callback)
        self.logger.debug(f"Subscribed to {event_type}")
    
    def emit(self, event_type: str, data: Dict[str, Any], source: str = "unknown"):
        """📢 Emitir un evento"""
        event = Event(type=event_type, data=data, source=source)
        
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    self.logger.error(f"Error in event callback: {e}")
        
        self.logger.debug(f"Emitted event: {event_type}")