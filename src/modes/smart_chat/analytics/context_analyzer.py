"""
Context Analyzer - Análisis profundo de contexto conversacional
"""

import logging
import re
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ContextAnalyzer:
    """ Analizador profundo de contexto conversacional"""
    
    def __init__(self):
        self.topic_keywords = {
            "soccer": ["soccer", "football", "futbol", "goal", "team", "player", "match", "game"],
            "food": ["food", "eat", "cook", "restaurant", "meal", "delicious", "taste", "recipe"],
            "travel": ["travel", "trip", "vacation", "visit", "country", "city", "tourist"],
            "music": ["music", "song", "listen", "play", "instrument", "concert", "band"],
            "family": ["family", "mother", "father", "sister", "brother", "parents", "children"],
            "work": ["work", "job", "career", "office", "boss", "colleague", "meeting"]
        }
        logger.info("ContextAnalyzer inicializado")
    
    def analyze_message_context(self, user_input: str, 
                              conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """ Analiza contexto completo del mensaje"""
        try:
            user_lower = user_input.lower()
            
            # Detectar tema
            topic_analysis = self._detect_topic(user_lower)
            
            # Detectar emoción
            emotion_analysis = self._detect_emotion(user_lower)
            
            # Detectar intención
            intent_analysis = self._detect_user_intent(user_lower)
            
            # Evaluar complejidad
            complexity_analysis = self._evaluate_complexity(user_input)
            
            return {
                "topic": topic_analysis["topic"],
                "topic_confidence": topic_analysis["confidence"],
                "emotion": emotion_analysis["emotion"],
                "emotion_confidence": emotion_analysis["confidence"],
                "user_intent": intent_analysis["intent"],
                "intent_confidence": intent_analysis["confidence"],
                "complexity_level": complexity_analysis["level"],
                "word_count": len(user_input.split()),
                "has_question": "?" in user_input,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing context: {e}")
            return self._get_default_context()
    
    def _detect_topic(self, user_lower: str) -> Dict[str, Any]:
        """ Detecta tema principal"""
        topic_scores = {}
        
        for topic, keywords in self.topic_keywords.items():
            score = sum(1 for keyword in keywords if keyword in user_lower)
            if score > 0:
                topic_scores[topic] = score / len(keywords)
        
        if topic_scores:
            best_topic = max(topic_scores.keys(), key=topic_scores.get)
            confidence = topic_scores[best_topic]
            return {"topic": best_topic, "confidence": min(confidence * 2, 1.0)}
        
        return {"topic": "general", "confidence": 0.5}
    
    def _detect_emotion(self, user_lower: str) -> Dict[str, Any]:
        """ Detecta emoción"""
        positive_words = ["love", "like", "enjoy", "happy", "excited", "great", "awesome", "amazing"]
        negative_words = ["hate", "dislike", "sad", "angry", "frustrated", "terrible", "awful"]
        confused_words = ["confused", "don't understand", "what", "how", "help"]
        
        positive_score = sum(1 for word in positive_words if word in user_lower)
        negative_score = sum(1 for word in negative_words if word in user_lower)
        confused_score = sum(1 for word in confused_words if word in user_lower)
        
        if confused_score > 0:
            return {"emotion": "confused", "confidence": 0.7}
        elif positive_score > negative_score:
            return {"emotion": "positive", "confidence": 0.7}
        elif negative_score > positive_score:
            return {"emotion": "negative", "confidence": 0.7}
        else:
            return {"emotion": "neutral", "confidence": 0.6}
    
    def _detect_user_intent(self, user_lower: str) -> Dict[str, Any]:
        """ Detecta intención del usuario"""
        if "?" in user_lower or any(word in user_lower for word in ["what", "how", "when", "where", "why"]):
            return {"intent": "asking_question", "confidence": 0.8}
        elif any(word in user_lower for word in ["love", "like", "enjoy", "excited"]):
            return {"intent": "expressing_enthusiasm", "confidence": 0.7}
        elif any(word in user_lower for word in ["don't understand", "confused", "help"]):
            return {"intent": "seeking_clarification", "confidence": 0.8}
        else:
            return {"intent": "making_statement", "confidence": 0.6}
    
    def _evaluate_complexity(self, user_input: str) -> Dict[str, Any]:
        """ Evalúa complejidad del mensaje"""
        word_count = len(user_input.split())
        
        if word_count <= 3:
            return {"level": "beginner", "score": 0.3}
        elif word_count <= 8:
            return {"level": "intermediate", "score": 0.6}
        else:
            return {"level": "advanced", "score": 0.9}
    
    def _get_default_context(self) -> Dict[str, Any]:
        """ Contexto por defecto en caso de error"""
        return {
            "topic": "general",
            "topic_confidence": 0.5,
            "emotion": "neutral", 
            "emotion_confidence": 0.5,
            "user_intent": "making_statement",
            "intent_confidence": 0.5,
            "complexity_level": "intermediate",
            "word_count": 0,
            "has_question": False,
            "timestamp": datetime.now().isoformat()
        }
