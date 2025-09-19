"""
Message Processor - Procesamiento de mensajes de usuario
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class MessageProcessor:
    """ Procesador de mensajes de usuario"""
    
    def __init__(self):
        logger.info("MessageProcessor inicializado")
    
    def process_user_message(self, user_input: str) -> Dict[str, Any]:
        """ Procesa mensaje del usuario"""
        try:
            cleaned_input = user_input.strip()
            
            return {
                "original_input": user_input,
                "cleaned_input": cleaned_input,
                "word_count": len(cleaned_input.split()),
                "character_count": len(cleaned_input),
                "has_punctuation": any(char in cleaned_input for char in ".,!?;:"),
                "processing_success": True
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "original_input": user_input,
                "cleaned_input": user_input,
                "processing_success": False,
                "error": str(e)
            }
