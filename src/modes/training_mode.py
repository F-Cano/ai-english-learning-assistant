import random
from typing import List, Dict, Any

class TrainingMode:
    """Modo de entrenamiento estructurado con preguntas adaptativas"""
    
    def __init__(self, assistant):
        self.assistant = assistant
        self.questions_asked = 0
        self.max_questions = 5
    
    def generate_questions(self) -> List[str]:
        """Genera preguntas adaptativas basadas en errores frecuentes"""
        base_questions = [
            "What did you do yesterday?",
            "Describe your favorite place.",
            "What is your dream job?",
            "Tell me about your hobbies.",
            "What is your favorite movie and why?",
            "How do you usually spend your weekends?",
            "What's the most interesting place you've visited?",
            "Describe your perfect day.",
            "What are your goals for this year?",
            "Tell me about your family."
        ]
        
        # Añadir preguntas específicas para errores frecuentes
        try:
            frequent_errors = self.assistant.error_service.get_frequent_errors(2)
            for correction in list(frequent_errors.keys())[:3]:  # Solo las primeras 3
                base_questions.append(f"Please use this phrase correctly in a sentence: '{correction}'")
        except Exception as e:
            print(f"⚠️  No se pudieron cargar errores frecuentes: {e}")
        
        random.shuffle(base_questions)
        return base_questions
    
    def run(self):
        """Ejecuta el modo de entrenamiento"""
        print("\n🎓 Iniciando modo entrenamiento...")
        print("💡 Responde en inglés para obtener mejor feedback")
        print("💬 Puedes decir 'skip' para saltar una pregunta o 'quit' para terminar")
        
        try:
            self.assistant.speak("Starting training mode. Please respond in English for better feedback.", "en")
        except Exception as e:
            print(f"⚠️  Error en TTS: {e}")
        
        questions = self.generate_questions()
        
        for i, question in enumerate(questions[:self.max_questions], 1):
            print(f"\n{'='*60}")
            print(f"❓ Pregunta {i}/{self.max_questions}: {question}")
            
            # Traducir pregunta para comprensión
            try:
                translation = self.assistant.translation_service.translate(question, "en", "es")
                print(f"🔄 En español: {translation}")
            except Exception as e:
                print(f"⚠️  Error en traducción: {e}")
            
            # Reproducir pregunta
            try:
                self.assistant.speak(question, "en")
            except Exception as e:
                print(f"⚠️  Error en TTS: {e}")
            
            # Escuchar respuesta
            try:
                print("\n🎙️  Esperando tu respuesta...")
                text, language = self.assistant.listen()
                
                if not text.strip():
                    print("❌ No se detectó audio. Intenta de nuevo.")
                    continue
                
                # Verificar comandos especiales
                if self._is_skip_command(text):
                    print("⏭️  Pregunta saltada.")
                    continue
                
                if self._is_exit_command(text):
                    print("🚪 Saliendo del modo entrenamiento...")
                    break
                
                # Procesar respuesta
                result = self.assistant.process_user_input(text, language)
                self._provide_feedback(result)
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Entrenamiento interrumpido por el usuario")
                break
            except Exception as e:
                print(f"❌ Error procesando respuesta: {e}")
                continue
        
        # Mostrar resumen final
        self._show_final_summary()
    
    def _is_skip_command(self, text: str) -> bool:
        """Verifica si es un comando para saltar"""
        skip_commands = ["skip", "next", "saltar", "siguiente"]
        return text.lower().strip() in skip_commands
    
    def _is_exit_command(self, text: str) -> bool:
        """Verifica si es un comando de salida"""
        exit_commands = ["quit", "exit", "salir", "terminar", "bye", "adiós", "stop"]
        return text.lower().strip() in exit_commands
    
    def _provide_feedback(self, result: Dict[str, Any]):
        """Proporciona feedback detallado"""
        print(f"\n👤 Dijiste: '{result['original_text']}'")
        print(f"🌐 Idioma detectado: {result['detected_language']}")
        
        if result["improvement_detected"]:
            print("🎉 ¡Excelente! Corregiste un error que habías cometido antes.")
            try:
                self.assistant.speak("Great job! You corrected a past mistake.", "en")
            except:
                pass
        
        if result["translation"]:
            print(f"🔄 Traducción: {result['translation']}")
        
        if result["grammar_correction"]:
            print(f"✏️  Corrección sugerida: '{result['grammar_correction']}'")
            print("💡 Intenta usar la forma corregida en tu próxima respuesta.")
            try:
                self.assistant.speak(f"Here's a suggestion: {result['grammar_correction']}", "en")
            except:
                pass
        else:
            print("✅ ¡Perfecto! Tu gramática está correcta.")
            try:
                self.assistant.speak("Perfect grammar!", "en")
            except:
                pass
        
        if result["response"]:
            print(f"🤖 Respuesta del asistente: {result['response']}")
            try:
                self.assistant.speak(result["response"], "en")
            except:
                pass
    
    def _show_final_summary(self):
        """Muestra resumen final del entrenamiento"""
        print(f"\n{'='*60}")
        print("🎓 ¡Entrenamiento completado!")
        
        try:
            self.assistant.show_session_summary()
            
            # Obtener errores frecuentes para recomendaciones
            frequent_errors = self.assistant.error_service.get_frequent_errors(2)
            if frequent_errors:
                print("\n📝 Recomendaciones para mejorar:")
                for correction, data in list(frequent_errors.items())[:3]:
                    print(f"   • Practica: '{correction}' (error {data['veces']} veces)")
            else:
                print("\n🌟 ¡Excelente! No tienes errores frecuentes.")
                
        except Exception as e:
            print(f"⚠️  Error generando resumen: {e}")
        
        print("\n💪 ¡Sigue practicando para mejorar tu inglés!")
        
        try:
            self.assistant.speak("Training completed! Keep practicing to improve your English!", "en")
        except:
            pass