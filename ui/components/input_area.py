"""
Input area component for message entry and actions
"""
import tkinter as tk
from typing import Dict, Any, Callable, Optional
from core.events import AppEvent
from ui.components.base import UIComponent
from ui.constants import UIMessages, UIConstants
from config import config
from utils.logger import logger
from utils.validators import validate_message


class InputAreaComponent(UIComponent):
    """Input area component with text entry and action buttons"""
    
    def __init__(self, parent: tk.Widget, colors: Dict[str, str], 
                 app_state=None, event_manager=None,
                 send_callback: Callable = None, translate_callback: Callable = None):
        super().__init__(parent, colors, app_state, event_manager)
        self.send_callback = send_callback
        self.translate_callback = translate_callback
        
        # UI elements
        self.message_input = None
        self.send_button = None
        self.translate_button = None
        self.char_count_label = None
        
        self._setup_subscriptions()
    
    def _setup_subscriptions(self) -> None:
        """Setup event and state subscriptions"""
        # Subscribe to button state changes
        self.subscribe_to_state('send_button_enabled', self._on_send_button_state_change)
        self.subscribe_to_state('translate_button_enabled', self._on_translate_button_state_change)
        self.subscribe_to_state('chat_ready', self._on_chat_ready_change)
        self.subscribe_to_state('translation_ready', self._on_translation_ready_change)
        
        # Subscribe to events for button state updates
        self.subscribe_to_event(AppEvent.MESSAGE_SENDING, self._on_message_sending)
        self.subscribe_to_event(AppEvent.MESSAGE_RECEIVED, self._on_message_received)
        self.subscribe_to_event(AppEvent.TRANSLATION_START, self._on_translation_start)
        self.subscribe_to_event(AppEvent.TRANSLATION_SUCCESS, self._on_translation_complete)
        self.subscribe_to_event(AppEvent.TRANSLATION_ERROR, self._on_translation_complete)
    
    def create(self) -> tk.Frame:
        """Create input area component"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg'])
        
        self._create_input_container()
        self._create_action_buttons()
        self._create_char_counter()
        self._setup_bindings()
        
        self._is_created = True
        logger.debug("InputAreaComponent created")
        return self.frame
    
    def _create_input_container(self) -> None:
        """Create input text container"""
        input_frame = tk.Frame(self.frame, bg=self.colors['surface'])
        input_frame.pack(fill='x', pady=(0, config.UI_CONFIG['small_padding']))
        
        # Create text input
        self.message_input = tk.Text(
            input_frame,
            height=config.UI_CONFIG['input_height'],
            bg=self.colors['surface'],
            fg=self.colors['text'],
            font=self.get_font('normal'),
            wrap=tk.WORD,
            padx=15,
            pady=10,
            insertbackground=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white'
        )
        self.message_input.pack(side='left', fill='both', expand=True)
        
        # Create button container
        self.button_frame = tk.Frame(input_frame, bg=self.colors['surface'])
        self.button_frame.pack(side='right', fill='y', 
                              padx=(config.UI_CONFIG['small_padding'], 15), 
                              pady=10)
    
    def _create_action_buttons(self) -> None:
        """Create action buttons"""
        # Send button
        self.send_button = tk.Button(
            self.button_frame,
            text=UIMessages.BUTTON_SEND,
            bg=self.colors['primary'],
            fg='white',
            font=self.get_font('small', 'bold'),
            command=self._handle_send,
            cursor='hand2',
            width=config.UI_CONFIG['button_width'],
            height=2,
            relief='flat',
            borderwidth=0
        )
        self.send_button.pack(pady=(0, 5))
        
        # Translate button
        self.translate_button = tk.Button(
            self.button_frame,
            text=UIMessages.BUTTON_TRANSLATE,
            bg=self.colors['warning'],
            fg='white',
            font=self.get_font('tiny', 'bold'),
            command=self._handle_translate,
            cursor='hand2',
            width=config.UI_CONFIG['button_width'],
            height=2,
            state='disabled',
            relief='flat',
            borderwidth=0
        )
        self.translate_button.pack()
    
    def _create_char_counter(self) -> None:
        """Create character counter"""
        counter_frame = tk.Frame(self.frame, bg=self.colors['bg'])
        counter_frame.pack(fill='x')
        
        self.char_count_label = tk.Label(
            counter_frame,
            text="0 / 1000",
            font=self.get_font('tiny'),
            bg=self.colors['bg'],
            fg=self.colors['text_muted']
        )
        self.char_count_label.pack(side='right')
    
    def _setup_bindings(self) -> None:
        """Setup keyboard bindings and events"""
        if self.message_input:
            # Keyboard shortcuts
            self.message_input.bind('<Control-Return>', lambda e: self._handle_send())
            self.message_input.bind('<KeyRelease>', self._on_text_change)
            
            # Focus events
            self.message_input.bind('<FocusIn>', self._on_focus_in)
            self.message_input.bind('<FocusOut>', self._on_focus_out)
    
    def _on_text_change(self, event=None) -> None:
        """Handle text change in input"""
        if not self.message_input or not self.char_count_label:
            return
        
        try:
            content = self.message_input.get('1.0', 'end-1c')
            char_count = len(content)
            max_chars = UIConstants.MAX_MESSAGE_LENGTH
            
            # Update counter
            counter_text = f"{char_count} / {max_chars}"
            color = self.colors['error'] if char_count > max_chars else self.colors['text_muted']
            
            self.char_count_label.config(text=counter_text, fg=color)
            
            # Enable/disable send button based on content
            has_content = bool(content.strip())
            is_valid_length = char_count <= max_chars
            chat_ready = self.app_state.get('chat_ready', True) if self.app_state else True
            
            button_enabled = has_content and is_valid_length and chat_ready
            self._update_send_button_state(button_enabled)
            
        except tk.TclError:
            pass
    
    def _on_focus_in(self, event=None) -> None:
        """Handle input focus in"""
        if self.message_input:
            self.message_input.config(bg=self.colors['surface'])
    
    def _on_focus_out(self, event=None) -> None:
        """Handle input focus out"""
        if self.message_input:
            self.message_input.config(bg=self.colors['surface'])
    
    def _handle_send(self) -> None:
        """Handle send button click"""
        if not self._can_send():
            return
        
        message = self.get_text()
        if not validate_message(message):
            logger.warning("Invalid message content")
            return
        
        if self.send_callback:
            self.send_callback(message)
        
        # Clear input after sending
        self.clear_text()
    
    def _handle_translate(self) -> None:
        """Handle translate button click"""
        if not self._can_translate():
            return
        
        if self.translate_callback:
            self.translate_callback()
    
    def _can_send(self) -> bool:
        """Check if message can be sent"""
        if not self.app_state:
            return True
        
        return (self.app_state.get('chat_ready', True) and 
                self.app_state.get('send_button_enabled', True))
    
    def _can_translate(self) -> bool:
        """Check if translation can be performed"""
        if not self.app_state:
            return True
        
        return (self.app_state.get('translation_ready', True) and 
                self.app_state.get('translate_button_enabled', True))
    
    def get_text(self) -> str:
        """Get text from input"""
        if self.message_input and self.message_input.winfo_exists():
            try:
                return self.message_input.get('1.0', 'end-1c').strip()
            except tk.TclError:
                return ""
        return ""
    
    def clear_text(self) -> None:
        """Clear input text"""
        def clear():
            try:
                if self.message_input and self.message_input.winfo_exists():
                    self.message_input.delete('1.0', 'end')
                    self._on_text_change()  # Update counter
            except tk.TclError:
                pass
        
        self.safe_update(clear)
    
    def set_text(self, text: str) -> None:
        """Set input text"""
        def set_text():
            try:
                if self.message_input and self.message_input.winfo_exists():
                    self.message_input.delete('1.0', 'end')
                    self.message_input.insert('1.0', text)
                    self._on_text_change()  # Update counter
            except tk.TclError:
                pass
        
        self.safe_update(set_text)
    
    def focus_input(self) -> None:
        """Focus on input field"""
        def focus():
            try:
                if self.message_input and self.message_input.winfo_exists():
                    self.message_input.focus_set()
            except tk.TclError:
                pass
        
        self.safe_update(focus)
    
    def _update_button_safe(self, button: tk.Button, state: str, text: str) -> None:
        """Update button safely"""
        def update():
            try:
                if button and button.winfo_exists():
                    button.config(state=state, text=text)
            except tk.TclError:
                pass
        
        self.safe_update(update)
    
    def _update_send_button_state(self, enabled: bool) -> None:
        """Update send button state"""
        if self.send_button:
            state = 'normal' if enabled else 'disabled'
            self._update_button_safe(self.send_button, state, UIMessages.BUTTON_SEND)
    
    def _on_send_button_state_change(self, key: str, new_value: Any, old_value: Any) -> None:
        """Handle send button state change"""
        if self.send_button:
            state = 'normal' if new_value else 'disabled'
            self._update_button_safe(self.send_button, state, UIMessages.BUTTON_SEND)
    
    def _on_translate_button_state_change(self, key: str, new_value: Any, old_value: Any) -> None:
        """Handle translate button state change"""
        if self.translate_button:
            state = 'normal' if new_value else 'disabled'
            self._update_button_safe(self.translate_button, state, UIMessages.BUTTON_TRANSLATE)
    
    def _on_chat_ready_change(self, key: str, new_value: Any, old_value: Any) -> None:
        """Handle chat ready state change"""
        if self.send_button:
            state = 'normal' if new_value else 'disabled'
            text = UIMessages.BUTTON_SEND if new_value else UIMessages.BUTTON_SENDING
            self._update_button_safe(self.send_button, state, text)
    
    def _on_translation_ready_change(self, key: str, new_value: Any, old_value: Any) -> None:
        """Handle translation ready state change"""
        if self.translate_button:
            state = 'normal' if new_value else 'disabled'
            text = UIMessages.BUTTON_TRANSLATE if new_value else UIMessages.BUTTON_TRANSLATING
            self._update_button_safe(self.translate_button, state, text)
    
    def _on_message_sending(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle message sending event"""
        if self.send_button:
            self._update_button_safe(self.send_button, 'disabled', UIMessages.BUTTON_SENDING)
    
    def _on_message_received(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle message received event"""
        if self.send_button:
            self._update_button_safe(self.send_button, 'normal', UIMessages.BUTTON_SEND)
        
        # Enable translation button
        if self.translate_button:
            self._update_button_safe(self.translate_button, 'normal', UIMessages.BUTTON_TRANSLATE)
    
    def _on_translation_start(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle translation start event"""
        if self.translate_button:
            self._update_button_safe(self.translate_button, 'disabled', UIMessages.BUTTON_TRANSLATING)
    
    def _on_translation_complete(self, event: AppEvent, data: Dict[str, Any]) -> None:
        """Handle translation complete event"""
        if self.translate_button:
            self._update_button_safe(self.translate_button, 'normal', UIMessages.BUTTON_TRANSLATE)