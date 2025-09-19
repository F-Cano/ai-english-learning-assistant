"""
Context Translator - Traducción contextual inteligente
Migrado y mejorado desde smart_chat_mode.py
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ContextTranslator:
    """🌐 Traductor contextual inteligente"""
    
    def __init__(self, assistant):
        self.assistant = assistant
        self._init_translation_libraries()
        logger.info("ContextTranslator inicializado con bibliotecas completas")
    
    def _init_translation_libraries(self):
        """📚 Inicializa bibliotecas de traducción"""
        self.complete_translations = self._load_complete_phrase_library()
        self.word_translations = self._load_word_library()
        self.welcome_translations = self._load_welcome_library()
    
    def translate_to_spanish(self, english_text: str, context: Dict[str, Any] = None) -> str:
        """🌐 Traduce texto al español usando múltiples métodos - MIGRADO MEJORADO"""
        try:
            # Método 1: Usar servicio de traducción con parámetros correctos
            if hasattr(self.assistant, 'translation_service'):
                try:
                    # 🔧 LLAMADA CORREGIDA con parámetros correctos
                    return self.assistant.translation_service.translate(
                        text=english_text, 
                        source_lang='en', 
                        target_lang='es'
                    )
                except Exception as e:
                    logger.warning(f"Translation service failed: {e}")
            
            # Método 2: Traducción manual contextual mejorada
            return self._improved_manual_translation(english_text, context)
            
        except Exception as e:
            logger.error(f"Error in translation: {e}")
            return self._improved_manual_translation(english_text, context)

    def _improved_manual_translation(self, english_text: str, context: Dict[str, Any] = None) -> str:
        """📚 Traducción manual MEJORADA sin mezclar idiomas - MIGRADO"""
        
        # Limpiar texto de entrada - eliminar repeticiones
        cleaned_text = self._clean_repeated_text(english_text)
        
        # Buscar traducción completa exacta
        if cleaned_text in self.complete_translations:
            return self.complete_translations[cleaned_text]
        
        # Buscar traducciones parciales para frases largas
        for english_phrase, spanish_phrase in self.complete_translations.items():
            if english_phrase in cleaned_text:
                return cleaned_text.replace(english_phrase, spanish_phrase)
        
        # Traducción contextual específica
        if context:
            contextual_translation = self._get_contextual_translation(cleaned_text, context)
            if contextual_translation:
                return contextual_translation
        
        # Traducción palabra por palabra solo si no se encuentra frase completa
        return self._word_by_word_translation(cleaned_text)

    def _load_complete_phrase_library(self) -> Dict[str, str]:
        """📖 Carga biblioteca completa de frases - MIGRADO EXPANDIDO"""
        return {
            # Respuestas comunes completas
            "That's interesting!": "¡Eso es interesante!",
            "Can you tell me more about that?": "¿Puedes contarme más sobre eso?",
            "That's a good point.": "Ese es un buen punto.",
            "I understand what you mean.": "Entiendo lo que quieres decir.",
            "Tell me more about that.": "Cuéntame más sobre eso.",
            "What do you think about that?": "¿Qué piensas sobre eso?",
            "That sounds interesting.": "Eso suena interesante.",
            "I see what you mean.": "Veo lo que quieres decir.",
            "I'd love to hear more about that.": "Me encantaría escuchar más sobre eso.",
            "That's fascinating!": "¡Eso es fascinante!",
            "How do you feel about that?": "¿Cómo te sientes al respecto?",
            
            # Frases sobre deportes/soccer
            "Football is such an exciting sport!": "¡El fútbol es un deporte tan emocionante!",
            "What's your favorite team or player?": "¿Cuál es tu equipo o jugador favorito?",
            "That's awesome that you play soccer!": "¡Es genial que juegues fútbol!",
            "What position do you play?": "¿En qué posición juegas?",
            "How long have you been playing?": "¿Cuánto tiempo llevas jugando?",
            "Do you have a favorite professional team?": "¿Tienes un equipo profesional favorito?",
            "Soccer is fantastic!": "¡El fútbol es fantástico!",
            
            # Frases sobre comida
            "Food is such an interesting topic!": "¡La comida es un tema tan interesante!",
            "What kind of food do you enjoy most?": "¿Qué tipo de comida disfrutas más?",
            "Food is a wonderful topic to discuss.": "La comida es un tema maravilloso para discutir.",
            "Do you like to cook?": "¿Te gusta cocinar?",
            "What's your favorite dish?": "¿Cuál es tu plato favorito?",
            "That sounds delicious!": "¡Eso suena delicioso!",
            "What's your favorite type of cuisine?": "¿Cuál es tu tipo de cocina favorita?",
            
            # Respuestas de clarificación
            "I mean, could you tell me more details about playing soccer?": 
            "Quiero decir, ¿podrías contarme más detalles sobre jugar fútbol?",
            "Like, what position do you play or how long have you been playing?": 
            "Como, ¿en qué posición juegas o cuánto tiempo llevas jugando?",
            "Sorry for the confusion!": "¡Perdón por la confusión!",
            "Let me clarify!": "¡Déjame aclarar!",
            
            # Saludos y bienvenidas
            "Hello! Welcome to our intelligent chat.": "¡Hola! Bienvenido a nuestro chat inteligente.",
            "I'm excited to help you practice English!": "¡Estoy emocionado de ayudarte a practicar inglés!",
            "Ready to practice?": "¿Listo para practicar?",
        }

    def _load_word_library(self) -> Dict[str, str]:
        """🔤 Carga biblioteca de palabras individuales - MIGRADO EXPANDIDO"""
        return {
            # Palabras comunes
            "that's": "eso es", "that": "eso", "is": "es", "very": "muy",
            "really": "realmente", "interesting": "interesante", "good": "bueno",
            "great": "genial", "wonderful": "maravilloso", "about": "sobre",
            "more": "más", "tell": "contar", "me": "me", "you": "tú",
            "can": "puedes", "what": "qué", "how": "cómo", "when": "cuándo",
            "where": "dónde", "why": "por qué", "like": "gustar", "love": "encantar",
            "think": "pensar", "feel": "sentir", "want": "querer", "need": "necesitar",
            "enjoy": "disfrutar", "favorite": "favorito", "best": "mejor",
            
            # Deportes/Soccer
            "football": "fútbol", "soccer": "fútbol", "sport": "deporte",
            "team": "equipo", "player": "jugador", "game": "juego",
            "match": "partido", "play": "jugar", "position": "posición",
            "goal": "gol", "exciting": "emocionante", "awesome": "genial",
            
            # Comida
            "food": "comida", "eat": "comer", "delicious": "delicioso",
            "tasty": "sabroso", "cook": "cocinar", "dish": "plato",
            "cuisine": "cocina", "restaurant": "restaurante", "meal": "comida",
            
            # Tiempo
            "today": "hoy", "yesterday": "ayer", "tomorrow": "mañana",
            "always": "siempre", "never": "nunca", "sometimes": "a veces",
            
            # Conectores
            "and": "y", "but": "pero", "or": "o", "because": "porque",
            "also": "también", "too": "también", "however": "sin embargo"
        }

    def _load_welcome_library(self) -> Dict[str, str]:
        """👋 Carga biblioteca de mensajes de bienvenida - MIGRADO MEJORADO"""
        return {
            # Bienvenidas completas
            "Hello again! Great to see you back for session #4. Ready to practice?": 
            "¡Hola de nuevo! Me alegra verte de vuelta para la sesión #4. ¿Listo para practicar?",
            
            "Hello again! Great to see you back": 
            "¡Hola de nuevo! Me alegra verte de vuelta",
            
            # Componentes de bienvenida
            "for session": "para la sesión", "session #": "sesión #",
            "great": "genial", "see": "ver", "back": "de vuelta",
            "hello": "hola", "again": "de nuevo", "ready": "listo",
            "to": "para", "practice": "practicar", "for": "para", "session": "sesión"
        }

    def _clean_repeated_text(self, text: str) -> str:
        """🧹 Limpia texto repetido y malformado - MIGRADO"""
        if not text:
            return ""
        
        # Remover "🤖 IA:" al inicio si existe
        text = text.replace("🤖 IA:", "").strip()
        
        # Detectar y eliminar repeticiones obvias
        sentences = text.split('. ')
        
        # Si hay oraciones repetidas, tomar solo la primera
        unique_sentences = []
        seen = set()
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence not in seen:
                unique_sentences.append(sentence)
                seen.add(sentence)
        
        # Reconstruir texto
        clean_text = '. '.join(unique_sentences)
        
        # Asegurar que termina correctamente
        if clean_text and not clean_text.endswith(('.', '!', '?')):
            clean_text += '.'
        
        return clean_text

    def _word_by_word_translation(self, english_text: str) -> str:
        """🔤 Traducción palabra por palabra mejorada - MIGRADO"""
        
        # Separar en palabras y traducir
        words = english_text.lower().split()
        translated_words = []
        
        for word in words:
            # Limpiar puntuación
            clean_word = word.strip('.,!?')
            punctuation = word[len(clean_word):] if len(word) > len(clean_word) else ''
            
            # Traducir palabra
            if clean_word in self.word_translations:
                translated_words.append(self.word_translations[clean_word] + punctuation)
            else:
                # Mantener palabra original si no hay traducción
                translated_words.append(word)
        
        return ' '.join(translated_words).capitalize()

    def _get_contextual_translation(self, text: str, context: Dict[str, Any]) -> str:
        """🎯 Obtiene traducción contextual específica"""
        topic = context.get("topic", "general")
        
        # Traducciones específicas por contexto de soccer
        if topic == "soccer" or "football" in text.lower() or "soccer" in text.lower():
            soccer_specific = {
                "That's awesome!": "¡Eso es genial!",
                "Tell me more about it": "Cuéntame más sobre eso",
                "What position": "Qué posición",
                "How long": "Cuánto tiempo"
            }
            
            for eng, esp in soccer_specific.items():
                if eng.lower() in text.lower():
                    return text.replace(eng, esp)
        
        # Traducciones específicas por contexto de comida
        elif topic == "food" or "food" in text.lower():
            food_specific = {
                "That sounds great": "Eso suena genial",
                "What kind": "Qué tipo",
                "Do you like": "Te gusta"
            }
            
            for eng, esp in food_specific.items():
                if eng.lower() in text.lower():
                    return text.replace(eng, esp)
        
        return None

    def translate_welcome_message(self, english_text: str) -> str:
        """👋 Traduce mensajes de bienvenida específicamente - MIGRADO MEJORADO"""
        
        # Traducir frase completa si existe
        for eng_phrase, spanish_phrase in self.welcome_translations.items():
            if eng_phrase.lower() in english_text.lower():
                english_text = english_text.replace(eng_phrase, spanish_phrase)
        
        # Si aún quedan partes en inglés, traducir palabra por palabra
        words = english_text.split()
        translated_words = []
        
        for word in words:
            clean_word = word.lower().strip('.,!?#')
            punctuation = word[len(clean_word):] if len(word) > len(clean_word) else ''
            
            if clean_word in self.welcome_translations:
                translated_words.append(self.welcome_translations[clean_word] + punctuation)
            elif clean_word in self.word_translations:
                translated_words.append(self.word_translations[clean_word] + punctuation)
            else:
                translated_words.append(word)  # Mantener palabra original
        
        result = ' '.join(translated_words)
        
        # Limpiar y corregir resultado final
        result = result.replace("Me alegra verte de vuelta for session", "Me alegra verte de vuelta para la sesión")
        result = result.replace("Ready to practice?", "¿Listo para practicar?")
        result = result.replace("session #", "sesión #")
        
        return result

    def get_translation_quality_score(self, original: str, translated: str) -> float:
        """📊 Calcula puntuación de calidad de traducción"""
        try:
            # Métricas básicas de calidad
            length_ratio = len(translated) / len(original) if original else 0
            
            # Penalizar si queda mucho inglés en la traducción
            english_words = len([w for w in translated.split() if w.lower() in self.word_translations.keys()])
            total_words = len(translated.split())
            english_percentage = english_words / total_words if total_words > 0 else 1
            
            # Score basado en ratio de longitud y contenido traducido
            quality_score = max(0, min(1, (1 - english_percentage) * (1 - abs(1 - length_ratio))))
            
            return quality_score
            
        except Exception as e:
            logger.error(f"Error calculating translation quality: {e}")
            return 0.5

    def get_emergency_translation(self, english_text: str) -> str:
        """🚨 Traducción de emergencia"""
        return f"[Traduciendo: {english_text}]"
