"""
Ollama service for LLM communication
"""
import requests
import time
from typing import List, Dict, Any, Optional
from config import config
from core.events import EventManager, AppEvent
from core.exceptions import OllamaConnectionError, OllamaTimeoutError, ModelNotFoundError
from models.message import Message, MessageType
from models.translation import Translation, TranslationStatus
from utils.logger import logger
from utils.validators import validate_message, validate_url


class OllamaService:
    """Service for communicating with Ollama LLM"""
    
    def __init__(self, base_url: str = None, event_manager: EventManager = None):
        self.base_url = base_url or config.get_ollama_config()['base_url']
        self.event_manager = event_manager
        self.available_models: List[str] = []
        self.default_model: Optional[str] = None
        self.model_config = config.get_model_config()
        self.ollama_config = config.get_ollama_config()
        
        # Validate configuration
        if not validate_url(self.base_url):
            raise OllamaConnectionError(f"Invalid Ollama URL: {self.base_url}")
        
        logger.info(f"OllamaService initialized with URL: {self.base_url}")
        self._initialize_service()
    
    def _initialize_service(self) -> None:
        """Initialize the Ollama service"""
        try:
            if self._check_connection():
                self._load_available_models()
                logger.info("OllamaService initialized successfully")
            else:
                logger.warning("Failed to connect to Ollama during initialization")
                self._emit_disconnected_event()
        except Exception as e:
            logger.error(f"Error initializing OllamaService: {e}")
            self._emit_error_event(str(e))
    
    def _check_connection(self) -> bool:
        """Check connection to Ollama server"""
        try:
            timeout = self.ollama_config['connection_timeout']
            response = requests.get(
                f"{self.base_url}/api/tags", 
                timeout=timeout
            )
            
            if response.status_code == 200:
                logger.info("Connection to Ollama established")
                return True
            else:
                logger.error(f"Ollama responded with status: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout connecting to Ollama ({timeout}s)")
            return False
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama - is it running?")
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to Ollama: {e}")
            return False
    
    def _load_available_models(self) -> None:
        """Load available models from Ollama"""
        max_retries = self.ollama_config['max_retries']
        retry_delay = self.ollama_config['retry_delay']
        
        for attempt in range(max_retries):
            try:
                timeout = self.ollama_config['connection_timeout'] + (attempt * 5)
                response = requests.get(
                    f"{self.base_url}/api/tags", 
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    models_data = data.get('models', [])
                    self.available_models = [model['name'] for model in models_data]
                    self._select_best_model()
                    
                    self._emit_connected_event()
                    logger.info(f"Loaded {len(self.available_models)} models")
                    return
                else:
                    logger.warning(f"Unexpected response on attempt {attempt + 1}: {response.status_code}")
                    
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
        
        logger.error("Failed to load models after all attempts")
        self._emit_error_event("Failed to load models")
        self.available_models = []
    
    def _select_best_model(self) -> None:
        """Select the best available model"""
        if not self.available_models:
            logger.warning("No models available for selection")
            return
        
        preferred_order = self.model_config['preferred_order']
        
        # Find first preferred model that's available
        for preferred_model in preferred_order:
            for available_model in self.available_models:
                if preferred_model.lower() in available_model.lower():
                    self.default_model = available_model
                    logger.info(f"Selected model: {self.default_model}")
                    return
        
        # If no preferred model found, use first available
        if self.available_models:
            self.default_model = self.available_models[0]
            logger.info(f"Using first available model: {self.default_model}")
    
    def _create_chat_payload(self, message: str, model: str) -> Dict[str, Any]:
        """Create payload for chat request"""
        ai_prompts = config.get_ai_prompts()
        
        return {
            "model": model,
            "prompt": f"System: {ai_prompts['system_chat']}\n\nUser: {message}\n\nAlex:",
            "stream": False,
            "options": {
                "temperature": self.model_config['temperature_chat'],
                "max_tokens": self.model_config['max_tokens_chat'],
                "top_p": self.model_config['top_p']
            }
        }
    
    def _create_translation_payload(self, text: str, target_lang: str, model: str) -> Dict[str, Any]:
        """Create payload for translation request"""
        ai_prompts = config.get_ai_prompts()
        prompt = ai_prompts['translation_simple'].format(
            target_lang=target_lang,
            text=text
        )
        
        return {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.model_config['temperature_translation'],
                "max_tokens": self.model_config['max_tokens_translation'],
                "top_p": self.model_config['top_p']
            }
        }
    
    def _make_request(self, payload: Dict[str, Any], timeout: int) -> str:
        """Make HTTP request to Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                logger.error(f"HTTP error {response.status_code} from Ollama")
                return ""
                
        except requests.exceptions.Timeout:
            logger.warning(f"Request timeout ({timeout}s)")
            raise OllamaTimeoutError(f"Request timed out after {timeout}s")
        except requests.exceptions.ConnectionError:
            logger.error("Connection error with Ollama")
            raise OllamaConnectionError("Failed to connect to Ollama")
        except Exception as e:
            logger.error(f"Unexpected error in request: {e}")
            raise
    
    def generate_response(self, message: str, model: str = None) -> str:
        """Generate response for user message"""
        if not validate_message(message):
            raise ValueError("Invalid message content")
        
        # Emit sending event
        self._emit_sending_event(message)
        
        try:
            model = model or self.default_model
            if not model:
                raise ModelNotFoundError("No model available")
            
            payload = self._create_chat_payload(message, model)
            timeout = self.ollama_config['generation_timeout']
            
            logger.info(f"Generating response with {model}")
            response = self._make_request(payload, timeout)
            
            if response:
                logger.info("Response generated successfully")
                self._emit_received_event(response)
                return response
            else:
                error_msg = "Empty response from model"
                logger.error(error_msg)
                self._emit_error_event(error_msg)
                return "Sorry, I couldn't generate a response. Please try again."
                
        except OllamaTimeoutError:
            error_msg = "Response timeout"
            logger.error(error_msg)
            self._emit_error_event(error_msg)
            return "I'm taking too long to respond. Please try a shorter message."
        except Exception as e:
            error_msg = f"Error generating response: {e}"
            logger.error(error_msg)
            self._emit_error_event(error_msg)
            return "Sorry, there was an error processing your message."
    
    def translate_text(self, text: str, source_lang: str = "en", target_lang: str = "es") -> Translation:
        """Translate text using multiple models"""
        translation = Translation(
            original_text=text,
            source_language=source_lang,
            target_language=target_lang,
            status=TranslationStatus.PENDING
        )
        
        if not validate_message(text):
            translation.mark_failed("Invalid text content")
            return translation
        
        # Emit start event
        self._emit_translation_start_event(text)
        translation.status = TranslationStatus.IN_PROGRESS
        
        # Get models to try
        models_to_try = self._get_translation_models()
        timeouts = self.model_config['translation_timeouts']
        
        # Ensure enough timeouts
        while len(timeouts) < len(models_to_try):
            timeouts.append(timeouts[-1] + 15)
        
        logger.info(f"Starting translation with {len(models_to_try)} models")
        
        for attempt, (model, timeout) in enumerate(zip(models_to_try, timeouts)):
            try:
                payload = self._create_translation_payload(text, target_lang, model)
                
                logger.info(f"Translation attempt {attempt + 1}: {model} (timeout: {timeout}s)")
                translated_text = self._make_request(payload, timeout)
                
                if translated_text and translated_text != text:
                    logger.info(f"Translation successful with {model}")
                    translation.mark_completed(translated_text, model)
                    self._emit_translation_success_event(translation)
                    return translation
                else:
                    logger.warning(f"Empty or unchanged translation with {model}")
                    
            except Exception as e:
                logger.warning(f"Translation error with {model}: {e}")
                continue
        
        # All attempts failed
        error_msg = "Translation failed with all models"
        logger.error(error_msg)
        translation.mark_failed(error_msg)
        self._emit_translation_error_event(error_msg)
        return translation
    
    def _get_translation_models(self) -> List[str]:
        """Get list of models for translation"""
        models = []
        
        # Add default model
        if self.default_model:
            models.append(self.default_model)
        
        # Add specific preferred models
        preferred = ["mistral", "llama2"]
        for model_name in preferred:
            for available in self.available_models:
                if (model_name in available.lower() and 
                    available not in models):
                    models.append(available)
        
        return models if models else ["mistral"]  # Fallback
    
    def is_online(self) -> bool:
        """Check if Ollama is online"""
        return self._check_connection()
    
    def get_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            'online': self.is_online(),
            'models_count': len(self.available_models),
            'default_model': self.default_model,
            'base_url': self.base_url,
            'available_models': self.available_models,
            'config': self.ollama_config
        }
    
    def refresh_models(self) -> None:
        """Refresh models list"""
        logger.info("Refreshing models list...")
        self._load_available_models()
    
    # Event emission methods
    def _emit_connected_event(self) -> None:
        """Emit connected event"""
        if self.event_manager:
            self.event_manager.emit(AppEvent.OLLAMA_CONNECTED, {
                'models': self.available_models,
                'current_model': self.default_model,
                'models_count': len(self.available_models)
            })
    
    def _emit_disconnected_event(self) -> None:
        """Emit disconnected event"""
        if self.event_manager:
            self.event_manager.emit(AppEvent.OLLAMA_DISCONNECTED)
    
    def _emit_error_event(self, error: str) -> None:
        """Emit error event"""
        if self.event_manager:
            self.event_manager.emit(AppEvent.OLLAMA_ERROR, {'error': error})
    
    def _emit_sending_event(self, message: str) -> None:
        """Emit message sending event"""
        if self.event_manager:
            self.event_manager.emit(AppEvent.MESSAGE_SENDING, {'message': message})
    
    def _emit_received_event(self, response: str) -> None:
        """Emit message received event"""
        if self.event_manager:
            self.event_manager.emit(AppEvent.MESSAGE_RECEIVED, {'response': response})
    
    def _emit_translation_start_event(self, text: str) -> None:
        """Emit translation start event"""
        if self.event_manager:
            self.event_manager.emit(AppEvent.TRANSLATION_START, {'text': text})
    
    def _emit_translation_success_event(self, translation: Translation) -> None:
        """Emit translation success event"""
        if self.event_manager:
            self.event_manager.emit(AppEvent.TRANSLATION_SUCCESS, {
                'translation': translation.translated_text,
                'model_used': translation.model_used
            })
    
    def _emit_translation_error_event(self, error: str) -> None:
        """Emit translation error event"""
        if self.event_manager:
            self.event_manager.emit(AppEvent.TRANSLATION_ERROR, {'error': error})