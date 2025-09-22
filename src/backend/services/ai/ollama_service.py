"""
Ollama Service - Servicio unico de IA
"""
import requests
import json
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)

class OllamaService:
    """Servicio unico para Ollama - Simple y confiable"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.default_model = "mistral"
        self.available_models = []
        self._load_models()
    
    def _load_models(self) -> None:
        """Cargar modelos disponibles"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.available_models = [m['name'] for m in data.get('models', [])]
                logger.info(f"Modelos disponibles: {len(self.available_models)}")
                
                # Seleccionar mejor modelo disponible
                preferred = ["mistral", "llama3", "llama2", "gemma"]
                for model in preferred:
                    for available in self.available_models:
                        if model in available.lower():
                            self.default_model = available
                            break
                    if self.default_model != "mistral":
                        break
                        
        except Exception as e:
            logger.warning(f"No se pudieron cargar modelos: {e}")
    
    def is_online(self) -> bool:
        """Verificar si Ollama esta disponible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def chat(self, message: str, model: Optional[str] = None) -> str:
        """Chat principal con Ollama"""
        if not model:
            model = self.default_model
            
        try:
            # System prompt para enseñanza de inglés
            system_prompt = """You are Alex, a friendly English conversation partner and teacher.
            
Your goals:
- Help Spanish speakers practice English naturally
- Provide clear, encouraging responses  
- Correct grammar gently when needed
- Ask follow-up questions to continue conversation
- Keep responses conversational and educational

Always respond in English unless specifically asked to translate."""

            payload = {
                "model": model,
                "prompt": f"System: {system_prompt}\n\nUser: {message}\n\nAlex:",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 300,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'I apologize, but I could not generate a response.')
            else:
                return f"Sorry, I'm having technical difficulties (Error {response.status_code})"
                
        except requests.exceptions.Timeout:
            return "I'm thinking a bit slowly right now. Please try again in a moment."
        except requests.exceptions.ConnectionError:
            return "I can't connect to my brain right now. Please make sure Ollama is running."
        except Exception as e:
            return f"Oops! Something went wrong: {str(e)}"
    
    def translate(self, text: str, source_lang: str = "en", target_lang: str = "es") -> str:
        """Traducir texto usando Ollama"""
        try:
            prompt = f"Translate this text from {source_lang} to {target_lang}. Only provide the translation: {text}"
            
            payload = {
                "model": self.default_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "max_tokens": 200
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                translation = result.get('response', text).strip()
                return translation
            else:
                return text  # Devolver original si falla
                
        except Exception as e:
            logger.error(f"Error en traduccion: {e}")
            return text  # Devolver original si falla
    
    def get_models(self) -> List[str]:
        """Obtener lista de modelos"""
        return self.available_models
    
    def get_status(self) -> dict:
        """Obtener estado completo"""
        return {
            'online': self.is_online(),
            'models': len(self.available_models),
            'default_model': self.default_model,
            'url': self.base_url
        }
