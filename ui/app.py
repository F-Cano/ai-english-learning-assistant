"""
Main UI application class
"""
import tkinter as tk
from tkinter import messagebox
import threading
import time
from typing import Optional
from datetime import datetime
from core.state import AppState
from core.events import EventManager, AppEvent
from services.chat_service import ChatService
from services.translation_service import TranslationService
from ui.components.header import HeaderComponent
from ui.components.chat_display import ChatDisplayComponent
from ui.components.input_area import InputAreaComponent
from ui.components.footer import FooterComponent
from config import config
from utils.logger import logger


class EnglishAssistantApp:
    """Main English Assistant application"""
    
    def __init__(self):
        # Core system
        self.app_state = AppState()
        self.event_manager = EventManager()
        
        # Services
        self.chat_service: Optional[ChatService] = None
        self.translation_service: Optional[TranslationService] = None
        
        # UI
        self.root: Optional[tk.Tk] = None
        self.colors = config.get_color_scheme()
        
        # Components
        self.header: Optional[HeaderComponent] = None
        self.chat_display: Optional[ChatDisplayComponent] = None
        self.input_area: Optional[InputAreaComponent] = None
        self.footer: Optional[FooterComponent] = None
        
        # State
        self._is_running = False
        self._status_thread: Optional[threading.Thread] = None
        
        logger.info("EnglishAssistantApp initialized")
    
    def initialize(self) -> None:
        """Initialize the application"""
        try:
            logger.info("Initializing application...")
            
            self._setup_window()
            self._create_services()
            self._create_ui_components()
            self._start_background_tasks()
            
            # Mark as initialized
            self.app_state.set('ui_initialized', True)
            self.event_manager.emit(AppEvent.UI_READY)
            
            logger.info("Application initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}")
            raise
    
    def _setup_window(self) -> None:
        """Setup main window"""
        self.root = tk.Tk()
        self.root.title(config.WINDOW_CONFIG['title'])
        self.root.geometry(config.get_window_geometry())
        self.root.configure(bg=self.colors['bg'])
        
        # Set minimum size
        self.root.minsize(
            config.WINDOW_CONFIG['min_width'],
            config.WINDOW_CONFIG['min_height']
        )
        
        # Center window
        self._center_window()
        
        # Set close handler
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        logger.debug("Main window setup complete")
    
    def _center_window(self) -> None:
        """Center window on screen"""
        self.root.update_idletasks()
        
        window_width = config.WINDOW_CONFIG['width']
        window_height = config.WINDOW_CONFIG['height']
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def _create_services(self) -> None:
        """Create and initialize services"""
        try:
            self.chat_service = ChatService(
                event_manager=self.event_manager,
                app_state=self.app_state
            )
            
            self.translation_service = TranslationService(
                event_manager=self.event_manager,
                app_state=self.app_state
            )
            
            logger.info("Services created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create services: {e}")
            raise
    
    def _create_ui_components(self) -> None:
        """Create UI components"""
        try:
            # Main container
            main_frame = tk.Frame(self.root, bg=self.colors['bg'])
            main_frame.pack(fill='both', expand=True, 
                           padx=config.UI_CONFIG['padding'], 
                           pady=config.UI_CONFIG['padding'])
            
            # Create components
            self.header = HeaderComponent(
                main_frame, self.colors, 
                self.app_state, self.event_manager
            )
            header_frame = self.header.create()
            header_frame.pack(fill='x', pady=(0, config.UI_CONFIG['padding']))
            
            self.chat_display = ChatDisplayComponent(
                main_frame, self.colors,
                self.app_state, self.event_manager
            )
            chat_frame = self.chat_display.create()
            chat_frame.pack(fill='both', expand=True, 
                           pady=(0, config.UI_CONFIG['padding']))
            
            self.input_area = InputAreaComponent(
                main_frame, self.colors,
                self.app_state, self.event_manager,
                send_callback=self._send_message,
                translate_callback=self._translate_last_response
            )
            input_frame = self.input_area.create()
            input_frame.pack(fill='x', pady=(0, config.UI_CONFIG['small_padding']))
            
            self.footer = FooterComponent(
                main_frame, self.colors,
                self.app_state, self.event_manager
            )
            footer_frame = self.footer.create()
            footer_frame.pack(fill='x')
            
            # Set initial focus
            self.input_area.focus_input()
            
            # Mark components as ready
            self.app_state.set('components_ready', True)
            logger.info("UI components created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create UI components: {e}")
            raise
    
    def _start_background_tasks(self) -> None:
        """Start background tasks"""
        self._is_running = True
        
        # Start status monitoring thread
        self._status_thread = threading.Thread(
            target=self._status_monitor_loop,
            daemon=True
        )
        self._status_thread.start()
        
        logger.debug("Background tasks started")
    
    def _status_monitor_loop(self) -> None:
        """Background status monitoring loop"""
        while self._is_running:
            try:
                if self.chat_service:
                    is_online = self.chat_service.is_online()
                    current_online = self.app_state.get('ollama_online', False)
                    
                    if is_online != current_online:
                        if is_online:
                            # Service came online
                            status = self.chat_service.get_status()
                            ollama_info = status.get('ollama', {})
                            
                            self.event_manager.emit(AppEvent.OLLAMA_CONNECTED, {
                                'models': ollama_info.get('available_models', []),
                                'current_model': ollama_info.get('default_model'),
                                'models_count': ollama_info.get('models_count', 0)
                            })
                        else:
                            # Service went offline
                            self.event_manager.emit(AppEvent.OLLAMA_DISCONNECTED)
                
                # Sleep for configured interval
                time.sleep(config.OLLAMA_CONFIG['status_check_interval'])
                
            except Exception as e:
                logger.warning(f"Error in status monitor: {e}")
                time.sleep(5)  # Shorter sleep on error
    
    def _send_message(self, message: str = None) -> None:
        """Send message handler"""
        if message is None:
            message = self.input_area.get_text() if self.input_area else ""
        
        if not message.strip():
            return
        
        # Process message in background thread
        threading.Thread(
            target=self._process_message,
            args=(message,),
            daemon=True
        ).start()
    
    def _process_message(self, message: str) -> None:
        """Process message in background thread"""
        try:
            if self.chat_service:
                response_message = self.chat_service.send_message(message)
                logger.debug(f"Message processed: {response_message.status}")
            else:
                logger.error("Chat service not available")
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            self.event_manager.emit(AppEvent.MESSAGE_ERROR, {'error': str(e)})
    
    def _translate_last_response(self) -> None:
        """Translate last response handler"""
        if not self.translation_service:
            logger.error("Translation service not available")
            return
        
        # Process translation in background thread
        threading.Thread(
            target=self._process_translation,
            daemon=True
        ).start()
    
    def _process_translation(self) -> None:
        """Process translation in background thread"""
        try:
            if self.translation_service:
                translation = self.translation_service.translate_last_response()
                if translation:
                    logger.debug(f"Translation processed: {translation.status}")
                else:
                    logger.warning("No translation result")
            else:
                logger.error("Translation service not available")
                
        except Exception as e:
            logger.error(f"Error processing translation: {e}")
            self.event_manager.emit(AppEvent.TRANSLATION_ERROR, {'error': str(e)})
    
    def _on_closing(self) -> None:
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            logger.info("Application closing by user request")
            
            # Show session summary
            self._show_session_summary()
            
            # Stop background tasks
            self._is_running = False
            
            # Cleanup components
            self._cleanup_components()
            
            # Destroy window
            if self.root:
                self.root.destroy()
    
    def _show_session_summary(self) -> None:
        """Show session summary in console"""
        try:
            summary = self.app_state.get_summary()
            
            print("\n" + "="*50)
            print("SESSION SUMMARY")
            print("="*50)
            print(f"Messages sent: {summary['session']['messages_sent']}")
            print(f"Translations made: {summary['session']['translations_made']}")
            print(f"Errors encountered: {summary['session']['errors_count']}")
            print(f"Session duration: {summary['session']['uptime']}")
            print(f"Connection status: {'Online' if summary['connection']['online'] else 'Offline'}")
            print(f"Models available: {summary['connection']['models']}")
            print("="*50)
            
        except Exception as e:
            logger.error(f"Error showing session summary: {e}")
    
    def _cleanup_components(self) -> None:
        """Cleanup UI components"""
        try:
            components = [self.header, self.chat_display, self.input_area, self.footer]
            
            for component in components:
                if component:
                    component.destroy()
            
            logger.debug("UI components cleaned up")
            
        except Exception as e:
            logger.error(f"Error cleaning up components: {e}")
    
    def run(self) -> None:
        """Run the application"""
        try:
            logger.info("Starting English Assistant application...")
            self.initialize()
            
            if self.root:
                self.root.mainloop()
            
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise
        finally:
            self._is_running = False
            logger.info("Application stopped")