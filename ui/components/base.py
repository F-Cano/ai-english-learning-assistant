"""
Base UI component class
"""
import tkinter as tk
from typing import Dict, Any, Callable, Optional
from core.events import EventManager, AppEvent
from core.state import AppState
from utils.logger import logger


class UIComponent:
    """Base class for UI components"""
    
    def __init__(self, parent: tk.Widget, colors: Dict[str, str], 
                 app_state: AppState = None, event_manager: EventManager = None):
        self.parent = parent
        self.colors = colors
        self.app_state = app_state
        self.event_manager = event_manager
        self.frame: Optional[tk.Frame] = None
        self._is_created = False
        self._subscriptions = []
        
        logger.debug(f"UIComponent {self.__class__.__name__} initialized")
    
    def create(self) -> tk.Frame:
        """Create the component - must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement create()")
    
    def destroy(self) -> None:
        """Destroy the component and cleanup"""
        self._cleanup_subscriptions()
        
        if self.frame and self.frame.winfo_exists():
            self.frame.destroy()
        
        self._is_created = False
        logger.debug(f"UIComponent {self.__class__.__name__} destroyed")
    
    def show(self) -> None:
        """Show the component"""
        if self.frame and self.frame.winfo_exists():
            self.frame.pack()
    
    def hide(self) -> None:
        """Hide the component"""
        if self.frame and self.frame.winfo_exists():
            self.frame.pack_forget()
    
    def is_created(self) -> bool:
        """Check if component is created"""
        return self._is_created and self.frame and self.frame.winfo_exists()
    
    def subscribe_to_state(self, key: str, callback: Callable) -> None:
        """Subscribe to state changes"""
        if self.app_state:
            self.app_state.subscribe(key, callback)
            self._subscriptions.append(('state', key, callback))
    
    def subscribe_to_event(self, event: AppEvent, callback: Callable) -> None:
        """Subscribe to events"""
        if self.event_manager:
            self.event_manager.subscribe(event, callback)
            self._subscriptions.append(('event', event, callback))
    
    def _cleanup_subscriptions(self) -> None:
        """Cleanup all subscriptions"""
        for sub_type, key_or_event, callback in self._subscriptions:
            try:
                if sub_type == 'state' and self.app_state:
                    self.app_state.unsubscribe(key_or_event, callback)
                elif sub_type == 'event' and self.event_manager:
                    self.event_manager.unsubscribe(key_or_event, callback)
            except Exception as e:
                logger.warning(f"Error cleaning up subscription: {e}")
        
        self._subscriptions.clear()
    
    def safe_update(self, update_func: Callable) -> None:
        """Safely update UI in main thread"""
        if self.parent and self.parent.winfo_exists():
            try:
                self.parent.after(0, update_func)
            except tk.TclError:
                logger.warning("Failed to schedule UI update - widget destroyed")
    
    def get_font(self, size_key: str = 'normal', weight: str = 'normal') -> tuple:
        """Get font configuration"""
        from config import config
        return config.get_font(size_key, weight)