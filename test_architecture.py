#!/usr/bin/env python3
"""
Test completo del sistema AI English Learning Assistant
Demuestra la arquitectura modular mejorada
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importaciones
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import Settings, AudioConfig, ModelConfig, PathConfig
from src.utils.logging_config import setup_logging
from src.utils.error_handler import ErrorHandler
import logging

def test_configuration():
    """Prueba el sistema de configuración"""
    print("🔧 Testing Configuration System...")
    
    try:
        # Test configuración básica
        settings = Settings()
        assert settings.audio.sample_rate == 16000
        assert settings.models.whisper_model == "base"
        assert settings.paths.errors_file == "errores_memoria.json"
        
        # Test validación
        is_valid = settings.validate()
        assert is_valid == True
        
        print("✅ Configuration system working correctly")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_logging_system():
    """Prueba el sistema de logging centralizado"""
    print("\n📝 Testing Logging System...")
    
    try:
        settings = Settings()
        logger = setup_logging(settings)
        
        # Test logging
        logger.info("Test log message")
        print("✅ Logging system working correctly")
        return True
    except Exception as e:
        print(f"❌ Logging test failed: {e}")
        return False

def test_error_handler():
    """Prueba el sistema de manejo de errores"""
    print("\n⚠️  Testing Error Handler...")
    
    try:
        # Test safe execution
        def risky_function():
            raise ValueError("Test error")
        
        result = ErrorHandler.safe_execute(
            risky_function, 
            fallback_value="fallback", 
            context="test_function"
        )
        
        assert result == "fallback"
        
        # Test error logging
        try:
            raise RuntimeError("Test runtime error")
        except Exception as e:
            ErrorHandler.log_error(e, "test context")
        
        print("✅ Error handler working correctly")
        return True
    except Exception as e:
        print(f"❌ Error handler test failed: {e}")
        return False

def test_lightweight_services():
    """Prueba servicios que no requieren modelos pesados"""
    print("\n🚀 Testing Lightweight Services...")
    
    try:
        from src.services.error_service import ErrorMemoryService
        
        # Test error service
        settings = Settings()
        error_file = settings.paths.working_dir / "test_errors.json"
        error_service = ErrorMemoryService(error_file)
        
        # Test registering and retrieving errors
        error_service.register_error("I are happy", "I am happy")
        summary = error_service.get_session_summary()
        
        assert summary['total'] >= 1
        
        print("✅ Lightweight services working correctly")
        return True
    except Exception as e:
        print(f"❌ Lightweight services test failed: {e}")
        return False

def test_interfaces():
    """Prueba que las interfaces estén correctamente definidas"""
    print("\n🔧 Testing Interface Definitions...")
    
    try:
        from src.interfaces.base import (
            ISpeechToText, ITextToSpeech, ITranslator,
            IGrammarCorrector, IChatGenerator, IErrorTracker
        )
        
        # Verificar que las interfaces están definidas
        assert hasattr(ISpeechToText, 'recognize')
        assert hasattr(ITextToSpeech, 'speak')
        assert hasattr(ITranslator, 'translate')
        assert hasattr(IGrammarCorrector, 'correct')
        assert hasattr(IChatGenerator, 'generate_response')
        assert hasattr(IErrorTracker, 'register_error')
        
        print("✅ Interface definitions working correctly")
        return True
    except Exception as e:
        print(f"❌ Interface test failed: {e}")
        return False

def test_modular_imports():
    """Prueba que todos los módulos se puedan importar"""
    print("\n📦 Testing Modular Imports...")
    
    modules_to_test = [
        "src.config.settings",
        "src.interfaces.base",
        "src.services.error_service",
        "src.assistant.ai_assistant",
        "src.modes.training_mode",
        "src.modes.conversation_mode", 
        "src.modes.interactive_mode",
        "src.utils.logging_config",
        "src.utils.error_handler"
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    if not failed_imports:
        print("✅ All modular imports working correctly")
        return True
    else:
        print(f"❌ Failed imports: {failed_imports}")
        return False

def test_architecture_principles():
    """Prueba que se cumplan los principios de arquitectura"""
    print("\n🏗️  Testing Architecture Principles...")
    
    try:
        # Test separación de responsabilidades
        from src.config.settings import Settings
        from src.services.error_service import ErrorMemoryService
        from src.assistant.ai_assistant import AIAssistant
        
        # Test que las clases tienen responsabilidades específicas
        settings = Settings()
        
        # Settings solo maneja configuración
        assert hasattr(settings, 'audio')
        assert hasattr(settings, 'models')
        assert hasattr(settings, 'paths')
        
        # ErrorMemoryService solo maneja errores
        error_service = ErrorMemoryService(Path("test_errors.json"))
        assert hasattr(error_service, 'register_error')
        assert hasattr(error_service, 'get_frequent_errors')
        assert not hasattr(error_service, 'translate')  # No debe tener funciones de traducción
        
        print("✅ Architecture principles maintained")
        return True
    except Exception as e:
        print(f"❌ Architecture principles test failed: {e}")
        return False

def run_architecture_tests():
    """Ejecuta todos los tests de arquitectura"""
    print("🧪 Running AI English Assistant Architecture Tests")
    print("=" * 60)
    
    tests = [
        test_configuration,
        test_logging_system,
        test_error_handler,
        test_interfaces,
        test_modular_imports,
        test_lightweight_services,
        test_architecture_principles
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL" 
        print(f"{i+1:2d}. {test.__name__:<30} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Architecture is working correctly.")
        print("\n💡 Ready for:")
        print("   • Adding new AI models")
        print("   • Extending with new languages")
        print("   • Creating web interface")
        print("   • Adding more learning modes")
        print("   • Integrating with external APIs")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Check the issues above.")
    
    return passed == total

def show_architecture_summary():
    """Muestra resumen de la arquitectura implementada"""
    print("\n🏗️  ARCHITECTURE SUMMARY")
    print("=" * 60)
    print("""
✅ IMPLEMENTED COMPONENTS:

📁 Configuration Layer:
   • Settings management with dataclasses
   • Environment-specific path handling
   • Model configuration centralization

🔧 Interface Layer:
   • Abstract base classes for all services
   • Dependency injection ready
   • Service substitution support

🛠️  Service Layer:
   • Audio processing (recording, TTS, STT)
   • Error tracking and learning
   • Translation and grammar correction  
   • Conversational AI chat
   • Modular and testable

🎮 Mode Layer:
   • Training mode (structured questions)
   • Conversation mode (free chat)
   • Interactive mode (adaptive difficulty)
   • Easy to add new modes

🎯 Orchestration Layer:
   • AI Assistant main coordinator
   • Service initialization and management
   • User session control

🛡️  Utility Layer:
   • Centralized logging
   • Error handling with fallbacks
   • Retry mechanisms
   • Graceful shutdown

📁 PROJECT STRUCTURE:
src/
├── config/          # Configuration management
├── interfaces/      # Abstract service contracts  
├── services/        # Core AI and processing services
├── assistant/       # Main orchestration logic
├── modes/           # Different interaction modes
└── utils/           # Cross-cutting utilities

🎯 BENEFITS ACHIEVED:
   • Separation of concerns
   • Easy testing and mocking
   • Service substitution
   • Scalable architecture
   • Error resilience
   • Maintainable codebase
""")

if __name__ == "__main__":
    # Ejecutar tests
    success = run_architecture_tests()
    
    # Mostrar resumen de arquitectura
    show_architecture_summary()
    
    # Exit code
    sys.exit(0 if success else 1)