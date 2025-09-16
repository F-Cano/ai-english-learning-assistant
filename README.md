#  AI English Learning Assistant

Un asistente de IA avanzado para aprender inglés con múltiples modos de práctica, análisis gramatical en tiempo real y conversación por voz.

##  Características

###  Modos de Aprendizaje
- **Modo Entrenamiento**: Preguntas estructuradas con dificultad progresiva
- **Modo Conversación Libre**: Práctica natural sin restricciones
- **Modo Interactivo Híbrido**: Entrada por voz o teclado con retroalimentación adaptativa
- **Conversación por Voz**: Práctica en tiempo real con IA conversacional

###  Tecnologías de IA
- **Whisper (OpenAI)**: Reconocimiento de voz preciso
- **Grammar Correction**: Análisis y corrección gramatical automática
- **Language Detection**: Detección automática de idioma
- **Progress Tracking**: Seguimiento inteligente del progreso

###  Análisis Avanzado
- Detección automática de errores frecuentes
- Sugerencias personalizadas de mejora
- Estadísticas detalladas de rendimiento
- Retroalimentación adaptativa por nivel

## 🚀 Instalación

### Prerrequisitos
- Python 3.8+
- Micrófono y altavoces/auriculares
- Conexión a internet (para algunos servicios)

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/ai-english-assistant.git
cd ai-english-assistant
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configuración (opcional)
```bash
# Para funciones avanzadas con OpenAI
set OPENAI_API_KEY=tu_api_key_aqui
```

##  Uso

### Ejecutar el asistente
```bash
python main.py
```

### Modos disponibles
1. **🎓 Modo Entrenamiento**: Preguntas estructuradas
2. ** Conversación Libre**: Práctica sin límites
3. ** Modo Interactivo**: Entrada híbrida voz/teclado
4. ** Conversación por Voz**: IA conversacional en tiempo real

### Comandos especiales
- `voice` / `voz` - Cambiar a entrada por voz
- `stats` - Ver estadísticas de progreso
- `level` - Verificar nivel actual
- `easier` / `harder` - Ajustar dificultad
- `quit` - Salir del programa

##  Estructura del Proyecto

```
ai-english-assistant/
 src/
    assistant/           # Lógica principal del asistente
    services/           # Servicios de IA (STT, TTS, Grammar)
    modes/              # Diferentes modos de práctica
    interfaces/         # Interfaces y contratos
    utils/              # Utilidades y helpers
    config/             # Configuración del sistema
 data/                   # Datos de usuario y errores
├── requirements.txt        # Dependencias Python
├── main.py                # Punto de entrada
└── README.md              # Este archivo
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# OpenAI API (opcional)
OPENAI_API_KEY=tu_api_key

# Configuración de audio
AUDIO_SAMPLE_RATE=16000
AUDIO_SILENCE_DURATION=1.2
```

### Personalización
- Modifica `src/config/settings.py` para ajustar configuraciones
- Añade nuevas preguntas en los archivos de modo
- Personaliza la retroalimentación en los servicios

##  Características Técnicas

### Servicios de IA
- **WhisperSTT**: Reconocimiento de voz con Whisper
- **GrammarService**: Corrección gramatical avanzada
- **TranslationService**: Traducción bidireccional
- **ErrorTrackingService**: Seguimiento de errores frecuentes

### Arquitectura
- **Patrón Repository**: Para gestión de datos
- **Dependency Injection**: Servicios intercambiables
- **Event-Driven**: Sistema de eventos para progreso
- **Modular Design**: Fácil extensión y mantenimiento

##  Contribuir

1. Fork el proyecto
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

##  Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

##  Roadmap

- [ ] Integración con más modelos de IA
- [ ] Modo de práctica de pronunciación
- [ ] Dashboard web para estadísticas
- [ ] Aplicación móvil companion
- [ ] Integración con sistemas de learning management
- [ ] Soporte para más idiomas

##  Soporte

¿Tienes preguntas o problemas?
-  Email: fabiocano17@hotmail.com

##  Agradecimientos

- OpenAI por Whisper y GPT
- Hugging Face por los modelos de transformers
- Comunidad de Python por las increíbles librerías

---

 **¡Dale una estrella si este proyecto te ayuda a aprender inglés!** 
