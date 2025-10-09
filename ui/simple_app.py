"""
Simple application without event loops
"""
import tkinter as tk
from tkinter import messagebox
import threading
import time
import logging
from typing import Dict, Any, Optional

from core.app_state import AppState
from core.logging_setup import setup_logging
from core.events import AppEvent
from ui.components.header import HeaderComponent
from ui.components.chat_display import ChatDisplayComponent
from ui.components.input_area import InputAreaComponent
from ui.components.footer import FooterComponent
from config import config


class SimpleEnglishAssistantApp:
    """Simple English Assistant without complex event system"""
    
    def __init__(self):
        """Initialize simple application"""
        self.logger = logging.getLogger('ia_assistant')
        
        # Basic setup
        self.root = None
        self.app_state = AppState()
        self.colors = config.get_color_scheme()
        
        # Components
        self.header = None
        self.chat_display = None
        self.input_area = None
        self.footer = None
        
        # 🔄 USAR SERVICIO REAL DE OLLAMA
        from core.events import EventManager
        from core.services.ollama_service import OllamaService
        
        self.event_manager = EventManager()
        self.ollama_service = OllamaService(self.event_manager)
        self.is_processing = False
        
        # Suscribirse a eventos de Ollama
        self.event_manager.subscribe(AppEvent.OLLAMA_CONNECTED, self._on_ollama_connected)
        self.event_manager.subscribe(AppEvent.OLLAMA_DISCONNECTED, self._on_ollama_disconnected)
        self.event_manager.subscribe(AppEvent.MESSAGE_RECEIVED, self._on_message_received)
        self.event_manager.subscribe(AppEvent.MESSAGE_ERROR, self._on_message_error)

    def run(self) -> None:
        """Run the application"""
        try:
            self.logger.info("Starting Simple English Assistant")
            self._create_window()
            self._create_components()
            self._setup_simple_handlers()
            self._simulate_connection()
            
            self.logger.info("Application started successfully")
            self.root.mainloop()
            
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            messagebox.showerror("Error", f"Application error: {str(e)}")
        finally:
            self.logger.info("Application stopped")
    
    def _create_window(self) -> None:
        """Create main window"""
        self.root = tk.Tk()
        self.root.title(config.WINDOW_CONFIG['title'])
        self.root.geometry(config.get_window_geometry())
        self.root.minsize(
            config.WINDOW_CONFIG['min_width'],
            config.WINDOW_CONFIG['min_height']
        )
        self.root.configure(bg=self.colors['bg'])
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_components(self) -> None:
        """Create UI components"""
        try:
            # Header
            self.header = HeaderComponent(self.root, self.colors, None, self.app_state)
            header_frame = self.header.create()
            header_frame.pack(fill='x', padx=config.UI_CONFIG['padding'], pady=(config.UI_CONFIG['padding'], 0))
            
            # Chat display 
            self.chat_display = SimpleChatDisplay(self.root, self.colors, self.app_state)
            chat_frame = self.chat_display.create()
            chat_frame.pack(fill='both', expand=True, padx=config.UI_CONFIG['padding'], pady=config.UI_CONFIG['padding'])
            
            self.input_area = SimpleInputArea(self.root, self.colors, self.app_state)
            self.input_area.set_message_callback(self._handle_message)
            input_frame = self.input_area.create()
            input_frame.pack(fill='x', padx=config.UI_CONFIG['padding'], pady=(0, config.UI_CONFIG['padding']))
            
            # Footer
            self.footer = FooterComponent(self.root, self.colors, None, self.app_state)
            footer_frame = self.footer.create()
            footer_frame.pack(fill='x', padx=config.UI_CONFIG['padding'], pady=(0, config.UI_CONFIG['padding']))
            
        except Exception as e:
            self.logger.error(f"Failed to create components: {e}")
            raise
    
    def _setup_simple_handlers(self) -> None:
        """Setup simple handlers"""
        # Update header status
        if hasattr(self.header, 'status_label'):
            self.header.status_label.config(text="Conectando a Ollama...", bg=self.colors['warning'])
    
        # Start Ollama service
        self.ollama_service.start()

    def _simulate_connection(self) -> None:
        """Simulate connection"""
        def connect():
            time.sleep(2)
            self.is_connected = True
            
            # Update UI on main thread
            self.root.after(0, self._on_connected)
        
        threading.Thread(target=connect, daemon=True).start()
    
    def _on_connected(self) -> None:
        """Handle connection established"""
        self.logger.info("Service connected (mock)")
        
        # Update header
        if hasattr(self.header, 'status_label'):
            self.header.status_label.config(text="Conectado", bg=self.colors['success'])
        
        # Enable input
        if self.input_area:
            self.input_area.enable_send_button()
    
    def _on_ollama_connected(self, data):
        """Handle Ollama connection"""
        model = data.get('model', 'unknown')
        if hasattr(self.header, 'status_label'):
            self.header.status_label.config(text=f"Conectado ({model})", bg=self.colors['success'])
        
        if self.input_area:
            self.input_area.enable_send_button()
        
        # Mostrar mensaje de bienvenida
        welcome_msg = f"""¡Hola! Soy Alex, tu asistente para aprender inglés 😊

¿Qué deseas aprender o practicar el día de hoy?"""
        
        self.chat_display.add_message("Alex", welcome_msg, 'assistant')
    
    def _on_ollama_disconnected(self, data):
        """Handle Ollama disconnection"""
        reason = data.get('reason', 'unknown')
        if hasattr(self.header, 'status_label'):
            self.header.status_label.config(text="Desconectado", bg=self.colors['error'])
        
        if self.input_area:
            self.input_area.disable_send_button()
        
        # Mostrar mensaje de error
        error_msg = f"⚠️ Conexión perdida: {reason}\n\nPara reconectar:\n1. Abre terminal\n2. Ejecuta: ollama serve\n3. Reinicia la aplicación"
        self.chat_display.add_message("Sistema", error_msg, 'error')

    def _on_message_received(self, data):
        """Handle message received from Ollama"""
        message = data.get('message', '')
        model = data.get('model', '')
        
        if message:
            # Agregar respuesta del asistente
            self.chat_display.add_message("Alex", message, 'assistant')
            
            # Update stats
            if self.app_state:
                self.app_state.increment('messages_received')
                if hasattr(self.footer, '_update_stats_display'):
                    self.footer._update_stats_display()
        
        # Update UI state
        self._update_status("Listo", self.colors['success'])
        self.input_area.enable_send_button()
        self.is_processing = False
    
    def _on_message_error(self, data):
        """Handle message error"""
        error_msg = data.get('message', 'Unknown error')
        
        # Mostrar error en el chat
        self.chat_display.add_message("Error", f"❌ {error_msg}", 'error')
        
        # Update UI state
        self._update_status("Error", self.colors['error'])
        self.input_area.enable_send_button()
        self.is_processing = False

    def _handle_message(self, message: str) -> None:
        """Handle message using real Ollama"""
        if not message.strip():
            return
            
        if self.is_processing:
            messagebox.showwarning("Ocupado", "Ya estoy procesando un mensaje. Espera un momento.")
            return
        
        if not self.ollama_service.is_connected:
            messagebox.showerror("Error", "Ollama no está conectado.\n\n1. Abre terminal\n2. Ejecuta: ollama serve\n3. Reinicia la aplicación")
            return
        
        # Add user message immediately
        self.chat_display.add_message("Tú", message, 'user')
        
        # Update stats
        if self.app_state:
            self.app_state.increment('messages_sent')
            if hasattr(self.footer, '_update_stats_display'):
                self.footer._update_stats_display()
        
        # 🔄 ENVIAR A OLLAMA REAL
        self.is_processing = True
        self._update_status("Procesando con IA...", self.colors['warning'])
        self.input_area.disable_send_button()
        
        self.ollama_service.send_message(message)

    def _update_status(self, text: str, color: str) -> None:
        """Update status"""
        if hasattr(self.header, 'status_label'):
            self.header.status_label.config(text=text, bg=color)
    
    def _on_closing(self) -> None:
        """Handle window closing"""
        self.logger.info("Application closing...")
        self.root.quit()
        self.root.destroy()


