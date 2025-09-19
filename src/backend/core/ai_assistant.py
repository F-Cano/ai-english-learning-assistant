from typing import List, Optional, Dict, Any
import logging
from ..services.audio_service import AudioRecorder, WhisperSTT, GTTSService
from ..services.error_service import ErrorMemoryService
from ..services.translation_service import TranslationService
from ..services.grammar_service import GrammarService
from ..services.chat_service import ChatService
from ..config.settings import Settings

logger = logging.getLogger(__name__)

class AIAssistant:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.conversation_history: List[str] = []
        self._initialize_services()
    
    def _initialize_services(self):
        """Inicializa todos los servicios necesarios"""
        try:
            print("â³ Inicializando servicios...")
            
            # Servicios de audio
            self.audio_recorder = AudioRecorder(self.settings)
            self.stt_service = WhisperSTT(self.settings.models.whisper_model)
            self.tts_service = GTTSService(self.settings)
            
            # Servicios de procesamiento
            self.error_service = ErrorMemoryService(
                self.settings.paths.working_dir / self.settings.paths.errors_file
            )
            self.translation_service = TranslationService(self.settings)
            self.grammar_service = GrammarService(self.settings)
            self.chat_service = ChatService(self.settings)
            
            print("âœ… Servicios inicializados correctamente")
            logger.info("All services initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing services: {e}")
            raise
    
    def listen(self) -> tuple[str, str]:
        """Escucha y procesa audio del usuario"""
        audio_data = self.audio_recorder.record_audio()
        return self.stt_service.recognize(audio_data)
    
    def speak(self, text: str, language: str = "en") -> None:
        """Habla usando TTS"""
        self.tts_service.speak(text, language)
    
    def process_user_input(self, text: str, language: str) -> Dict[str, Any]:
        """Procesa entrada del usuario y genera respuesta completa"""
        result = {
            "original_text": text,
            "detected_language": language,
            "translation": None,
            "grammar_correction": None,
            "improvement_detected": False,
            "response": None
        }
        
        # Verificar mejoras
        if language.startswith("en"):
            result["improvement_detected"] = self.error_service.check_improvement(text)
            
            # Traducir al espaÃ±ol para comprensiÃ³n
            result["translation"] = self.translation_service.translate(text, "en", "es")
            
            # Corregir gramÃ¡tica
            correction = self.grammar_service.correct(text)
            if correction:
                result["grammar_correction"] = correction
                self.error_service.register_error(text, correction)
            
            # Generar respuesta
            result["response"] = self.chat_service.generate_response(
                " ".join(self.conversation_history[-6:]), text
            )
            
            # Actualizar historial
            self.conversation_history.append(text)
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
        elif language.startswith("es"):
            # Traducir al inglÃ©s
            result["translation"] = self.translation_service.translate(text, "es", "en")
        
        return result
    
    def training_mode(self):
        """Modo de entrenamiento estructurado"""
        from ..modes.training_mode import TrainingMode
        training = TrainingMode(self)
        training.run()
    
    def free_mode(self):
        """Modo de conversaciÃ³n libre"""
        from ..modes.conversation_mode import ConversationMode
        conversation = ConversationMode(self)
        conversation.run()
    
    def interactive_mode(self):
        """Modo interactivo híbrido (voz + teclado)"""
        from ..modes.interactive_mode import InteractiveMode
        interactive = InteractiveMode(self)
        interactive.run()
    
    def show_session_summary(self):
        """Muestra resumen de la sesiÃ³n"""
        summary = self.error_service.get_session_summary()
        print(f"\nðŸ“Š Resumen de la sesiÃ³n:")
        print(f"âš  Errores frecuentes: {summary['frequent']}")
        print(f"ðŸ”„ Errores ocasionales: {summary['occasional']}")
        print(f"ðŸ“ˆ Total de errores Ãºnicos: {summary['total']}")
    
    def run(self):
        """Bucle principal del asistente"""
        print("🎯 ¿Qué modo quieres usar?")
        print("1. 🎓 Modo entrenamiento (preguntas estructuradas)")
        print("2. 💬 Modo conversación libre")
        print("3. 🎮 Modo interactivo híbrido (NUEVO)")  # ← Nueva opción
        print("4. ❌ Salir")
        
        choice = input("\nElige una opción (1-4): ").strip()
        
        if choice == "1":
            self.training_mode()
        elif choice == "2":
            self.free_mode()
        elif choice == "3":
            self.interactive_mode()  # ← Nueva funcionalidad
        elif choice == "4":
            print("👋 ¡Hasta luego!")
            return
        else:
            print("❌ Opción inválida")
            self.run()