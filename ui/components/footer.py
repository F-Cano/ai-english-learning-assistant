"""
Footer component with status information
"""
import tkinter as tk
from typing import Dict, Any
from ui.components.base import UIComponent
from config import config


class FooterComponent(UIComponent):
    """Footer component with iOS-style design"""
    
    def __init__(self, parent: tk.Widget, colors: Dict[str, str], 
                 event_manager, app_state):
        super().__init__(parent, colors, event_manager, app_state)
        
        # Status labels
        self.status_label = None
        self.metrics_label = None
        
        # 🔄 CORREGIR: Usar método correcto para suscripciones
        self._setup_subscriptions()
    
    def _setup_subscriptions(self) -> None:
        """Setup event subscriptions"""
        try:
            # 🔄 AGREGAR ESTA LÍNEA AL INICIO
            if self.event_manager is None:
                return
            
            # 🔄 USAR app_state.subscribe en lugar de subscribe_to_state
            if hasattr(self.app_state, 'subscribe'):
                self.app_state.subscribe('messages_sent', self._on_metrics_change)
                self.app_state.subscribe('translations_made', self._on_metrics_change)
                self.app_state.subscribe('errors_count', self._on_metrics_change)
            
            # Eventos del event manager
            from core.events import AppEvent
            self.event_manager.subscribe(AppEvent.OLLAMA_CONNECTED, self._on_connection_change)
            self.event_manager.subscribe(AppEvent.OLLAMA_DISCONNECTED, self._on_connection_change)
            self.event_manager.subscribe(AppEvent.MESSAGE_SENT, self._on_message_sent)
            
        except Exception as e:
            print(f"DEBUG Footer: Error setting up subscriptions: {e}")
    
    def create(self) -> tk.Frame:
        """Create footer"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg'], height=40)
        self.frame.pack_propagate(False)
        
        self._create_status_display()
        self._create_metrics_display()
        
        return self.frame
    
    def _create_status_display(self) -> None:
        """Create connection status display"""
        self.status_label = tk.Label(
            self.frame,
            text="Listo",
            font=config.get_font_tuple(9, 'normal', 'text'),
            bg=self.colors['bg'],
            fg=self.colors['text_muted']
        )
        self.status_label.pack(side='left', padx=16, pady=10)
    
    def _create_metrics_display(self) -> None:
        """Create session metrics display"""
        self.metrics_label = tk.Label(
            self.frame,
            font=config.get_font_tuple(9, 'normal', 'text'),
            bg=self.colors['bg'],
            fg=self.colors['text_muted']
        )
        self.metrics_label.pack(side='right', padx=16, pady=10)

    
    def _on_connection_change(self, data: Dict[str, Any]) -> None:
        """Handle connection status changes"""
        if not self.status_label:
            return
        
        # Simple status based on event
        if 'connected' in str(data) or 'Conectado' in str(data):
            self.status_label.config(text="Conectado", fg=self.colors['success'])
        else:
            self.status_label.config(text="Desconectado", fg=self.colors['error'])
    
    