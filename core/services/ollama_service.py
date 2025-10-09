"""
Real Ollama service integration
"""
import logging
import threading
import time
import requests
import json
from typing import Optional, Dict, Any, Callable
from core.events import AppEvent


class OllamaService:
    """Real Ollama service integration"""
    
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.logger = logging.getLogger('ia_assistant')
        self.is_connected = False
        self.is_busy = False
        self.ollama_url = "http://localhost:11434"
        
        # 🎯 TUS MODELOS DISPONIBLES
        self.available_models = ["llama2", "mistral"]
        self.current_model = "mistral"  # Mistral es más rápido
        
    def start(self) -> None:
        """Start and check Ollama service"""
        self.logger.info("Starting Ollama service connection")
        threading.Thread(target=self._check_connection, daemon=True).start()
        
    def stop(self) -> None:
        """Stop service"""
        self.is_connected = False
        self.event_manager.emit(AppEvent.OLLAMA_DISCONNECTED, {'reason': 'stopped'})
        self.logger.info("Ollama service stopped")
        
    def _check_connection(self) -> None:
        """Check if Ollama is running and models are available"""
        try:
            # Verificar si Ollama está corriendo
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models_data = response.json()
                installed_models = [model['name'].split(':')[0] for model in models_data.get('models', [])]
                
                self.logger.info(f"Found installed models: {installed_models}")
                
                # Verificar si tenemos nuestros modelos
                available = [model for model in self.available_models if model in installed_models]
                
                if available:
                    # Usar el primer modelo disponible
                    self.current_model = available[0]
                    self.is_connected = True
                    self.event_manager.emit(AppEvent.OLLAMA_CONNECTED, {
                        'status': 'connected',
                        'model': self.current_model,
                        'available_models': available
                    })
                    self.logger.info(f"Ollama connected with model: {self.current_model}")
                else:
                    self.logger.error(f"None of the required models {self.available_models} found. Install with: ollama pull mistral")
                    self._handle_connection_error("Required models not found")
            else:
                self._handle_connection_error(f"Ollama API returned {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self._handle_connection_error("Ollama service not running. Start with: ollama serve")
        except requests.exceptions.Timeout:
            self._handle_connection_error("Ollama connection timeout")
        except Exception as e:
            self._handle_connection_error(f"Unexpected error: {str(e)}")
    
    def _handle_connection_error(self, error_msg: str):
        """Handle connection errors"""
        self.is_connected = False
        self.event_manager.emit(AppEvent.OLLAMA_DISCONNECTED, {'reason': error_msg})
        self.logger.error(f"Ollama connection failed: {error_msg}")
        
    def send_message(self, message: str, callback: Optional[Callable] = None) -> None:
        """Send message to Ollama"""
        if not self.is_connected:
            self.event_manager.emit(AppEvent.MESSAGE_ERROR, {
                'message': 'Ollama not connected. Please start Ollama service: ollama serve'
            })
            return
            
        if self.is_busy:
            self.event_manager.emit(AppEvent.MESSAGE_ERROR, {
                'message': 'Service is busy, please wait'
            })
            return
            
        # Process in background
        threading.Thread(
            target=self._process_message, 
            args=(message, callback), 
            daemon=True
        ).start()
        
    def _process_message(self, message: str, callback: Optional[Callable]) -> None:
        """Process message with real Ollama"""
        try:
            if self.is_busy:
                return
                
            self.is_busy = True
            self.event_manager.emit(AppEvent.UI_BUSY, {})
            
            self.logger.info(f"Sending to {self.current_model}: {message[:50]}...")
            
            # 🎯 PROMPT ESPECIALIZADO PARA ASISTENTE DE INGLÉS BILINGÜE
            system_prompt = """Eres Alex, un asistente bilingüe especializado en ayudar a aprender inglés. Tu misión es adaptarte al nivel y necesidades del usuario:

🎯 PRINCIPIOS CLAVE:
1. **Comprende AMBOS idiomas**: Español e inglés perfectamente
2. **Responde inteligentemente**: Usa el idioma que mejor sirva al usuario en cada momento
3. **Adapta tu ayuda**: Según el nivel y contexto de cada mensaje

📋 COMPORTAMIENTO POR SITUACIÓN:

**Cuando el usuario escribe en ESPAÑOL:**
- Responde en español de forma natural Y ofrece la versión en inglés cuando sea educativo
- Ejemplo: "¡Hola! ¿Cómo estás? (Hello! How are you?)"

**Cuando el usuario escribe en INGLÉS:**
- Responde en inglés y ayuda con correcciones si las necesita
- Si hay errores, corrígelos gentilmente y explica brevemente

**Cuando el usuario MEZCLA idiomas o pide ayuda específica:**
- Usa ambos idiomas para maximizar el aprendizaje
- Proporciona traducciones, explicaciones y ejemplos según sea necesario

**Para CUALQUIER pregunta sobre gramática, vocabulario o cultura:**
- Explica en el idioma que el usuario mejor entienda
- Siempre incluye ejemplos en ambos idiomas cuando sea útil

🎨 PERSONALIDAD: Amigable, paciente, educativo pero no abrumador. Máximo 2 emojis por mensaje.

Mensaje del usuario:"""
            
            full_prompt = f"{system_prompt} {message}"
            
            # Hacer request a Ollama
            response = self._call_ollama_api(full_prompt)
            
            if response:
                # Limpiar respuesta
                clean_response = response.strip()
                if clean_response:
                    # Emit successful response
                    self.event_manager.emit(AppEvent.MESSAGE_RECEIVED, {
                        'message': clean_response,
                        'sender': 'Alex',
                        'model': self.current_model
                    })
                    
                    self.logger.info(f"Response received from {self.current_model}")
                    
                    if callback:
                        callback(clean_response)
                else:
                    raise Exception("Empty response from Ollama")
            else:
                raise Exception("No response from Ollama")
                
        except Exception as e:
            error_msg = f'Error processing with {self.current_model}: {str(e)}'
            self.logger.error(error_msg)
            self.event_manager.emit(AppEvent.MESSAGE_ERROR, {
                'message': error_msg
            })
        finally:
            self.is_busy = False
            self.event_manager.emit(AppEvent.UI_READY, {})
    
    def _call_ollama_api(self, prompt: str) -> Optional[str]:
        """Call Ollama API and get response"""
        try:
            payload = {
                "model": self.current_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,  # Creatividad moderada
                    "top_p": 0.9,
                    "max_tokens": 500    # Respuestas concisas
                }
            }
            
            self.logger.debug(f"Calling Ollama API with model: {self.current_model}")
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60  # 60 segundos para respuestas largas
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                self.logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            self.logger.error("Ollama request timed out (60s)")
            return None
        except requests.exceptions.ConnectionError:
            self.logger.error("Lost connection to Ollama during request")
            return None
        except Exception as e:
            self.logger.error(f"Error calling Ollama API: {e}")
            return None
    
    def switch_model(self, model_name: str) -> bool:
        """Switch to different model"""
        if model_name in self.available_models:
            self.current_model = model_name
            self.logger.info(f"Switched to model: {model_name}")
            return True
        return False
            
    def get_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            'connected': self.is_connected,
            'busy': self.is_busy,
            'service': 'ollama_real',
            'current_model': self.current_model,
            'available_models': self.available_models,
            'url': self.ollama_url
        }