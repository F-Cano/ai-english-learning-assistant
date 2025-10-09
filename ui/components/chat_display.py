"""
Chat display component - CLEAN VERSION
"""
import tkinter as tk
from tkinter import scrolledtext
from typing import Dict, Any, Optional
from core.events import AppEvent
from ui.components.base import UIComponent
from config import config


class ChatDisplayComponent(UIComponent):
    """Clean chat display component"""
    
    def __init__(self, parent: tk.Widget, colors: Dict[str, str], 
                 event_manager, app_state):
        super().__init__(parent, colors, event_manager, app_state)
        self.chat_display: Optional[scrolledtext.ScrolledText] = None
    
    def create(self) -> tk.Frame:
        """Create chat display"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg'])
        self._create_chat_area()
        self._setup_text_tags()
        self._setup_events()
        return self.frame
    
    def _create_chat_area(self) -> None:
        """Create chat area with border"""
        container = tk.Frame(
            self.frame,
            bg=self.colors['surface'],
            relief='solid',
            bd=1
        )
        container.pack(fill='both', expand=True, padx=4, pady=4)
        
        self.chat_display = scrolledtext.ScrolledText(
            container,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            font=config.get_font('text'),
            wrap=tk.WORD,
            padx=12,
            pady=12,
            state='disabled',
            relief='flat',
            borderwidth=0,
            height=config.UI_CONFIG['chat_height']
        )
        self.chat_display.pack(fill='both', expand=True, padx=6, pady=6)
    
    def _setup_text_tags(self) -> None:
        """Setup text styling"""
        tags = {
            'user': {'foreground': self.colors['primary'], 'font': config.get_font('text_bold')},
            'assistant': {'foreground': self.colors['success'], 'font': config.get_font('text_bold')},
            'translation': {'foreground': self.colors['accent'], 'font': config.get_font('text_bold')},
            'error': {'foreground': self.colors['error'], 'font': config.get_font('text')},
            'timestamp': {'foreground': self.colors['text_muted'], 'font': config.get_font('small')},
            'welcome_title': {'foreground': self.colors['primary'], 'font': config.get_font('title')},
            'welcome_text': {'foreground': self.colors['text'], 'font': config.get_font('text')},
        }
        
        for tag, style in tags.items():
            self.chat_display.tag_configure(tag, **style)
    
    def _setup_events(self) -> None:
        """Setup event subscriptions"""
        events = [
            (AppEvent.MESSAGE_SENT, self._on_message_sent),
            (AppEvent.MESSAGE_RECEIVED, self._on_message_received),
            (AppEvent.TRANSLATION_SUCCESS, self._on_translation_received),
            (AppEvent.MESSAGE_ERROR, self._on_message_error),
        ]
        
        for event, handler in events:
            self.event_manager.subscribe(event, handler)
        
        # Show welcome
        self.frame.after(500, self._show_welcome)
    
    def _on_message_sent(self, data: Dict[str, Any]) -> None:
        self._add_message("Tú", data.get('message', ''), 'user')
    
    def _on_message_received(self, data: Dict[str, Any]) -> None:
        self._add_message("Asistente", data.get('message', ''), 'assistant')
    
    def _on_translation_received(self, data: Dict[str, Any]) -> None:
        original = data.get('original', '')
        translation = data.get('translation', '')
        self._add_message("Traducción", f"'{original}' → '{translation}'", 'translation')
    
    def _on_message_error(self, data: Dict[str, Any]) -> None:
        self._add_message("Error", data.get('message', 'Error'), 'error')
    
    def _add_message(self, sender: str, message: str, tag: str) -> None:
        """Add message to display"""
        if not self.chat_display:
            return
            
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n", 'welcome_text')
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def _show_welcome(self) -> None:
        """Show initial status message"""
        if not self.chat_display:
            return
            
        self.chat_display.config(state='normal')
        
        # Solo mostrar un mensaje simple de estado
        status_msg = "Conectando con el asistente...\n\n"
        
        self.chat_display.insert(tk.END, status_msg, 'timestamp')
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)