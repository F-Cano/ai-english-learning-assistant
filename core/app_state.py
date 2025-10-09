"""
Application state management
"""
import logging
from typing import Dict, Any, Callable, List
from datetime import datetime


class AppState:
    """Manages application state and provides state change notifications"""
    
    def __init__(self):
        self.logger = logging.getLogger('ia_assistant')
        self._state: Dict[str, Any] = {}
        self._subscribers: Dict[str, List[Callable]] = {}
        self._session_start = datetime.now()
        
        # Initialize default state
        self._init_default_state()
        
        self.logger.debug("AppState initialized")
    
    def _init_default_state(self) -> None:
        """Initialize default application state"""
        self._state = {
            'ui_initialized': False,
            'ollama_online': False,
            'welcome_shown': False,
            'current_session': None,
            'messages_sent': 0,
            'translations_made': 0,
            'errors_count': 0,
            'last_activity': datetime.now(),
            'session_start': self._session_start
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get state value"""
        return self._state.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set state value and notify subscribers"""
        old_value = self._state.get(key)
        self._state[key] = value
        self._state['last_activity'] = datetime.now()
        
        # Notify subscribers if value changed
        if old_value != value:
            self._notify_subscribers(key, value, old_value)
        
        self.logger.debug(f"State updated: {key} = {value}")
    
    def increment(self, key: str, amount: int = 1) -> None:
        """Increment numeric state value"""
        current = self.get(key, 0)
        self.set(key, current + amount)
    
    def subscribe(self, key: str, callback: Callable) -> None:
        """Subscribe to state changes"""
        if key not in self._subscribers:
            self._subscribers[key] = []
        
        self._subscribers[key].append(callback)
        self.logger.debug(f"Subscribed to state changes for: {key}")
    
    def unsubscribe(self, key: str, callback: Callable) -> None:
        """Unsubscribe from state changes"""
        if key in self._subscribers and callback in self._subscribers[key]:
            self._subscribers[key].remove(callback)
            self.logger.debug(f"Unsubscribed from state changes for: {key}")
    
    def _notify_subscribers(self, key: str, new_value: Any, old_value: Any) -> None:
        """Notify subscribers of state changes"""
        if key in self._subscribers:
            for callback in self._subscribers[key]:
                try:
                    callback(key, new_value, old_value)
                except Exception as e:
                    self.logger.error(f"Error notifying subscriber for {key}: {e}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get session summary"""
        now = datetime.now()
        uptime = now - self._session_start
        
        return {
            'session': {
                'start_time': self._session_start,
                'current_time': now,
                'uptime': str(uptime),
                'messages_sent': self.get('messages_sent', 0),
                'translations_made': self.get('translations_made', 0),
                'errors_count': self.get('errors_count', 0)
            },
            'connection': {
                'online': self.get('ollama_online', False),
                'models': []
            },
            'ui': {
                'initialized': self.get('ui_initialized', False),
                'welcome_shown': self.get('welcome_shown', False)
            }
        }
    
    def reset(self) -> None:
        """Reset application state"""
        self._init_default_state()
        self.logger.info("Application state reset")
    
    def dump_state(self) -> Dict[str, Any]:
        """Get complete state dump for debugging"""
        return dict(self._state)