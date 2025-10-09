"""
Event system with debugging to catch loops
"""
import logging
from enum import Enum
from typing import Dict, List, Callable, Any
from collections import defaultdict


class AppEvent(Enum):
    """Application events"""
    # UI Events
    UI_READY = "ui_ready"
    UI_BUSY = "ui_busy"
    
    # Message Events
    MESSAGE_SENT = "message_sent"
    MESSAGE_RECEIVED = "message_received"
    MESSAGE_ERROR = "message_error"
    
    # Translation Events
    TRANSLATION_START = "translation_start"
    TRANSLATION_SUCCESS = "translation_success"
    TRANSLATION_ERROR = "translation_error"
    
    # Ollama Events
    OLLAMA_CONNECTED = "ollama_connected"
    OLLAMA_DISCONNECTED = "ollama_disconnected"


class EventManager:
    """Event manager with loop prevention"""
    
    def __init__(self):
        self.subscribers: Dict[AppEvent, List[Callable]] = defaultdict(list)
        self.logger = logging.getLogger('ia_assistant.events')
        self._event_count = defaultdict(int)  # 🔄 CONTADOR DE EVENTOS
        self._max_events_per_second = 10      # 🔄 LÍMITE DE EVENTOS
        
    def subscribe(self, event: AppEvent, callback: Callable) -> None:
        """Subscribe to an event with duplicate check"""
        # 🔄 PREVENIR SUSCRIPCIONES DUPLICADAS
        if callback not in self.subscribers[event]:
            self.subscribers[event].append(callback)
            self.logger.debug(f"Subscribed to {event.value}, total subscribers: {len(self.subscribers[event])}")
        else:
            self.logger.warning(f"Duplicate subscription prevented for {event.value}")
    
    def unsubscribe(self, event: AppEvent, callback: Callable) -> None:
        """Unsubscribe from an event"""
        if callback in self.subscribers[event]:
            self.subscribers[event].remove(callback)
            self.logger.debug(f"Unsubscribed from {event.value}")
    
    def emit(self, event: AppEvent, data: Dict[str, Any] = None) -> None:
        """Emit an event with loop detection"""
        if data is None:
            data = {}
            
        # 🔄 DETECTAR LOOP - CONTAR EVENTOS
        self._event_count[event] += 1
        
        # 🔄 SI HAY DEMASIADOS EVENTOS DEL MISMO TIPO, PARAR
        if self._event_count[event] > self._max_events_per_second:
            self.logger.error(f"EVENT LOOP DETECTED! {event.value} emitted {self._event_count[event]} times. STOPPING.")
            return
            
        # 🔄 RESETEAR CONTADOR CADA 100 EVENTOS
        if sum(self._event_count.values()) % 100 == 0:
            self._event_count.clear()
        
        self.logger.debug(f"Emitting {event.value} to {len(self.subscribers[event])} subscribers")
        
        # Notify all subscribers
        for callback in self.subscribers[event].copy():  # Use copy to avoid modification during iteration
            try:
                callback(data)
            except Exception as e:
                self.logger.error(f"Error in event handler for {event.value}: {e}")
    
    def clear_subscribers(self, event: AppEvent = None) -> None:
        """Clear subscribers for specific event or all events"""
        if event:
            self.subscribers[event].clear()
            self.logger.info(f"Cleared all subscribers for {event.value}")
        else:
            self.subscribers.clear()
            self.logger.info("Cleared all subscribers")
    
    def get_subscriber_count(self, event: AppEvent) -> int:
        """Get number of subscribers for an event"""
        return len(self.subscribers[event])