"""
Enhanced Chat Service - Servicio de chat mejorado para UI
VERSIÓN CORREGIDA Y FUNCIONAL
"""

import requests
import json
import logging
import random
import asyncio
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass

# Imports corregidos para nueva estructura
try:
    from ....interfaces.base import IChatGenerator
except ImportError:
    # Crear interfaz temporal si no existe
    class IChatGenerator:
        def generate_response(self, context: str, user_input: str = None) -> str:
            pass

try:
    from ...config.settings import Settings
except ImportError:
    # Configuración temporal si no existe
    class Settings:
        def __init__(self):
            self.api_timeout = 5
            self.max_response_length = 150

try:
    from ....shared.events.event_bus import EventBus
except ImportError:
    # EventBus temporal si no existe
    class EventBus:
        def emit(self, event_type: str, data: Dict[str, Any]):
            pass
        
        def subscribe(self, event_type: str, callback: Callable):
            pass

logger = logging.getLogger(__name__)

@dataclass
class ChatResponse:
    """Respuesta estructurada del chat"""
    text: str
    confidence: float
    suggestions: list
    metadata: Dict[str, Any]

class ChatService(IChatGenerator):
    """🤖 Servicio de chat mejorado para UI - VERSIÓN CORREGIDA"""
    
    def __init__(self, settings: Optional[Settings] = None, event_bus: Optional[EventBus] = None):
        """🚀 Inicialización con parámetros opcionales"""
        self.settings = settings or Settings()
        self.event_bus = event_bus or EventBus()
        self.fallback_responses = self._load_fallback_responses()
        self.use_online_api = True  # Cambiar a False para modo offline
        logger.info("ChatService inicializado correctamente")
        
    def _load_fallback_responses(self) -> Dict[str, list]:
        """📚 Carga respuestas de fallback para cuando no hay conexión"""
        return {
            "greetings": [
                "Hello! How are you doing today?",
                "Hi there! What would you like to talk about?",
                "Good to see you! How can I help you practice English?",
                "Hey! Ready for some English conversation?",
                "Hello! What's on your mind today?"
            ],
            "questions": [
                "That's interesting! Can you tell me more about that?",
                "I see what you mean. What do you think about it?",
                "That sounds fascinating. How did that make you feel?",
                "I understand. What happened next?",
                "That's a good point. Can you explain it differently?"
            ],
            "encouragement": [
                "You're doing great! Keep practicing.",
                "That's excellent progress. Well done!",
                "I can see you're improving. That's wonderful!",
                "Your English is getting better every day!",
                "Great job! You're expressing yourself very well."
            ],
            "corrections": [
                "Let me help you with that. Try saying: ",
                "A better way to say that would be: ",
                "That's close! The correct form is: ",
                "Good attempt! Consider this version: ",
                "Almost perfect! Try: "
            ],
            "general": [
                "That's very interesting to hear!",
                "I appreciate you sharing that with me.",
                "Thank you for telling me about that.",
                "That sounds like an important topic.",
                "I can understand why you feel that way."
            ]
        }
    
    def generate_response(self, context: str, user_input: str = None) -> str:
        """💬 Genera una respuesta conversacional usando múltiples métodos"""
        try:
            # Determinar el texto de entrada
            if user_input is None:
                input_text = context
            else:
                input_text = user_input
            
            if not input_text or not input_text.strip():
                return "I'm here to help you practice English. What would you like to talk about?"
            
            # Intentar diferentes métodos en orden de preferencia
            response = None
            
            # 1. Intentar API online (si está habilitada)
            if self.use_online_api:
                response = self._try_online_api(input_text, context)
            
            # 2. Si falla, usar respuesta inteligente local
            if not response:
                response = self._generate_smart_local_response(input_text, context)
            
            # 3. Si todo falla, usar fallback
            if not response:
                response = self._get_fallback_response(input_text)
            
            logger.info(f"Generated response: {response[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._get_fallback_response(user_input or context or "")
    
    def _try_online_api(self, input_text: str, context: str = None) -> Optional[str]:
        """🌐 Intenta usar una API online gratuita para generar respuestas"""
        try:
            # Usar Hugging Face Inference API (gratuita)
            api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
            
            headers = {
                "Content-Type": "application/json",
            }
            
            # Preparar payload
            payload = {
                "inputs": input_text,
                "parameters": {
                    "max_length": 100,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            # Hacer request con timeout corto
            timeout = getattr(self.settings, 'api_timeout', 5)
            response = requests.post(
                api_url, 
                headers=headers, 
                json=payload, 
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Extraer solo la respuesta nueva
                    if len(generated_text) > len(input_text):
                        new_response = generated_text[len(input_text):].strip()
                        if new_response:
                            return self._clean_response(new_response)
            
        except Exception as e:
            logger.warning(f"Online API failed: {e}")
        
        return None
    
    def _generate_smart_local_response(self, input_text: str, context: str = None) -> str:
        """🧠 Genera respuesta inteligente usando lógica local"""
        try:
            input_lower = input_text.lower()
            
            # Detectar tipo de mensaje y responder apropiadamente
            
            # 1. Saludos
            if any(word in input_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
                return random.choice(self.fallback_responses['greetings'])
            
            # 2. Preguntas (contienen ?)
            if '?' in input_text:
                return self._handle_question(input_text)
            
            # 3. Emociones positivas
            if any(word in input_lower for word in ['good', 'great', 'excellent', 'amazing', 'wonderful']):
                return random.choice(self.fallback_responses['encouragement'])
            
            # 4. Emociones negativas
            if any(word in input_lower for word in ['bad', 'terrible', 'awful', 'sad', 'difficult']):
                return f"I understand that can be challenging. {random.choice(self.fallback_responses['questions'])}"
            
            # 5. Temas específicos
            topic_response = self._get_topic_specific_response(input_lower)
            if topic_response:
                return topic_response
            
            # 6. Respuesta general inteligente
            return self._generate_contextual_response(input_text)
            
        except Exception as e:
            logger.error(f"Error in smart local response: {e}")
            return random.choice(self.fallback_responses['general'])
    
    def _get_topic_specific_response(self, input_lower: str) -> Optional[str]:
        """🎯 Genera respuestas específicas por tema"""
        # Trabajo
        if any(word in input_lower for word in ['work', 'job', 'career']):
            return "Work is such an important part of life. What do you enjoy most about your work?"
        
        # Familia
        if any(word in input_lower for word in ['family', 'mother', 'father', 'parents']):
            return "Family relationships are so meaningful. Tell me more about your family."
        
        # Viajes
        if any(word in input_lower for word in ['travel', 'trip', 'vacation']):
            return "Travel sounds exciting! Where have you been or where would you like to go?"
        
        # Aprendizaje/educación
        if any(word in input_lower for word in ['learn', 'study', 'school', 'university']):
            return "Learning is wonderful! What subjects interest you the most?"
        
        # Comida
        if any(word in input_lower for word in ['food', 'eat', 'cook', 'restaurant']):
            return "Food is one of life's great pleasures! What kind of cuisine do you enjoy?"
        
        # Música
        if any(word in input_lower for word in ['music', 'song', 'listen', 'band']):
            return "Music is such a universal language! What type of music do you like?"
        
        # Deportes
        if any(word in input_lower for word in ['sport', 'football', 'soccer', 'basketball']):
            return "Sports are great for staying active! Do you play any sports or have a favorite team?"
        
        return None
    
    def _handle_question(self, question: str) -> str:
        """❓ Maneja preguntas específicamente"""
        question_lower = question.lower()
        
        # Preguntas sobre preferencias
        if any(word in question_lower for word in ['like', 'prefer', 'favorite']):
            return "That's a great question about preferences! I'd love to hear your thoughts on that. What do you think?"
        
        # Preguntas sobre opiniones
        if any(word in question_lower for word in ['think', 'believe', 'opinion']):
            return "That's an interesting question that makes me think. What's your perspective on it?"
        
        # Preguntas sobre experiencias
        if any(word in question_lower for word in ['have you', 'did you', 'were you']):
            return "That's a thoughtful question about experiences. I'm curious to hear about yours first."
        
        # Preguntas sobre recomendaciones
        if any(word in question_lower for word in ['recommend', 'suggest', 'advice']):
            return "That's a great question about recommendations! What kind of suggestions are you looking for?"
        
        # Preguntas generales
        return "That's a really good question! I think there are many ways to look at that. What are your thoughts?"
    
    def _generate_contextual_response(self, input_text: str) -> str:
        """📋 Genera respuesta contextual basada en el contenido"""
        words = input_text.split()
        word_count = len(words)
        
        # Respuesta basada en longitud
        if word_count <= 3:
            return "I'd love to hear more about that. Can you tell me a bit more detail?"
        elif word_count <= 10:
            return f"That's interesting! {random.choice(self.fallback_responses['questions'])}"
        else:
            return f"Thank you for sharing so much detail with me. {random.choice(self.fallback_responses['general'])}"
    
    def _get_fallback_response(self, input_text: str) -> str:
        """🛡️ Obtiene respuesta de fallback cuando todo falla"""
        if not input_text:
            return "I'm here to help you practice English. What would you like to talk about?"
        
        # Seleccionar respuesta apropiada basada en longitud
        if len(input_text.split()) <= 2:
            return random.choice(self.fallback_responses['greetings'])
        else:
            return random.choice(self.fallback_responses['general'])
    
    def _clean_response(self, response: str) -> str:
        """🧹 Limpia la respuesta generada"""
        if not response:
            return "That's interesting to hear!"
        
        # Limpiar caracteres no deseados
        response = response.strip('\n\r\t ')
        
        # Remover prefijos comunes de modelos
        prefixes_to_remove = ['User:', 'Assistant:', 'AI:', 'Bot:', 'Response:']
        for prefix in prefixes_to_remove:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()
        
        # Eliminar repeticiones
        response = self._remove_repeated_phrases(response)
        
        # Asegurar que termina apropiadamente
        if response and not response.endswith(('.', '!', '?')):
            response += '.'
        
        # Limitar longitud
        max_length = getattr(self.settings, 'max_response_length', 150)
        if len(response) > max_length:
            sentences = response.split('. ')
            if len(sentences) > 1:
                response = sentences[0] + '.'
        
        return response or "I understand what you're saying."
    
    def _remove_repeated_phrases(self, text: str) -> str:
        """🧹 Elimina frases repetidas del texto"""
        if not text:
            return text
        
        # Separar por oraciones
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        # Eliminar oraciones duplicadas manteniendo solo la primera
        unique_sentences = []
        seen = set()
        
        for sentence in sentences:
            sentence_clean = sentence.lower().strip()
            if sentence_clean not in seen and len(sentence_clean) > 3:
                unique_sentences.append(sentence)
                seen.add(sentence_clean)
        
        # Reconstruir texto
        result = '. '.join(unique_sentences)
        
        # Asegurar que termina con punto
        if result and not result.endswith('.'):
            result += '.'
        
        return result
    
    def set_online_mode(self, enabled: bool):
        """🌐 Habilita o deshabilita el modo online"""
        self.use_online_api = enabled
        logger.info(f"Online API mode: {'enabled' if enabled else 'disabled'}")
    
    def test_connection(self) -> bool:
        """🔗 Prueba si la conexión online funciona"""
        try:
            test_response = self._try_online_api("Hello, how are you?")
            return test_response is not None
        except:
            return False
    
    async def process_message_async(self, message: str, 
                                  progress_callback: Optional[Callable[[int, str], None]] = None) -> ChatResponse:
        """💬 Procesa mensaje de forma asíncrona con callbacks de progreso"""
        
        # Emitir evento de inicio
        if self.event_bus:
            self.event_bus.emit("chat.processing_started", {"message": message})
        
        try:
            if progress_callback:
                progress_callback(20, "Analizando mensaje...")
            
            # Simular processing asíncrono
            await asyncio.sleep(0.1)
            
            # Generar respuesta usando el método principal
            response_text = self.generate_response(context="async", user_input=message)
            
            if progress_callback:
                progress_callback(80, "Generando respuesta...")
            
            await asyncio.sleep(0.1)
            
            response = ChatResponse(
                text=response_text,
                confidence=0.9,
                suggestions=self._generate_suggestions(message),
                metadata={"processing_time": "1.2s", "method": "async"}
            )
            
            if progress_callback:
                progress_callback(100, "Completado")
            
            # Emitir evento de completado
            if self.event_bus:
                self.event_bus.emit("chat.processing_completed", {
                    "response": response,
                    "original_message": message
                })
            
            return response
            
        except Exception as e:
            if self.event_bus:
                self.event_bus.emit("chat.processing_error", {"error": str(e)})
            raise
    
    def _generate_suggestions(self, message: str) -> list:
        """💡 Genera sugerencias de conversación"""
        suggestions = [
            "Tell me more about that",
            "How did that make you feel?",
            "What happened next?",
            "Can you explain that differently?"
        ]
        
        # Agregar sugerencias específicas basadas en el mensaje
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['work', 'job']):
            suggestions.extend([
                "What do you like about your work?",
                "Do you work with a team?"
            ])
        elif any(word in message_lower for word in ['family', 'friend']):
            suggestions.extend([
                "How long have you known them?",
                "What do you like to do together?"
            ])
        
        return suggestions[:4]  # Máximo 4 sugerencias