"""
Chat Service - Interfaz simple para la UI
"""
from .ollama_service import OllamaService
import logging

logger = logging.getLogger(__name__)

class ChatService:
    """Servicio de chat simple y directo"""
    
    def __init__(self):
        self.ollama = OllamaService()
        logger.info("ChatService inicializado")
    
    def send_message(self, message: str) -> str:
        """Enviar mensaje y obtener respuesta"""
        if not message.strip():
            return "Please send a message!"
        
        return self.ollama.chat(message)
    
    def translate_message(self, message: str, source: str = "en", target: str = "es") -> str:
        """Traducir mensaje"""
        return self.ollama.translate(message, source, target)
    
    def is_online(self) -> bool:
        """Verificar si esta online"""
        return self.ollama.is_online()
    
    def get_status(self) -> dict:
        """Obtener estado del servicio"""
        return self.ollama.get_status()
    
    def get_models(self) -> list:
        """Obtener modelos disponibles"""
        return self.ollama.get_models()
