import random
from typing import Dict, Any, List, Tuple
from enum import Enum

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"

class InteractiveMode:
    """Modo interactivo híbrido con entrada por voz o teclado"""
    
    def __init__(self, assistant):
        self.assistant = assistant
        self.difficulty = DifficultyLevel.INTERMEDIATE
        self.conversation_count = 0
        self.correct_responses = 0
        self.grammar_errors = 0
        self.user_performance = {
            'total_responses': 0,
            'correct_grammar': 0,
            'needs_help': 0,
            'wants_challenge': 0,
            'consecutive_poor': 0,
            'consecutive_excellent': 0
        }
    
    def run(self):
        """Ejecuta el modo interactivo híbrido"""
        print("\n Modo Interactivo Híbrido")
        print("=" * 50)
        print(" Puedes responder por VOZ  o TECLADO ")
        print(" Responde en INGLÉS o ESPAÑOL")
        print("🎯 El sistema se adapta a tu nivel automáticamente")
        
        self._show_commands()
        self._choose_initial_difficulty()
        
        # Saludo inicial
        initial_greeting = self._get_greeting()
        self._ask_question(initial_greeting["question"], initial_greeting["translation"])
        
        while True:
            try:
                # Obtener respuesta del usuario (voz o teclado)
                user_response, input_method = self._get_user_input()
                
                if not user_response.strip():
                    print(" Respuesta vacía. Intenta de nuevo.")
                    continue
                
                # Verificar comandos especiales
                if self._handle_special_commands(user_response):
                    continue
                
                # Comando de salida
                if self._is_exit_command(user_response):
                    break
                
                # Procesar respuesta y dar feedback
                feedback = self._process_and_feedback(user_response, input_method)
                
                # Generar siguiente pregunta basada en el rendimiento
                next_question = self._generate_adaptive_question(feedback)
                self._ask_question(next_question["question"], next_question["translation"])
                
                self.conversation_count += 1
                
                # Evaluar progreso cada 5 respuestas
                if self.conversation_count % 5 == 0:
                    self._evaluate_progress()
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f" Error: {e}")
                continue
        
        self._show_final_summary()
    
    def _show_commands(self):
        """Muestra comandos disponibles"""
        print(f"""
 COMANDOS DISPONIBLES:
    Para escribir: Simplemente escribe tu respuesta
    Para hablar: Escribe 'voice' o 'voz' y presiona Enter
   
    COMANDOS ESPECIALES:
    'help' - Mostrar ayuda
    'easier' - Bajar un nivel de dificultad
    'harder' - Subir un nivel de dificultad
    'level' - Ver nivel actual e información
    'change_level' - Elegir nuevo nivel
    'stats' - Ver estadísticas
    'quit' - Salir
        """)
    
    def _choose_initial_difficulty(self):
        """Permite al usuario elegir su nivel inicial"""
        print(f"\n SELECCIONA TU NIVEL DE INGLÉS:")
        print("=" * 40)
        
        print("1.  PRINCIPIANTE")
        print("    Preguntas básicas (nombre, edad, colores)")
        print("    Vocabulario simple")
        print("    Ideal para empezar")
        
        print("\n2.  INTERMEDIO")
        print("    Conversación cotidiana")
        print("    Preguntas sobre experiencias")
        print("    Nivel estándar")
        
        print("\n3.  AVANZADO")
        print("    Temas complejos y abstractos")
        print("    Preguntas de análisis y opinión")
        print("    Desafío máximo")
        
        print("\n4.  AUTOMÁTICO")
        print("    El sistema detecta tu nivel basado en errores previos")
        print("    Se adapta automáticamente")
        
        suggested_level = self._get_suggested_level()
        print(f"\n Sugerencia del sistema: {suggested_level}")
        
        while True:
            try:
                choice = input("\n  Elige tu nivel (1-4): ").strip()
                
                if choice == "1":
                    self.difficulty = DifficultyLevel.BEGINNER
                    print(" Nivel seleccionado: PRINCIPIANTE")
                    break
                elif choice == "2":
                    self.difficulty = DifficultyLevel.INTERMEDIATE
                    print(" Nivel seleccionado: INTERMEDIO")
                    break
                elif choice == "3":
                    self.difficulty = DifficultyLevel.ADVANCED
                    print(" Nivel seleccionado: AVANZADO")
                    break
                elif choice == "4":
                    self._set_automatic_difficulty()
                    print(f" Nivel automático: {self.difficulty.value.upper()}")
                    break
                else:
                    print(" Opción inválida. Elige 1, 2, 3 o 4.")
                    
            except KeyboardInterrupt:
                print("\n\n  Saliendo...")
                return
    
    def _get_suggested_level(self) -> str:
        """Obtiene el nivel sugerido basado en el historial"""
        try:
            frequent_errors = self.assistant.error_service.get_frequent_errors(2)
            total_errors = len(frequent_errors)
            
            if total_errors > 10:
                return " PRINCIPIANTE (tienes muchos errores registrados)"
            elif total_errors > 5:
                return " INTERMEDIO (tienes algunos errores registrados)"
            elif total_errors > 0:
                return " AVANZADO (pocos errores registrados)"
            else:
                return " INTERMEDIO (sin historial de errores)"
        except:
            return " INTERMEDIO (nivel por defecto)"
    
    def _set_automatic_difficulty(self):
        """Establece dificultad automática basada en errores previos"""
        try:
            frequent_errors = self.assistant.error_service.get_frequent_errors(2)
            total_errors = len(frequent_errors)
            
            if total_errors > 10:
                self.difficulty = DifficultyLevel.BEGINNER
            elif total_errors > 5:
                self.difficulty = DifficultyLevel.INTERMEDIATE  
            else:
                self.difficulty = DifficultyLevel.ADVANCED
        except:
            self.difficulty = DifficultyLevel.INTERMEDIATE
    
    def _get_user_input(self) -> Tuple[str, str]:
        """Obtiene entrada del usuario por voz o teclado"""
        print(f"\n{'-'*40}")
        print(" Tu respuesta (escribe directamente o 'voice' para hablar):")
        
        user_input = input("  ").strip()
        
        if user_input.lower() in ['voice', 'voz', 'v']:
            print(" Modo voz activado...")
            try:
                text, language = self.assistant.listen()
                return text, "voice"
            except Exception as e:
                print(f" Error en reconocimiento de voz: {e}")
                print(" Cambiando a modo teclado...")
                typed_input = input("  Escribe tu respuesta: ")
                return typed_input, "keyboard"
        else:
            return user_input, "keyboard"
    
    def _process_and_feedback(self, user_response: str, input_method: str) -> Dict[str, Any]:
        """Procesa la respuesta y genera feedback inteligente"""
        detected_language = self._detect_language_simple(user_response)
        result = self.assistant.process_user_input(user_response, detected_language)
        
        feedback = {
            'original': user_response,
            'language': detected_language,
            'input_method': input_method,
            'has_errors': bool(result.get('grammar_correction')),
            'translation': result.get('translation'),
            'correction': result.get('grammar_correction'),
            'improvement': result.get('improvement_detected'),
            'quality': self._assess_response_quality(user_response, result)
        }
        
        self._display_feedback(feedback)
        self._update_user_performance(feedback)
        
        return feedback
    
    def _assess_response_quality(self, response: str, result: Dict) -> str:
        """Evalúa la calidad de la respuesta"""
        word_count = len(response.split())
        has_errors = bool(result.get('grammar_correction'))
        
        if word_count < 3:
            return "too_short"
        elif word_count < 8 and not has_errors:
            return "good_short"
        elif word_count >= 8 and not has_errors:
            return "excellent"
        elif has_errors and word_count >= 5:
            return "good_with_errors"
        else:
            return "needs_improvement"
    
    def _display_feedback(self, feedback: Dict[str, Any]):
        """Muestra feedback detallado y motivacional"""
        print(f"\n ANÁLISIS DE TU RESPUESTA:")
        print(f"    Dijiste: '{feedback['original']}'")
        print(f"    Idioma: {feedback['language']}")
        print(f"    Método: {' Voz' if feedback['input_method'] == 'voice' else ' Teclado'}")
        
        quality_feedback = {
            "too_short": {
                "emoji": "", 
                "message": "Tu respuesta es muy corta. Intenta añadir más detalles.",
                "suggestion": "Por ejemplo: 'I am fine, thank you. How about you?'"
            },
            "good_short": {
                "emoji": "", 
                "message": "¡Bien! Respuesta correcta y concisa.",
                "suggestion": "¿Puedes expandir un poco más tu respuesta?"
            },
            "excellent": {
                "emoji": "", 
                "message": "¡Excelente! Respuesta completa y sin errores.",
                "suggestion": "¡Perfecto! Sigues así."
            },
            "good_with_errors": {
                "emoji": "", 
                "message": "Buena respuesta con algunos errores menores.",
                "suggestion": "Revisa la gramática y intenta de nuevo."
            },
            "needs_improvement": {
                "emoji": "", 
                "message": "Puedes mejorar. ¡No te rindas!",
                "suggestion": "Intenta usar frases más simples primero."
            }
        }
        
        quality_info = quality_feedback.get(feedback['quality'], quality_feedback["needs_improvement"])
        print(f"   {quality_info['emoji']} {quality_info['message']}")
        
        if feedback['translation']:
            target_lang = "español" if feedback['language'].startswith('en') else "inglés"
            print(f"    En {target_lang}: {feedback['translation']}")
        
        if feedback['correction']:
            print(f"    Corrección: '{feedback['correction']}'")
            print(f"    {quality_info['suggestion']}")
        
        if feedback['improvement']:
            print("    ¡Genial! Corregiste un error que habías cometido antes.")
            self.correct_responses += 1
        
        try:
            if feedback['has_errors'] and feedback['correction']:
                self.assistant.speak(f"Here's a suggestion: {feedback['correction']}", "en")
            elif feedback['quality'] == "excellent":
                self.assistant.speak("Excellent response!", "en")
        except:
            pass
    
    def _update_user_performance(self, feedback: Dict[str, Any]):
        """Actualiza estadísticas de rendimiento del usuario"""
        self.user_performance['total_responses'] += 1
        
        if not feedback['has_errors']:
            self.user_performance['correct_grammar'] += 1
        
        if feedback['quality'] in ['too_short', 'needs_improvement']:
            self.user_performance['needs_help'] += 1
        elif feedback['quality'] == 'excellent':
            self.user_performance['wants_challenge'] += 1
    
    def _generate_adaptive_question(self, last_feedback: Dict[str, Any]) -> Dict[str, str]:
        """Genera pregunta adaptativa con ajustes graduales"""
        if last_feedback['quality'] in ['too_short', 'needs_improvement']:
            self.user_performance['consecutive_poor'] = self.user_performance.get('consecutive_poor', 0) + 1
            
            if self.user_performance['consecutive_poor'] >= 2:
                if self.difficulty == DifficultyLevel.ADVANCED:
                    self.difficulty = DifficultyLevel.INTERMEDIATE
                    print(" Ajustando a nivel INTERMEDIO (2 respuestas difíciles)")
                elif self.difficulty == DifficultyLevel.INTERMEDIATE:
                    self.difficulty = DifficultyLevel.BEGINNER
                    print(" Ajustando a nivel PRINCIPIANTE (2 respuestas difíciles)")
                
                self.user_performance['consecutive_poor'] = 0
        
        elif last_feedback['quality'] == 'excellent':
            self.user_performance['consecutive_excellent'] = self.user_performance.get('consecutive_excellent', 0) + 1
            self.user_performance['consecutive_poor'] = 0
            
            if self.user_performance['consecutive_excellent'] >= 3:
                if self.difficulty == DifficultyLevel.BEGINNER:
                    self.difficulty = DifficultyLevel.INTERMEDIATE
                    print(" ¡Subiendo a nivel INTERMEDIO! (3 respuestas excelentes)")
                elif self.difficulty == DifficultyLevel.INTERMEDIATE:
                    self.difficulty = DifficultyLevel.ADVANCED  
                    print(" ¡Subiendo a nivel AVANZADO! (3 respuestas excelentes)")
                
                self.user_performance['consecutive_excellent'] = 0
        else:
            self.user_performance['consecutive_poor'] = 0
            self.user_performance['consecutive_excellent'] = 0
        
        return self._get_question_by_difficulty()
    
    def _get_question_by_difficulty(self) -> Dict[str, str]:
        """Obtiene pregunta según el nivel de dificultad"""
        questions = {
            DifficultyLevel.BEGINNER: [
                {"question": "What is your name?", "translation": "¿Cuál es tu nombre?"},
                {"question": "How old are you?", "translation": "¿Cuántos años tienes?"},
                {"question": "What is your favorite color?", "translation": "¿Cuál es tu color favorito?"},
                {"question": "Do you like pizza?", "translation": "¿Te gusta la pizza?"},
                {"question": "What day is today?", "translation": "¿Qué día es hoy?"}
            ],
            DifficultyLevel.INTERMEDIATE: [
                {"question": "What did you do last weekend?", "translation": "¿Qué hiciste el fin de semana pasado?"},
                {"question": "Describe your perfect vacation.", "translation": "Describe tus vacaciones perfectas."},
                {"question": "What are your hobbies and why do you enjoy them?", "translation": "¿Cuáles son tus pasatiempos y por qué los disfrutas?"},
                {"question": "If you could meet any historical figure, who would it be?", "translation": "Si pudieras conocer a cualquier figura histórica, ¿quién sería?"},
                {"question": "What's the most interesting book you've read recently?", "translation": "¿Cuál es el libro más interesante que has leído recientemente?"}
            ],
            DifficultyLevel.ADVANCED: [
                {"question": "What are your thoughts on the impact of artificial intelligence on society?", "translation": "¿Cuáles son tus pensamientos sobre el impacto de la inteligencia artificial en la sociedad?"},
                {"question": "If you could change one thing about the education system, what would it be and why?", "translation": "Si pudieras cambiar una cosa del sistema educativo, ¿qué sería y por qué?"},
                {"question": "Describe a challenging situation you faced and how you overcame it.", "translation": "Describe una situación desafiante que enfrentaste y cómo la superaste."},
                {"question": "What role do you think technology should play in addressing climate change?", "translation": "¿Qué papel crees que debería tener la tecnología para abordar el cambio climático?"},
                {"question": "How do cultural differences influence the way people communicate?", "translation": "¿Cómo influyen las diferencias culturales en la forma en que las personas se comunican?"}
            ]
        }
        
        selected_questions = questions[self.difficulty]
        question_data = random.choice(selected_questions)
        
        return {
            "question": question_data["question"],
            "translation": question_data["translation"]
        }
    
    def _get_greeting(self) -> Dict[str, str]:
        """Obtiene saludo inicial"""
        greetings = [
            {"question": "Hi! How are you today?", "translation": "¡Hola! ¿Cómo estás hoy?"},
            {"question": "Hello! What's your name?", "translation": "¡Hola! ¿Cuál es tu nombre?"},
            {"question": "Good day! How has your week been?", "translation": "¡Buen día! ¿Cómo ha sido tu semana?"}
        ]
        return random.choice(greetings)
    
    def _ask_question(self, question: str, translation: str):
        """Hace una pregunta al usuario"""
        print(f"\n AI: {question}")
        print(f" Español: {translation}")
        
        try:
            self.assistant.speak(question, "en")
        except:
            pass
    
    def _detect_language_simple(self, text: str) -> str:
        """Detección simple de idioma basada en palabras comunes"""
        english_words = ['the', 'and', 'is', 'are', 'i', 'you', 'my', 'have', 'has', 'was', 'were']
        spanish_words = ['el', 'la', 'y', 'es', 'son', 'yo', 'tu', 'mi', 'tengo', 'tiene', 'era', 'fueron']
        
        text_lower = text.lower()
        english_count = sum(1 for word in english_words if word in text_lower)
        spanish_count = sum(1 for word in spanish_words if word in text_lower)
        
        return "en" if english_count > spanish_count else "es"
    
    def _handle_special_commands(self, text: str) -> bool:
        """Maneja comandos especiales"""
        command = text.lower().strip()
        
        if command == "help":
            self._show_commands()
            return True
        elif command == "easier":
            self._manual_difficulty_change("easier")
            return True
        elif command == "harder":
            self._manual_difficulty_change("harder")
            return True
        elif command == "level":
            print(f" Nivel actual: {self.difficulty.value.upper()}")
            self._show_level_info()
            return True
        elif command == "stats":
            self._show_stats()
            return True
        elif command == "change_level":
            self._choose_initial_difficulty()
            return True
        
        return False
    
    def _manual_difficulty_change(self, direction: str):
        """Cambia la dificultad manualmente"""
        old_level = self.difficulty.value.upper()
        
        if direction == "easier":
            if self.difficulty == DifficultyLevel.ADVANCED:
                self.difficulty = DifficultyLevel.INTERMEDIATE
            elif self.difficulty == DifficultyLevel.INTERMEDIATE:
                self.difficulty = DifficultyLevel.BEGINNER
            else:
                print(" Ya estás en el nivel más fácil")
                return
        
        elif direction == "harder":
            if self.difficulty == DifficultyLevel.BEGINNER:
                self.difficulty = DifficultyLevel.INTERMEDIATE
            elif self.difficulty == DifficultyLevel.INTERMEDIATE:
                self.difficulty = DifficultyLevel.ADVANCED
            else:
                print(" Ya estás en el nivel más difícil")
                return
        
        new_level = self.difficulty.value.upper()
        print(f" Nivel cambiado: {old_level}  {new_level}")
        
        self.user_performance['consecutive_poor'] = 0
        self.user_performance['consecutive_excellent'] = 0
    
    def _show_level_info(self):
        """Muestra información del nivel actual"""
        level_info = {
            DifficultyLevel.BEGINNER: {
                "descripcion": "Preguntas básicas y vocabulario simple",
                "ejemplos": ["What is your name?", "Do you like pizza?", "What day is today?"]
            },
            DifficultyLevel.INTERMEDIATE: {
                "descripcion": "Conversación cotidiana y experiencias personales", 
                "ejemplos": ["What did you do last weekend?", "Describe your hobbies", "Tell me about your family"]
            },
            DifficultyLevel.ADVANCED: {
                "descripcion": "Temas complejos y análisis profundo",
                "ejemplos": ["Impact of AI on society", "Education system changes", "Climate change solutions"]
            }
        }
        
        info = level_info[self.difficulty]
        print(f"\n Nivel {self.difficulty.value.upper()}:")
        print(f"   {info['descripcion']}")
        print(f"   Ejemplos: {', '.join(info['ejemplos'][:2])}...")
    
    def _show_stats(self):
        """Muestra estadísticas del usuario"""
        if self.user_performance['total_responses'] > 0:
            accuracy = (self.user_performance['correct_grammar'] / self.user_performance['total_responses']) * 100
            print(f"""
 TUS ESTADÍSTICAS:
    Respuestas totales: {self.user_performance['total_responses']}
    Precisión gramatical: {accuracy:.1f}%
    Nivel actual: {self.difficulty.value.upper()}
    Mejoras detectadas: {self.correct_responses}
            """)
        else:
            print(" Aún no hay estadísticas disponibles.")
    
    def _is_exit_command(self, text: str) -> bool:
        """Verifica comandos de salida"""
        exit_commands = ["quit", "exit", "salir", "bye", "adiós", "goodbye", "terminar"]
        return text.lower().strip() in exit_commands
    
    def _evaluate_progress(self):
        """Evalúa progreso y da recomendaciones"""
        total = self.user_performance['total_responses']
        if total == 0:
            return
        
        accuracy = (self.user_performance['correct_grammar'] / total) * 100
        
        print(f"\n EVALUACIÓN DE PROGRESO:")
        if accuracy >= 80:
            print(" ¡Excelente progreso! Tu inglés está mejorando mucho.")
        elif accuracy >= 60:
            print(" Buen progreso. Sigue practicando con constancia.")
        else:
            print(" Sigue esforzándote. La práctica hace al maestro.")
    
    def _show_final_summary(self):
        """Muestra resumen final"""
        print(f"\n{'='*50}")
        print(" RESUMEN DE LA SESIÓN INTERACTIVA")
        self._show_stats()
        
        try:
            self.assistant.show_session_summary()
        except:
            pass
        
        print("\n ¡Gracias por practicar en modo interactivo!")
        print(" Tip: La práctica constante es clave para el éxito.")
        
        try:
            self.assistant.speak("Great job practicing! Keep up the good work!", "en")
        except:
            pass
