"""
Grammar Service usando Ollama
"""
import logging
from typing import Optional
from .ollama_service import OllamaService

logger = logging.getLogger(__name__)

class GrammarService:
    """Servicio de correccion gramatical usando Ollama"""
    
    def __init__(self):
        self.ollama = OllamaService()
        self.grammar_model = "llama2"
        logger.info("GrammarService inicializado con Ollama")
    
    def correct(self, text: str) -> Optional[str]:
        """Corrige gramatica usando Ollama"""
        try:
            corrected = self.ollama.correct_grammar(text, self.grammar_model)
            
            if corrected.strip().lower() == text.strip().lower():
                return None
            
            return corrected
        except Exception as e:
            logger.error(f"Error en correccion gramatical: {e}")
            return None
