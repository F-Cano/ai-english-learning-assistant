"""
Footer component with metrics and information
"""
import tkinter as tk
import webbrowser
from typing import Dict, Any
from datetime import datetime
from ui.components.base import UIComponent
from ui.constants import UIMessages
from config import config
from utils.logger import logger


class FooterComponent(UIComponent):
    """Footer component with session metrics and links"""
    
    def __init__(self, parent: tk.Widget, colors: Dict[str, str], 
                 app_state=None, event_manager=None):
        super().__init__(parent, colors, app_state, event_manager)
        self.metrics_label = None
        self.help_label = None
        self.ollama_link = None
        self._setup_subscriptions()
    
    def _setup_subscriptions(self) -> None:
        """Setup state subscriptions"""
        # Subscribe to metrics changes
        self.subscribe_to_state('messages_sent', self._on_metrics_change)
        self.subscribe_to_state('translations_made', self._on_metrics_change)
        self.subscribe_to_state('errors_count', self._on_metrics_change)
    
    def create(self) -> tk.Frame:
        """Create footer component"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg'])
        
        self._create_help_section()
        self._create_metrics_section()
        self._create_links_section()
        
        self._is_created = True
        logger.debug("FooterComponent created")
        return self.frame
    
    def _create_help_section(self) -> None:
        """Create help information section"""
        self.help_label = tk.Label(
            self.frame,
            text=UIMessages.FOOTER_HELP,
            font=self.get_font('tiny'),
            bg=self.colors['bg'],
            fg=self.colors['text_muted']
        )
        self.help_label.pack(side='left')
    
    def _create_metrics_section(self) -> None:
        """Create session metrics section"""
        self.metrics_label = tk.Label(
            self.frame,
            text=self._get_metrics_text(),
            font=self.get_font('tiny'),
            bg=self.colors['bg'],
            fg=self.colors['text_secondary']
        )
        self.metrics_label.pack(side='left', padx=(20, 0))
    
    def _create_links_section(self) -> None:
        """Create links section"""
        # Ollama link
        self.ollama_link = tk.Label(
            self.frame,
            text=UIMessages.FOOTER_OLLAMA_LINK,
            font=self.get_font('tiny', 'normal'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            cursor='hand2'
        )
        self.ollama_link.pack(side='right')
        self.ollama_link.bind('<Button-1>', self._open_ollama_website)
        
        # Session time
        session_label = tk.Label(
            self.frame,
            text=self._get_session_time(),
            font=self.get_font('tiny'),
            bg=self.colors['bg'],
            fg=self.colors['text_muted']
        )
        session_label.pack(side='right', padx=(0, 20))
        
        # Update session time periodically
        self._schedule_time_update()
    
    def _get_metrics_text(self) -> str:
        """Get formatted metrics text"""
        if not self.app_state:
            return "Messages: 0 | Translations: 0"
        
        messages = self.app_state.get('messages_sent', 0)
        translations = self.app_state.get('translations_made', 0)
        errors = self.app_state.get('errors_count', 0)
        
        base_text = f"Messages: {messages} | Translations: {translations}"
        if errors > 0:
            base_text += f" | Errors: {errors}"
        
        return base_text
    
    def _get_session_time(self) -> str:
        """Get formatted session time"""
        if not self.app_state:
            return "Session: 0:00"
        
        session_start = self.app_state.get('session_start')
        if not session_start:
            return "Session: 0:00"
        
        duration = datetime.now() - session_start
        hours, remainder = divmod(int(duration.total_seconds()), 3600)
        minutes, _ = divmod(remainder, 60)
        
        if hours > 0:
            return f"Session: {hours}:{minutes:02d}h"
        else:
            return f"Session: {minutes}:02d"
    
    def _update_metrics_safe(self, text: str) -> None:
        """Update metrics display safely"""
        def update():
            try:
                if self.metrics_label and self.metrics_label.winfo_exists():
                    self.metrics_label.config(text=text)
            except tk.TclError:
                pass
        
        self.safe_update(update)
    
    def _schedule_time_update(self) -> None:
        """Schedule session time update"""
        def update_time():
            try:
                if self.frame and self.frame.winfo_exists():
                    # Find and update session time label
                    for child in self.frame.winfo_children():
                        if (isinstance(child, tk.Label) and 
                            hasattr(child, 'cget') and 
                            'Session:' in child.cget('text')):
                            child.config(text=self._get_session_time())
                            break
                    
                    # Schedule next update
                    self.frame.after(60000, update_time)  # Update every minute
            except tk.TclError:
                pass
        
        if self.frame:
            self.frame.after(60000, update_time)  # First update in 1 minute
    
    def _open_ollama_website(self, event=None) -> None:
        """Open Ollama website in browser"""
        try:
            webbrowser.open('https://ollama.ai')
            logger.info("Opened Ollama website")
        except Exception as e:
            logger.error(f"Failed to open Ollama website: {e}")
    
    def _on_metrics_change(self, key: str, new_value: Any, old_value: Any) -> None:
        """Handle metrics state changes"""
        metrics_text = self._get_metrics_text()
        self._update_metrics_safe(metrics_text)