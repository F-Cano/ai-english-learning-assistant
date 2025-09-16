"""
Script para probar servicios individuales
"""
from src.config.settings import Settings
import torch

print("🧪 Probando servicios individuales...")

def test_audio_service():
    print("\n🎤 Probando servicio de audio...")
    try:
        from src.services.audio_service import AudioRecorder, GTTSService
        settings = Settings()
        
        # Test TTS
        tts = GTTSService(settings)
        print("✅ TTS service creado")
        
        # Test Audio Recorder
        recorder = AudioRecorder(settings)
        print("✅ Audio recorder creado")
        
        return True
    except Exception as e:
        print(f"❌ Error en audio service: {e}")
        return False

def test_error_service():
    print("\n📝 Probando servicio de errores...")
    try:
        from src.services.error_service import ErrorMemoryService
        settings = Settings()
        
        error_service = ErrorMemoryService(
            settings.paths.working_dir / settings.paths.errors_file
        )
        
        # Test básico
        summary = error_service.get_session_summary()
        print(f"✅ Error service funcionando. Errores: {summary['total']}")
        
        return True
    except Exception as e:
        print(f"❌ Error en error service: {e}")
        return False

def test_heavy_services():
    print("\n🧠 Probando servicios con modelos de IA...")
    print("⚠️  Esto puede tomar varios minutos la primera vez...")
    
    try:
        from src.services.translation_service import TranslationService
        from src.services.grammar_service import GrammarService
        from src.services.chat_service import ChatService
        
        settings = Settings()
        
        print("📥 Cargando modelos...")
        translation = TranslationService(settings)
        print("✅ Translation service cargado")
        
        grammar = GrammarService(settings)
        print("✅ Grammar service cargado")
        
        chat = ChatService(settings)
        print("✅ Chat service cargado")
        
        # Test básico de traducción
        result = translation.translate("Hello", "en", "es")
        print(f"✅ Traducción test: 'Hello' → '{result}'")
        
        return True
    except Exception as e:
        print(f"❌ Error en heavy services: {e}")
        return False

if __name__ == "__main__":
    print(f"🔧 Usando PyTorch: {torch.__version__}")
    print(f"🖥️  CUDA disponible: {torch.cuda.is_available()}")
    
    # Probar servicios ligeros primero
    audio_ok = test_audio_service()
    error_ok = test_error_service()
    
    if audio_ok and error_ok:
        print("\n🎯 Servicios básicos OK. ¿Probar servicios pesados? (y/n)")
        choice = input().lower().strip()
        
        if choice == 'y':
            heavy_ok = test_heavy_services()
            if heavy_ok:
                print("\n🎉 ¡Todos los servicios funcionando!")
            else:
                print("\n⚠️  Algunos servicios pesados fallaron")
        else:
            print("\n⏭️  Saltando servicios pesados")
    else:
        print("\n❌ Algunos servicios básicos fallaron")