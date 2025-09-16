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

def main():
    """Función principal"""
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
        
        # Ejecutar bucle principal
        assistant.run()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Aplicación interrumpida por el usuario")
        logger.info("Application interrupted by user")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        logger.critical(f"Critical error: {e}")
        raise

if __name__ == "__main__":
    main()