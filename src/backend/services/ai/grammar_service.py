from transformers import pipeline
import torch
from typing import Optional, Dict, Any
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
    
    def correct_grammar(self, text: str, language: str = "en") -> str:
        """Corrige gramática con mejor manejo de contracciones"""
        try:
            # Prefijar texto para mejor contexto
            prompt = f"Please correct only the grammar and punctuation of this English sentence, keeping contractions like 'I'm', 'don't', etc.: '{text}'"
            
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=50,  # Reducir tokens para correcciones cortas
                    min_length=len(inputs[0]) + 5,
                    temperature=0.3,  # Más conservador
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2
                )
            
            corrected = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Limpiar la respuesta para extraer solo la corrección
            corrected = corrected.replace(prompt, "").strip()
            
            # Verificar que la corrección es válida
            if len(corrected) > len(text) * 2 or not corrected.strip():
                return text  # Devolver original si la corrección es extraña
            
            # Mantener contracciones comunes
            corrected = self._fix_contractions(corrected)
            
            return corrected.strip()
            
        except Exception as e:
            logger.error(f"Error en corrección gramatical: {e}")
            return text

    def _fix_contractions(self, text: str) -> str:
        """Arregla contracciones comunes"""
        contractions = {
            "I m": "I'm",
            "don t": "don't", 
            "can t": "can't",
            "won t": "won't",
            "isn t": "isn't",
            "aren t": "aren't",
            "doesn t": "doesn't",
            "haven t": "haven't",
            "hasn t": "hasn't"
        }
        
        for wrong, correct in contractions.items():
            text = text.replace(wrong, correct)
        
        return text
    
    def _process_and_feedback(self, user_response: str, input_method: str) -> Dict[str, Any]:
        """Procesa la respuesta y genera feedback inteligente"""
        detected_language = self._detect_language_simple(user_response)
        
        # Detectar si el usuario no entiende
        confusion_phrases = [
            "i don't understand", "i dont understand", "no entiendo", 
            "i'm confused", "im confused", "what", "que", "sorry", 
            "i didn't get it", "i didnt get it", "no comprendo",
            "can you repeat", "could you repeat", "puedes repetir"
        ]
        
        user_confused = any(phrase in user_response.lower() for phrase in confusion_phrases)
        
        # Procesar con los servicios del asistente
        result = self.assistant.process_user_input(user_response, detected_language)
        
        feedback = {
            'original': user_response,
            'language': detected_language,
            'input_method': input_method,
            'has_errors': bool(result.get('grammar_correction')),
            'translation': result.get('translation'),
            'correction': result.get('grammar_correction'),
            'improvement': result.get('improvement_detected'),
            'user_confused': user_confused,  # ← Nueva detección
            'quality': self._assess_response_quality(user_response, result, user_confused)
        }
        
        self._display_feedback(feedback)
        self._update_user_performance(feedback)
        
        return feedback

    def _assess_response_quality(self, response: str, result: Dict, user_confused: bool = False) -> str:
        """Evalúa la calidad de la respuesta"""
        # Si el usuario está confundido, marcarlo como necesita ayuda
        if user_confused:
            return "needs_help"
        
        word_count = len(response.split())
        has_errors = bool(result.get('grammar_correction'))
        
        if word_count < 3:
            return "too_short"
        elif word_count < 8 and not has_errors:
            return "good_short"
        elif word_count >= 8 and not has_errors:
            return "excellent"
        elif has_errors and word_count >= 5:
            return "good_with_errors"
        else:
            return "needs_improvement"