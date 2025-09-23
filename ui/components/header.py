"""
Header component with title and status indicator
"""
import tkinter as tk
from typing import Dict, Any
from core.events import AppEvent
from ui.components.base import UIComponent
from ui.constants import UIMessages
from config import config
from utils.logger import logger


class HeaderComponent(UIComponent):
    """Header component with title and connection status"""
    
    def __init__(self, parent: tk.Widget, colors: Dict[str, str], 
                 app_state=None, event_manager=None):
        super().__init__(parent, colors, app_state, event_manager)
        self.status_label = None
        self.title_label = None
        self._setup_subscriptions()
    
    def _setup_subscriptions(self) -> None:
        """Setup event and state subscriptions"""
        # Subscribe to connection state changes
        self.subscribe_to_state('ollama_online', self._on_connection_change)
        self.subscribe_to_state('models_count', self._on_models_change)
        
        # Subscribe to connection events
        self.subscribe_to_event(AppEvent.OLLAMA_CONNECTED, self._on_ollama_connected)
        self.subscribe_to_event(AppEvent.OLLAMA_DISCONNECTED, self._on_ollama_disconnected)
        self.subscribe_to_event(AppEvent.OLLAMA_ERROR, self._on_ollama_error)
    
    def create(self) -> tk.Frame:
        """Create header component"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg'])
        
        self._create_title()
        self._create_status_indicator()
        
        self._is_created = True
        logger.debug("HeaderComponent created")
        return self.frame
    
    def _create_title(self) -> None:
        """Create title label"""
        self.title_label = tk.Label(
            self.frame,
            text=config.WINDOW_CONFIG['title'],
            font=self.get_font('title', 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.title_label.pack(side='left')
    
    def _create_status_indicator(self) -> None:
        """Create status indicator"""
        status_frame = tk.Frame(self.frame, bg=self.colors['surface'])
        status_frame.pack(side='right', padx=config.UI_CONFIG['small_padding'], pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text=UIMessages.STATUS_INITIALIZING,
            font=self.get_font('small'),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary'],
            padx=15,
            pady=8
        )
        self.status_label.pack()
    
    def _update_status(self, text: str, color: str) -> None:
        """Update status display safely"""
        def update():
            try:
                if self.status_label and self.status_label.winfo_exists():
                    self.status_label.config(text=text, fg=color)
            except tk.TclError:
                pass
        
        self.safe_update(update)
    
    def _on_connection_change(self, key: str, new_value: Any, old_value: Any) -> None:
        """Handle connection state changes"""
        if key == 'ollama_online':
            if new_value:
                models_count = self.app_state.get('models_count', 0)
                status_text = f"{UIMessages.STATUS_ONLINE} ({models_count} models)"
                color = self.colors['success']
            else:
                status_text = UIMessages.STATUS_OFFLINE
                color = self.colors['error']
            
            self._update_status(status_text, color)
    
    def _on_models_change(self, key: str, new_value: Any, old_value: Any) -> None:
        """Handle models count changes"""
        if key == 'models_count' and self.app_state.get('ollama_online', False):
            status_text = f"{UIMessages.STATUS_ONLINE} ({new_value} models)"
            color = self.colors['success']
            self._update_status(status_text, color)
    
    def _on_ollama_connected(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle Ollama connected event"""
        models_count = len(data.get('models', []))
        status_text = f"Conectado ({models_count} modelos)"
        color = self.colors['success']
        self._update_status(status_text, color)
    
    def _on_ollama_disconnected(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle Ollama disconnected event"""
        status_text = UIMessages.STATUS_DISCONNECTED
        color = self.colors['error']
        self._update_status(status_text, color)
    
    def _on_ollama_error(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle Ollama error event"""
        status_text = UIMessages.STATUS_ERROR
        color = self.colors['error']
        self._update_status(status_text, color)