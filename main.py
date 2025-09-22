"""
IA English Assistant - Version final con Ollama
"""
import sys
import os
sys.path.append('src')

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
import webbrowser

from src.backend.services.ai.chat_service import ChatService
from src.config.settings import settings

class EnglishAssistantApp:
    """Aplicacion final - Solo Ollama + UI moderna"""
    
    def __init__(self):
        self.setup_window()
        self.setup_styles()
        self.create_interface()
        self.setup_chat_service()
        self.show_welcome()
        
    def setup_window(self):
        """Configurar ventana principal"""
        self.root = tk.Tk()
        self.root.title(settings.app_title)
        self.root.geometry(f"{settings.window_width}x{settings.window_height}")
        self.root.configure(bg='#1a1a1a')
        
        # Centrar ventana
        self.center_window()
        
        # Configurar cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Centrar ventana en pantalla"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (settings.window_width // 2)
        y = (self.root.winfo_screenheight() // 2) - (settings.window_height // 2)
        self.root.geometry(f'{settings.window_width}x{settings.window_height}+{x}+{y}')
        
    def setup_styles(self):
        """Configurar estilos modernos"""
        # Colores del tema oscuro
        self.colors = {
            'bg': '#1a1a1a',
            'surface': '#2a2a2a', 
            'primary': '#0066cc',
            'success': '#00cc66',
            'warning': '#ffaa00',
            'error': '#ff4444',
            'text': '#ffffff',
            'text_secondary': '#cccccc',
            'text_muted': '#888888'
        }
        
    def create_interface(self):
        """Crear interfaz principal"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Chat area
        self.create_chat_area(main_frame)
        
        # Input area
        self.create_input_area(main_frame)
        
        # Footer
        self.create_footer(main_frame)
        
    def create_header(self, parent):
        """Crear header con titulo y estado"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Titulo principal
        title_label = tk.Label(
            header_frame,
            text="IA English Assistant",
            font=('Arial', 18, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title_label.pack(side='left')
        
        # Estado de Ollama
        self.status_frame = tk.Frame(header_frame, bg=self.colors['surface'])
        self.status_frame.pack(side='right', padx=10, pady=5)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Connecting...",
            font=('Arial', 10),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary'],
            padx=15,
            pady=8
        )
        self.status_label.pack()
        
    def create_chat_area(self, parent):
        """Crear area de chat"""
        chat_frame = tk.Frame(parent, bg=self.colors['bg'])
        chat_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # ScrolledText para mensajes
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            font=('Arial', 11),
            wrap=tk.WORD,
            padx=15,
            pady=15,
            insertbackground=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            state='disabled'
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Configurar tags para colores
        self.setup_chat_tags()
        
    def setup_chat_tags(self):
        """Configurar tags para colores en el chat"""
        self.chat_display.tag_configure('user', 
                                       foreground=self.colors['primary'],
                                       font=('Arial', 11, 'bold'))
        self.chat_display.tag_configure('assistant',
                                       foreground=self.colors['success'], 
                                       font=('Arial', 11, 'bold'))
        self.chat_display.tag_configure('system',
                                       foreground=self.colors['warning'],
                                       font=('Arial', 10, 'italic'))
        self.chat_display.tag_configure('error',
                                       foreground=self.colors['error'],
                                       font=('Arial', 10))
        self.chat_display.tag_configure('timestamp',
                                       foreground=self.colors['text_muted'],
                                       font=('Arial', 9))
        
    def create_input_area(self, parent):
        """Crear area de input"""
        input_frame = tk.Frame(parent, bg=self.colors['bg'])
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Frame interno
        inner_frame = tk.Frame(input_frame, bg=self.colors['surface'])
        inner_frame.pack(fill='x', padx=0, pady=0)
        
        # Input de texto
        self.message_input = tk.Text(
            inner_frame,
            height=3,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            font=('Arial', 11),
            wrap=tk.WORD,
            padx=15,
            pady=10,
            insertbackground=self.colors['primary'],
            selectbackground=self.colors['primary'],
            selectforeground='white'
        )
        self.message_input.pack(side='left', fill='both', expand=True)
        
        # Frame de botones
        button_frame = tk.Frame(inner_frame, bg=self.colors['surface'])
        button_frame.pack(side='right', fill='y', padx=(10, 15), pady=10)
        
        # Boton enviar
        self.send_button = tk.Button(
            button_frame,
            text="Send",
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            command=self.send_message,
            cursor='hand2',
            width=8,
            height=2
        )
        self.send_button.pack(pady=(0, 5))
        
        # Boton traducir
        self.translate_button = tk.Button(
            button_frame,
            text="Translate",
            bg=self.colors['warning'],
            fg='white',
            font=('Arial', 9, 'bold'),
            command=self.translate_last,
            cursor='hand2',
            width=8,
            height=2
        )
        self.translate_button.pack()
        
        # Bind eventos
        self.message_input.bind('<Control-Return>', lambda e: self.send_message())
        self.message_input.bind('<KeyRelease>', self.on_text_change)
        
    def create_footer(self, parent):
        """Crear footer con informacion"""
        footer_frame = tk.Frame(parent, bg=self.colors['bg'])
        footer_frame.pack(fill='x')
        
        # Informacion
        info_label = tk.Label(
            footer_frame,
            text="Tip: Press Ctrl+Enter to send | Powered by Ollama",
            font=('Arial', 9),
            bg=self.colors['bg'],
            fg=self.colors['text_muted']
        )
        info_label.pack(side='left')
        
        # Enlace a Ollama
        ollama_link = tk.Label(
            footer_frame,
            text="Get Ollama",
            font=('Arial', 9, 'underline'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            cursor='hand2'
        )
        ollama_link.pack(side='right')
        ollama_link.bind('<Button-1>', lambda e: webbrowser.open('https://ollama.ai'))
        
    def setup_chat_service(self):
        """Configurar servicio de chat"""
        try:
            self.chat_service = ChatService()
            self.last_assistant_message = ""
            
            # Verificar estado en hilo separado
            threading.Thread(target=self.check_status_loop, daemon=True).start()
            
        except Exception as e:
            self.update_status("Error", self.colors['error'])
            self.add_system_message(f"Error inicializando: {e}")
    
    def check_status_loop(self):
        """Loop para verificar estado de Ollama"""
        while True:
            try:
                if self.chat_service.is_online():
                    status = self.chat_service.get_status()
                    status_text = f"Online ({status['models']} models)"
                    self.root.after(0, lambda: self.update_status(status_text, self.colors['success']))
                else:
                    self.root.after(0, lambda: self.update_status("Offline", self.colors['error']))
                    
            except Exception as e:
                self.root.after(0, lambda: self.update_status("Error", self.colors['error']))
            
            import time
            time.sleep(10)  # Verificar cada 10 segundos
    
    def update_status(self, text, color):
        """Actualizar estado visual"""
        self.status_label.config(text=text, fg=color)
        
    def show_welcome(self):
        """Mostrar mensaje de bienvenida"""
        welcome_msg = """Welcome to IA English Assistant!

I'm here to help you practice English conversation. I can:
- Have natural conversations with you
- Help with grammar and vocabulary  
- Translate between English and Spanish
- Answer questions about English

Just type a message and let's start chatting!"""
        
        self.add_assistant_message(welcome_msg)
        
    def send_message(self):
        """Enviar mensaje"""
        message = self.message_input.get('1.0', 'end-1c').strip()
        
        if not message:
            return
            
        # Mostrar mensaje del usuario
        self.add_user_message(message)
        
        # Limpiar input
        self.message_input.delete('1.0', 'end')
        
        # Deshabilitar boton
        self.send_button.config(state='disabled', text='Sending...')
        
        # Procesar en hilo separado
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message):
        """Procesar mensaje en hilo separado"""
        try:
            response = self.chat_service.send_message(message)
            self.last_assistant_message = response
            
            # Mostrar respuesta
            self.root.after(0, lambda: self.add_assistant_message(response))
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.root.after(0, lambda: self.add_assistant_message(error_msg))
        
        finally:
            # Rehabilitar boton
            self.root.after(0, lambda: self.send_button.config(state='normal', text='Send'))
    
    def translate_last(self):
        """Traducir ultimo mensaje del asistente"""
        if not self.last_assistant_message:
            self.add_system_message("No hay mensaje para traducir")
            return
            
        # Deshabilitar boton
        self.translate_button.config(state='disabled', text='Translating...')
        
        # Traducir en hilo separado
        threading.Thread(target=self.process_translation, daemon=True).start()
    
    def process_translation(self):
        """Procesar traduccion en hilo separado"""
        try:
            translation = self.chat_service.translate_message(self.last_assistant_message)
            
            # Mostrar traduccion
            self.root.after(0, lambda: self.add_system_message(f"Traduccion: {translation}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.add_system_message(f"Error en traduccion: {e}"))
        
        finally:
            # Rehabilitar boton
            self.root.after(0, lambda: self.translate_button.config(state='normal', text='Translate'))
    
    def add_user_message(self, message):
        """Agregar mensaje del usuario"""
        timestamp = datetime.now().strftime("%H:%M")
        self.add_to_chat(f"[{timestamp}] You:", "user")
        self.add_to_chat(f"{message}\n", "")
        
    def add_assistant_message(self, message):
        """Agregar mensaje del asistente"""
        timestamp = datetime.now().strftime("%H:%M")
        self.add_to_chat(f"\n[{timestamp}] Assistant:", "assistant")
        self.add_to_chat(f"{message}\n", "")
        
    def add_system_message(self, message):
        """Agregar mensaje del sistema"""
        timestamp = datetime.now().strftime("%H:%M")
        self.add_to_chat(f"\n[{timestamp}] System: {message}\n", "system")
        
    def add_to_chat(self, text, tag):
        """Agregar texto al chat"""
        self.chat_display.config(state='normal')
        self.chat_display.insert('end', text, tag)
        self.chat_display.config(state='disabled')
        self.chat_display.see('end')
        
    def on_text_change(self, event):
        """Manejar cambios en el texto"""
        # Auto-resize del input
        content = self.message_input.get('1.0', 'end-1c')
        lines = content.count('\n') + 1
        new_height = min(max(lines, 1), 6)  # Entre 1 y 6 lineas
        self.message_input.config(height=new_height)
        
    def on_closing(self):
        """Manejar cierre de la aplicacion"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            
    def run(self):
        """Ejecutar aplicacion"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        print("Iniciando IA English Assistant...")
        app = EnglishAssistantApp()
        app.run()
    except KeyboardInterrupt:
        print("\nAplicacion cerrada")
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para cerrar...")
