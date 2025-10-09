"""
Header component with modern design
"""
import tkinter as tk
from typing import Dict, Any
from ui.components.base import UIComponent
from config import config


class HeaderComponent(UIComponent):
    """Header component with clean design"""
    
    def __init__(self, parent: tk.Widget, colors: Dict[str, str], 
                 event_manager, app_state):
        super().__init__(parent, colors, event_manager, app_state)
        self.title_label = None
        self.status_label = None
    
    def create(self) -> tk.Frame:
        """Create header"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg'], height=50)  # 🔄 Reducido altura
        self.frame.pack_propagate(False)
        
        self._create_title()
        self._create_status_indicator()
        self._setup_event_subscriptions()
        
        return self.frame
    
    def _create_title(self) -> None:
        """Create title with smaller font"""
        self.title_label = tk.Label(
            self.frame,
            text=config.WINDOW_CONFIG['title'],
            font=config.get_font_tuple(13, 'bold', 'title'),  # 🔄 Reducido de 15 a 13
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.title_label.pack(side='left', padx=(16, 0), pady=15)  # 🔄 Ajustado padding
    
    def _create_status_indicator(self) -> None:
        """Create compact status indicator"""
        self.status_label = tk.Label(
            self.frame,
            text="Iniciando",  # 🔄 Sin emoji
            font=config.get_font_tuple(8, 'normal', 'text'),  # 🔄 Reducido de 9 a 8
            bg=self.colors['warning'],
            fg='white',
            padx=10,  # 🔄 Reducido padding
            pady=4,   # 🔄 Reducido padding
            relief='flat',
            bd=0
        )
        self.status_label.pack(side='right', padx=16, pady=15)  # 🔄 Ajustado padding
    
    def _setup_event_subscriptions(self) -> None:
        """Setup event subscriptions"""
        try:
            # 🔄 AGREGAR ESTA LÍNEA AL INICIO
            if self.event_manager is None:
                return
                
            from core.events import AppEvent
            
            self.event_manager.subscribe(AppEvent.OLLAMA_CONNECTED, self._on_ollama_connected)
            self.event_manager.subscribe(AppEvent.OLLAMA_DISCONNECTED, self._on_ollama_disconnected)
            self.event_manager.subscribe(AppEvent.UI_BUSY, self._on_ui_busy)
            self.event_manager.subscribe(AppEvent.UI_READY, self._on_ui_ready)
        except Exception as e:
            print(f"DEBUG Header: Error setting up subscriptions: {e}")
    
    def _on_ollama_connected(self, data: Dict[str, Any]) -> None:
        """Handle Ollama connected"""
        if self.status_label:
            self.status_label.config(text="Conectado", bg=self.colors['success'])  # 🔄 Sin emoji
    
    def _on_ollama_disconnected(self, data: Dict[str, Any]) -> None:
        """Handle Ollama disconnected"""
        if self.status_label:
            self.status_label.config(text="Desconectado", bg=self.colors['error'])  # 🔄 Sin emoji
    
    def _on_ui_busy(self, data: Dict[str, Any]) -> None:
        """Handle UI busy"""
        if self.status_label:
            self.status_label.config(text="Procesando...", bg=self.colors['warning'])  # 🔄 Sin emoji
    
    def _on_ui_ready(self, data: Dict[str, Any]) -> None:
        """Handle UI ready"""
        if self.status_label:
            self.status_label.config(text="Listo", bg=self.colors['success'])  # 🔄 Sin emoji