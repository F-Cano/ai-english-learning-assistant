"""
Translation service for text translation
"""
from typing import List, Optional
from core.events import EventManager
from core.state import AppState
from models.translation import Translation, TranslationStatus
from services.ollama_service import OllamaService
from utils.logger import logger
from utils.validators import validate_message


class TranslationService:
    """Service for text translation"""
    
    def __init__(self, event_manager: EventManager = None, app_state: AppState = None):
        self.event_manager = event_manager
        self.app_state = app_state
        self.ollama_service = OllamaService(event_manager=event_manager)
        self.translation_history: List[Translation] = []
        
        logger.info("TranslationService initialized")
    
    def translate(self, text: str, source_lang: str = "en", target_lang: str = "es") -> Translation:
        """Translate text from source to target language"""
        if not validate_message(text):
            raise ValueError("Invalid text content")
        
        logger.info(f"Translating text: {text[:50]}...")
        
        # Use Ollama service for translation
        translation = self.ollama_service.translate_text(text, source_lang, target_lang)
        
        # Add to history
        self.translation_history.append(translation)
        
        # Update state
        if self.app_state and translation.is_completed:
            self.app_state.increment('translations_made')
            self.app_state.set('last_translation', translation.translated_text)
        elif self.app_state and translation.is_failed:
            self.app_state.increment('errors_count')
        
        # Keep only recent translations
        if len(self.translation_history) > 50:
            self.translation_history = self.translation_history[-50:]
        
        return translation
    
    def translate_last_response(self) -> Optional[Translation]:
        """Translate the last assistant response"""
        if not self.app_state:
            logger.warning("No app state available for translation")
            return None
        
        last_response = self.app_state.get('last_response', '')
        if not last_response:
            logger.warning("No last response available for translation")
            return None
        
        return self.translate(last_response)
    
    def get_translation_history(self, count: int = 10) -> List[Translation]:
        """Get recent translation history"""
        return self.translation_history[-count:] if self.translation_history else []
    
    def clear_history(self) -> None:
        """Clear translation history"""
        self.translation_history.clear()
        logger.info("Translation history cleared")
    
    def get_status(self) -> dict:
        """Get translation service status"""
        ollama_status = self.ollama_service.get_status()
        
        return {
            'online': ollama_status['online'],
            'history_count': len(self.translation_history),
            'ollama': ollama_status
        }