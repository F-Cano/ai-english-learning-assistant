"""
Chat display component for showing conversation
"""
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from typing import Dict, Any
from core.events import AppEvent
from ui.components.base import UIComponent
from ui.constants import UIMessages, UIConstants
from config import config
from utils.logger import logger


class ChatDisplayComponent(UIComponent):
    """Chat display area component"""
    
    def __init__(self, parent: tk.Widget, colors: Dict[str, str], 
                 app_state=None, event_manager=None):
        super().__init__(parent, colors, app_state, event_manager)
        self.chat_display = None
        self._setup_subscriptions()
    
    def _setup_subscriptions(self) -> None:
        """Setup event subscriptions"""
        # Subscribe to message events
        self.subscribe_to_event(AppEvent.MESSAGE_SENDING, self._on_message_sending)
        self.subscribe_to_event(AppEvent.MESSAGE_RECEIVED, self._on_message_received)
        self.subscribe_to_event(AppEvent.MESSAGE_ERROR, self._on_message_error)
        
        # Subscribe to translation events
        self.subscribe_to_event(AppEvent.TRANSLATION_SUCCESS, self._on_translation_success)
        self.subscribe_to_event(AppEvent.TRANSLATION_ERROR, self._on_translation_error)
    
    def create(self) -> tk.Frame:
        """Create chat display component"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg'])
        
        self._create_scrolled_text()
        self._setup_text_tags()
        self._show_welcome_message()
        
        self._is_created = True
        logger.debug("ChatDisplayComponent created")
        return self.frame
    
    def _create_scrolled_text(self) -> None:
        """Create scrolled text widget"""
        self.chat_display = scrolledtext.ScrolledText(
            self.frame,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            font=self.get_font('normal'),
            wrap=tk.WORD,
            padx=15,
            pady=15,
            insertbackground=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            state='disabled'
        )
        self.chat_display.pack(fill='both', expand=True)
    
    def _setup_text_tags(self) -> None:
        """Setup text formatting tags"""
        if not self.chat_display:
            return
        
        self.chat_display.tag_configure('user', 
                                       foreground=self.colors['primary'],
                                       font=self.get_font('normal', 'bold'))
        self.chat_display.tag_configure('assistant',
                                       foreground=self.colors['success'], 
                                       font=self.get_font('normal', 'bold'))
        self.chat_display.tag_configure('system',
                                       foreground=self.colors['warning'],
                                       font=self.get_font('small', 'italic'))
        self.chat_display.tag_configure('error',
                                       foreground=self.colors['error'],
                                       font=self.get_font('small', 'italic'))
        self.chat_display.tag_configure('translation',
                                       foreground=self.colors['text_secondary'],
                                       font=self.get_font('small'))
        self.chat_display.tag_configure('timestamp',
                                       foreground=self.colors['text_muted'],
                                       font=self.get_font('tiny'))
    
    def _show_welcome_message(self) -> None:
        """Show welcome message"""
        timestamp = datetime.now().strftime("%H:%M")
        self._add_message_safe(timestamp, "Assistant", UIMessages.WELCOME_DESCRIPTION.strip(), "assistant")
    
    def _add_text_safe(self, text: str, tag: str = "") -> None:
        """Add text to chat display safely"""
        def add_text():
            try:
                if self.chat_display and self.chat_display.winfo_exists():
                    self.chat_display.config(state='normal')
                    self.chat_display.insert('end', text, tag)
                    self.chat_display.config(state='disabled')
                    self.chat_display.see('end')
            except tk.TclError:
                pass
        
        self.safe_update(add_text)
    
    def _add_message_safe(self, timestamp: str, sender: str, message: str, tag: str) -> None:
        """Add complete message safely"""
        # Add some spacing for readability
        prefix = "\n" if sender != "You" else ""
        
        # Add timestamp and sender
        self._add_text_safe(f"{prefix}[{timestamp}] ", "timestamp")
        self._add_text_safe(f"{sender}:", tag)
        self._add_text_safe(f" {message}\n", "")
    
    def clear_chat(self) -> None:
        """Clear chat display"""
        def clear():
            try:
                if self.chat_display and self.chat_display.winfo_exists():
                    self.chat_display.config(state='normal')
                    self.chat_display.delete('1.0', 'end')
                    self.chat_display.config(state='disabled')
            except tk.TclError:
                pass
        
        self.safe_update(clear)
        self._show_welcome_message()
        logger.debug("Chat display cleared")
    
    def _on_message_sending(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle message sending event"""
        message = data.get('message', '')
        timestamp = datetime.now().strftime("%H:%M")
        self._add_message_safe(timestamp, "You", message, "user")
    
    def _on_message_received(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle message received event"""
        response = data.get('response', '')
        timestamp = datetime.now().strftime("%H:%M")
        self._add_message_safe(timestamp, "Assistant", response, "assistant")
    
    def _on_message_error(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle message error event"""
        error = data.get('error', 'Unknown error')
        timestamp = datetime.now().strftime("%H:%M")
        error_msg = f"Error: {error}"
        self._add_message_safe(timestamp, "System", error_msg, "error")
    
    def _on_translation_success(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle translation success event"""
        translation = data.get('translation', '')
        model_used = data.get('model_used', 'unknown')
        timestamp = datetime.now().strftime("%H:%M")
        
        translation_msg = f"Translation ({model_used}): {translation}"
        self._add_message_safe(timestamp, "Translator", translation_msg, "translation")
    
    def _on_translation_error(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle translation error event"""
        error = data.get('error', 'Translation failed')
        timestamp = datetime.now().strftime("%H:%M")
        self._add_message_safe(timestamp, "System", f"Translation error: {error}", "error")