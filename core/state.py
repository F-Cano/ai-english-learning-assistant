"""
Centralized application state management
"""
from typing import Dict, List, Callable, Any
from datetime import datetime
from utils.logger import logger


class AppState:
    """Centralized application state container"""
    
    def __init__(self):
        self._state = {
            # Connection state
            'ollama_online': False,
            'models_available': [],
            'current_model': None,
            'models_count': 0,
            
            # Chat state
            'chat_ready': True,
            'last_message': "",
            'last_response': "",
            'message_history': [],
            
            # Translation state
            'translation_ready': True,
            'last_translation': "",
            
            # UI state
            'ui_initialized': False,
            'components_ready': False,
            'send_button_enabled': True,
            'translate_button_enabled': True,
            
            # Session metrics
            'messages_sent': 0,
            'translations_made': 0,
            'session_start': datetime.now(),
            'errors_count': 0
        }
        
        # State change observers
        self._state_observers: Dict[str, List[Callable]] = {}
        
        logger.info("AppState initialized")
    
    def get(self, key: str, default=None) -> Any:
        """Get state value"""
        return self._state.get(key, default)
    
    def set(self, key: str, value: Any, notify: bool = True) -> None:
        """Set state value"""
        old_value = self._state.get(key)
        self._state[key] = value
        
        if notify and old_value != value:
            self._notify_observers(key, value, old_value)
        
        logger.debug(f"State changed: {key} = {value}")
    
    def update(self, updates: Dict[str, Any], notify: bool = True) -> None:
        """Update multiple state values"""
        changes = {}
        
        for key, value in updates.items():
            old_value = self._state.get(key)
            self._state[key] = value
            if old_value != value:
                changes[key] = (value, old_value)
        
        if notify:
            for key, (new_value, old_value) in changes.items():
                self._notify_observers(key, new_value, old_value)
        
        logger.debug(f"State updated: {list(updates.keys())}")
    
    def subscribe(self, key: str, callback: Callable) -> None:
        """Subscribe to state changes"""
        if key not in self._state_observers:
            self._state_observers[key] = []
        
        self._state_observers[key].append(callback)
        logger.debug(f"Observer subscribed to {key}")
    
    def unsubscribe(self, key: str, callback: Callable) -> None:
        """Unsubscribe from state changes"""
        if key in self._state_observers:
            try:
                self._state_observers[key].remove(callback)
                logger.debug(f"Observer unsubscribed from {key}")
            except ValueError:
                logger.warning(f"Observer not found for {key}")
    
    def _notify_observers(self, key: str, new_value: Any, old_value: Any) -> None:
        """Notify state change observers"""
        if key in self._state_observers:
            for callback in self._state_observers[key]:
                try:
                    callback(key, new_value, old_value)
                except Exception as e:
                    logger.error(f"Error in state observer for {key}: {e}")
    
    def increment(self, key: str, amount: int = 1) -> None:
        """Increment numeric state value"""
        current = self.get(key, 0)
        if isinstance(current, (int, float)):
            self.set(key, current + amount)
        else:
            logger.warning(f"Cannot increment non-numeric value for {key}")
    
    def reset_metrics(self) -> None:
        """Reset session metrics"""
        self.update({
            'messages_sent': 0,
            'translations_made': 0,
            'errors_count': 0,
            'session_start': datetime.now()
        })
        logger.info("Session metrics reset")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get complete state summary"""
        return {
            'connection': {
                'online': self.get('ollama_online'),
                'models': self.get('models_count', 0),
                'current_model': self.get('current_model')
            },
            'session': {
                'messages_sent': self.get('messages_sent'),
                'translations_made': self.get('translations_made'),
                'errors_count': self.get('errors_count'),
                'uptime': datetime.now() - self.get('session_start'),
                'start_time': self.get('session_start')
            },
            'ui': {
                'ready': self.get('ui_initialized'),
                'chat_ready': self.get('chat_ready'),
                'translation_ready': self.get('translation_ready')
            }
        }
    
    def export_state(self) -> Dict[str, Any]:
        """Export current state (for debugging/logging)"""
        return self._state.copy()
    
    def get_observer_count(self, key: str) -> int:
        """Get number of observers for a state key"""
        return len(self._state_observers.get(key, []))