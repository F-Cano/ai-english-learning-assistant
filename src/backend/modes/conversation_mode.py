from typing import Dict, Any

class ConversationMode:
    """Modo de conversación libre con el asistente"""
    
    def __init__(self, assistant):
        self.assistant = assistant
        self.conversation_count = 0
    
    def run(self):
        """Ejecuta el modo de conversación libre"""
        print("\n💬 Iniciando modo conversación libre...")
        print("🗣️  Puedes hablar en español o inglés")
        print("💡 Comandos útiles: 'help', 'summary', 'quit' para salir")
        
        try:
            self.assistant.speak("Hello! Let's have a conversation. You can speak in English or Spanish.", "en")
        except Exception as e:
            print(f"⚠️  Error en TTS: {e}")
        
        while True:
            try:
                print(f"\n{'-'*50}")
                print("🎙️  Esperando tu mensaje...")
                
                # Escuchar usuario
                text, language = self.assistant.listen()
                
                if not text.strip():
                    print("❌ No se detectó audio. Intenta de nuevo.")
                    continue
                
                # Verificar comandos especiales
                if self._handle_special_commands(text):
                    continue
                
                # Comandos de salida
                if self._is_exit_command(text):
                    print("👋 ¡Hasta luego!")
                    try:
                        self.assistant.speak("Goodbye! It was nice talking with you.", "en")
                    except:
                        pass
                    break
                
                # Procesar entrada normal
                result = self.assistant.process_user_input(text, language)
                self._display_results(result)
                
                # Responder
                if result["response"]:
                    print(f"🤖 Asistente: {result['response']}")
                    try:
                        self.assistant.speak(result["response"], "en")
                    except Exception as e:
                        print(f"⚠️  Error en TTS: {e}")
                
                self.conversation_count += 1
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Conversación interrumpida por el usuario")
                break
            except Exception as e:
                print(f"❌ Error en conversación: {e}")
                continue
        
        self._show_conversation_summary()
    
    def _handle_special_commands(self, text: str) -> bool:
        """Maneja comandos especiales. Retorna True si se manejó un comando."""
        command = text.lower().strip()
        
        if command == "help":
            self._show_help()
            return True
        
        if command == "summary":
            self.assistant.show_session_summary()
            return True
        
        if command in ["clear", "limpiar"]:
            print("\n" * 20)  # Limpiar pantalla
            print("🧹 Pantalla limpiada")
            return True
        
        return False
    
    def _show_help(self):
        """Muestra comandos disponibles"""
        print("""
🆘 COMANDOS DISPONIBLES:
   
   🗣️  CONVERSACIÓN:
   • Habla normalmente en español o inglés
   • El asistente detectará el idioma automáticamente
   
   🔧 COMANDOS ESPECIALES:
   • 'help' - Mostrar esta ayuda
   • 'summary' - Ver resumen de errores
   • 'clear' - Limpiar pantalla
   • 'quit', 'exit', 'salir' - Terminar conversación
   
   💡 TIPS:
   • Habla en inglés para obtener correcciones
   • Habla en español para practicar traducción
   • El asistente recordará tus errores para ayudarte
        """)
    
    def _is_exit_command(self, text: str) -> bool:
        """Verifica si es un comando de salida"""
        exit_commands = ["quit", "exit", "salir", "terminar", "bye", "adiós", "goodbye"]
        return text.lower().strip() in exit_commands
    
    def _display_results(self, result: Dict[str, Any]):
        """Muestra los resultados del procesamiento"""
        print(f"\n👤 Dijiste: '{result['original_text']}'")
        print(f"🌐 Idioma: {result['detected_language']}")
        
        if result["translation"]:
            if result['detected_language'].startswith('en'):
                print(f"🔄 En español: {result['translation']}")
            else:
                print(f"🔄 En inglés: {result['translation']}")
        
        if result["grammar_correction"]:
            print(f"✏️  Sugerencia: '{result['grammar_correction']}'")
        
        if result["improvement_detected"]:
            print("🎉 ¡Genial! Corregiste un error previo.")
    
    def _show_conversation_summary(self):
        """Muestra resumen de la conversación"""
        print(f"\n{'='*50}")
        print("💬 Resumen de la conversación:")
        print(f"   💭 Intercambios: {self.conversation_count}")
        
        try:
            self.assistant.show_session_summary()
        except Exception as e:
            print(f"⚠️  Error mostrando resumen: {e}")
        
        print("\n👏 ¡Gracias por practicar!")