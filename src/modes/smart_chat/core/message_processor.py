"""
Message Processor - Procesamiento inteligente completo de mensajes
Migrado y mejorado desde smart_chat_mode.py
"""

import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class MessageProcessor:
    """🧠 Procesador inteligente completo de mensajes"""
    
    def __init__(self, assistant):
        self.assistant = assistant
        self.processing_phases = 8  # Número de fases de análisis
        logger.info("MessageProcessor inicializado con 8 fases de análisis")
    
    def process_intelligent_message(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """🧠 Procesa mensaje con inteligencia contextual completa - MIGRADO"""
        try:
            print(f"   🔄 Ejecutando {self.processing_phases} fases de análisis...")
            
            # 1️⃣ ANÁLISIS DE COMPRENSIÓN
            print("   🔍 Analizando comprensión...")
            comprehension = self._analyze_comprehension(user_input, context)
            
            # 2️⃣ PROCESAMIENTO COGNITIVO
            print("   🤔 Procesamiento cognitivo...")
            thinking = self._cognitive_processing(user_input, comprehension)
            
            # 3️⃣ EVALUACIÓN DE PROGRESO
            print("   📊 Evaluando progreso...")
            progress_evaluation = self._evaluate_progress(user_input, comprehension, thinking)
            
            # 4️⃣ DETECCIÓN DE ERRORES
            print("   ✏️ Detectando errores...")
            error_analysis = self._analyze_errors(user_input, context)
            
            # 5️⃣ ALMACENAMIENTO DE DATOS
            print("   💾 Almacenando datos...")
            self._store_learning_data(user_input, comprehension, thinking, progress_evaluation)
            
            # 6️⃣ ANÁLISIS DE MEJORAS
            print("   📈 Analizando mejoras...")
            improvement_analysis = self._analyze_improvements(progress_evaluation, context)
            
            # 7️⃣ GENERACIÓN DE FEEDBACK
            print("   🎯 Generando feedback...")
            feedback = self._generate_adaptive_feedback(error_analysis, improvement_analysis)
            
            # 8️⃣ CREACIÓN DE RESPUESTA
            print("   💡 Creando respuesta...")
            ai_response = self._generate_intelligent_response(user_input, context, thinking)
            
            # 🏗️ CONSTRUIR RESULTADO COMPLETO
            result = {
                "user_input": user_input,
                "ai_response": ai_response,
                "comprehension": comprehension,
                "thinking": thinking,
                "progress_evaluation": progress_evaluation,
                "error_analysis": error_analysis,
                "feedback": feedback,
                "improvement_analysis": improvement_analysis,
                "processing_phases": self.processing_phases,
                "timestamp": datetime.now().isoformat(),
                "confidence_score": self._calculate_confidence_score(comprehension, thinking)
            }
            
            logger.info(f"Message processed through {self.processing_phases} phases successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in intelligent message processing: {e}")
            return self._get_error_fallback_result(user_input, str(e))

    def _analyze_comprehension(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """🔍 Análisis profundo de comprensión - MIGRADO"""
        try:
            # Análisis básico del input
            input_analysis = self._basic_input_analysis(user_input)
            
            # Detección de idioma y mezcla
            language_analysis = self._detect_language_mix(user_input)
            
            # Análisis de complejidad
            complexity_analysis = self._analyze_complexity(user_input)
            
            # Detección emocional
            emotion_analysis = self._detect_emotion(user_input)
            
            # Análisis de tema
            topic_analysis = self._analyze_topic(user_input)
            
            return {
                "input_length": len(user_input),
                "word_count": len(user_input.split()),
                "language": language_analysis["primary_language"],
                "language_mix": language_analysis["is_mixed"],
                "complexity_level": complexity_analysis["level"],
                "complexity_score": complexity_analysis["score"],
                "emotion": emotion_analysis["primary_emotion"],
                "emotion_confidence": emotion_analysis["confidence"],
                "topic": topic_analysis["primary_topic"],
                "topic_confidence": topic_analysis["confidence"],
                "has_questions": "?" in user_input,
                "input_type": self._classify_input_type(user_input),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in comprehension analysis: {e}")
            return {"error": str(e), "language": "mixed", "complexity_level": "intermediate"}

    def _cognitive_processing(self, user_input: str, comprehension: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """🤔 Procesamiento cognitivo avanzado - MIGRADO"""
        try:
            # Generar respuesta usando el servicio de chat
            cognitive_prompt = self._build_cognitive_prompt(user_input, comprehension)
            cognitive_response = self.assistant.chat_service.generate_response(cognitive_prompt)
            
            # Analizar la respuesta cognitiva
            thinking_analysis = {
                "cognitive_response": cognitive_response,
                "processing_strategy": self._determine_processing_strategy(comprehension),
                "response_approach": self._determine_response_approach(user_input, comprehension),
                "adaptation_level": self._calculate_adaptation_level(comprehension),
                "teaching_opportunities": self._identify_teaching_opportunities(user_input, comprehension)
            }
            
            return thinking_analysis
            
        except Exception as e:
            logger.error(f"Error in cognitive processing: {e}")
            return None

    def _evaluate_progress(self, user_input: str, comprehension: Dict[str, Any], 
                          thinking: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """📊 Evaluación completa de progreso - MIGRADO"""
        try:
            # Indicadores de progreso
            progress_indicators = {
                "improvement_detected": self._detect_improvement(user_input, comprehension),
                "areas_of_growth": self._identify_growth_areas(comprehension),
                "challenge_level": self._assess_challenge_level(comprehension),
                "engagement_level": self._measure_engagement(user_input, comprehension)
            }
            
            # Métricas de progreso
            progress_metrics = {
                "fluency_estimate": self._estimate_fluency(comprehension),
                "complexity_handling": comprehension.get("complexity_score", 0.5),
                "topic_engagement": comprehension.get("topic_confidence", 0.5),
                "emotional_expression": comprehension.get("emotion_confidence", 0.5)
            }
            
            # Recomendaciones de progreso
            progress_recommendations = self._generate_progress_recommendations(
                progress_indicators, progress_metrics
            )
            
            return {
                "progress_indicators": progress_indicators,
                "progress_metrics": progress_metrics,
                "recommendations": progress_recommendations,
                "overall_progress_score": self._calculate_overall_progress_score(progress_metrics),
                "evaluation_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in progress evaluation: {e}")
            return {"error": str(e), "overall_progress_score": 0.5}

    def _analyze_errors(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """✏️ Análisis completo de errores - MIGRADO"""
        try:
            # Usar el servicio de gramática para detectar errores
            grammar_correction = self.assistant.grammar_service.correct_grammar(user_input)
            
            # Analizar tipos de errores
            error_types = self._classify_error_types(user_input, grammar_correction)
            
            # Generar correcciones suaves
            gentle_corrections = self._generate_gentle_corrections(error_types)
            
            return {
                "original_text": user_input,
                "corrected_text": grammar_correction,
                "has_errors": user_input != grammar_correction,
                "error_types": error_types,
                "gentle_corrections": gentle_corrections,
                "error_severity": self._assess_error_severity(error_types),
                "correction_priority": self._prioritize_corrections(error_types)
            }
            
        except Exception as e:
            logger.error(f"Error in error analysis: {e}")
            return {"error": str(e), "has_errors": False}

    def _store_learning_data(self, user_input: str, comprehension: Dict[str, Any], 
                           thinking: Optional[Dict[str, Any]], progress: Dict[str, Any]):
        """💾 Almacena datos de aprendizaje - MIGRADO"""
        try:
            import os
            import json
            
            # Crear directorio si no existe
            session_dir = "data/sessions"
            os.makedirs(session_dir, exist_ok=True)
            
            # Generar nombre de archivo único
            timestamp = int(time.time())
            filename = f"smart_chat_{timestamp}.json"
            filepath = os.path.join(session_dir, filename)
            
            # Preparar datos para almacenar
            learning_data = {
                "session_id": f"smart_chat_{timestamp}",
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "comprehension_analysis": comprehension,
                "cognitive_processing": thinking,
                "progress_evaluation": progress,
                "processing_metadata": {
                    "phases_completed": self.processing_phases,
                    "processing_time": time.time()
                }
            }
            
            # Guardar datos
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(learning_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Progress data saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error storing learning data: {e}")

    def _analyze_improvements(self, progress_evaluation: Dict[str, Any], 
                            context: Dict[str, Any]) -> Dict[str, Any]:
        """📈 Análisis de mejoras - MIGRADO"""
        try:
            progress_indicators = progress_evaluation.get("progress_indicators", {})
            progress_metrics = progress_evaluation.get("progress_metrics", {})
            
            # Detectar áreas de mejora
            improvement_areas = []
            if progress_metrics.get("fluency_estimate", 0) < 0.6:
                improvement_areas.append("fluency")
            if progress_metrics.get("complexity_handling", 0) < 0.5:
                improvement_areas.append("complexity_handling")
            
            # Detectar fortalezas
            strengths = []
            if progress_indicators.get("engagement_level", 0) > 0.7:
                strengths.append("high_engagement")
            if progress_metrics.get("emotional_expression", 0) > 0.6:
                strengths.append("emotional_expression")
            
            return {
                "improvement_areas": improvement_areas,
                "detected_strengths": strengths,
                "improvement_trend": self._calculate_improvement_trend(progress_metrics),
                "next_focus_areas": self._suggest_focus_areas(improvement_areas),
                "motivation_level": progress_indicators.get("engagement_level", 0.5)
            }
            
        except Exception as e:
            logger.error(f"Error in improvement analysis: {e}")
            return {"improvement_areas": [], "detected_strengths": []}

    def _generate_adaptive_feedback(self, error_analysis: Dict[str, Any], 
                                  improvement_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """🎯 Genera feedback adaptativo - MIGRADO"""
        try:
            # Generar logros de aprendizaje
            learning_wins = []
            strengths = improvement_analysis.get("detected_strengths", [])
            if "high_engagement" in strengths:
                learning_wins.append("Excelente participación en la conversación")
            if "emotional_expression" in strengths:
                learning_wins.append("Buena expresión emocional en inglés")
            
            # Generar correcciones suaves
            gentle_corrections = error_analysis.get("gentle_corrections", [])
            
            # Generar sugerencias de mejora
            improvement_suggestions = []
            improvement_areas = improvement_analysis.get("improvement_areas", [])
            for area in improvement_areas:
                if area == "fluency":
                    improvement_suggestions.append("Practica con frases más largas")
                elif area == "complexity_handling":
                    improvement_suggestions.append("Intenta usar vocabulario más variado")
            
            return {
                "learning_wins": learning_wins,
                "gentle_corrections": gentle_corrections,
                "improvement_suggestions": improvement_suggestions,
                "encouragement_level": self._calculate_encouragement_level(error_analysis, improvement_analysis),
                "feedback_tone": self._determine_feedback_tone(improvement_analysis)
            }
            
        except Exception as e:
            logger.error(f"Error generating adaptive feedback: {e}")
            return {"learning_wins": [], "gentle_corrections": [], "improvement_suggestions": []}

    def _generate_intelligent_response(self, user_input: str, context: Dict[str, Any], 
                                     thinking: Optional[Dict[str, Any]]) -> str:
        """💡 Genera respuesta inteligente contextual - MIGRADO"""
        try:
            # Detectar tema específico para respuesta más relevante
            user_lower = user_input.lower()
            
            if 'futbol' in user_lower or 'fútbol' in user_lower or 'football' in user_lower or 'soccer' in user_lower:
                # Respuesta específica para fútbol
                prompt = self._build_soccer_prompt(user_input, context)
                
            elif 'food' in user_lower or 'comida' in user_lower:
                # Respuesta específica para comida
                prompt = self._build_food_prompt(user_input, context)
                
            elif '?' in user_input and len(user_input.strip()) < 15:
                # Respuesta para confusión (preguntas cortas)
                prompt = self._build_clarification_prompt(user_input, context)
                
            else:
                # Prompt general pero contextual
                prompt = self._build_general_contextual_prompt(user_input, context)

            # Generar respuesta usando el servicio de chat
            response = self.assistant.chat_service.generate_response(prompt)
            
            # Limpiar y validar respuesta
            if response and len(response.strip()) > 5:
                return response.strip()
            else:
                return self._get_fallback_response(user_input, context)
            
        except Exception as e:
            logger.error(f"Error generating intelligent response: {e}")
            return self._get_fallback_response(user_input, context)

    # ================ MÉTODOS AUXILIARES ================

    def _basic_input_analysis(self, user_input: str) -> Dict[str, Any]:
        """📝 Análisis básico del input"""
        return {
            "length": len(user_input),
            "word_count": len(user_input.split()),
            "has_punctuation": any(p in user_input for p in '.,!?'),
            "is_question": '?' in user_input,
            "is_short": len(user_input.split()) < 3
        }

    def _detect_language_mix(self, user_input: str) -> Dict[str, Any]:
        """🌐 Detecta mezcla de idiomas"""
        spanish_words = ['de', 'el', 'la', 'que', 'es', 'en', 'un', 'una', 'con', 'por', 'para', 'como', 'más', 'pero', 'su', 'me', 'ya', 'muy', 'todo', 'si', 'le', 'da', 'mi', 'te', 'y', 'a', 'se', 'lo', 'futbol', 'fútbol', 'comida']
        english_words = ['the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'you', 'that', 'he', 'was', 'for', 'on', 'are', 'as', 'with', 'his', 'they', 'i', 'at', 'be', 'this', 'have', 'from', 'or', 'one', 'had', 'by', 'word', 'but', 'not', 'what', 'all', 'were', 'we', 'when', 'your', 'can', 'said', 'there', 'each', 'which', 'do', 'how', 'their', 'if', 'will', 'up', 'other', 'about', 'out', 'many', 'then', 'them', 'these', 'so', 'some', 'her', 'would', 'make', 'like', 'into', 'him', 'time', 'has', 'two', 'more', 'go', 'no', 'way', 'could', 'my', 'than', 'first', 'water', 'been', 'call', 'who', 'its', 'now', 'find', 'long', 'down', 'day', 'did', 'get', 'come', 'made', 'may', 'part', 'soccer', 'football', 'food']
        
        words = user_input.lower().split()
        spanish_count = sum(1 for word in words if word in spanish_words)
        english_count = sum(1 for word in words if word in english_words)
        total_words = len(words)
        
        if total_words == 0:
            return {"primary_language": "unknown", "is_mixed": False}
        
        spanish_ratio = spanish_count / total_words
        english_ratio = english_count / total_words
        
        if spanish_ratio > english_ratio:
            primary = "spanish"
        elif english_ratio > spanish_ratio:
            primary = "english"
        else:
            primary = "mixed"
        
        is_mixed = spanish_count > 0 and english_count > 0
        
        return {
            "primary_language": primary,
            "is_mixed": is_mixed,
            "spanish_ratio": spanish_ratio,
            "english_ratio": english_ratio
        }

    def _analyze_complexity(self, user_input: str) -> Dict[str, Any]:
        """🔍 Analiza complejidad del input"""
        words = user_input.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        # Factores de complejidad
        has_long_words = any(len(word) > 6 for word in words)
        has_complex_structure = len(words) > 8
        has_subordination = any(word in user_input.lower() for word in ['because', 'although', 'however', 'therefore'])
        
        # Calcular score de complejidad
        complexity_score = 0
        if avg_word_length > 4: complexity_score += 0.3
        if has_long_words: complexity_score += 0.2
        if has_complex_structure: complexity_score += 0.3
        if has_subordination: complexity_score += 0.2
        
        # Determinar nivel
        if complexity_score > 0.6:
            level = "advanced"
        elif complexity_score > 0.3:
            level = "intermediate"
        else:
            level = "beginner"
        
        return {
            "level": level,
            "score": min(1.0, complexity_score),
            "avg_word_length": avg_word_length,
            "has_complex_structure": has_complex_structure
        }

    def _detect_emotion(self, user_input: str) -> Dict[str, Any]:
        """😊 Detecta emoción en el input"""
        input_lower = user_input.lower()
        
        # Palabras emocionales
        positive_words = ['great', 'awesome', 'love', 'like', 'enjoy', 'fantastic', 'amazing', 'wonderful', 'excellent', 'perfect', 'bueno', 'genial', 'me gusta', 'excelente']
        negative_words = ['bad', 'hate', 'terrible', 'awful', 'horrible', 'worst', 'disgusting', 'malo', 'odio', 'terrible']
        confused_words = ['confused', 'don\'t understand', 'what', 'how', 'why', 'confuso', 'no entiendo', 'qué', 'cómo', 'por qué']
        excited_words = ['excited', 'can\'t wait', 'amazing', 'incredible', 'wow', 'emocionado', 'increíble', 'guau']
        
        # Contar palabras emocionales
        positive_count = sum(1 for word in positive_words if word in input_lower)
        negative_count = sum(1 for word in negative_words if word in input_lower)
        confused_count = sum(1 for word in confused_words if word in input_lower)
        excited_count = sum(1 for word in excited_words if word in input_lower)
        
        # Detectar preguntas cortas (confusión)
        if '?' in user_input and len(user_input.strip()) < 15:
            confused_count += 2
        
        # Determinar emoción predominante
        emotion_scores = {
            "positive": positive_count,
            "negative": negative_count,
            "confused": confused_count,
            "excited": excited_count,
            "neutral": 1  # Base neutral
        }
        
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[primary_emotion] / sum(emotion_scores.values())
        
        return {
            "primary_emotion": primary_emotion,
            "confidence": confidence,
            "emotion_scores": emotion_scores
        }

    def _analyze_topic(self, user_input: str) -> Dict[str, Any]:
        """🎯 Analiza tema del input"""
        input_lower = user_input.lower()
        
        # Temas y palabras clave
        topics = {
            "soccer": ['soccer', 'football', 'futbol', 'fútbol', 'team', 'player', 'game', 'sport', 'match', 'goal', 'play', 'position'],
            "food": ['food', 'comida', 'eat', 'cook', 'restaurant', 'dish', 'meal', 'cuisine', 'delicious', 'taste', 'flavor'],
            "travel": ['travel', 'trip', 'vacation', 'country', 'city', 'visit', 'tourism', 'viaje', 'país', 'ciudad'],
            "music": ['music', 'song', 'band', 'singer', 'concert', 'instrument', 'música', 'canción', 'banda'],
            "family": ['family', 'mother', 'father', 'brother', 'sister', 'parents', 'familia', 'madre', 'padre'],
            "work": ['work', 'job', 'office', 'career', 'business', 'company', 'trabajo', 'oficina', 'empresa']
        }
        
        # Calcular scores por tema
        topic_scores = {}
        for topic, keywords in topics.items():
            score = sum(1 for keyword in keywords if keyword in input_lower)
            if score > 0:
                topic_scores[topic] = score
        
        if not topic_scores:
            return {"primary_topic": "general", "confidence": 0.5}
        
        primary_topic = max(topic_scores, key=topic_scores.get)
        confidence = topic_scores[primary_topic] / sum(topic_scores.values())
        
        return {
            "primary_topic": primary_topic,
            "confidence": confidence,
            "topic_scores": topic_scores
        }

    def _classify_input_type(self, user_input: str) -> str:
        """📋 Clasifica tipo de input"""
        if '?' in user_input:
            return "question"
        elif len(user_input.split()) < 3:
            return "short_response"
        elif any(word in user_input.lower() for word in ['i think', 'i believe', 'in my opinion', 'creo que', 'pienso que']):
            return "opinion"
        elif any(word in user_input.lower() for word in ['i like', 'i love', 'i enjoy', 'me gusta', 'me encanta']):
            return "preference"
        else:
            return "statement"

    def _build_soccer_prompt(self, user_input: str, context: Dict[str, Any]) -> str:
        """⚽ Construye prompt específico para soccer"""
        return f"""You are an enthusiastic English teacher who loves sports. A student wants to talk about soccer/football.

Student said: "{user_input}"
Their level: {context.get('language_level', 'intermediate')}

Respond enthusiastically about soccer in English (1-2 sentences max). Ask follow-up questions about their soccer experience:"""

    def _build_food_prompt(self, user_input: str, context: Dict[str, Any]) -> str:
        """🍕 Construye prompt específico para comida"""
        return f"""You are a friendly English teacher who enjoys talking about food and cooking. A student wants to discuss food.

Student said: "{user_input}"
Their level: {context.get('language_level', 'intermediate')}

Respond warmly about food in English (1-2 sentences max). Ask about their food preferences or cooking experience:"""

    def _build_clarification_prompt(self, user_input: str, context: Dict[str, Any]) -> str:
        """❓ Construye prompt para clarificación"""
        return f"""You are a patient English teacher. A student seems confused and asked: "{user_input}"

Provide a helpful clarification in English (1-2 sentences). Be clear and supportive:"""

    def _build_general_contextual_prompt(self, user_input: str, context: Dict[str, Any]) -> str:
        """🌐 Construye prompt general pero contextual"""
        emotion = context.get('emotion', 'neutral')
        topic = context.get('topic', 'general')
        
        return f"""You are a friendly English teacher having a natural conversation. 

Student said: "{user_input}"
Student's emotion: {emotion}
Topic: {topic}
Their level: {context.get('language_level', 'intermediate')}

Respond naturally in English (1-2 sentences max). Be encouraging and engaging:"""

    def _get_fallback_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """🛡️ Respuesta de emergencia contextual"""
        user_lower = user_input.lower()
        
        # Respuestas específicas por tema
        if any(word in user_lower for word in ['futbol', 'fútbol', 'football', 'soccer']):
            return "Football is such an exciting sport! What's your favorite team or player?"
        
        elif any(word in user_lower for word in ['food', 'comida']):
            return "Food is a wonderful topic! What kind of cuisine do you enjoy most?"
        
        elif '?' in user_input and len(user_input.strip()) < 15:
            return "That's a great question! Let me help you understand that better."
        
        else:
            return "That's interesting! I'd love to hear more about your thoughts on this."

    def _get_error_fallback_result(self, user_input: str, error_msg: str) -> Dict[str, Any]:
        """🚨 Resultado de fallback en caso de error"""
        return {
            "user_input": user_input,
            "ai_response": "I understand what you're saying. Let's continue our conversation!",
            "error": error_msg,
            "processing_phases": 0,
            "timestamp": datetime.now().isoformat(),
            "confidence_score": 0.3
        }

    def _calculate_confidence_score(self, comprehension: Dict[str, Any], thinking: Optional[Dict[str, Any]]) -> float:
        """📊 Calcula score de confianza del procesamiento"""
        base_score = 0.7
        
        # Ajustar según comprensión
        if comprehension.get("complexity_level") == "advanced":
            base_score += 0.1
        elif comprehension.get("complexity_level") == "beginner":
            base_score -= 0.1
        
        # Ajustar según procesamiento cognitivo
        if thinking and thinking.get("cognitive_response"):
            base_score += 0.1
        
        return min(1.0, max(0.0, base_score))

    # ================ MÉTODOS AUXILIARES ADICIONALES ================
    
    def _detect_improvement(self, user_input: str, comprehension: Dict[str, Any]) -> bool:
        """📈 Detecta si hay mejora en el mensaje"""
        # Lógica simple para detectar mejora
        return comprehension.get("complexity_score", 0) > 0.5

    def _identify_growth_areas(self, comprehension: Dict[str, Any]) -> List[str]:
        """🌱 Identifica áreas de crecimiento"""
        areas = []
        if comprehension.get("emotion_confidence", 0) > 0.6:
            areas.append("emotional_expression")
        if comprehension.get("topic_confidence", 0) > 0.7:
            areas.append("topic_knowledge")
        return areas

    def _assess_challenge_level(self, comprehension: Dict[str, Any]) -> str:
        """🎯 Evalúa nivel de desafío"""
        complexity = comprehension.get("complexity_score", 0.5)
        if complexity > 0.7:
            return "high"
        elif complexity > 0.4:
            return "medium"
        else:
            return "low"

    def _measure_engagement(self, user_input: str, comprehension: Dict[str, Any]) -> float:
        """📊 Mide nivel de engagement"""
        base_engagement = 0.5
        
        # Aumentar por longitud del mensaje
        if len(user_input.split()) > 5:
            base_engagement += 0.2
        
        # Aumentar por emoción positiva
        if comprehension.get("emotion") in ["positive", "excited"]:
            base_engagement += 0.2
        
        return min(1.0, base_engagement)

    def _estimate_fluency(self, comprehension: Dict[str, Any]) -> float:
        """🗣️ Estima fluidez"""
        complexity = comprehension.get("complexity_score", 0.5)
        language_mix = comprehension.get("language_mix", False)
        
        fluency = complexity
        if language_mix:
            fluency -= 0.1  # Penalizar mezcla de idiomas
        
        return max(0.0, min(1.0, fluency))

    def _calculate_overall_progress_score(self, metrics: Dict[str, Any]) -> float:
        """📊 Calcula score general de progreso"""
        scores = [
            metrics.get("fluency_estimate", 0.5),
            metrics.get("complexity_handling", 0.5),
            metrics.get("topic_engagement", 0.5),
            metrics.get("emotional_expression", 0.5)
        ]
        return sum(scores) / len(scores)

    def _generate_progress_recommendations(self, indicators: Dict[str, Any], metrics: Dict[str, Any]) -> List[str]:
        """💡 Genera recomendaciones de progreso"""
        recommendations = []
        
        if metrics.get("fluency_estimate", 0) < 0.6:
            recommendations.append("Practica con oraciones más largas")
        
        if indicators.get("engagement_level", 0) > 0.7:
            recommendations.append("Continúa con tu excelente participación")
        
        return recommendations

    def _classify_error_types(self, original: str, corrected: str) -> List[str]:
        """📝 Clasifica tipos de errores"""
        if original == corrected:
            return []
        
        error_types = []
        
        # Detectar errores básicos
        if len(original.split()) != len(corrected.split()):
            error_types.append("word_order")
        
        if original.lower() != corrected.lower():
            error_types.append("grammar")
        
        return error_types

    def _generate_gentle_corrections(self, error_types: List[str]) -> List[Dict[str, str]]:
        """✏️ Genera correcciones suaves"""
        corrections = []
        
        for error_type in error_types:
            if error_type == "grammar":
                corrections.append({
                    "error": "Pequeño ajuste gramatical",
                    "correction": "Versión corregida disponible",
                    "explanation": "Solo un pequeño ajuste para que suene más natural"
                })
        
        return corrections

    def _assess_error_severity(self, error_types: List[str]) -> str:
        """⚖️ Evalúa severidad de errores"""
        if not error_types:
            return "none"
        elif len(error_types) == 1:
            return "minor"
        else:
            return "moderate"

    def _prioritize_corrections(self, error_types: List[str]) -> List[str]:
        """🎯 Prioriza correcciones"""
        priority_order = ["grammar", "word_order", "spelling"]
        return [et for et in priority_order if et in error_types]

    def _calculate_improvement_trend(self, metrics: Dict[str, Any]) -> str:
        """📈 Calcula tendencia de mejora"""
        avg_score = sum(metrics.values()) / len(metrics) if metrics else 0.5
        
        if avg_score > 0.7:
            return "positive"
        elif avg_score > 0.4:
            return "stable"
        else:
            return "needs_attention"

    def _suggest_focus_areas(self, improvement_areas: List[str]) -> List[str]:
        """🎯 Sugiere áreas de enfoque"""
        if "fluency" in improvement_areas:
            return ["practice_longer_sentences", "use_connectors"]
        elif "complexity_handling" in improvement_areas:
            return ["expand_vocabulary", "try_complex_structures"]
        else:
            return ["maintain_current_level"]

    def _calculate_encouragement_level(self, error_analysis: Dict[str, Any], improvement_analysis: Dict[str, Any]) -> str:
        """💪 Calcula nivel de ánimo necesario"""
        has_errors = error_analysis.get("has_errors", False)
        strengths = improvement_analysis.get("detected_strengths", [])
        
        if has_errors and not strengths:
            return "high"  # Necesita mucho ánimo
        elif has_errors and strengths:
            return "moderate"  # Balance entre ánimo y corrección
        else:
            return "low"  # Solo celebrar logros

    def _determine_feedback_tone(self, improvement_analysis: Dict[str, Any]) -> str:
        """🎵 Determina tono del feedback"""
        motivation = improvement_analysis.get("motivation_level", 0.5)
        
        if motivation > 0.7:
            return "celebratory"
        elif motivation > 0.4:
            return "encouraging"
        else:
            return "supportive"

    def _determine_processing_strategy(self, comprehension: Dict[str, Any]) -> str:
        """🧠 Determina estrategia de procesamiento"""
        complexity = comprehension.get("complexity_level", "intermediate")
        emotion = comprehension.get("emotion", "neutral")
        
        if emotion == "confused":
            return "clarification_focused"
        elif complexity == "beginner":
            return "supportive_simple"
        elif complexity == "advanced":
            return "challenging_engaging"
        else:
            return "balanced_adaptive"

    def _determine_response_approach(self, user_input: str, comprehension: Dict[str, Any]) -> str:
        """🎯 Determina enfoque de respuesta"""
        topic = comprehension.get("topic", "general")
        emotion = comprehension.get("emotion", "neutral")
        
        if emotion == "confused":
            return "clarifying"
        elif topic in ["soccer", "food"]:
            return "topic_specific"
        else:
            return "general_engaging"

    def _calculate_adaptation_level(self, comprehension: Dict[str, Any]) -> float:
        """⚙️ Calcula nivel de adaptación necesario"""
        complexity = comprehension.get("complexity_score", 0.5)
        emotion_confidence = comprehension.get("emotion_confidence", 0.5)
        
        return (complexity + emotion_confidence) / 2

    def _identify_teaching_opportunities(self, user_input: str, comprehension: Dict[str, Any]) -> List[str]:
        """🎓 Identifica oportunidades de enseñanza"""
        opportunities = []
        
        topic = comprehension.get("topic", "general")
        if topic == "soccer":
            opportunities.append("sports_vocabulary")
        elif topic == "food":
            opportunities.append("food_vocabulary")
        
        if comprehension.get("has_questions", False):
            opportunities.append("question_formation")
        
        return opportunities
