"""
Input area component with text input and action buttons
"""
import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any, Optional
from ui.components.base import UIComponent
from config import config


class InputAreaComponent(UIComponent):
    """Input area component with modern styling"""
    
    def __init__(self, parent: tk.Widget, colors: Dict[str, str], 
                 event_manager, app_state):
        super().__init__(parent, colors, event_manager, app_state)
        self.message_input: Optional[tk.Text] = None
        self.send_button: Optional[tk.Button] = None
        self.translate_button: Optional[tk.Button] = None
    
    def create(self) -> tk.Frame:
        """Create input area with rounded borders effect"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg'])
        
        self._create_input_container()
        self._create_action_buttons()
        self._setup_event_bindings()
        self._setup_event_subscriptions()
        
        return self.frame
    
    def _create_input_container(self) -> None:
        """Create input text area with rounded borders effect"""
        input_frame = tk.Frame(self.frame, bg=self.colors['bg'])
        input_frame.pack(fill='x', pady=(0, 10))
        
        # 🔄 CONTAINER CON EFECTO DE BORDES REDONDEADOS
        outer_container = tk.Frame(
            input_frame,
            bg=self.colors['border'],  # Color del borde
            relief='flat'
        )
        outer_container.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Inner container
        input_container = tk.Frame(
            outer_container,
            bg=self.colors['surface'],
            relief='flat'
        )
        input_container.pack(fill='both', expand=True, padx=1, pady=1)
        
        # 🔄 TEXT WIDGET CON FUENTE MÁS PEQUEÑA
        self.message_input = tk.Text(
            input_container,
            height=3,  # 🔄 Reducido de 4 a 3
            wrap=tk.WORD,
            font=config.get_font_tuple(10, 'normal', 'text'),  # 🔄 Reducido de 12 a 10
            bg=self.colors['surface'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            relief='flat',
            borderwidth=0,
            highlightthickness=0,
            padx=10,  # 🔄 Reducido padding
            pady=8    # 🔄 Reducido padding
        )
        self.message_input.pack(fill='both', expand=True, padx=4, pady=4)
        
        # Placeholder text
        self._add_placeholder()
        
        # Button container
        button_container = tk.Frame(input_frame, bg=self.colors['bg'])
        button_container.pack(side='right', fill='y')
        
        # Store for later use
        self.button_frame = button_container
    
    def _add_placeholder(self) -> None:
        """Add placeholder text"""
        if self.message_input:
            placeholder = "Escribe tu mensaje aquí..."
            self.message_input.insert("1.0", placeholder)
            self.message_input.config(fg=self.colors['text_muted'])
            
            # Bind focus events for placeholder
            self.message_input.bind("<FocusIn>", self._on_focus_in)
            self.message_input.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event) -> None:
        """Handle focus in - remove placeholder"""
        if self.message_input.get("1.0", "end-1c") == "Escribe tu mensaje aquí...":
            self.message_input.delete("1.0", tk.END)
            self.message_input.config(fg=self.colors['text'])
    
    def _on_focus_out(self, event) -> None:
        """Handle focus out - add placeholder if empty"""
        if not self.message_input.get("1.0", "end-1c").strip():
            self.message_input.insert("1.0", "Escribe tu mensaje aquí...")
            self.message_input.config(fg=self.colors['text_muted'])
    
    def _create_action_buttons(self) -> None:
        """Create compact action buttons without emojis"""
        # 🔄 BOTÓN ENVIAR MÁS PEQUEÑO Y LIMPIO
        self.send_button = tk.Button(
            self.button_frame,
            text="Enviar",  # 🔄 Sin emoji
            command=self._handle_send,
            font=config.get_font_tuple(9, 'normal', 'text'),  # 🔄 Reducido de 11 a 9
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_dark'],
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            padx=14,  # 🔄 Reducido padding
            pady=6,   # 🔄 Reducido padding
            cursor='hand2',
            width=10  # 🔄 Reducido ancho
        )
        self.send_button.pack(pady=(0, 6), fill='x')
        
        # 🔄 BOTÓN TRADUCIR MÁS PEQUEÑO Y LIMPIO
        self.translate_button = tk.Button(
            self.button_frame,
            text="Traducir",  # 🔄 Sin emoji
            command=self._handle_translate,
            font=config.get_font_tuple(9, 'normal', 'text'),  # 🔄 Reducido de 11 a 9
            bg=self.colors['accent'],
            fg='white',
            activebackground=self.colors['accent_dark'],
            activeforeground='white',
            relief='flat',
            borderwidth=0,
            padx=14,  # 🔄 Reducido padding
            pady=6,   # 🔄 Reducido padding
            cursor='hand2',
            width=10, # 🔄 Reducido ancho
            state='disabled'
        )
        self.translate_button.pack(fill='x')
    
    def _setup_event_bindings(self) -> None:
        """Setup keyboard shortcuts"""
        if self.message_input:
            self.message_input.bind('<Control-Return>', lambda e: self._handle_send())
            self.message_input.bind('<Control-t>', lambda e: self._handle_translate())
            self.message_input.bind('<KeyRelease>', self._on_text_change)
    
    def _setup_event_subscriptions(self) -> None:
        """Setup event subscriptions"""
        from core.events import AppEvent
        
        try:
            self.event_manager.subscribe(AppEvent.OLLAMA_CONNECTED, self._on_ollama_connected)
            self.event_manager.subscribe(AppEvent.OLLAMA_DISCONNECTED, self._on_ollama_disconnected)
            self.event_manager.subscribe(AppEvent.UI_BUSY, self._on_ui_busy)
            self.event_manager.subscribe(AppEvent.UI_READY, self._on_ui_ready)
        except Exception as e:
            print(f"DEBUG InputArea: Error setting up subscriptions: {e}")
    
    def _on_text_change(self, event) -> None:
        """Handle text change events"""
        if self.message_input and self.translate_button:
            text = self.message_input.get("1.0", "end-1c").strip()
            placeholder = "Escribe tu mensaje aquí..."
            
            if text and text != placeholder:
                self.translate_button.config(state='normal')
            else:
                self.translate_button.config(state='disabled')
    
    def _handle_send(self) -> None:
        """Handle send button click"""
        if not self.message_input:
            return
        
        message = self.message_input.get("1.0", "end-1c").strip()
        placeholder = "Escribe tu mensaje aquí..."
        
        if not message or message == placeholder:
            messagebox.showwarning("Mensaje vacío", "Por favor escribe un mensaje antes de enviarlo.")
            return
        
        # Emit message sent event
        from core.events import AppEvent
        self.event_manager.emit(AppEvent.MESSAGE_SENT, {'message': message})
        
        # Clear input
        self.message_input.delete("1.0", tk.END)
        self._add_placeholder()
        
        # Update button state
        if self.translate_button:
            self.translate_button.config(state='disabled')
    
    def _handle_translate(self) -> None:
        """Handle translate button click"""
        if not self.message_input:
            return
        
        text = self.message_input.get("1.0", "end-1c").strip()
        placeholder = "Escribe tu mensaje aquí..."
        
        if not text or text == placeholder:
            messagebox.showwarning("Texto vacío", "Por favor escribe un texto antes de traducirlo.")
            return
        
        # Emit translation request
        from core.events import AppEvent
        self.event_manager.emit(AppEvent.TRANSLATION_START, {
            'text': text,
            'source_lang': 'es',
            'target_lang': 'en'
        })
    
    def _on_ollama_connected(self, data: Dict[str, Any]) -> None:
        """Handle Ollama connected"""
        if self.send_button:
            self.send_button.config(state='normal')
    
    def _on_ollama_disconnected(self, data: Dict[str, Any]) -> None:
        """Handle Ollama disconnected"""
        if self.send_button:
            self.send_button.config(state='disabled')
    
    def _on_ui_busy(self, data: Dict[str, Any]) -> None:
        """Handle UI busy state"""
        if self.send_button:
            self.send_button.config(state='disabled', text='Enviando...')  # 🔄 Sin emoji
        if self.translate_button:
            self.translate_button.config(state='disabled', text='Traduciendo...')  # 🔄 Sin emoji
    
    def _on_ui_ready(self, data: Dict[str, Any]) -> None:
        """Handle UI ready state"""
        if self.send_button:
            self.send_button.config(state='normal', text='Enviar')  # 🔄 Sin emoji
        
        # Solo habilitar traducir si hay texto
        if self.message_input and self.translate_button:
            text = self.message_input.get("1.0", "end-1c").strip()
            placeholder = "Escribe tu mensaje aquí..."
            
            if text and text != placeholder:
                self.translate_button.config(state='normal', text='Traducir')  # 🔄 Sin emoji
            else:
                self.translate_button.config(state='disabled', text='Traducir')  # 🔄 Sin emoji