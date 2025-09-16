"""
Script para verificar la configuración
"""
from src.config.settings import Settings
import json

print("🔧 Verificando configuración...")

try:
    settings = Settings()
    settings.validate()
    
    print("✅ Configuración creada exitosamente")
    print(f"📁 Directorio de trabajo: {settings.paths.working_dir}")
    print(f"📄 Archivo de errores: {settings.paths.errors_file}")
    print(f"🎵 Archivo de audio: {settings.audio.audio_file}")
    print(f"🧠 Modelo Whisper: {settings.models.whisper_model}")
    
    # Verificar que el archivo de errores existe
    errors_file = settings.paths.working_dir / settings.paths.errors_file
    if errors_file.exists():
        with open(errors_file, 'r', encoding='utf-8') as f:
            errors_data = json.load(f)
        print(f"📚 Errores en memoria: {len(errors_data)} registros")
    else:
        print("📚 Archivo de errores no existe (se creará automáticamente)")
    
    print("\n🎉 ¡Configuración válida!")
    
except Exception as e:
    print(f"❌ Error en configuración: {e}")