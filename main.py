import os
import logging
from pathlib import Path
from src.config.settings import Settings
from src.assistant.ai_assistant import AIAssistant

def setup_logging(settings: Settings):
    """Configura el sistema de logging"""
    log_file = settings.paths.logs_dir / "assistant.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def show_menu():
    """Muestra el menú principal del asistente"""
    print("\n" + "="*60)
    print("🤖 ASISTENTE DE INGLÉS CON INTELIGENCIA ARTIFICIAL")
    print("="*60)
    print("Selecciona una opción:")
    print()
    print("1. 📚 Práctica de Vocabulario")
    print("2. 🎤 Práctica de Pronunciación") 
    print("3. 📖 Lectura de Texto")
    print("4. 🎮 Modo Interactivo Híbrido")
    print("5. 🧠 Chat Inteligente (IA Avanzada)")
    print("6. 📊 Ver Estadísticas")
    print("7. ⚙️ Configuración")
    print("8. ❌ Salir")
    print()

def show_basic_statistics():
    """Muestra estadísticas básicas"""
    print("\n📊 ESTADÍSTICAS BÁSICAS:")
    print("="*40)
    print("📝 Función de estadísticas en desarrollo")
    print("💡 Por ahora, usa los modos de práctica para generar datos")
    print("🔜 Próximamente: estadísticas detalladas de progreso")

def show_basic_configuration():
    """Muestra configuración básica"""
    print("\n⚙️ CONFIGURACIÓN BÁSICA:")
    print("="*40)
    print("📝 Panel de configuración en desarrollo")
    print("💡 Las configuraciones se manejan automáticamente")
    print("🔜 Próximamente: configuración personalizada de modelos")

def main():
    """Función principal del programa"""
    assistant = None
    
    try:
        # Configurar settings
        settings = Settings()
        settings.validate()
        
        # Configurar logging
        setup_logging(settings)
        logger = logging.getLogger(__name__)
        
        # Cambiar al directorio de trabajo
        os.chdir(settings.paths.working_dir)
        
        print("🚀 Iniciando Asistente de IA para práctica de inglés...")
        logger.info("Starting AI Assistant application")
        
        # Crear e inicializar el asistente
        assistant = AIAssistant(settings)
        
        while True:
            show_menu()
            choice = input("▶️  Tu elección: ").strip()
            
            if choice == "1":
                try:
                    # 🔧 USAR MÉTODO EXISTENTE
                    assistant.practice_vocabulary()
                except Exception as e:
                    print(f"❌ Error en modo vocabulario: {e}")
                    
            elif choice == "2":
                try:
                    # 🔧 USAR MÉTODO EXISTENTE
                    assistant.practice_pronunciation()
                except Exception as e:
                    print(f"❌ Error en modo pronunciación: {e}")
                    
            elif choice == "3":
                try:
                    # 🔧 USAR MÉTODO EXISTENTE
                    assistant.read_text()
                except Exception as e:
                    print(f"❌ Error en modo lectura: {e}")
                    
            elif choice == "4":
                try:
                    from src.modes.interactive_mode import InteractiveMode
                    interactive = InteractiveMode(assistant)
                    interactive.run()
                except ImportError:
                    print("❌ Modo interactivo no disponible")
                except Exception as e:
                    print(f"❌ Error en modo interactivo: {e}")
                    
            elif choice == "5":
                try:
                    from src.modes.smart_chat_mode import SmartChatMode
                    smart_chat = SmartChatMode(assistant)
                    smart_chat.run()
                except ImportError:
                    print("❌ Chat inteligente no disponible aún")
                    print("💡 Usa la opción 4 (Modo Interactivo) mientras tanto")
                except Exception as e:
                    print(f"❌ Error en chat inteligente: {e}")
                    
            elif choice == "6":
                try:
                    # 🔧 USAR FUNCIÓN BÁSICA TEMPORAL
                    show_basic_statistics()
                except Exception as e:
                    print(f"❌ Error mostrando estadísticas: {e}")
                    
            elif choice == "7":
                try:
                    # 🔧 USAR FUNCIÓN BÁSICA TEMPORAL
                    show_basic_configuration()
                except Exception as e:
                    print(f"❌ Error en configuración: {e}")
                    
            elif choice == "8":
                print("👋 ¡Hasta luego! Sigue practicando.")
                logger.info("Application exited by user")
                break
                
            else:
                print("❌ Opción inválida. Por favor, elige 1-8.")
                
    except KeyboardInterrupt:
        print("\n\n⚠️ Programa interrumpido por el usuario.")
        if assistant:
            logger.info("Application interrupted by user")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        if assistant:
            logger.critical(f"Critical error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if assistant:
            try:
                assistant.cleanup()
            except:
                pass
        print("🔚 Programa terminado.")

if __name__ == "__main__":
    main()