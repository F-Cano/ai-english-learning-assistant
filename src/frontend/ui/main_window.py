# frontend/ui/main_window.py
"""
Main Window - Ventana principal de la aplicación IA
VERSIÓN CORREGIDA Y FUNCIONAL
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import logging
from typing import Optional, Callable
from datetime import datetime
import threading
import json
import os

logger = logging.getLogger(__name__)

class MainController:
    """🎮 Controlador principal temporal hasta implementar el real"""
    
    def __init__(self):
        self.session_active = False
        logger.info("MainController temporal inicializado")
    
    def new_session(self):
        """🆕 Nueva sesión"""
        self.session_active = True
        logger.info("Nueva sesión iniciada")
        return {"session_id": "new_session", "status": "created"}
    
    def load_session(self):
        """📂 Cargar sesión"""
        logger.info("Cargando sesión...")
        return {"session_id": "loaded_session", "status": "loaded"}
    
    def end_session(self):
        """🏁 Finalizar sesión"""
        self.session_active = False
        logger.info("Sesión finalizada")

class ChatController:
    """💬 Controlador de chat temporal"""
    
    def __init__(self):
        self.message_history = []
        logger.info("ChatController temporal inicializado")
    
    def send_message(self, message: str, callback: Optional[Callable] = None):
        """📤 Enviar mensaje"""
        try:
            # Simular procesamiento
            response = f"Entiendo lo que dices sobre: '{message[:50]}...'. ¡Continúa!"
            
            # Agregar al historial
            self.message_history.append({
                "user": message,
                "ai": response,
                "timestamp": datetime.now().isoformat()
            })
            
            if callback:
                callback({"user_message": message, "ai_response": response})
            
            return response
            
        except Exception as e:
            logger.error(f"Error enviando mensaje: {e}")
            return "Lo siento, hubo un error procesando tu mensaje."

class ChatWidget(ttk.Frame):
    """💬 Widget de chat completo y funcional"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.controller: Optional[ChatController] = None
        self.message_history = []
        self._create_widgets()
        self._setup_layout()
        self._setup_events()
        logger.info("ChatWidget inicializado")
    
    def _create_widgets(self):
        """🎨 Crear widgets del chat"""
        # Chat display area
        self.chat_frame = ttk.Frame(self)
        
        # Chat text area with scrollbar
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            width=60,
            height=25,
            font=('Segoe UI', 10),
            state=tk.DISABLED,
            bg='#f8f9fa',
            fg='#212529'
        )
        
        # Input frame
        self.input_frame = ttk.Frame(self)
        
        # Input text area
        self.input_text = tk.Text(
            self.input_frame,
            wrap=tk.WORD,
            width=50,
            height=3,
            font=('Segoe UI', 10),
            bg='white',
            fg='#212529'
        )
        
        # Send button
        self.send_button = ttk.Button(
            self.input_frame,
            text="Enviar",
            command=self._send_message,
            style="Accent.TButton"
        )
        
        # Clear button
        self.clear_button = ttk.Button(
            self.input_frame,
            text="Limpiar",
            command=self._clear_chat
        )
        
        # Progress bar (hidden by default)
        self.progress_bar = ttk.Progressbar(
            self,
            mode='indeterminate',
            length=300
        )
        
        # Status label
        self.status_label = ttk.Label(
            self,
            text="Listo para chatear",
            font=('Segoe UI', 9)
        )
    
    def _setup_layout(self):
        """📐 Configurar layout del chat"""
        # Chat frame
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar (initially hidden)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        self.progress_bar.pack_forget()  # Hide initially
        
        # Input frame
        self.input_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Input layout
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.input_frame)
        buttons_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.send_button.pack(fill=tk.X, pady=(0, 2))
        self.clear_button.pack(fill=tk.X)
        
        # Status label
        self.status_label.pack(fill=tk.X)
    
    def _setup_events(self):
        """⚡ Configurar eventos"""
        # Enter key to send message
        self.input_text.bind('<Control-Return>', lambda e: self._send_message())
        self.input_text.bind('<KeyRelease>', self._on_input_change)
        
        # Focus on input by default
        self.input_text.focus()
    
    def _send_message(self):
        """📤 Enviar mensaje"""
        message = self.input_text.get("1.0", tk.END).strip()
        
        if not message:
            return
        
        if not self.controller:
            self._add_system_message("⚠️ Controlador no conectado")
            return
        
        # Disable input while processing
        self._set_processing(True)
        
        # Add user message to display
        self._add_user_message(message)
        
        # Clear input
        self.input_text.delete("1.0", tk.END)
        
        # Send message in background thread
        def send_async():
            try:
                response = self.controller.send_message(message, self._on_response_received)
            except Exception as e:
                logger.error(f"Error in send_async: {e}")
                self._add_system_message(f"❌ Error: {str(e)}")
            finally:
                self.after(0, lambda: self._set_processing(False))
        
        threading.Thread(target=send_async, daemon=True).start()
    
    def _on_response_received(self, response_data: dict):
        """📨 Callback cuando se recibe respuesta"""
        try:
            ai_response = response_data.get("ai_response", "Sin respuesta")
            self.after(0, lambda: self._add_ai_message(ai_response))
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            self.after(0, lambda: self._add_system_message(f"❌ Error procesando respuesta: {e}"))
    
    def _add_user_message(self, message: str):
        """👤 Agregar mensaje del usuario"""
        timestamp = datetime.now().strftime("%H:%M")
        self._add_message(f"[{timestamp}] TÚ: {message}\n", "user")
    
    def _add_ai_message(self, message: str):
        """🤖 Agregar mensaje de la IA"""
        timestamp = datetime.now().strftime("%H:%M")
        self._add_message(f"[{timestamp}] IA: {message}\n\n", "ai")
    
    def _add_system_message(self, message: str):
        """⚙️ Agregar mensaje del sistema"""
        timestamp = datetime.now().strftime("%H:%M")
        self._add_message(f"[{timestamp}] SISTEMA: {message}\n", "system")
    
    def _add_message(self, message: str, message_type: str):
        """📝 Agregar mensaje al display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Configure tags for different message types
        if message_type == "user":
            self.chat_display.insert(tk.END, message, "user_tag")
        elif message_type == "ai":
            self.chat_display.insert(tk.END, message, "ai_tag")
        else:
            self.chat_display.insert(tk.END, message, "system_tag")
        
        # Configure text tags
        self.chat_display.tag_config("user_tag", foreground="#0066cc", font=('Segoe UI', 10, 'bold'))
        self.chat_display.tag_config("ai_tag", foreground="#28a745", font=('Segoe UI', 10))
        self.chat_display.tag_config("system_tag", foreground="#6c757d", font=('Segoe UI', 9, 'italic'))
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def _clear_chat(self):
        """🧹 Limpiar chat"""
        if messagebox.askyesno("Confirmar", "¿Limpiar todo el historial de chat?"):
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.message_history.clear()
            self._add_system_message("Chat limpiado")
    
    def _set_processing(self, processing: bool):
        """⚙️ Establecer estado de procesamiento"""
        if processing:
            self.send_button.config(state=tk.DISABLED)
            self.input_text.config(state=tk.DISABLED)
            self.progress_bar.pack(fill=tk.X, pady=(0, 5))
            self.progress_bar.start()
            self.status_label.config(text="Procesando mensaje...")
        else:
            self.send_button.config(state=tk.NORMAL)
            self.input_text.config(state=tk.NORMAL)
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.status_label.config(text="Listo para chatear")
            self.input_text.focus()
    
    def _on_input_change(self, event):
        """📝 Callback cuando cambia el input"""
        text = self.input_text.get("1.0", tk.END).strip()
        char_count = len(text)
        self.status_label.config(text=f"Caracteres: {char_count}")
    
    def set_controller(self, controller: ChatController):
        """🎮 Establecer controlador"""
        self.controller = controller
        self._add_system_message("✅ Controlador conectado - ¡Listo para chatear!")
        logger.info("Controller conectado al ChatWidget")

class SettingsDialog:
    """⚙️ Diálogo de configuraciones"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configuraciones")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self._create_widgets()
        self._center_dialog()
    
    def _create_widgets(self):
        """🎨 Crear widgets de configuración"""
        # Notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        
        # Theme selection
        ttk.Label(general_frame, text="Tema:").pack(anchor=tk.W, pady=(10, 5))
        theme_var = tk.StringVar(value="clam")
        theme_combo = ttk.Combobox(general_frame, textvariable=theme_var, 
                                  values=["clam", "alt", "default", "classic"])
        theme_combo.pack(fill=tk.X, padx=(0, 0), pady=(0, 10))
        
        # Font size
        ttk.Label(general_frame, text="Tamaño de fuente:").pack(anchor=tk.W, pady=(0, 5))
        font_scale = tk.Scale(general_frame, from_=8, to=16, orient=tk.HORIZONTAL)
        font_scale.set(10)
        font_scale.pack(fill=tk.X, pady=(0, 10))
        
        # AI tab
        ai_frame = ttk.Frame(notebook)
        notebook.add(ai_frame, text="IA")
        
        # Response mode
        ttk.Label(ai_frame, text="Modo de respuesta:").pack(anchor=tk.W, pady=(10, 5))
        response_var = tk.StringVar(value="balanced")
        response_combo = ttk.Combobox(ai_frame, textvariable=response_var,
                                     values=["fast", "balanced", "detailed"])
        response_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Auto-save
        auto_save_var = tk.BooleanVar(value=True)
        auto_save_check = ttk.Checkbutton(ai_frame, text="Guardar sesiones automáticamente",
                                         variable=auto_save_var)
        auto_save_check.pack(anchor=tk.W, pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.dialog)
        buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(buttons_frame, text="OK", 
                  command=self._save_settings).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(buttons_frame, text="Cancelar", 
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
    
    def _center_dialog(self):
        """📐 Centrar diálogo"""
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Calculate position
        x = (self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 200)
        y = (self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 150)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _save_settings(self):
        """💾 Guardar configuraciones"""
        # Aquí implementar guardado real
        messagebox.showinfo("Info", "Configuraciones guardadas")
        self.dialog.destroy()

class MainWindow:
    """🖥️ Ventana principal de la aplicación IA - VERSIÓN CORREGIDA"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.controller: Optional[MainController] = None
        self.chat_controller: Optional[ChatController] = None
        self._setup_window()
        self._create_widgets()
        self._setup_layout()
        self._setup_events()
        self._initialize_controllers()
        logger.info("MainWindow inicializada correctamente")
    
    def _setup_window(self):
        """⚙️ Configurar ventana principal"""
        self.root.title("IA Language Assistant")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set icon if available
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "app_icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass  # No icon available
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure("Accent.TButton", font=('Segoe UI', 9, 'bold'))
        style.configure("Title.TLabel", font=('Segoe UI', 12, 'bold'))
    
    def _create_widgets(self):
        """🎨 Crear widgets de la interfaz"""
        # Menu bar
        self._create_menu_bar()
        
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        
        # Chat widget (main area)
        self.chat_widget = ChatWidget(self.main_frame)
        
        # Side panel para configuraciones y información
        self.side_panel = ttk.Frame(self.main_frame, width=250)
        self._create_side_panel()
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root, 
            text="IA Language Assistant - Listo", 
            relief=tk.SUNKEN,
            font=('Segoe UI', 9)
        )
    
    def _create_menu_bar(self):
        """📋 Crear barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nueva Sesión", command=self._new_session, accelerator="Ctrl+N")
        file_menu.add_command(label="Cargar Sesión", command=self._load_session, accelerator="Ctrl+O")
        file_menu.add_command(label="Guardar Sesión", command=self._save_session, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exportar Chat", command=self._export_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self._on_closing, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=edit_menu)
        edit_menu.add_command(label="Limpiar Chat", command=self._clear_chat)
        edit_menu.add_command(label="Configuraciones", command=self._open_settings, accelerator="Ctrl+,")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=view_menu)
        view_menu.add_command(label="Alternar Panel Lateral", command=self._toggle_side_panel)
        view_menu.add_command(label="Temas", command=self._open_themes)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self._show_about)
    
    def _create_side_panel(self):
        """📊 Crear panel lateral"""
        # Title
        title_label = ttk.Label(self.side_panel, text="Panel de Control", style="Title.TLabel")
        title_label.pack(pady=(10, 20))
        
        # Session info frame
        session_frame = ttk.LabelFrame(self.side_panel, text="Información de Sesión")
        session_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.session_status = ttk.Label(session_frame, text="Estado: Inactiva")
        self.session_status.pack(anchor=tk.W, padx=10, pady=5)
        
        self.session_time = ttk.Label(session_frame, text="Duración: 00:00")
        self.session_time.pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Quick actions frame
        actions_frame = ttk.LabelFrame(self.side_panel, text="Acciones Rápidas")
        actions_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(actions_frame, text="Nueva Sesión", 
                  command=self._new_session).pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(actions_frame, text="Guardar Chat", 
                  command=self._save_session).pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(actions_frame, text="Configuraciones", 
                  command=self._open_settings).pack(fill=tk.X, padx=10, pady=(5, 10))
        
        # Stats frame
        stats_frame = ttk.LabelFrame(self.side_panel, text="Estadísticas")
        stats_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.messages_count = ttk.Label(stats_frame, text="Mensajes: 0")
        self.messages_count.pack(anchor=tk.W, padx=10, pady=5)
        
        self.words_count = ttk.Label(stats_frame, text="Palabras: 0")
        self.words_count.pack(anchor=tk.W, padx=10, pady=(0, 10))
    
    def _setup_layout(self):
        """📐 Configurar layout"""
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat widget (main area)
        self.chat_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Side panel
        self.side_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Status bar
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _setup_events(self):
        """⚡ Configurar eventos"""
        # Window events
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Keyboard shortcuts
        self.root.bind_all("<Control-n>", lambda e: self._new_session())
        self.root.bind_all("<Control-o>", lambda e: self._load_session())
        self.root.bind_all("<Control-s>", lambda e: self._save_session())
        self.root.bind_all("<Control-q>", lambda e: self._on_closing())
        self.root.bind_all("<Control-comma>", lambda e: self._open_settings())
    
    def _initialize_controllers(self):
        """🎮 Inicializar controladores"""
        try:
            # Create controllers
            self.controller = MainController()
            self.chat_controller = ChatController()
            
            # Connect chat controller to widget
            self.chat_widget.set_controller(self.chat_controller)
            
            self._update_status("Controladores inicializados correctamente")
            logger.info("Controladores inicializados correctamente")
            
        except Exception as e:
            error_msg = f"Error inicializando controladores: {e}"
            self._update_status(error_msg)
            logger.error(error_msg)
    
    def run(self):
        """🚀 Ejecutar aplicación"""
        try:
            self._update_status("Aplicación iniciada")
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Error ejecutando aplicación: {e}")
            messagebox.showerror("Error", f"Error ejecutando aplicación: {e}")
    
    # Event handlers
    def _new_session(self):
        """🆕 Nueva sesión"""
        try:
            if self.controller:
                result = self.controller.new_session()
                self.session_status.config(text="Estado: Activa")
                self._update_status("Nueva sesión iniciada")
                self.chat_widget._add_system_message("🆕 Nueva sesión iniciada")
        except Exception as e:
            logger.error(f"Error creating new session: {e}")
            messagebox.showerror("Error", f"Error creando nueva sesión: {e}")
    
    def _load_session(self):
        """📂 Cargar sesión"""
        try:
            file_path = filedialog.askopenfilename(
                title="Cargar Sesión",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                # Implementar carga real aquí
                self._update_status(f"Sesión cargada: {os.path.basename(file_path)}")
                self.chat_widget._add_system_message(f"📂 Sesión cargada: {os.path.basename(file_path)}")
                
        except Exception as e:
            logger.error(f"Error loading session: {e}")
            messagebox.showerror("Error", f"Error cargando sesión: {e}")
    
    def _save_session(self):
        """💾 Guardar sesión"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Guardar Sesión",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                # Implementar guardado real aquí
                session_data = {
                    "timestamp": datetime.now().isoformat(),
                    "messages": getattr(self.chat_controller, 'message_history', [])
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, indent=2, ensure_ascii=False)
                
                self._update_status(f"Sesión guardada: {os.path.basename(file_path)}")
                self.chat_widget._add_system_message(f"💾 Sesión guardada: {os.path.basename(file_path)}")
                
        except Exception as e:
            logger.error(f"Error saving session: {e}")
            messagebox.showerror("Error", f"Error guardando sesión: {e}")
    
    def _export_chat(self):
        """📤 Exportar chat"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Exportar Chat",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                # Get chat content
                chat_content = self.chat_widget.chat_display.get("1.0", tk.END)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Exportado desde IA Language Assistant\n")
                    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(chat_content)
                
                self._update_status(f"Chat exportado: {os.path.basename(file_path)}")
                messagebox.showinfo("Éxito", "Chat exportado correctamente")
                
        except Exception as e:
            logger.error(f"Error exporting chat: {e}")
            messagebox.showerror("Error", f"Error exportando chat: {e}")
    
    def _clear_chat(self):
        """🧹 Limpiar chat"""
        self.chat_widget._clear_chat()
    
    def _open_settings(self):
        """⚙️ Abrir configuraciones"""
        SettingsDialog(self.root)
    
    def _open_themes(self):
        """🎨 Abrir selector de temas"""
        themes = ['clam', 'alt', 'default', 'classic', 'vista', 'xpnative']
        current_theme = ttk.Style().theme_use()
        
        theme = messagebox.askquestion("Temas", 
                                      f"Tema actual: {current_theme}\n¿Cambiar tema?")
        if theme == 'yes':
            # Implementar selector de temas
            messagebox.showinfo("Info", "Selector de temas en desarrollo")
    
    def _toggle_side_panel(self):
        """👁️ Alternar panel lateral"""
        if self.side_panel.winfo_viewable():
            self.side_panel.pack_forget()
        else:
            self.side_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
    
    def _show_about(self):
        """ℹ️ Mostrar información"""
        about_text = """
IA Language Assistant v2.0

Una aplicación inteligente para practicar idiomas
con asistencia de inteligencia artificial.

Desarrollado con Python y Tkinter
        """
        messagebox.showinfo("Acerca de", about_text)
    
    def _update_status(self, message: str):
        """📊 Actualizar barra de estado"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_bar.config(text=f"[{timestamp}] {message}")
        self.root.update_idletasks()
    
    def _on_closing(self):
        """🚪 Manejar cierre de aplicación"""
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            try:
                if self.controller:
                    self.controller.end_session()
                logger.info("Aplicación cerrada correctamente")
                self.root.destroy()
            except Exception as e:
                logger.error(f"Error closing application: {e}")
                self.root.destroy()

# Función principal para ejecutar la aplicación
def main():
    """🚀 Función principal"""
    try:
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create and run application
        app = MainWindow()
        app.run()
        
    except Exception as e:
        logger.error(f"Error en función principal: {e}")
        messagebox.showerror("Error Fatal", f"Error iniciando aplicación: {e}")

if __name__ == "__main__":
    main()