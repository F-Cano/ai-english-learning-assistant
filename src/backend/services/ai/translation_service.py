"""
Translation Service usando Ollama
"""
import logging
from typing import Optional
from .ollama_service import OllamaService

logger = logging.getLogger(__name__)

class TranslationService:
    """Servicio de traduccion usando Ollama"""
    
    def __init__(self):
        self.ollama = OllamaService()
        self.translation_model = "llama2"
        logger.info("TranslationService inicializado con Ollama")
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Traduce texto usando Ollama"""
        try:
            return self.ollama.translate_text(text, source_lang, target_lang, self.translation_model)
        except Exception as e:
            logger.error(f"Error en traduccion: {e}")
            return text