# Simple components without event system
class SimpleChatDisplay:
    """Simple chat display without events"""
    
    def __init__(self, parent, colors, app_state):
        self.parent = parent
        self.colors = colors
        self.app_state = app_state
        self.chat_display = None
        
    def create(self):
        """Create chat display"""
        from tkinter import scrolledtext
        
        self.frame = tk.Frame(self.parent, bg=self.colors['bg'])
        
        container = tk.Frame(self.frame, bg=self.colors['surface'], relief='solid', bd=1)
        container.pack(fill='both', expand=True, padx=4, pady=4)
        
        self.chat_display = scrolledtext.ScrolledText(
            container,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            font=config.get_font('text'),
            wrap=tk.WORD,
            padx=12, pady=12,
            state='disabled',
            relief='flat', borderwidth=0,
            height=config.UI_CONFIG['chat_height']
        )
        self.chat_display.pack(fill='both', expand=True, padx=6, pady=6)
        
        self._setup_tags()
        self._show_welcome()
        
        return self.frame
    
    def _setup_tags(self):
        """Setup text tags"""
        tags = {
            'user': {'foreground': self.colors['primary'], 'font': config.get_font('text_bold')},
            'assistant': {'foreground': self.colors['success'], 'font': config.get_font('text_bold')},
            'translation': {'foreground': self.colors['accent'], 'font': config.get_font('text_bold')},
            'error': {'foreground': self.colors['error']},
            'timestamp': {'foreground': self.colors['text_muted'], 'font': config.get_font('small')},
            'welcome_title': {'foreground': self.colors['primary'], 'font': config.get_font('title')},
            'welcome_text': {'foreground': self.colors['text']},
        }
        
        for tag, style in tags.items():
            self.chat_display.tag_configure(tag, **style)
    
    def add_message(self, sender: str, message: str, tag: str) -> None:
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
    
    def _show_welcome(self):
        """Show initial status message"""
        self.chat_display.config(state='normal')
        
        # Solo mostrar mensaje de estado inicial
        status_msg = "Iniciando asistente de inglés...\n\n"
        
        self.chat_display.insert(tk.END, status_msg, 'timestamp')
        
        self.chat_display.config(state='disabled')


