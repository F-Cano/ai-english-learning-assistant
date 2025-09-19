"""
Smart Chat Mode - Modo de conversación inteligente REFACTORIZADO
Versión modular con todos los componentes separados
"""

import logging
import uuid
from typing import Dict, Any, List
from datetime import datetime

# Importar módulos refactorizados - NUEVA ESTRUCTURA
from .smart_chat.core.profile_manager import ProfileManager
from .smart_chat.analytics.context_analyzer import ContextAnalyzer
from .smart_chat.analytics.progress_tracker import ProgressTracker
from .smart_chat.processing.message_processor import MessageProcessor
from .smart_chat.processing.context_translator import ContextTranslator
from .smart_chat.formatting.bilingual_formatter import BilingualFormatter
from .smart_chat.responses.topic_responder import TopicResponder

logger = logging.getLogger(__name__)

class SmartChatMode:
    """ Modo de conversación inteligente - ARQUITECTURA MODULAR"""
    
    def __init__(self):
        """ Inicialización del sistema modular"""
        # Generar ID de sesión único
        self.session_id = str(uuid.uuid4())[:8]
        
        # 1 INICIALIZAR MÓDULOS CORE
        logger.info(" Inicializando Smart Chat Mode - Versión Modular")
        
        try:
            # Core Components
            self.profile_manager = ProfileManager()
            self.context_analyzer = ContextAnalyzer()
            self.progress_tracker = ProgressTracker(self.session_id)
            
            # Processing Components
            self.message_processor = MessageProcessor()
            self.context_translator = ContextTranslator()
            
            # Formatting Components
            self.bilingual_formatter = BilingualFormatter()
            
            # Response Components
            self.topic_responder = TopicResponder(
                context_analyzer=self.context_analyzer,
                progress_tracker=self.progress_tracker
            )
            
            # 2️⃣ CONFIGURACIÓN DE SESIÓN
            self.conversation_history = []
            self.session_start_time = datetime.now()
            self.is_active = True
            
            logger.info(f" Smart Chat Mode inicializado exitosamente - Sesión: {self.session_id}")
            logger.info(" Módulos cargados: ProfileManager, ContextAnalyzer, ProgressTracker, MessageProcessor, ContextTranslator, BilingualFormatter, TopicResponder")
            
        except Exception as e:
            logger.error(f" Error inicializando Smart Chat Mode: {e}")
            raise

    def process_message(self, user_input: str) -> Dict[str, Any]:
        """ Procesa mensaje del usuario con arquitectura modular"""
        try:
            logger.info(f" Procesando mensaje: '{user_input[:50]}...' (Sesión: {self.session_id})")
            
            # 1️⃣ OBTENER PERFIL DE USUARIO
            user_profile = self.profile_manager.get_user_profile()
            logger.debug(f"👤 Perfil obtenido: Nivel {user_profile.get('language_level', 'unknown')}")
            
            # 2 PROCESAR MENSAJE INICIAL
            processed_message = self.message_processor.process_user_message(user_input)
            logger.debug(f" Mensaje procesado: {len(processed_message.get('cleaned_input', ''))} caracteres")
            
            # 3 ANALIZAR CONTEXTO COMPLETO
            context = self.context_analyzer.analyze_message_context(
                user_input=user_input,
                conversation_history=self.conversation_history
            )
            logger.debug(f"🔍 Contexto: {context.get('topic', 'unknown')} (confianza: {context.get('topic_confidence', 0):.2f})")
            
            # 4 TRADUCIR CONTEXTO SI ES NECESARIO
            translation_data = self.context_translator.translate_if_needed(
                user_input=user_input,
                context=context,
                user_profile=user_profile
            )
            logger.debug(f" Traducción: {translation_data.get('translation_applied', False)}")
            
            # 5 GENERAR RESPUESTA ESPECIALIZADA
            response_data = self.topic_responder.generate_topic_response(
                user_input=user_input,
                context=context,
                user_profile=user_profile
            )
            logger.debug(f" Respuesta generada: {response_data.get('response_strategy', 'unknown')}")
            
            # 6 FORMATEAR RESPUESTA BILINGÜE
            formatted_response = self.bilingual_formatter.format_response(
                response_data=response_data,
                translation_data=translation_data,
                user_profile=user_profile,
                context=context
            )
            logger.debug(f" Formato: {formatted_response.get('format_type', 'unknown')}")
            
            # 7 RASTREAR PROGRESO
            interaction_data = {
                "user_input": user_input,
                "ai_response": formatted_response.get("final_response", ""),
                "context": context,
                "response_data": response_data,
                "translation_data": translation_data,
                "user_profile": user_profile
            }
            
            self.progress_tracker.track_message_interaction(interaction_data)
            logger.debug(" Progreso rastreado exitosamente")
            
            # 8 ACTUALIZAR PERFIL DE USUARIO
            self.profile_manager.update_user_profile(
                interaction_data=interaction_data,
                context=context,
                progress_data=self.progress_tracker.get_session_summary()
            )
            logger.debug(" Perfil actualizado")
            
            # 9 AGREGAR A HISTORIAL
            conversation_turn = {
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "ai_response": formatted_response.get("final_response", ""),
                "context": context,
                "response_strategy": response_data.get("response_strategy", "unknown"),
                "turn_number": len(self.conversation_history) + 1
            }
            self.conversation_history.append(conversation_turn)
            
            #  CONSTRUIR RESPUESTA FINAL
            final_result = self._build_final_response(
                formatted_response=formatted_response,
                response_data=response_data,
                context=context,
                translation_data=translation_data,
                user_profile=user_profile,
                processed_message=processed_message
            )
            
            logger.info(f"✅ Mensaje procesado exitosamente - Estrategia: {response_data.get('response_strategy', 'unknown')}")
            return final_result
            
        except Exception as e:
            logger.error(f" Error procesando mensaje: {e}")
            return self._get_error_response(user_input, str(e))

    def _build_final_response(self, formatted_response: Dict[str, Any], response_data: Dict[str, Any],
                            context: Dict[str, Any], translation_data: Dict[str, Any],
                            user_profile: Dict[str, Any], processed_message: Dict[str, Any]) -> Dict[str, Any]:
        """ Construye respuesta final consolidada"""
        try:
            # Obtener componentes principales
            ai_response = formatted_response.get("final_response", "I understand what you're saying!")
            
            # Construir análisis consolidado
            analysis = {
                "topic": context.get("topic", "general"),
                "topic_confidence": context.get("topic_confidence", 0.5),
                "emotion": context.get("emotion", "neutral"),
                "emotion_confidence": context.get("emotion_confidence", 0.5),
                "complexity_level": context.get("complexity_level", "intermediate"),
                "user_intent": context.get("user_intent", "making_statement"),
                "response_strategy": response_data.get("response_strategy", "conversational_expansion"),
                "engagement_level": response_data.get("engagement_level", "moderate"),
                "learning_focus": response_data.get("learning_focus", "conversational_skills")
            }
            
            # Construir información de progreso
            progress_info = {
                "improvements_detected": response_data.get("improvement_analysis", {}).get("detected_strengths", []),
                "areas_to_improve": response_data.get("improvement_analysis", {}).get("improvement_areas", []),
                "vocabulary_opportunities": response_data.get("vocabulary_opportunities", []),
                "overall_progress_score": response_data.get("progress_evaluation", {}).get("overall_progress_score", 0.5),
                "session_quality": response_data.get("progress_evaluation", {}).get("session_quality", "good")
            }
            
            # Construir información de traducción
            translation_info = {
                "translation_applied": translation_data.get("translation_applied", False),
                "source_language": translation_data.get("source_language", "en"),
                "target_language": translation_data.get("target_language", "en"),
                "confidence": translation_data.get("confidence", 1.0)
            }
            
            # Construir información de formato
            format_info = {
                "format_type": formatted_response.get("format_type", "standard"),
                "bilingual_elements": formatted_response.get("bilingual_elements", {}),
                "formatting_applied": formatted_response.get("formatting_applied", [])
            }
            
            # Construir sugerencias
            suggestions = {
                "follow_up_suggestions": response_data.get("follow_up_suggestions", []),
                "conversation_direction": response_data.get("next_conversation_direction", "continue"),
                "learning_recommendations": response_data.get("improvement_analysis", {}).get("specific_suggestions", [])
            }
            
            # Estadísticas de sesión
            session_stats = {
                "session_id": self.session_id,
                "turn_number": len(self.conversation_history) + 1,
                "total_interactions": len(self.conversation_history),
                "session_duration_minutes": (datetime.now() - self.session_start_time).total_seconds() / 60,
                "user_level": user_profile.get("language_level", "intermediate")
            }
            
            return {
                # Respuesta principal
                "ai_response": ai_response,
                
                # Análisis detallado
                "analysis": analysis,
                "progress": progress_info,
                "translation": translation_info,
                "formatting": format_info,
                "suggestions": suggestions,
                "session": session_stats,
                
                # Metadatos
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "processing_time_ms": 0,  # Se puede agregar medición real
                "version": "2.0-modular"
            }
            
        except Exception as e:
            logger.error(f"Error building final response: {e}")
            return self._get_error_response("", str(e))

    def _get_error_response(self, user_input: str, error_message: str) -> Dict[str, Any]:
        """ Respuesta de error"""
        return {
            "ai_response": "I'm sorry, I had trouble processing that. Could you try saying it differently?",
            "analysis": {
                "topic": "general",
                "topic_confidence": 0.5,
                "emotion": "neutral",
                "complexity_level": "intermediate",
                "response_strategy": "error_recovery"
            },
            "progress": {
                "improvements_detected": [],
                "areas_to_improve": [],
                "overall_progress_score": 0.5
            },
            "translation": {
                "translation_applied": False
            },
            "formatting": {
                "format_type": "error"
            },
            "suggestions": {
                "follow_up_suggestions": ["Try rephrasing your message"],
                "conversation_direction": "clarification"
            },
            "session": {
                "session_id": self.session_id,
                "turn_number": len(self.conversation_history) + 1
            },
            "success": False,
            "error": error_message,
            "timestamp": datetime.now().isoformat()
        }

    # Métodos auxiliares simplificados
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """ Obtiene historial de conversación"""
        return self.conversation_history.copy()

    def get_user_profile(self) -> Dict[str, Any]:
        """ Obtiene perfil actual del usuario"""
        return self.profile_manager.get_user_profile()

    def get_session_id(self) -> str:
        """ Obtiene ID de sesión"""
        return self.session_id

    def is_session_active(self) -> bool:
        """ Verifica si la sesión está activa"""
        return self.is_active
