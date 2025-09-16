"""
Script para verificar que todas las importaciones funcionen
"""
print("🧪 Verificando importaciones...")

try:
    from src.config.settings import Settings
    print("✅ Settings importado correctamente")
    
    from src.services.audio_service import AudioRecorder, WhisperSTT, GTTSService
    print("✅ Audio services importados correctamente")
    
    from src.services.error_service import ErrorMemoryService
    print("✅ Error service importado correctamente")
    
    from src.services.translation_service import TranslationService
    print("✅ Translation service importado correctamente")
    
    from src.services.grammar_service import GrammarService
    print("✅ Grammar service importado correctamente")
    
    from src.services.chat_service import ChatService
    print("✅ Chat service importado correctamente")
    
    from src.assistant.ai_assistant import AIAssistant
    print("✅ AI Assistant importado correctamente")
    
    print("\n🎉 ¡Todas las importaciones exitosas!")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")