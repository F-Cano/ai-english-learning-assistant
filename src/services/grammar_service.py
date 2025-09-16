from transformers import pipeline
import torch
from typing import Optional
from ..interfaces.base import IGrammarCorrector
from ..config.settings import Settings
import logging

logger = logging.getLogger(__name__)

class GrammarService(IGrammarCorrector):
    def __init__(self, settings: Settings):
        self.settings = settings
        self._load_model()
    
    def _load_model(self):
        """Carga el modelo de corrección gramatical"""
        try:
            device = 0 if torch.cuda.is_available() else -1
            self.grammar_corrector = pipeline(
                "text2text-generation",
                model=self.settings.models.grammar_model,
                device=device
            )
            logger.info("Grammar correction model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading grammar model: {e}")
            raise
    
    def correct(self, text: str) -> Optional[str]:
        """Corrige errores gramaticales en inglés"""
        try:
            correction = self.grammar_corrector(text)[0]['generated_text']
            if correction.lower() != text.lower():
                logger.info(f"Grammar correction: {text} -> {correction}")
                return correction
            return None
        except Exception as e:
            logger.error(f"Error in grammar correction: {e}")
            return None