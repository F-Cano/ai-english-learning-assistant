import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import os
import logging

logger = logging.getLogger(__name__)

@dataclass
class UserProgress:
    """Seguimiento detallado del progreso del usuario"""
    session_id: str
    total_messages: int = 0
    grammar_errors: int = 0
    vocabulary_level: str = "beginner"
    fluency_score: float = 0.0
    topics_discussed: List[str] = None
    improvement_areas: List[str] = None
    strengths: List[str] = None
    session_start: str = None
    last_activity: str = None
    
    def __post_init__(self):
        if self.topics_discussed is None:
            self.topics_discussed = []
        if self.improvement_areas is None:
            self.improvement_areas = []
        if self.strengths is None:
            self.strengths = []
        if self.session_start is None:
            self.session_start = datetime.now().isoformat()

@dataclass
class MessageAnalysis:
    """Análisis completo de un mensaje"""
    original_text: str
    detected_language: str
    grammar_errors: List[Dict[str, str]]
    vocabulary_level: str
    complexity_score: float
    emotional_tone: str
    learning_intent: str
    topics: List[str]
    fluency_indicators: Dict[str, Any]
    timestamp: str

class SmartChatMode:
    """Chat Mode con IA verdaderamente inteligente y análisis profundo"""
    
    def __init__(self, assistant):
        """Inicializa el Chat Mode inteligente"""
        self.assistant = assistant
        self.session_id = f"smart_chat_{int(time.time())}"
        
        # 🔧 CARGAR PERFIL ANTES DE CREAR PROGRESO
        self.learning_profile = self._load_or_create_learning_profile()
        
        # Crear progreso de sesión
        self.user_progress = UserProgress(session_id=self.session_id)
        self.conversation_history: List[Dict[str, Any]] = []
        self.analysis_cache = {}
        
        # Configuración
        self.deep_analysis_enabled = True
        self.progress_tracking_enabled = True
        self.feedback_mode = "adaptive"
        
        # 🚀 ACTUALIZAR PERFIL AL INICIAR
        self._update_profile_on_session_start()

    def run(self):
        """Ejecuta el chat inteligente"""
        print("\n🧠 CHAT INTELIGENTE - IA Avanzada Bilingüe")
        print("=" * 70)
        print("🎯 Análisis profundo en tiempo real")
        print("📊 Seguimiento de progreso automático") 
        print("🔍 Detección inteligente de errores")
        print("📈 Feedback adaptativo personalizado")
        print("🌐 Respuestas bilingües (inglés + español)")
        print("⚡ Optimizado para velocidad")
        
        # 🔧 MOSTRAR BIENVENIDA PERSONALIZADA
        self._show_welcome_message_with_profile()
        
        # 🌐 MENSAJE DE BIENVENIDA BILINGÜE (YA NO SOLO INGLÉS)
        welcome = self._generate_personalized_welcome()
        print(f"\n🤖 IA: {welcome}")
        
        while True:
            try:
                # Obtener entrada del usuario
                user_input = self._get_user_input()
                
                if not user_input.strip():
                    continue
                
                # Verificar comandos especiales
                if self._handle_commands(user_input):
                    continue
                
                # Salir si es necesario
                if self._is_exit_command(user_input):
                    break
                
                # 🧠 PROCESAMIENTO INTELIGENTE COMPLETO
                print("\n🧠 Analizando mensaje...")
                analysis_result = self._process_message_intelligently(user_input)
                
                # 🌐 MOSTRAR RESPUESTA BILINGÜE (CORREGIR MÉTODO)
                self._display_intelligent_bilingual_response(analysis_result)
                
                # Actualizar perfiles y progreso
                self._update_learning_analytics(analysis_result)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
    
        self._show_session_summary()
    
    def _process_message_intelligently(self, user_input: str) -> Dict[str, Any]:
        """🧠 Procesamiento inteligente completo del mensaje"""
        
        # FASE 1: 🔍 COMPRENSIÓN PROFUNDA
        print("   🔍 Analizando comprensión...")
        comprehension = self._deep_comprehension_analysis(user_input)
        
        # FASE 2: 🤔 ANÁLISIS COGNITIVO  
        print("   🤔 Procesamiento cognitivo...")
        cognitive_analysis = self._cognitive_processing(user_input, comprehension)
        
        # FASE 3: 📊 EVALUACIÓN DE PROGRESO
        print("   📊 Evaluando progreso...")
        progress_evaluation = self._evaluate_user_progress(user_input, comprehension)
        
        # FASE 4: ✏️ DETECCIÓN AVANZADA DE ERRORES
        print("   ✏️ Detectando errores...")
        error_analysis = self._advanced_error_detection(user_input)
        
        # FASE 5: 💾 ALMACENAMIENTO INTELIGENTE
        print("   💾 Almacenando datos...")
        storage_result = self._intelligent_data_storage(user_input, comprehension, error_analysis)
        
        # FASE 6: 📈 ANÁLISIS DE MEJORA
        print("   📈 Analizando mejoras...")
        improvement_analysis = self._analyze_improvement_patterns()
        
        # FASE 7: 🎯 GENERACIÓN DE FEEDBACK
        print("   🎯 Generando feedback...")
        feedback = self._generate_adaptive_feedback(
            comprehension, cognitive_analysis, progress_evaluation, 
            error_analysis, improvement_analysis
        )
        
        # FASE 8: 💡 RESPUESTA ADAPTATIVA
        print("   💡 Creando respuesta...")
        ai_response = self._generate_adaptive_response(
            user_input, comprehension, cognitive_analysis, feedback
        )
        
        return {
            'user_input': user_input,
            'comprehension': comprehension,
            'cognitive_analysis': cognitive_analysis,
            'progress_evaluation': progress_evaluation,
            'error_analysis': error_analysis,
            'improvement_analysis': improvement_analysis,
            'feedback': feedback,
            'ai_response': ai_response,
            'timestamp': datetime.now().isoformat(),
            'processing_phases': 8
        }
    
    def _deep_comprehension_analysis(self, user_input: str) -> Dict[str, Any]:
        """🔍 Análisis profundo de comprensión"""
        try:
            comprehension_prompt = f"""
Perform deep comprehension analysis of this user message as an advanced AI language learning system.

User message: "{user_input}"

Analyze comprehensively and respond in JSON format:
{{
    "language_detected": "en|es|mixed",
    "complexity_level": "A1|A2|B1|B2|C1|C2",
    "intent_type": "question|statement|request|confusion|practice|conversation",
    "emotional_state": "confident|uncertain|frustrated|curious|excited|neutral",
    "grammar_complexity": "basic|intermediate|advanced",
    "vocabulary_sophistication": "elementary|intermediate|advanced",
    "sentence_structure": "simple|compound|complex",
    "communication_goal": "learn|practice|get_help|casual_chat|seek_correction",
    "topic_category": "identified_topic",
    "fluency_indicators": {{
        "natural_flow": "poor|fair|good|excellent",
        "word_choice": "limited|adequate|varied|sophisticated",
        "coherence": "unclear|basic|clear|very_clear"
    }},
    "learning_signals": ["signal1", "signal2"]
}}
"""

            response = self.assistant.chat_service.generate_response(
                comprehension_prompt,
                "Analyze this message deeply for language learning insights."
            )
            
            try:
                analysis = json.loads(response)
                return analysis
            except json.JSONDecodeError:
                return self._fallback_comprehension_analysis(user_input)
                
        except Exception as e:
            print(f"      ⚠️ Error en comprensión: {e}")
            return self._fallback_comprehension_analysis(user_input)
    
    def _cognitive_processing(self, user_input: str, comprehension: Dict[str, Any]) -> Dict[str, Any]:
        """🤔 Procesamiento cognitivo avanzado"""
        try:
            cognitive_prompt = f"""
As an advanced AI language tutor, perform cognitive processing analysis.

User message: "{user_input}"
Comprehension analysis: {json.dumps(comprehension, indent=2)}

Think strategically about:
1. What does this user REALLY need right now?
2. What are the hidden learning opportunities?
3. How can I challenge them appropriately?
4. What misconceptions might they have?
5. How does this fit their learning journey?

Respond in JSON:
{{
    "user_needs_assessment": "what_user_needs_most",
    "learning_opportunities": ["opportunity1", "opportunity2"],
    "appropriate_challenge_level": "too_easy|just_right|too_hard",
    "potential_misconceptions": ["misconception1"],
    "learning_stage": "beginner|developing|intermediate|advanced|proficient",
    "cognitive_load": "low|medium|high",
    "recommended_approach": "supportive|challenging|corrective|encouraging",
    "next_steps_suggestion": "what_to_focus_on_next",
    "engagement_strategy": "how_to_keep_them_engaged"
}}
"""

            response = self.assistant.chat_service.generate_response(
                cognitive_prompt,
                "Perform cognitive analysis for optimal learning."
            )
            
            try:
                analysis = json.loads(response)
                return analysis
            except json.JSONDecodeError:
                return self._fallback_cognitive_analysis(comprehension)
                
        except Exception as e:
            print(f"      ⚠️ Error en procesamiento cognitivo: {e}")
            return self._fallback_cognitive_analysis(comprehension)
    
    def _evaluate_user_progress(self, user_input: str, comprehension: Dict[str, Any]) -> Dict[str, Any]:
        """📊 Evaluación inteligente del progreso"""
        try:
            # Obtener historial reciente para comparación
            recent_history = self._get_recent_performance_data()
            
            evaluation_prompt = f"""
Evaluate user progress based on current message and recent performance history.

Current message: "{user_input}"
Current analysis: {json.dumps(comprehension, indent=2)}
Recent performance: {json.dumps(recent_history, indent=2)}

Evaluate and respond in JSON:
{{
    "current_performance": {{
        "grammar_accuracy": "poor|fair|good|excellent",
        "vocabulary_usage": "limited|adequate|good|advanced",
        "fluency_level": "low|medium|high",
        "complexity_handling": "struggling|developing|comfortable|advanced"
    }},
    "progress_indicators": {{
        "improvement_detected": true/false,
        "areas_of_growth": ["area1", "area2"],
        "areas_needing_work": ["area1", "area2"],
        "consistency_level": "inconsistent|developing|stable|strong"
    }},
    "learning_velocity": "slow|steady|fast|accelerating",
    "confidence_indicators": "low|building|moderate|high",
    "readiness_for_advancement": true/false,
    "personalized_recommendations": ["rec1", "rec2"]
}}
"""

            response = self.assistant.chat_service.generate_response(
                evaluation_prompt,
                "Evaluate comprehensive user progress."
            )
            
            try:
                evaluation = json.loads(response)
                return evaluation
            except json.JSONDecodeError:
                return self._fallback_progress_evaluation()
                
        except Exception as e:
            print(f"      ⚠️ Error en evaluación de progreso: {e}")
            return self._fallback_progress_evaluation()
    
    def _advanced_error_detection(self, user_input: str) -> Dict[str, Any]:
        """✏️ Detección avanzada de errores con contexto"""
        try:
            # Usar el servicio de gramática existente
            grammar_correction = self.assistant.grammar_service.correct(user_input)
            
            # Análisis más profundo con IA
            error_prompt = f"""
Perform advanced error analysis beyond basic grammar correction.

Original: "{user_input}"
Grammar correction: "{grammar_correction}"

Analyze comprehensively and respond in JSON:
{{
    "grammar_errors": [
        {{
            "type": "subject_verb|article|preposition|tense|etc",
            "original": "incorrect_phrase",
            "corrected": "correct_phrase", 
            "explanation": "why_this_is_wrong",
            "severity": "minor|moderate|major"
        }}
    ],
    "style_issues": [
        {{
            "issue": "word_choice|formality|clarity|etc",
            "suggestion": "improvement_suggestion",
            "impact": "readability|professionalism|clarity"
        }}
    ],
    "vocabulary_opportunities": [
        {{
            "basic_word": "simple_word_used",
            "advanced_alternatives": ["alternative1", "alternative2"],
            "context_appropriateness": "explanation"
        }}
    ],
    "overall_assessment": {{
        "error_density": "low|medium|high",
        "error_patterns": ["pattern1", "pattern2"],
        "improvement_priority": "grammar|vocabulary|style|fluency"
    }}
}}
"""

            response = self.assistant.chat_service.generate_response(
                error_prompt,
                "Perform comprehensive error analysis."
            )
            
            try:
                error_analysis = json.loads(response)
                # Agregar corrección básica si no está incluida
                error_analysis['basic_correction'] = grammar_correction
                return error_analysis
            except json.JSONDecodeError:
                return self._fallback_error_analysis(user_input, grammar_correction)
                
        except Exception as e:
            print(f"      ⚠️ Error en detección de errores: {e}")
            return self._fallback_error_analysis(user_input, None)
    
    def _intelligent_data_storage(self, user_input: str, comprehension: Dict[str, Any], error_analysis: Dict[str, Any]) -> Dict[str, str]:
        """💾 Almacenamiento inteligente de datos de aprendizaje"""
        try:
            # Actualizar progreso del usuario
            self.user_progress.total_messages += 1
            self.user_progress.last_activity = datetime.now().isoformat()
            
            # Extraer datos relevantes
            if comprehension.get('complexity_level'):
                self.user_progress.vocabulary_level = comprehension['complexity_level']
            
            # Contar errores
            grammar_errors = len(error_analysis.get('grammar_errors', []))
            self.user_progress.grammar_errors += grammar_errors
            
            # Actualizar temas discutidos
            topic = comprehension.get('topic_category')
            if topic and topic not in self.user_progress.topics_discussed:
                self.user_progress.topics_discussed.append(topic)
            
            # Guardar mensaje en historial
            message_record = {
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input,
                'comprehension_level': comprehension.get('complexity_level'),
                'error_count': grammar_errors,
                'topic': topic,
                'emotional_state': comprehension.get('emotional_state'),
                'fluency_score': self._calculate_fluency_score(comprehension)
            }
            
            self.conversation_history.append(message_record)
            
            # Persistir datos
            self._save_progress_data()
            
            return {
                'status': 'success',
                'records_updated': 'user_progress, conversation_history',
                'new_topics': str(len(self.user_progress.topics_discussed)),
                'total_messages': str(self.user_progress.total_messages)
            }
            
        except Exception as e:
            print(f"      ⚠️ Error en almacenamiento: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _analyze_improvement_patterns(self) -> Dict[str, Any]:
        """📈 Análisis profundo de patrones de mejora"""
        try:
            if len(self.conversation_history) < 3:
                return {'status': 'insufficient_data', 'message': 'Necesitamos más datos'}
            
            # Analizar últimos mensajes vs anteriores
            recent_messages = self.conversation_history[-5:]
            older_messages = self.conversation_history[-10:-5] if len(self.conversation_history) >= 10 else []
            
            improvement_prompt = f"""
Analyze learning improvement patterns from conversation data.

Recent messages (last 5): {json.dumps(recent_messages, indent=2)}
Older messages (previous 5): {json.dumps(older_messages, indent=2)}

Analyze patterns and respond in JSON:
{{
    "improvement_trends": {{
        "grammar_accuracy": "improving|stable|declining",
        "vocabulary_complexity": "growing|stable|simplifying", 
        "fluency_development": "increasing|steady|struggling",
        "confidence_level": "building|stable|decreasing"
    }},
    "learning_velocity": {{
        "speed": "slow|moderate|fast",
        "consistency": "irregular|developing|consistent",
        "breakthrough_moments": ["moment1", "moment2"]
    }},
    "areas_of_excellence": ["strength1", "strength2"],
    "areas_needing_focus": ["weakness1", "weakness2"],
    "predicted_next_milestone": "what_user_will_achieve_next",
    "learning_style_indicators": ["visual|auditory|kinesthetic|etc"],
    "motivation_level": "low|moderate|high|very_high"
}}
"""

            response = self.assistant.chat_service.generate_response(
                improvement_prompt,
                "Analyze comprehensive learning improvement patterns."
            )
            
            try:
                analysis = json.loads(response)
                return analysis
            except json.JSONDecodeError:
                return self._fallback_improvement_analysis()
                
        except Exception as e:
            print(f"      ⚠️ Error en análisis de mejora: {e}")
            return self._fallback_improvement_analysis()
    
    def _generate_adaptive_feedback(self, comprehension: Dict[str, Any], cognitive: Dict[str, Any], 
                                   progress: Dict[str, Any], errors: Dict[str, Any], 
                                   improvement: Dict[str, Any]) -> Dict[str, Any]:
        """🎯 Generación de feedback adaptativo personalizado"""
        try:
            feedback_prompt = f"""
Generate highly personalized, adaptive feedback for a language learner.

Analysis data:
- Comprehension: {json.dumps(comprehension, indent=2)}
- Cognitive assessment: {json.dumps(cognitive, indent=2)}  
- Progress evaluation: {json.dumps(progress, indent=2)}
- Error analysis: {json.dumps(errors, indent=2)}
- Improvement patterns: {json.dumps(improvement, indent=2)}

Create feedback that is:
1. Encouraging but honest
2. Specific and actionable
3. Appropriate for their level
4. Motivating for continued learning

Respond in JSON:
{{
    "primary_feedback": "main_encouraging_message",
    "specific_improvements": ["improvement1", "improvement2"],
    "gentle_corrections": [
        {{
            "error": "what_they_did",
            "correction": "how_to_fix_it",
            "explanation": "why_this_matters"
        }}
    ],
    "learning_wins": ["achievement1", "achievement2"],
    "next_challenges": ["challenge1", "challenge2"],
    "motivation_boost": "personalized_encouraging_message",
    "practical_tips": ["tip1", "tip2"],
    "progress_acknowledgment": "recognition_of_growth"
}}
"""

            response = self.assistant.chat_service.generate_response(
                feedback_prompt,
                "Generate personalized adaptive feedback."
            )
            
            try:
                feedback = json.loads(response)
                return feedback
            except json.JSONDecodeError:
                return self._fallback_feedback_generation(errors)
                
        except Exception as e:
            print(f"      ⚠️ Error en generación de feedback: {e}")
            return self._fallback_feedback_generation(errors)
    
    def _generate_adaptive_response(self, user_input: str, comprehension: Dict[str, Any], 
                                   cognitive: Dict[str, Any], feedback: Dict[str, Any]) -> str:
        """💡 Generación de respuesta adaptativa inteligente"""
        try:
            response_prompt = f"""
Generate an intelligent, adaptive response as an AI language learning assistant.

User said: "{user_input}"
Comprehension analysis: {json.dumps(comprehension, indent=2)}
Cognitive assessment: {json.dumps(cognitive, indent=2)}
Generated feedback: {json.dumps(feedback, indent=2)}

Create a response that:
1. Addresses their message naturally
2. Incorporates appropriate feedback
3. Continues the conversation meaningfully
4. Matches their language level
5. Encourages continued learning
6. Is conversational, not robotic

Respond naturally and conversationally in the same language they used:
"""

            response = self.assistant.chat_service.generate_response(
                response_prompt,
                "Generate natural, adaptive conversation response."
            )
            
            return response.strip()
            
        except Exception as e:
            print(f"      ⚠️ Error en generación de respuesta: {e}")
            return "I understand what you're saying. That's a great point! Could you tell me more about your thoughts on this?"
    
    def _display_intelligent_response(self, analysis_result: Dict[str, Any]):
        """🖥️ Muestra la respuesta inteligente con análisis completo"""
        
        print(f"\n{'='*70}")
        
        # Respuesta principal de la IA
        ai_response = analysis_result['ai_response']
        print(f"🤖 IA: {ai_response}")
        
        # Mostrar feedback si es detallado
        if self.feedback_mode in ['detailed', 'adaptive']:
            feedback = analysis_result.get('feedback', {})
            
            if feedback.get('learning_wins'):
                print(f"\n🎉 Logros detectados:")
                for win in feedback['learning_wins'][:2]:
                    print(f"   ✅ {win}")
            
            if feedback.get('gentle_corrections'):
                print(f"\n✏️ Sugerencias amigables:")
                for correction in feedback['gentle_corrections'][:2]:
                    print(f"   📝 {correction.get('error', '')} → {correction.get('correction', '')}")
                    if correction.get('explanation'):
                        print(f"      💡 {correction['explanation']}")
            
            if feedback.get('next_challenges'):
                print(f"\n🎯 Próximos desafíos:")
                for challenge in feedback['next_challenges'][:2]:
                    print(f"   🚀 {challenge}")
        
        # Mostrar progreso si está habilitado
        if self.progress_tracking_enabled:
            progress = analysis_result.get('progress_evaluation', {})
            improvement = analysis_result.get('improvement_analysis', {})
            
            if progress.get('progress_indicators', {}).get('improvement_detected'):
                print(f"\n📈 ¡Mejora detectada!")
                areas = progress['progress_indicators'].get('areas_of_growth', [])
                if areas:
                    print(f"   🌱 Crecimiento en: {', '.join(areas[:2])}")
            
            # Mostrar nivel actual
            comprehension = analysis_result.get('comprehension', {})
            if comprehension.get('complexity_level'):
                level = comprehension['complexity_level']
                print(f"\n📊 Nivel actual: {level}")
        
        # Información de procesamiento (modo debug)
        phases = analysis_result.get('processing_phases', 0)
        print(f"\n⚡ Procesado en {phases} fases de análisis inteligente")
        
        print(f"{'='*70}")
    
    def _get_user_input(self) -> str:
        """⌨️ Obtiene entrada del usuario (solo texto, sin audio)"""
        print(f"\n💬 Tú:")
        return input("▶️  ").strip()
    
    def _handle_commands(self, text: str) -> bool:
        """🎛️ Maneja comandos especiales"""
        command = text.lower().strip()
        
        if command == "help":
            self._show_commands()
            return True
        elif command == "profile":
            self._show_detailed_learning_profile()
            return True
        elif command == "progress":
            self._show_progress_summary()
            return True
        elif command == "feedback detailed":
            self.feedback_mode = "detailed"
            print("🔍 Modo feedback detallado activado")
            return True
        elif command == "feedback minimal":
            self.feedback_mode = "minimal"
            print("⚡ Modo feedback mínimo activado")
            return True
        elif command == "feedback adaptive":
            self.feedback_mode = "adaptive"
            print("🎯 Modo feedback adaptativo activado")
            return True
        elif command == "reset":
            self._reset_session()
            return True
        elif command == "save":
            self._save_session()
            return True
        
        return False
    
    def _show_commands(self):
        """📋 Muestra comandos disponibles"""
        print(f"""
🎮 COMANDOS DEL CHAT INTELIGENTE:
   💬 Escribe normalmente para chatear
   
   🔧 COMANDOS ESPECIALES:
   • 'profile' - Ver perfil de aprendizaje detallado
   • 'progress' - Ver resumen de progreso  
   • 'feedback detailed' - Feedback muy detallado
   • 'feedback adaptive' - Feedback inteligente (default)
   • 'feedback minimal' - Feedback mínimo
   • 'reset' - Reiniciar sesión
   • 'save' - Guardar progreso
   • 'help' - Mostrar esta ayuda
   • 'quit' - Salir
        """)
    
    def _generate_personalized_welcome(self) -> str:
        """👋 Genera bienvenida personalizada BILINGÜE desde el inicio"""
        try:
            profile_data = self.learning_profile
            
            # 🎯 GENERAR BIENVENIDA EN INGLÉS
            english_welcome = self._generate_english_welcome(profile_data)
            
            # 🌐 CREAR VERSIÓN BILINGÜE COMPLETA
            bilingual_welcome = self._create_welcome_bilingual_format(english_welcome)
            
            return bilingual_welcome
            
        except Exception as e:
            logger.error(f"Error generating welcome: {e}")
            return self._get_default_bilingual_welcome()

    def _generate_english_welcome(self, profile_data: Dict[str, Any]) -> str:
        """🇺🇸 Genera bienvenida en inglés"""
        try:
            total_sessions = profile_data.get("user_stats", {}).get("total_sessions", 1)
            current_level = profile_data.get("learning_progress", {}).get("current_level", "A2")
            
            if total_sessions == 1:
                return "Hello! Welcome to our intelligent chat. I'm excited to help you practice English!"
            elif total_sessions < 5:
                return f"Hello again! Great to see you back for session #{total_sessions}. Ready to practice?"
            else:
                return f"Welcome back! You've completed {total_sessions} sessions. Let's continue your learning journey!"
                
        except Exception as e:
            return "Hello! Welcome to our intelligent English practice chat. Let's start learning together!"

    def _create_welcome_bilingual_format(self, english_welcome: str) -> str:
        """🌐 Crea formato bilingüe para la bienvenida"""
        
        # 🎯 TRADUCIR AL ESPAÑOL
        spanish_welcome = self._translate_welcome_to_spanish(english_welcome)
        
        # 📝 CREAR EXPLICACIÓN INICIAL
        explanation = self._create_welcome_explanation()
        
        # 🏗️ FORMATO BILINGÜE COMPLETO
        return f"""{english_welcome}

🌐 TRADUCCIÓN: {spanish_welcome}

💡 EXPLICACIÓN: {explanation}

📚 INSTRUCCIONES: 
   • Puedes escribir en inglés o español
   • Te responderé en inglés con traducción al español
   • Te ayudaré a entender todo lo que digo
   • ¡No tengas miedo de cometer errores!

🎯 ¿De qué te gustaría hablar hoy?"""

    def _translate_welcome_to_spanish(self, english_text: str) -> str:
        """🌐 Traduce mensajes de bienvenida específicos MEJORADO"""
    
        # Diccionario completo de traducciones de bienvenida
        welcome_translations = {
            # Frases completas de bienvenida
            "Hello again! Great to see you back for session #4. Ready to practice?": 
            "¡Hola de nuevo! Me alegra verte de vuelta para la sesión #4. ¿Listo para practicar?",
            
            "Hello again! Great to see you back": 
            "¡Hola de nuevo! Me alegra verte de vuelta",
            
            "Ready to practice?": 
            "¿Listo para practicar?",
            
            "for session": "para la sesión",
            "session #": "sesión #",
            
            # Traducciones palabra por palabra para casos no cubiertos
            "for": "para",
            "session": "sesión",
            "ready": "listo",
            "to": "para",
            "practice": "practicar",
            "great": "genial",
            "see": "ver",
            "you": "te",
            "back": "de vuelta",
            "hello": "hola",
            "again": "de nuevo"
        }
    
        # Traducir frase completa si existe
        for eng_phrase, spanish_phrase in welcome_translations.items():
            if eng_phrase.lower() in english_text.lower():
                english_text = english_text.replace(eng_phrase, spanish_phrase)
    
        # Si aún quedan partes en inglés, traducir palabra por palabra
        words = english_text.split()
        translated_words = []
    
        for word in words:
            clean_word = word.lower().strip('.,!?#')
            punctuation = word[len(clean_word):] if len(word) > len(clean_word) else ''
        
            if clean_word in welcome_translations:
                translated_words.append(welcome_translations[clean_word] + punctuation)
            else:
                translated_words.append(word)  # Mantener palabra original
    
        result = ' '.join(translated_words)
    
        # Limpiar y corregir resultado final
        result = result.replace("Me alegra verte de vuelta for session", "Me alegra verte de vuelta para la sesión")
        result = result.replace("Ready to practice?", "¿Listo para practicar?")
        result = result.replace("session #", "sesión #")
    
        return result

    def _create_welcome_explanation(self) -> str:
        """📝 Crea explicación de bienvenida en español"""
        return ("Te estoy dando la bienvenida a nuestro chat inteligente. "
                "Este sistema te ayudará a practicar inglés de manera gradual y comprensible. "
                "Siempre te traduciré lo que digo para que no te pierdas.")

    def _get_default_bilingual_welcome(self) -> str:
        """🚨 Bienvenida bilingüe de emergencia"""
        return """Hello! Welcome to our intelligent English practice chat!

🌐 TRADUCCIÓN: ¡Hola! ¡Bienvenido a nuestro chat inteligente para practicar inglés!

💡 EXPLICACIÓN: Te estoy dando la bienvenida y mostrándote que este es un lugar seguro para practicar inglés.

📚 INSTRUCCIONES:
   • Escribe en inglés o español - ¡ambos están bien!
   • Siempre te traduciré mis respuestas
   • Te explico todo para que entiendas
   • Los errores son parte del aprendizaje

🎯 What would you like to talk about today? (¿De qué te gustaría hablar hoy?)"""

    # === MÉTODOS DE FALLBACK ===
    
    def _fallback_comprehension_analysis(self, user_input: str) -> Dict[str, Any]:
        """Análisis de comprensión básico como fallback"""
        words = user_input.split()
        return {
            "language_detected": "en" if any(w in user_input.lower() for w in ['the', 'and', 'is']) else "es",
            "complexity_level": "B1" if len(words) > 10 else "A2",
            "intent_type": "conversation",
            "emotional_state": "neutral",
            "fluency_indicators": {"natural_flow": "fair", "word_choice": "adequate", "coherence": "clear"}
        }
    
    def _fallback_cognitive_analysis(self, comprehension: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis cognitivo básico como fallback"""
        return {
            "user_needs_assessment": "practice conversation",
            "learning_opportunities": ["vocabulary expansion", "grammar practice"],
            "appropriate_challenge_level": "just_right",
            "recommended_approach": "encouraging"
        }
    
    def _fallback_progress_evaluation(self) -> Dict[str, Any]:
        """Evaluación de progreso básica como fallback"""
        return {
            "current_performance": {"grammar_accuracy": "good", "vocabulary_usage": "adequate"},
            "progress_indicators": {"improvement_detected": True, "areas_of_growth": ["fluency"]},
            "learning_velocity": "steady"
        }
    
    def _fallback_error_analysis(self, user_input: str, grammar_correction: Optional[str]) -> Dict[str, Any]:
        """Análisis de errores básico como fallback"""
        has_errors = grammar_correction and grammar_correction != user_input
        return {
            "grammar_errors": [{"type": "general", "original": user_input, "corrected": grammar_correction}] if has_errors else [],
            "overall_assessment": {"error_density": "low" if not has_errors else "medium"},
            "basic_correction": grammar_correction
        }
    
    def _fallback_improvement_analysis(self) -> Dict[str, Any]:
        """Análisis de mejora básico como fallback"""
        return {
            "improvement_trends": {"grammar_accuracy": "stable", "vocabulary_complexity": "stable"},
            "areas_of_excellence": ["participation"],
            "areas_needing_focus": ["consistency"]
        }
    
    def _fallback_feedback_generation(self, errors: Dict[str, Any]) -> Dict[str, Any]:
        """Generación de feedback básica como fallback"""
        has_errors = bool(errors.get('grammar_errors'))
        return {
            "primary_feedback": "Great job participating in the conversation!",
            "learning_wins": ["active engagement"],
            "gentle_corrections": errors.get('grammar_errors', [])[:1],
            "motivation_boost": "Keep practicing - you're doing well!"
        }
    
    # === MÉTODOS DE UTILIDAD ===
    
    def _update_learning_analytics(self, analysis_result: Dict[str, Any]):
        """📊 Actualiza análisis de aprendizaje basado en resultados"""
        try:
            # Extraer datos del análisis
            user_input = analysis_result.get('user_input', '')
            comprehension = analysis_result.get('comprehension', {})
            progress_evaluation = analysis_result.get('progress_evaluation', {})
            error_analysis = analysis_result.get('error_analysis', {})
            improvement_analysis = analysis_result.get('improvement_analysis', {})
            
            # 📈 ACTUALIZAR PROGRESO DEL USUARIO
            
            # 1. Incrementar contador de mensajes
            self.user_progress.total_messages += 1
            self.user_progress.last_activity = datetime.now().isoformat()
            
            # 2. Actualizar nivel de vocabulario
            detected_level = comprehension.get('complexity_level', 'A2')
            if detected_level:
                self.user_progress.vocabulary_level = detected_level
            
            # 3. Contar errores gramaticales
            grammar_errors = len(error_analysis.get('grammar_errors', []))
            self.user_progress.grammar_errors += grammar_errors
            
            # 4. Actualizar score de fluidez
            fluency_indicators = comprehension.get('fluency_indicators', {})
            new_fluency_score = self._calculate_fluency_score(comprehension)
            if new_fluency_score > 0:
                # Promedio ponderado con score anterior
                current_score = self.user_progress.fluency_score
                self.user_progress.fluency_score = (current_score * 0.7 + new_fluency_score * 0.3)
            
            # 5. Actualizar temas discutidos
            topic = comprehension.get('topic_category')
            if topic and topic not in self.user_progress.topics_discussed:
                self.user_progress.topics_discussed.append(topic)
                # Limitar a últimos 10 temas
                if len(self.user_progress.topics_discussed) > 10:
                    self.user_progress.topics_discussed = self.user_progress.topics_discussed[-10:]
            
            # 6. Actualizar fortalezas detectadas
            current_performance = progress_evaluation.get('current_performance', {})
            for area, level in current_performance.items():
                if level in ['good', 'excellent', 'advanced']:
                    strength_description = f"{area}: {level}"
                    if strength_description not in self.user_progress.strengths:
                        self.user_progress.strengths.append(strength_description)
                        # Limitar a últimas 5 fortalezas
                        if len(self.user_progress.strengths) > 5:
                            self.user_progress.strengths = self.user_progress.strengths[-5:]
            
            # 7. Actualizar áreas de mejora
            areas_needing_work = progress_evaluation.get('progress_indicators', {}).get('areas_needing_work', [])
            for area in areas_needing_work:
                if area not in self.user_progress.improvement_areas:
                    self.user_progress.improvement_areas.append(area)
                    # Limitar a últimas 5 áreas
                    if len(self.user_progress.improvement_areas) > 5:
                        self.user_progress.improvement_areas = self.user_progress.improvement_areas[-5:]
            
            # 📊 ACTUALIZAR PERFIL DE APRENDIZAJE GLOBAL
            
            # 8. Actualizar estadísticas globales
            self.learning_profile['total_messages'] = self.learning_profile.get('total_messages', 0) + 1
            self.learning_profile['average_level'] = self.user_progress.vocabulary_level
            self.learning_profile['last_session'] = datetime.now().isoformat()
            
            # 9. Actualizar áreas fuertes en perfil global
            if self.user_progress.strengths:
                profile_strengths = self.learning_profile.get('strong_areas', [])
                for strength in self.user_progress.strengths:
                    area_name = strength.split(':')[0]  # Extraer solo el nombre del área
                    if area_name not in profile_strengths:
                        profile_strengths.append(area_name)
                self.learning_profile['strong_areas'] = profile_strengths[-5:]  # Últimas 5
            
            # 10. Actualizar áreas de mejora en perfil global
            if self.user_progress.improvement_areas:
                self.learning_profile['improvement_areas'] = self.user_progress.improvement_areas.copy()
            
            # 11. Actualizar temas preferidos
            if self.user_progress.topics_discussed:
                self.learning_profile['preferred_topics'] = self.user_progress.topics_discussed.copy()
            
            # 📝 GUARDAR DATOS ACTUALIZADOS
            self._save_progress_data()
            
            # 📊 LOG DE ACTUALIZACIÓN
            logger.info(f"Learning analytics updated: "
                       f"Messages: {self.user_progress.total_messages}, "
                       f"Level: {self.user_progress.vocabulary_level}, "
                       f"Fluency: {self.user_progress.fluency_score:.2f}")
        
        except Exception as e:
            logger.error(f"Error updating learning analytics: {e}")
            print(f"   ⚠️ Error actualizando análisis: {e}")
    
    def _calculate_fluency_score(self, comprehension: Dict[str, Any]) -> float:
        """📊 Calcula score de fluidez basado en análisis de comprensión"""
        try:
            indicators = comprehension.get('fluency_indicators', {})
            
            # Mapear valores textuales a números
            score_mapping = {
                'poor': 0.2, 'low': 0.2,
                'fair': 0.4, 'basic': 0.4,
                'good': 0.7, 'medium': 0.6,
                'excellent': 1.0, 'high': 0.9, 'advanced': 1.0,
                'limited': 0.3, 'adequate': 0.5, 'varied': 0.8, 'sophisticated': 1.0,
                'unclear': 0.2, 'clear': 0.7, 'very_clear': 1.0
            }
            
            # Obtener scores individuales
            flow_score = score_mapping.get(indicators.get('natural_flow', 'fair'), 0.5)
            choice_score = score_mapping.get(indicators.get('word_choice', 'adequate'), 0.5)
            coherence_score = score_mapping.get(indicators.get('coherence', 'clear'), 0.7)
            
            # Calcular promedio ponderado
            fluency_score = (flow_score * 0.4 + choice_score * 0.3 + coherence_score * 0.3)
            
            return round(fluency_score, 3)
            
        except Exception as e:
            logger.warning(f"Error calculating fluency score: {e}")
            return 0.5  # Score neutral por defecto

    def _save_progress_data(self):
        """💾 Guarda datos de progreso de manera segura"""
        try:
            import os
            
            # Crear directorios si no existen
            os.makedirs("data/learning_profiles", exist_ok=True)
            os.makedirs("data/sessions", exist_ok=True)
            
            # Guardar perfil de aprendizaje actualizado
            profile_path = "data/learning_profiles/user_profile.json"
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(self.learning_profile, f, indent=2, ensure_ascii=False)
            
            # Guardar datos de la sesión actual
            session_path = f"data/sessions/{self.session_id}.json"
            session_data = {
                'session_id': self.session_id,
                'progress': asdict(self.user_progress),
                'conversation_history': self.conversation_history[-20:],  # Solo últimos 20 mensajes
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_messages': self.user_progress.total_messages,
                    'current_level': self.user_progress.vocabulary_level,
                    'fluency_score': self.user_progress.fluency_score,
                    'topics_count': len(self.user_progress.topics_discussed),
                    'error_count': self.user_progress.grammar_errors
                }
            }
            
            with open(session_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Progress data saved to {session_path}")
            
        except Exception as e:
            logger.error(f"Error saving progress data: {e}")
            print(f"   ⚠️ Error guardando progreso: {e}")

    def _show_learning_profile(self):
        """Muestra perfil de aprendizaje"""
        profile = self.learning_profile
        print(f"\n📊 TU PERFIL DE APRENDIZAJE:")
        print(f"   📈 Sesiones completadas: {profile.get('total_sessions', 0)}")
        print(f"   💬 Mensajes totales: {profile.get('total_messages', 0)}")
        print(f"   🎯 Nivel promedio: {profile.get('average_level', 'A2')}")
        
        if profile.get('strong_areas'):
            print(f"   💪 Fortalezas: {', '.join(profile['strong_areas'][:3])}")
        
        if profile.get('improvement_areas'):
            print(f"   🎯 Trabajando en: {', '.join(profile['improvement_areas'][:3])}")
    
    def _show_detailed_learning_profile(self):
        """Muestra perfil detallado"""
        print(f"\n📊 PERFIL DE APRENDIZAJE DETALLADO:")
        print(f"{'='*50}")
        
        profile = self.learning_profile
        progress = self.user_progress
        
        print(f"📈 PROGRESO GENERAL:")
        print(f"   • Sesiones: {profile.get('total_sessions', 0)}")
        print(f"   • Mensajes totales: {profile.get('total_messages', 0)}")
        print(f"   • Nivel actual: {progress.vocabulary_level}")
        print(f"   • Score de fluidez: {progress.fluency_score:.2f}")
        
        print(f"\n🎯 SESIÓN ACTUAL:")
        print(f"   • Mensajes en esta sesión: {progress.total_messages}")
        print(f"   • Errores gramaticales: {progress.grammar_errors}")
        print(f"   • Temas discutidos: {len(progress.topics_discussed)}")
        
        if progress.topics_discussed:
            print(f"   • Temas: {', '.join(progress.topics_discussed)}")
        
        if progress.strengths:
            print(f"\n💪 FORTALEZAS:")
            for strength in progress.strengths:
                print(f"   ✅ {strength}")
        
        if progress.improvement_areas:
            print(f"\n🎯 ÁREAS DE MEJORA:")
            for area in progress.improvement_areas:
                print(f"   📈 {area}")
    
    def _show_progress_summary(self):
        """Muestra resumen de progreso"""
        print(f"\n📈 RESUMEN DE PROGRESO:")
        print(f"{'='*40}")
        
        if len(self.conversation_history) > 0:
            recent_fluency = [msg.get('fluency_score', 0) for msg in self.conversation_history[-5:]]
            avg_fluency = sum(recent_fluency) / len(recent_fluency) if recent_fluency else 0
            
            recent_errors = [msg.get('error_count', 0) for msg in self.conversation_history[-5:]]
            avg_errors = sum(recent_errors) / len(recent_errors) if recent_errors else 0
            
            print(f"📊 Fluidez promedio (últimos 5): {avg_fluency:.2f}")
            print(f"❌ Errores promedio (últimos 5): {avg_errors:.1f}")
            
            # Tendencia
            if len(self.conversation_history) >= 5:
                older_fluency = [msg.get('fluency_score', 0) for msg in self.conversation_history[-10:-5]]
                if older_fluency:
                    old_avg = sum(older_fluency) / len(older_fluency)
                    if avg_fluency > old_avg + 0.1:
                        print("📈 ¡Tendencia: MEJORANDO!")
                    elif avg_fluency < old_avg - 0.1:
                        print("📉 Tendencia: Necesita más práctica")
                    else:
                        print("📊 Tendencia: ESTABLE")
        else:
            print("📊 Necesitamos más datos para mostrar progreso")
    
    def _reset_session(self):
        """Reinicia la sesión"""
        self.conversation_history = []
        self.user_progress = UserProgress(session_id=f"smart_chat_{int(time.time())}")
        print("🔄 Sesión reiniciada")
    
    def _save_session(self):
        """Guarda la sesión actual"""
        self._save_progress_data()
        print("💾 Sesión guardada exitosamente")
    
    def _is_exit_command(self, text: str) -> bool:
        """Verifica comandos de salida"""
        exit_commands = ["quit", "exit", "salir", "bye", "goodbye", "terminar"]
        return text.lower().strip() in exit_commands
    
    def _show_session_summary(self):
        """Muestra resumen de la sesión"""
        print(f"\n{'='*70}")
        print("🧠 RESUMEN DE SESIÓN - CHAT INTELIGENTE")
        print(f"{'='*70}")
        
        progress = self.user_progress
        
        print(f"📊 ESTADÍSTICAS DE SESIÓN:")
        print(f"   💬 Mensajes intercambiados: {progress.total_messages}")
        print(f"   ❌ Errores detectados: {progress.grammar_errors}")
        print(f"   📚 Nivel alcanzado: {progress.vocabulary_level}")
        print(f"   🎯 Temas explorados: {len(progress.topics_discussed)}")
        
        if progress.topics_discussed:
            print(f"   📝 Temas: {', '.join(progress.topics_discussed)}")
        
        # Cálculo de duración
        if progress.session_start:
            start = datetime.fromisoformat(progress.session_start)
            duration = datetime.now() - start
            minutes = int(duration.total_seconds() / 60)
            print(f"   ⏱️ Duración: {minutes} minutos")
        
        print(f"\n🎯 ANÁLISIS FINAL:")
        if progress.total_messages >= 5:
            error_rate = (progress.grammar_errors / progress.total_messages) * 100
            print(f"   📈 Tasa de precisión: {100 - error_rate:.1f}%")
            
            if error_rate < 20:
                print("   🌟 ¡Excelente precisión!")
            elif error_rate < 40:
                print("   ✅ Buena precisión, sigue practicando")
            else:
                print("   💪 Hay espacio para mejorar, ¡no te rindas!")
        
        print(f"\n🎉 ¡Gracias por usar el Chat Inteligente!")
        print(f"💡 Tip: Tus datos se guardan automáticamente para seguir tu progreso")
        
        # Guardar datos finales
        self._save_progress_data()
    
    def _analyze_conversation_context(self, user_input: str) -> Dict[str, Any]:
        """🔍 Analiza el contexto conversacional con IA"""
        try:
            conversation_history = self._get_recent_conversation_history()
            full_prompt = f"""You are a conversation context analyzer. Analyze the user's message and respond in JSON format:
{{
    "intent": "ask_question|share_info|seek_help|casual_chat",
    "emotion": "happy|sad|confused|excited|neutral|frustrated",
    "topic": "identified_topic",
    "language_level": "beginner|intermediate|advanced",
    "response_type": "informative|supportive|corrective|conversational",
    "user_needs": "what_the_user_seems_to_need"
}}

Recent conversation: {conversation_history}
Current user message: "{user_input}"

Analysis:"""

            # 🔧 USAR MÉTODO COMPATIBLE
            response = self.assistant.chat_service.generate_response(full_prompt)
            
            try:
                analysis = json.loads(response)
                return analysis
            except json.JSONDecodeError:
                return {
                    "intent": "casual_chat",
                    "emotion": "neutral",
                    "topic": "general",
                    "language_level": "intermediate",
                    "response_type": "conversational",
                    "user_needs": "engage in conversation"
                }
                
        except Exception as e:
            print(f"   ⚠️ Error en análisis de contexto: {e}")
            return {
                "intent": "casual_chat",
                "emotion": "neutral", 
                "topic": "general",
                "language_level": "intermediate",
                "response_type": "conversational",
                "user_needs": "engage in conversation"
            }

    def _think_about_response(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """🤔 Sistema de pensamiento estratégico para respuestas"""
        try:
            full_prompt = f"""Think strategically about the best response approach. Respond in JSON:
{{
    "strategy": "brief_description_of_approach",
    "tone": "friendly|professional|encouraging",
    "should_correct_grammar": true/false,
    "follow_up_questions": ["question1", "question2"],
    "key_points_to_address": ["point1", "point2"],
    "conversation_direction": "where_to_steer_the_conversation"
}}

User said: "{user_input}"
Context: {json.dumps(context, indent=2)}

Strategic analysis:"""

            # 🔧 USAR MÉTODO COMPATIBLE
            thinking_response = self.assistant.chat_service.generate_response(full_prompt)
            
            try:
                thinking_result = json.loads(thinking_response)
                return thinking_result
            except json.JSONDecodeError:
                return {
                    "strategy": "Respond naturally and helpfully",
                    "tone": "friendly",
                    "should_correct_grammar": False,
                    "follow_up_questions": [],
                    "key_points_to_address": [],
                    "conversation_direction": "continue current topic"
                }
                
        except Exception as e:
            print(f"   ⚠️ Error en pensamiento estratégico: {e}")
            return {
                "strategy": "Respond naturally",
                "tone": "friendly",
                "should_correct_grammar": False,
                "follow_up_questions": [],
                "key_points_to_address": [],
                "conversation_direction": "continue naturalmente"
            }

    def _generate_intelligent_response(self, user_input: str, context: Dict[str, Any], thinking: Optional[Dict[str, Any]]) -> str:
        """💡 Genera respuesta bilingüe inteligente para aprendices"""
        try:
            # 🧠 DETECTAR IDIOMA DEL USUARIO
            user_language = self._detect_user_language(user_input)
            user_level = context.get('language_level', 'intermediate')
            
            # 🎯 GENERAR RESPUESTA EN INGLÉS PRIMERO
            english_response = self._generate_english_response(user_input, context, thinking)
            
            # 🌐 CREAR RESPUESTA BILINGÜE COMPLETA
            bilingual_response = self._create_bilingual_response(
                english_response, user_input, user_language, user_level
            )
            
            return bilingual_response
            
        except Exception as e:
            print(f"   ⚠️ Error generando respuesta: {e}")
            return self._get_emergency_bilingual_response(user_input)

    def _detect_user_language(self, user_input: str) -> str:
        """🔍 Detecta el idioma principal del usuario"""
        spanish_indicators = [
            'que', 'como', 'donde', 'cuando', 'porque', 'para', 'con', 'sin', 'muy', 'pero',
            'también', 'siempre', 'nunca', 'hacer', 'estar', 'ser', 'tener', 'decir',
            'hola', 'gracias', 'por favor', 'lo siento', 'no entiendo'
        ]
        
        english_indicators = [
            'the', 'and', 'that', 'have', 'for', 'not', 'with', 'you', 'this', 'but',
            'his', 'from', 'they', 'she', 'her', 'been', 'than', 'its', 'who', 'did'
        ]
        
        words = user_input.lower().split()
        spanish_count = sum(1 for word in words if word in spanish_indicators)
        english_count = sum(1 for word in words if word in english_indicators)
        
        if spanish_count > english_count:
            return 'spanish'
        elif english_count > spanish_count:
            return 'english'
        else:
            return 'mixed'

    def _generate_english_response(self, user_input: str, context: Dict[str, Any], thinking: Optional[Dict[str, Any]]) -> str:
        """🇺🇸 Genera respuesta en inglés usando ChatService MEJORADO"""
        try:
            # Detectar tema específico para respuesta más relevante
            user_lower = user_input.lower()
            
            if 'futbol' in user_lower or 'fútbol' in user_lower or 'football' in user_lower:
                # Respuesta específica para fútbol
                football_prompt = f"""You are an English teacher. A student wants to talk about football/soccer.

Student said: "{user_input}"
Their level: {context.get('language_level', 'intermediate')}

Respond enthusiastically about football in English (1-2 sentences):"""
                
            elif 'food' in user_lower or 'comida' in user_lower:
                # Respuesta específica para comida
                football_prompt = f"""You are an English teacher. A student wants to talk about food.

Student said: "{user_input}"
Their level: {context.get('language_level', 'intermediate')}

Respond enthusiastically about food in English (1-2 sentences):"""
                
            else:
                # Prompt general
                football_prompt = f"""You are an English teacher having a friendly conversation. 

Student said: "{user_input}"
Their level: {context.get('language_level', 'intermediate')}
Their emotion: {context.get('emotion', 'neutral')}

Respond naturally in English (1-2 sentences max):"""

            response = self.assistant.chat_service.generate_response(football_prompt)
            
            # Limpiar y validar respuesta
            if response and len(response.strip()) > 5:
                return response.strip()
            else:
                return self._get_fallback_english_response(user_input, context)
            
        except Exception as e:
            print(f"   ⚠️ Error en respuesta inglés: {e}")
            return self._get_fallback_english_response(user_input, context)

    def _get_fallback_english_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """🛡️ Respuesta de emergencia en inglés"""
        emotion = context.get('emotion', 'neutral')
        
        if emotion == 'confused':
            return "I understand that can be confusing. Let me help you with that."
        elif emotion == 'excited':
            return "That sounds really exciting! Tell me more about it."
        elif emotion == 'frustrated':
            return "I can see this is challenging. Don't worry, we'll work through it together."
        elif '?' in user_input:
            return "That's a great question! I'd like to help you understand that better."
        else:
            return "That's interesting! I'd love to hear more about your thoughts on this."

    def _translate_to_spanish(self, english_text: str) -> str:
        """🌐 Traduce texto al español usando múltiples métodos CORREGIDO"""
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
                    print(f"   ⚠️ Error en servicio de traducción: {e}")
        
            # Método 2: Traducción manual mejorada
            return self._improved_manual_translation(english_text)
        
        except Exception as e:
            print(f"   ⚠️ Error traduciendo: {e}")
            return self._improved_manual_translation(english_text)

    def _improved_manual_translation(self, english_text: str) -> str:
        """📚 Traducción manual MEJORADA sin mezclar idiomas"""
        
        # Limpiar texto de entrada - eliminar repeticiones
        cleaned_text = self._clean_repeated_text(english_text)
        
        # Diccionario de traducciones completas (frases completas)
        complete_translations = {
            # Respuestas comunes completas
            "That's interesting!": "¡Eso es interesante!",
            "Can you tell me more about that?": "¿Puedes contarme más sobre eso?",
            "That's a good point.": "Ese es un buen punto.",
            "I understand what you mean.": "Entiendo lo que quieres decir.",
            "Tell me more about that.": "Cuéntame más sobre eso.",
            "What do you think about that?": "¿Qué piensas sobre eso?",
            "That sounds interesting.": "Eso suena interesante.",
            "I see what you mean.": "Veo lo que quieres decir.",
            "Food is such an interesting topic!": "¡La comida es un tema tan interesante!",
            "What kind of food do you enjoy most?": "¿Qué tipo de comida disfrutas más?",
            "I'd love to hear more about that.": "Me encantaría escuchar más sobre eso.",
            "That's fascinating!": "¡Eso es fascinante!",
            "How do you feel about that?": "¿Cómo te sientes al respecto?",
            "What's your favorite type of cuisine?": "¿Cuál es tu tipo de cocina favorita?",
            
            # Frases sobre comida específicas
            "Food is a wonderful topic to discuss.": "La comida es un tema maravilloso para discutir.",
            "Do you like to cook?": "¿Te gusta cocinar?",
            "What's your favorite dish?": "¿Cuál es tu plato favorito?",
            "That sounds delicious!": "¡Eso suena delicioso!",
        }
        
        # Buscar traducción completa exacta
        if cleaned_text in complete_translations:
            return complete_translations[cleaned_text]
        
        # Buscar traducciones parciales para frases largas
        for english_phrase, spanish_phrase in complete_translations.items():
            if english_phrase in cleaned_text:
                return cleaned_text.replace(english_phrase, spanish_phrase)
        
        # Traducción palabra por palabra solo si no se encuentra frase completa
        return self._word_by_word_translation(cleaned_text)

    def _clean_repeated_text(self, text: str) -> str:
        """🧹 Limpia texto repetido y malformado"""
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
        """🔤 Traducción palabra por palabra mejorada"""
        
        # Diccionario de palabras individuales
        word_translations = {
            # Palabras comunes
            "that's": "eso es",
            "that": "eso",
            "is": "es",
            "very": "muy",
            "really": "realmente",
            "interesting": "interesante",
            "good": "bueno",
            "great": "genial",
            "wonderful": "maravilloso",
            "about": "sobre",
            "more": "más",
            "tell": "contar",
            "me": "me",
            "you": "tú",
            "can": "puedes",
            "what": "qué",
            "how": "cómo",
            "when": "cuándo",
            "where": "dónde",
            "why": "por qué",
            "food": "comida",
            "eat": "comer",
            "like": "gustar",
            "love": "encantar",
            "think": "pensar",
            "feel": "sentir",
            "want": "querer",
            "need": "necesitar",
            "enjoy": "disfrutar",
            "favorite": "favorito",
            "best": "mejor",
            "delicious": "delicioso",
            "tasty": "sabroso"
        }
        
        # Separar en palabras y traducir
        words = english_text.lower().split()
        translated_words = []
        
        for word in words:
            # Limpiar puntuación
            clean_word = word.strip('.,!?')
            punctuation = word[len(clean_word):] if len(word) > len(clean_word) else ''
            
            # Traducir palabra
            if clean_word in word_translations:
                translated_words.append(word_translations[clean_word] + punctuation)
            else:
                # Mantener palabra original si no hay traducción
                translated_words.append(word)
    
        return ' '.join(translated_words).capitalize()

    def _create_bilingual_response(self, english_response: str, user_input: str, user_language: str, user_level: str) -> str:
        """🌐 Crea respuesta bilingüe completa con explicaciones MEJORADA"""
        
        # 🧹 LIMPIAR RESPUESTA EN INGLÉS
        clean_english = self._clean_repeated_text(english_response)
        
        # 🎯 TRADUCIR RESPUESTA AL ESPAÑOL
        spanish_translation = self._translate_to_spanish(clean_english)
        
        # 📝 CREAR EXPLICACIÓN CONTEXTUAL
        explanation = self._create_contextual_explanation(clean_english, user_input, user_level)
        
        # 🏗️ CONSTRUIR RESPUESTA BILINGÜE SEGÚN NIVEL
        if user_level in ['beginner', 'A1', 'A2']:
            # Principiantes: Máxima explicación
            return f"""{clean_english}

🌐 TRADUCCIÓN: {spanish_translation}

💡 EXPLICACIÓN: {explanation}

📚 TIP: Intenta responder en inglés, pero si no puedes, está bien responder en español. ¡Estás aprendiendo!"""

        elif user_level in ['intermediate', 'B1', 'B2']:
            # Intermedio: Equilibrado
            return f"""{clean_english}

🌐 En español: {spanish_translation}

💡 {explanation}"""

        else:  # advanced, C1, C2
            # Avanzado: Menos traducción
            return f"""{clean_english}

🌐 (Traducción: {spanish_translation})"""

    def _get_emergency_bilingual_response(self, user_input: str) -> str:
        """🚨 Respuesta de emergencia bilingüe"""
        return f"""🤖 IA: I understand what you're saying. That's interesting!

🌐 TRADUCCIÓN: Entiendo lo que me dices. ¡Eso es interesante!

💡 EXPLICACIÓN: Te estoy mostrando que entiendo tu mensaje y que me parece interesante el tema.

📚 TIP: Puedes responder en inglés o español. ¡Ambos están bien para practicar!"""

    def _load_or_create_learning_profile(self) -> Dict[str, Any]:
        """📚 Carga o crea el perfil de aprendizaje del usuario"""
        try:
            import os
            
            # Crear directorio si no existe
            profile_dir = "data/learning_profiles"
            os.makedirs(profile_dir, exist_ok=True)
            
            profile_path = os.path.join(profile_dir, "user_profile.json")
            
            # Intentar cargar perfil existente
            if os.path.exists(profile_path):
                try:
                    with open(profile_path, 'r', encoding='utf-8') as f:
                        profile = json.load(f)
                        
                    # Validar que el perfil tiene la estructura correcta
                    if self._validate_profile_structure(profile):
                        print("📚 Perfil de aprendizaje cargado exitosamente")
                        return profile
                    else:
                        print("⚠️ Perfil corrupto, creando uno nuevo...")
                        
                except (json.JSONDecodeError, IOError) as e:
                    print(f"⚠️ Error leyendo perfil: {e}, creando uno nuevo...")
            
            # Crear perfil nuevo si no existe o está corrupto
            new_profile = self._create_default_profile()
            
            # Guardar el nuevo perfil
            try:
                with open(profile_path, 'w', encoding='utf-8') as f:
                    json.dump(new_profile, f, indent=2, ensure_ascii=False)
                print("✨ Nuevo perfil de aprendizaje creado")
            except IOError as e:
                print(f"⚠️ Error guardando perfil: {e}")
            
            return new_profile
            
        except Exception as e:
            print(f"❌ Error en perfil de aprendizaje: {e}")
            return self._create_default_profile()

    def _create_default_profile(self) -> Dict[str, Any]:
        """🆕 Crea un perfil de aprendizaje por defecto"""
        return {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "user_stats": {
                "total_sessions": 0,
                "total_messages": 0,
                "total_practice_time": 0,  # en minutos
                "streak_days": 0
            },
            "learning_progress": {
                "current_level": "A2",
                "average_level": "A2", 
                "fluency_score": 0.5,
                "grammar_accuracy": 0.6,
                "vocabulary_strength": 0.5
            },
            "skill_areas": {
                "strong_areas": ["enthusiasm", "participation"],
                "improvement_areas": ["grammar", "vocabulary", "fluency"],
                "focus_areas": ["basic_conversation", "common_phrases"]
            },
            "learning_preferences": {
                "preferred_topics": ["general_conversation", "daily_life"],
                "learning_style": "interactive",
                "difficulty_preference": "gradual",
                "feedback_style": "encouraging"
            },
            "conversation_history": {
                "favorite_topics": [],
                "challenging_topics": [],
                "recent_topics": []
            },
            "goals": {
                "short_term": ["improve daily conversation", "reduce grammar errors"],
                "long_term": ["achieve fluency", "confident communication"],
                "current_focus": "basic communication skills"
            },
            "achievements": {
                "milestones_reached": [],
                "consecutive_days": 0,
                "best_fluency_score": 0.5,
                "topics_mastered": []
            }
        }

    def _validate_profile_structure(self, profile: Dict[str, Any]) -> bool:
        """✅ Valida que el perfil tenga la estructura correcta"""
        try:
            required_keys = [
                "version", "created", "user_stats", "learning_progress", 
                "skill_areas", "learning_preferences"
            ]
            
            # Verificar claves principales
            for key in required_keys:
                if key not in profile:
                    return False
            
            # Verificar estructura de user_stats
            stats_keys = ["total_sessions", "total_messages"]
            for key in stats_keys:
                if key not in profile["user_stats"]:
                    return False
            
            # Verificar estructura de learning_progress
            progress_keys = ["current_level", "fluency_score"]
            for key in progress_keys:
                if key not in profile["learning_progress"]:
                    return False
            
            return True
            
        except Exception:
            return False

    def _update_profile_on_session_start(self):
        """🚀 Actualiza el perfil al iniciar sesión"""
        try:
            # Incrementar sesiones
            self.learning_profile["user_stats"]["total_sessions"] += 1
            
            # Actualizar última sesión
            self.learning_profile["last_updated"] = datetime.now().isoformat()
            
            # Calcular racha de días (simplificado)
            last_session = self.learning_profile.get("last_session_date")
            today = datetime.now().date().isoformat()
            
            if last_session == today:
                # Misma fecha, no incrementar racha
                pass
            elif last_session:
                # Verificar si es día consecutivo (lógica simplificada)
                self.learning_profile["user_stats"]["streak_days"] += 1
            else:
                # Primera sesión
                self.learning_profile["user_stats"]["streak_days"] = 1
            
            self.learning_profile["last_session_date"] = today
            
            # Guardar cambios
            self._save_profile_updates()
            
        except Exception as e:
            print(f"⚠️ Error actualizando perfil en inicio: {e}")

    def _save_profile_updates(self):
        """💾 Guarda actualizaciones del perfil"""
        try:
            import os
            
            profile_dir = "data/learning_profiles"
            os.makedirs(profile_dir, exist_ok=True)
            profile_path = os.path.join(profile_dir, "user_profile.json")
            
            # Actualizar timestamp
            self.learning_profile["last_updated"] = datetime.now().isoformat()
            
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(self.learning_profile, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving profile updates: {e}")

    def _show_welcome_message_with_profile(self):
        """👋 Muestra mensaje de bienvenida personalizado"""
        try:
            stats = self.learning_profile.get("user_stats", {})
            progress = self.learning_profile.get("learning_progress", {})
            
            total_sessions = stats.get("total_sessions", 0)
            current_level = progress.get("current_level", "A2")
            streak = stats.get("streak_days", 0)
            
            if total_sessions == 1:
                welcome_msg = f"🎉 ¡Bienvenido al Chat Inteligente! Esta es tu primera sesión."
            elif total_sessions < 5:
                welcome_msg = f"👋 ¡Hola de nuevo! Esta es tu sesión #{total_sessions}."
            else:
                welcome_msg = f"🌟 ¡Excelente! Ya tienes {total_sessions} sesiones de práctica."
            
            print(f"\n{welcome_msg}")
            print(f"📊 Nivel actual: {current_level}")
            
            if streak > 1:
                print(f"🔥 Racha de práctica: {streak} días")
            
            # Mostrar objetivo del día
            focus = self.learning_profile.get("goals", {}).get("current_focus", "comunicación básica")
            print(f"🎯 Enfoque de hoy: {focus}")
            
        except Exception as e:
            print("👋 ¡Bienvenido al Chat Inteligente!")
            logger.error(f"Error in welcome message: {e}")
    
    def _get_recent_conversation_history(self) -> str:
        """📝 Obtiene historial reciente de conversación"""
        try:
            if not self.conversation_history:
                return "No previous conversation in this session."
            
            # Obtener últimos 5 mensajes
            recent = self.conversation_history[-5:]
            
            history_text = "Recent conversation:\n"
            for msg in recent:
                timestamp = msg.get('timestamp', 'Unknown time')
                user_input = msg.get('user_input', 'No input')
                history_text += f"- User: {user_input}\n"
            
            return history_text
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return "Error retrieving conversation history."

    def _get_recent_performance_data(self) -> Dict[str, Any]:
        """📊 Obtiene datos de rendimiento reciente"""
        try:
            if len(self.conversation_history) < 3:
                return {
                    "status": "insufficient_data",
                    "message": "Need more conversation data",
                    "recent_messages": len(self.conversation_history)
                }
            
            # Analizar últimos 5 mensajes
            recent_messages = self.conversation_history[-5:]
            
            # Calcular métricas
            total_errors = sum(msg.get('error_count', 0) for msg in recent_messages)
            avg_fluency = sum(msg.get('fluency_score', 0.5) for msg in recent_messages) / len(recent_messages)
            
            levels_detected = [msg.get('comprehension_level') for msg in recent_messages if msg.get('comprehension_level')]
            most_common_level = max(set(levels_detected), key=levels_detected.count) if levels_detected else 'A2'
            
            topics = [msg.get('topic') for msg in recent_messages if msg.get('topic')]
            unique_topics = list(set(topics))
            
            return {
                "recent_messages_count": len(recent_messages),
                "average_error_rate": total_errors / len(recent_messages) if recent_messages else 0,
                "average_fluency_score": avg_fluency,
                "most_common_level": most_common_level,
                "topics_covered": unique_topics,
                "improvement_trend": "stable",  # Simplificado
                "consistency_level": "developing" if avg_fluency > 0.5 else "needs_work"
            }
            
        except Exception as e:
            logger.error(f"Error getting performance data: {e}")
            return {
                "status": "error",
                "message": str(e),
                "recent_messages": 0
            }

    def _get_target_language_for_response(self, user_input: str) -> str:
        """🎯 Determina idioma objetivo para la respuesta"""
        # Detectar idioma del usuario
        spanish_words = ['que', 'como', 'es', 'para', 'con', 'muy', 'pero', 'también']
        english_words = ['the', 'and', 'is', 'for', 'with', 'very', 'but', 'also']
        
        input_lower = user_input.lower()
        spanish_count = sum(1 for word in spanish_words if word in input_lower)
        english_count = sum(1 for word in english_words if word in input_lower)
        
        if spanish_count > english_count:
            return "Spanish with English practice"
        else:
            return "English with Spanish support"

    def _display_intelligent_bilingual_response(self, analysis_result: Dict[str, Any]):
        """🖥️ Muestra respuesta inteligente SIEMPRE en formato bilingüe"""
        
        print(f"\n{'='*70}")
        
        # 🌐 LA RESPUESTA YA DEBERÍA SER BILINGÜE
        ai_response = analysis_result['ai_response']
        
        # Si por algún motivo no es bilingüe, convertirla
        if "🌐 TRADUCCIÓN:" not in ai_response and "🌐 En español:" not in ai_response:
            # Convertir respuesta simple a formato bilingüe
            user_input = analysis_result.get('user_input', '')
            context = analysis_result.get('comprehension', {})
            
            bilingual_version = self._create_bilingual_response(
                ai_response, user_input, 'mixed', 'intermediate'
            )
            ai_response = bilingual_version
        
        print(f"🤖 IA: {ai_response}")
        
        # Mostrar feedback adicional si está habilitado
        if self.feedback_mode in ['detailed', 'adaptive']:
            feedback = analysis_result.get('feedback', {})
            
            if feedback.get('learning_wins'):
                print(f"\n🎉 Logros detectados:")
                for win in feedback['learning_wins'][:2]:
                    print(f"   ✅ {win}")
            
            if feedback.get('gentle_corrections'):
                print(f"\n✏️ Sugerencias amigables:")
                for correction in feedback['gentle_corrections'][:2]:
                    print(f"   📝 {correction.get('error', '')} → {correction.get('correction', '')}")
                    if correction.get('explanation'):
                        print(f"      💡 {correction['explanation']}")
            
            if feedback.get('next_challenges'):
                print(f"\n🎯 Próximos desafíos:")
                for challenge in feedback['next_challenges'][:2]:
                    print(f"   🚀 {challenge}")
        
        # Mostrar progreso si está habilitado
        if self.progress_tracking_enabled:
            progress = analysis_result.get('progress_evaluation', {})
            
            if progress.get('progress_indicators', {}).get('improvement_detected'):
                print(f"\n📈 ¡Mejora detectada!")
                areas = progress['progress_indicators'].get('areas_of_growth', [])
                if areas:
                    print(f"   🌱 Crecimiento en: {', '.join(areas[:2])}")
            
            # Mostrar nivel actual
            comprehension = analysis_result.get('comprehension', {})
            if comprehension.get('complexity_level'):
                level = comprehension['complexity_level']
                print(f"\n📊 Nivel actual: {level}")
    
        # Información de procesamiento
        phases = analysis_result.get('processing_phases', 0)
        print(f"\n⚡ Procesado en {phases} fases de análisis inteligente")
        
        print(f"{'='*70}")
    
    def _create_contextual_explanation(self, english_response: str, user_input: str, user_level: str) -> str:
        """📝 Crea explicación contextual en español"""
    
        # Detectar tipo de respuesta para explicación apropiada
        english_lower = english_response.lower()
        user_lower = user_input.lower()
        
        # Explicaciones específicas por contexto
        if 'football' in user_lower or 'futbol' in user_lower or 'fútbol' in user_lower:
            if '?' in english_response:
                return "Te estoy haciendo una pregunta sobre fútbol para conocer más sobre tus gustos deportivos y practicar vocabulario relacionado con deportes."
            else:
                return "Te estoy respondiendo a tu interés por el fútbol y mostrando que es un tema genial para practicar inglés."
        
        elif 'food' in user_lower or 'comida' in user_lower:
            if '?' in english_response:
                return "Te estoy preguntando sobre comida para conocer tus preferencias culinarias y practicar vocabulario de alimentos."
            else:
                return "Te estoy respondiendo a tu interés por la comida, que es un tema excelente para aprender nuevo vocabulario."
        
        # Explicaciones por tipo de respuesta
        elif '?' in english_response:
            return "Te estoy haciendo una pregunta para continuar nuestra conversación y practicar más inglés juntos."
        
        elif any(word in english_lower for word in ['great', 'wonderful', 'excellent', 'amazing']):
            return "Te estoy dando una respuesta positiva y de ánimo para motivarte a seguir practicando."
        
        elif any(word in english_lower for word in ['understand', 'see', 'know', 'interesting']):
            return "Te estoy mostrando que comprendo lo que me dices y que encuentro interesante tu mensaje."
        
        elif any(word in english_lower for word in ['tell me', 'more', 'about', 'explain']):
            return "Te estoy pidiendo que me cuentes más detalles sobre el tema para seguir practicando conversación."
        
        elif 'welcome' in english_lower or 'hello' in english_lower:
            return "Te estoy dando la bienvenida y estableciendo un ambiente amigable para nuestra práctica de inglés."
        
        else:
            return "Te estoy respondiendo de manera natural para mantener nuestra conversación y ayudarte a practicar inglés."