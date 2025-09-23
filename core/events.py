"""
Event system for application-wide communication
"""
from enum import Enum
from typing import Dict, List, Callable, Any
from utils.logger import logger


class AppEvent(Enum):
    """Application event types"""
    # Connection events
    OLLAMA_CONNECTED = "ollama_connected"
    OLLAMA_DISCONNECTED = "ollama_disconnected"
    OLLAMA_ERROR = "ollama_error"
    
    # Message events
    MESSAGE_SENDING = "message_sending"
    MESSAGE_SENT = "message_sent"
    MESSAGE_RECEIVED = "message_received"
    MESSAGE_ERROR = "message_error"
    
    # Translation events
    TRANSLATION_START = "translation_start"
    TRANSLATION_SUCCESS = "translation_success"
    TRANSLATION_ERROR = "translation_error"
    
    # UI events
    UI_READY = "ui_ready"
    UI_BUSY = "ui_busy"
    UI_ERROR = "ui_error"


class EventManager:
    """Centralized event management system"""
    
    def __init__(self):
        self._event_handlers: Dict[AppEvent, List[Callable]] = {}
        logger.info("EventManager initialized")
    
    def subscribe(self, event: AppEvent, handler: Callable) -> None:
        """Subscribe to an event"""
        if event not in self._event_handlers:
            self._event_handlers[event] = []
        
        self._event_handlers[event].append(handler)
        logger.debug(f"Handler subscribed to {event.value}")
    
    def unsubscribe(self, event: AppEvent, handler: Callable) -> None:
        """Unsubscribe from an event"""
        if event in self._event_handlers:
            try:
                self._event_handlers[event].remove(handler)
                logger.debug(f"Handler unsubscribed from {event.value}")
            except ValueError:
                logger.warning(f"Handler not found for {event.value}")
    
    def emit(self, event: AppEvent, data: Dict[str, Any] = None) -> None:
        """Emit an event to all subscribers"""
        if data is None:
            data = {}
        
        logger.debug(f"Event emitted: {event.value} with data: {data}")
        
        # Execute handlers
        if event in self._event_handlers:
            for handler in self._event_handlers[event]:
                try:
                    handler(event, data)
                except Exception as e:
                    logger.error(f"Error in event handler for {event.value}: {e}")
    
    def clear_handlers(self, event: AppEvent = None) -> None:
        """Clear handlers for specific event or all events"""
        if event:
            if event in self._event_handlers:
                self._event_handlers[event].clear()
                logger.debug(f"Handlers cleared for {event.value}")
        else:
            self._event_handlers.clear()
            logger.debug("All event handlers cleared")
    
    def get_handler_count(self, event: AppEvent) -> int:
        """Get number of handlers for an event"""
        return len(self._event_handlers.get(event, []))
    
    def list_events(self) -> List[AppEvent]:
        """List all events with registered handlers"""
        return list(self._event_handlers.keys())