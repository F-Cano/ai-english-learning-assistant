from abc import ABC, abstractmethod
from typing import Tuple, List, Optional, Dict, Any
import numpy as np

class ISpeechToText(ABC):
    @abstractmethod
    def recognize(self, audio_data: np.ndarray) -> Tuple[str, str]:
        """Convierte audio a texto y detecta idioma"""
        pass

class ITextToSpeech(ABC):
    @abstractmethod
    def speak(self, text: str, language: str = "en") -> None:
        """Convierte texto a voz"""
        pass

class ITranslator(ABC):
    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Traduce texto entre idiomas"""
        pass

class IGrammarCorrector(ABC):
    @abstractmethod
    def correct(self, text: str) -> Optional[str]:
        """Corrige errores gramaticales"""
        pass

class IChatGenerator(ABC):
    @abstractmethod
    def generate_response(self, context: str, user_input: str) -> str:
        """Genera respuesta conversacional"""
        pass

class IErrorTracker(ABC):
    @abstractmethod
    def register_error(self, original: str, correction: str) -> None:
        """Registra un error cometido"""
        pass
    
    @abstractmethod
    def get_frequent_errors(self, threshold: int = 3) -> Dict[str, Any]:
        """Obtiene errores frecuentes"""
        pass