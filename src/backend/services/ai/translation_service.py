from transformers import pipeline
import torch
from ..interfaces.base import ITranslator
from ..config.settings import Settings
import logging

logger = logging.getLogger(__name__)

class TranslationService(ITranslator):
    def __init__(self, settings: Settings):
        self.settings = settings
        self._load_models()
    
    def _load_models(self):
        """Carga los modelos de traducción"""
        try:
            device = 0 if torch.cuda.is_available() else -1
            self.translator_en = pipeline(
                "translation", 
                model=self.settings.models.translator_en_model,
                device=device
            )
            self.translator_es = pipeline(
                "translation",
                model=self.settings.models.translator_es_model,
                device=device
            )
            logger.info("Translation models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading translation models: {e}")
            raise
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Traduce texto entre idiomas"""
        try:
            if source_lang == "es" and target_lang == "en":
                result = self.translator_en(text)[0]['translation_text']
            elif source_lang == "en" and target_lang == "es":
                result = self.translator_es(text)[0]['translation_text']
            else:
                logger.warning(f"Unsupported translation: {source_lang} -> {target_lang}")
                return text
            
            logger.info(f"Translated: {text[:30]}... -> {result[:30]}...")
            return result
            
        except Exception as e:
            logger.error(f"Error in translation: {e}")
            return text