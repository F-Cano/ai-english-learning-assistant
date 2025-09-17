import os
import logging
from pathlib import Path
from src.config.settings import Settings
from src.assistant.ai_assistant import AIAssistant
from src.utils.logging_config import setup_logging
from src.utils.error_handler import graceful_shutdown

@graceful_shutdown
def main():
    """Función principal mejorada con mejor manejo de errores"""
    try:
        # Configurar settings
        settings = Settings()
        settings.validate()
        
        # Configurar logging centralizado
        setup_logging(settings)
        logger = logging.getLogger(__name__)
        
        # Cambiar al directorio de trabajo
        os.chdir(settings.paths.working_dir)
        
        print("🚀 Iniciando Asistente de IA para práctica de inglés...")
        print(f"📂 Directorio de trabajo: {settings.paths.working_dir}")
        print(f"📋 Archivo de errores: {settings.paths.errors_file}")
        print(f"📝 Logs en: {settings.paths.logs_dir}")
        
        logger.info("Starting AI Assistant application")
        
        # Crear e inicializar el asistente
        assistant = AIAssistant(settings)
        
        # Ejecutar bucle principal
        assistant.run()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Aplicación interrumpida por el usuario")
        if 'logger' in locals():
            logger.info("Application interrupted by user")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        if 'logger' in locals():
            logger.critical(f"Critical error: {e}")
        raise

if __name__ == "__main__":
    main()