class SimpleInputArea:
    """Simple input area without events"""
    
    def __init__(self, parent, colors, app_state):
        self.parent = parent
        self.colors = colors
        self.app_state = app_state
        self.message_callback = None
        self.translation_callback = None
        self.message_input = None
        self.send_button = None
        self.translate_button = None
    
    def create(self):
        """Create input area"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg'])
        
        input_frame = tk.Frame(self.frame, bg=self.colors['bg'])
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Input container
        container = tk.Frame(input_frame, bg=self.colors['surface'], relief='solid', bd=1)
        container.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.message_input = tk.Text(
            container,
            height=config.UI_CONFIG['input_height'],
            wrap=tk.WORD,
            font=config.get_font('text'),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            relief='flat', borderwidth=0,
            padx=10, pady=8
        )
        self.message_input.pack(fill='both', expand=True, padx=4, pady=4)
        
        # Buttons
        button_container = tk.Frame(input_frame, bg=self.colors['bg'])
        button_container.pack(side='right', fill='y')
        
        self.send_button = tk.Button(
            button_container,
            text="Enviar",
            command=self._handle_send,
            font=config.get_font('small_bold'),
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            padx=14, pady=6,
            state='disabled'
        )
        self.send_button.pack(pady=(0, 6), fill='x')
        
        # Add placeholder
        self._add_placeholder()
        
        return self.frame
    
    def _add_placeholder(self):
        """Add placeholder text"""
        placeholder = ""
        self.message_input.insert("1.0", placeholder)
        self.message_input.config(fg=self.colors['text_muted'])
        
        self.message_input.bind("<FocusIn>", self._on_focus_in)
        self.message_input.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Handle focus in"""
        if self.message_input.get("1.0", "end-1c") == "":
            self.message_input.delete("1.0", tk.END)
            self.message_input.config(fg=self.colors['text'])
    
    def _on_focus_out(self, event):
        """Handle focus out"""
        if not self.message_input.get("1.0", "end-1c").strip():
            self.message_input.insert("1.0", "")
            self.message_input.config(fg=self.colors['text_muted'])
    
    def set_message_callback(self, callback):
        """Set message callback"""
        self.message_callback = callback
    
    def set_translation_callback(self, callback):
        """Set translation callback"""
    
    def enable_send_button(self):
        """Enable send button"""
        if self.send_button:
            self.send_button.config(state='normal')
    
    def disable_send_button(self):
        """Disable send button"""
        if self.send_button:
            self.send_button.config(state='disabled')
    
    def _handle_send(self):
        """Handle send"""
        message = self.message_input.get("1.0", "end-1c").strip()
        if message and message != "":
            if self.message_callback:
                self.message_callback(message)
            self.message_input.delete("1.0", tk.END)
            self._add_placeholder()
    
    def _handle_translate(self):
        """Handle translate"""
