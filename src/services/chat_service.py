from transformers import pipeline
import torch
from ..interfaces.base import IChatGenerator
from ..config.settings import Settings
import logging

logger = logging.getLogger(__name__)

class ChatService(IChatGenerator):
    def __init__(self, settings: Settings):
        self.settings = settings
        self._load_model()
    
    def _load_model(self):
        """Carga el modelo de generación de chat"""
        try:
            device = 0 if torch.cuda.is_available() else -1
            self.chat_model = pipeline(
                "text-generation",
                model=self.settings.models.chat_model,
                device=device
            )
            logger.info("Chat model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading chat model: {e}")
            raise
    
    def generate_response(self, context: str, user_input: str) -> str:
        """Genera una respuesta conversacional"""
        try:
            input_text = context + " " + user_input if context else user_input
            response = self.chat_model(
                input_text, 
                max_length=150, 
                pad_token_id=50256
            )[0]['generated_text']
            
            # Extraer solo la respuesta nueva
            if context:
                response = response[len(input_text):].strip()
            
            logger.info(f"Generated response: {response[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I couldn't generate a response."