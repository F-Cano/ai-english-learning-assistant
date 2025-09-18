import requests
import json
import logging
import random
from typing import Optional
from ..interfaces.base import IChatGenerator
from ..config.settings import Settings

logger = logging.getLogger(__name__)

class ChatService(IChatGenerator):
    """Chat service ligero sin dependencias pesadas"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.fallback_responses = self._load_fallback_responses()
        self.use_online_api = True  # Cambiar a False para modo offline
        
    def _load_fallback_responses(self) -> dict:
        """Carga respuestas de fallback para cuando no hay conexión"""
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
        """Genera una respuesta conversacional usando múltiples métodos"""
        try:
            # Determinar el texto de entrada
            if user_input is None:
                input_text = context
            else:
                input_text = user_input
            
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
            return self._get_fallback_response(user_input or context)
    
    def _try_online_api(self, input_text: str, context: str = None) -> Optional[str]:
        """Intenta usar una API online gratuita para generar respuestas"""
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
            response = requests.post(
                api_url, 
                headers=headers, 
                json=payload, 
                timeout=5  # 5 segundos máximo
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
        """Genera respuesta inteligente usando lógica local"""
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
            if any(word in input_lower for word in ['work', 'job', 'career']):
                return "Work is such an important part of life. What do you enjoy most about your work?"
            
            if any(word in input_lower for word in ['family', 'mother', 'father', 'parents']):
                return "Family relationships are so meaningful. Tell me more about your family."
            
            if any(word in input_lower for word in ['travel', 'trip', 'vacation']):
                return "Travel sounds exciting! Where have you been or where would you like to go?"
            
            # 6. Aprendizaje/educación
            if any(word in input_lower for word in ['learn', 'study', 'school', 'university']):
                return "Learning is wonderful! What subjects interest you the most?"
            
            # 7. Respuesta general inteligente
            return self._generate_contextual_response(input_text)
            
        except Exception as e:
            logger.error(f"Error in smart local response: {e}")
            return random.choice(self.fallback_responses['general'])
    
    def _handle_question(self, question: str) -> str:
        """Maneja preguntas específicamente"""
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
        
        # Preguntas generales
        return "That's a really good question! I think there are many ways to look at that. What are your thoughts?"
    
    def _generate_contextual_response(self, input_text: str) -> str:
        """Genera respuesta contextual basada en el contenido"""
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
        """Obtiene respuesta de fallback cuando todo falla"""
        if not input_text:
            return "I'm here to help you practice English. What would you like to talk about?"
        
        # Seleccionar respuesta apropiada basada en longitud
        if len(input_text.split()) <= 2:
            return random.choice(self.fallback_responses['greetings'])
        else:
            return random.choice(self.fallback_responses['general'])
    
    def _clean_response(self, response: str) -> str:
        """Limpia la respuesta generada"""
        if not response:
            return "That's interesting to hear!"
        
        # Limpiar caracteres no deseados
        response = response.strip('\n\r\t ')
        
        # Remover prefijos comunes de modelos
        prefixes_to_remove = ['User:', 'Assistant:', 'AI:', 'Bot:', 'Response:']
        for prefix in prefixes_to_remove:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()
        
        # Asegurar que termina apropiadamente
        if response and not response.endswith(('.', '!', '?')):
            response += '.'
        
        return response or "I understand what you're saying."
    
    def _simple_clean_response(self, response: str) -> str:
        """🧹 Limpieza simple y efectiva MEJORADA"""
        if not response:
            return "I understand what you're saying."
        
        # Remover caracteres no deseados
        response = response.strip('\n\r\t ')
        
        # 🔧 NUEVA FUNCIONALIDAD: Eliminar repeticiones de frases
        response = self._remove_repeated_phrases(response)
        
        # Si está vacío después de limpiar
        if not response:
            return "That's interesting. Tell me more."
        
        # Cortar si es muy largo (primera oración)
        if len(response) > 150:
            sentences = response.split('. ')
            if len(sentences) > 1:
                response = sentences[0] + '.'
        
        return response.strip() or "I see what you mean."
    
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
            if sentence_clean not in seen:
                unique_sentences.append(sentence)
                seen.add(sentence_clean)
        
        # Reconstruir texto
        result = '. '.join(unique_sentences)
        
        # Asegurar que termina con punto
        if result and not result.endswith('.'):
            result += '.'
        
        return result
    
    def set_online_mode(self, enabled: bool):
        """Habilita o deshabilita el modo online"""
        self.use_online_api = enabled
        logger.info(f"Online API mode: {'enabled' if enabled else 'disabled'}")
    
    def test_connection(self) -> bool:
        """Prueba si la conexión online funciona"""
        try:
            test_response = self._try_online_api("Hello, how are you?")
            return test_response is not None
        except:
            return False