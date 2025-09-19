"""
Topic Responder - Respuestas especializadas por tema
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class TopicResponder:
    """ Generador de respuestas especializadas por tema"""
    
    def __init__(self, context_analyzer, progress_tracker):
        self.context_analyzer = context_analyzer
        self.progress_tracker = progress_tracker
        logger.info("TopicResponder inicializado")
    
    def generate_topic_response(self, user_input: str, context: Dict[str, Any], 
                              user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """ Genera respuesta especializada por tema"""
        try:
            topic = context.get("topic", "general")
            emotion = context.get("emotion", "neutral")
            
            # Generar respuesta basada en tema
            if topic == "soccer":
                ai_response = self._generate_soccer_response(user_input)
            elif topic == "food":
                ai_response = self._generate_food_response(user_input)
            else:
                ai_response = self._generate_general_response(user_input)
            
            return {
                "ai_response": ai_response,
                "response_strategy": f"{topic}_response",
                "topic_analysis": {
                    "topic": topic,
                    "confidence": context.get("topic_confidence", 0.5)
                },
                "improvement_analysis": {
                    "detected_strengths": ["active_participation"],
                    "improvement_areas": [],
                    "specific_suggestions": ["Keep sharing your thoughts!"]
                },
                "progress_evaluation": {
                    "overall_progress_score": 0.7,
                    "session_quality": "good"
                },
                "vocabulary_opportunities": [],
                "follow_up_suggestions": ["Tell me more about that!"],
                "learning_focus": "conversational_skills",
                "engagement_level": "moderate",
                "next_conversation_direction": "continue",
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating topic response: {e}")
            return self._get_fallback_response()
    
    def _generate_soccer_response(self, user_input: str) -> str:
        """ Genera respuesta sobre fútbol"""
        if "play" in user_input.lower():
            return "That's awesome that you play soccer! What position do you usually play?"
        elif "team" in user_input.lower():
            return "Teams are so important in soccer! Do you have a favorite team?"
        else:
            return "Soccer is such a universal sport! What do you enjoy most about football?"
    
    def _generate_food_response(self, user_input: str) -> str:
        """🍕 Genera respuesta sobre comida"""
        if "like" in user_input.lower() or "love" in user_input.lower():
            return "That sounds delicious! What makes that food special to you?"
        elif "cook" in user_input.lower():
            return "Cooking is such a wonderful skill! What's your favorite dish to prepare?"
        else:
            return "Food is one of life's great pleasures! Tell me more about your food experiences."
    
    def _generate_general_response(self, user_input: str) -> str:
        """ Genera respuesta general"""
        if "?" in user_input:
            return "That's a great question! I'm here to help you explore this topic."
        else:
            return "That's really interesting! Could you tell me more about that?"
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """ Respuesta de fallback"""
        return {
            "ai_response": "I understand what you're saying! Please continue.",
            "response_strategy": "fallback",
            "error": "Fallback response used"
        }
