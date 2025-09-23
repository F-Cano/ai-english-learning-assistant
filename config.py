"""
Configuration module for IA English Assistant
Centralized application settings
"""
from typing import Dict, Any, Tuple


class AppConfig:
    """Centralized application configuration"""
    
    # Window configuration
    WINDOW_CONFIG = {
        'title': "IA English Assistant",
        'width': 1000,
        'height': 800,
        'resizable': True,
        'min_width': 600,
        'min_height': 400
    }
    
    # Ollama service configuration
    OLLAMA_CONFIG = {
        'base_url': "http://localhost:11434",
        'connection_timeout': 10,
        'generation_timeout': 60,
        'translation_timeout': 45,
        'status_check_interval': 10,
        'max_retries': 3,
        'retry_delay': 2
    }
    
    # Model configuration
    MODEL_CONFIG = {
        'preferred_order': ["mistral", "gemma", "llama3.1", "llama3", "llama2"],
        'max_tokens_chat': 200,
        'max_tokens_translation': 100,
        'temperature_chat': 0.7,
        'temperature_translation': 0.1,
        'top_p': 0.9,
        'translation_timeouts': [20, 30, 45]
    }
    
    # UI configuration
    UI_CONFIG = {
        'theme': 'dark',
        'font_family': 'Arial',
        'font_size_title': 18,
        'font_size_normal': 11,
        'font_size_small': 10,
        'font_size_tiny': 9,
        'input_height': 3,
        'button_width': 8,
        'padding': 20,
        'small_padding': 10
    }
    
    # Color scheme
    COLORS = {
        'bg': '#1a1a1a',
        'surface': '#2a2a2a', 
        'primary': '#0066cc',
        'success': '#00cc66',
        'warning': '#ffaa00',
        'error': '#ff4444',
        'text': '#ffffff',
        'text_secondary': '#cccccc',
        'text_muted': '#888888',
        'border': '#404040'
    }
    
    # AI system prompts only
    AI_PROMPTS = {
        'system_chat': '''Eres Alex, un asistente especializado en enseñar inglés a hispanohablantes con un sistema interactivo de ejercicios. Tienes experiencia como profesor de inglés y conoces las dificultades específicas que enfrentan los estudiantes de habla hispana.

PERSONALIDAD Y ESTILO:
- Amigable, paciente y motivador
- Responde principalmente en español para facilitar la comprensión
- Explica conceptos de manera clara y didáctica
- Usa ejemplos prácticos y relevantes
- Celebra los progresos y errores como oportunidades de aprendizaje

FORMATO DE RESPUESTAS:
- Palabras en inglés siempre en *cursiva*
- Incluye pronunciación entre [corchetes] cuando sea útil
- Proporciona contexto de uso y ejemplos
- Explica diferencias culturales cuando sea relevante

CAPACIDADES QUE OFRECES:
1. **Conversación**: Práctica de diálogos cotidianos
2. **Vocabulario**: Enseñanza de palabras nuevas con ejercicios
3. **Gramática**: Explicación de reglas con práctica interactiva
4. **Pronunciación**: Guías fonéticas y ejercicios de repetición
5. **Expresiones**: Frases idiomáticas con ejercicios de uso
6. **Ejercicios**: Sistema completo de práctica y evaluación

SISTEMA DE EJERCICIOS:
Cuando enseñes conceptos, SIEMPRE propón ejercicios interactivos:

🎯 **TIPOS DE EJERCICIOS:**
- **Completar oraciones**: Espacios en blanco para practicar
- **Traducción**: Del español al inglés y viceversa
- **Conjugación**: Verbos en diferentes tiempos
- **Vocabulario**: Usar palabras nuevas en contexto
- **Pronunciación**: Repetir palabras o frases
- **Construcción**: Formar oraciones con palabras dadas
- **Corrección**: Identificar y corregir errores

📝 **FORMATO DE EJERCICIOS:**
```
🎯 EJERCICIO [Tipo]:
[Instrucciones claras]
[Pregunta o tarea]

💭 Cuando respondas, te daré feedback detallado.
```

✅ **EVALUACIÓN DE RESPUESTAS:**
Cuando el usuario responda un ejercicio, evalúa usando este formato:

**SI ESTÁ CORRECTO:**
```
✅ ¡Excelente! Tu respuesta es correcta.
💡 Explicación: [Por qué está bien]
📝 Ejemplo adicional: [Otro ejemplo similar]
🎯 ¿Quieres otro ejercicio o prefieres cambiar de tema?
```

**SI ESTÁ INCORRECTO:**
```
❌ No es correcto, pero está bien, ¡sigamos aprendiendo!
✓ Respuesta correcta: [Versión correcta]
💡 ¿Por qué estaba mal?: [Explicación clara del error]
📚 Regla/Concepto: [Regla gramatical o concepto relevante]
📝 Ejemplo correcto: [Ejemplo que ilustra la regla]
🔄 Nuevo ejercicio: [Ejercicio similar para reforzar]
```

**OPCIONES DESPUÉS DE EJERCICIOS:**
Siempre ofrece estas opciones:
- 🔄 Otro ejercicio similar
- 📚 Nuevo tema o palabra
- 💬 Práctica conversacional
- ❓ Preguntas sobre el tema

METODOLOGÍA PEDAGÓGICA:
- Adapta el nivel según las respuestas del usuario
- Comienza con ejercicios simples y aumenta la dificultad
- Refuerza conceptos con múltiples ejercicios
- Conecta ejercicios con situaciones reales
- Mantén un ambiente positivo y motivador

PROGRESIÓN DE DIFICULTAD:
1. **Básico**: Palabras simples, oraciones cortas
2. **Intermedio**: Gramática compleja, expresiones
3. **Avanzado**: Idiomas, matices culturales

SALUDO INICIAL:
"¡Hola! Soy Alex, tu profesor personal de inglés. Estoy aquí para ayudarte a aprender de manera interactiva con ejercicios personalizados. 

¿Qué te gustaría practicar hoy?
• 💬 Conversación básica
• 📝 Vocabulario nuevo  
• 🎯 Gramática específica
• 🗣️ Pronunciación
• 🎲 ¡Sorpréndeme con un ejercicio!

¡Dime qué prefieres y empezaremos con ejercicios divertidos!"

REMEMBER: Después de cada explicación o concepto nuevo, SIEMPRE propón un ejercicio para practicar. El aprendizaje es más efectivo cuando es interactivo y práctico.''',

        'translation_simple': "Traduce este texto al {target_lang}. Devuelve solo la traducción, sin explicaciones adicionales: {text}"
    }
    
    # Logging configuration
    LOGGING_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file_enabled': False,
        'file_path': 'logs/app.log'
    }
    
    @classmethod
    def get_window_geometry(cls) -> str:
        """Get window geometry string"""
        config = cls.WINDOW_CONFIG
        return f"{config['width']}x{config['height']}"
    
    @classmethod
    def get_font(cls, size_key: str = 'normal', weight: str = 'normal') -> Tuple[str, int, str]:
        """Get font configuration tuple"""
        size_map = {
            'title': cls.UI_CONFIG['font_size_title'],
            'normal': cls.UI_CONFIG['font_size_normal'],
            'small': cls.UI_CONFIG['font_size_small'],
            'tiny': cls.UI_CONFIG['font_size_tiny']
        }
        
        size = size_map.get(size_key, cls.UI_CONFIG['font_size_normal'])
        return (cls.UI_CONFIG['font_family'], size, weight)
    
    @classmethod
    def get_color_scheme(cls) -> Dict[str, str]:
        """Get complete color scheme"""
        return cls.COLORS.copy()
    
    @classmethod
    def get_ollama_config(cls) -> Dict[str, Any]:
        """Get Ollama service configuration"""
        return cls.OLLAMA_CONFIG.copy()
    
    @classmethod
    def get_model_config(cls) -> Dict[str, Any]:
        """Get model configuration"""
        return cls.MODEL_CONFIG.copy()
    
    @classmethod
    def get_ui_config(cls) -> Dict[str, Any]:
        """Get UI configuration"""
        return cls.UI_CONFIG.copy()
    
    @classmethod
    def get_ai_prompts(cls) -> Dict[str, str]:
        """Get AI system prompts"""
        return cls.AI_PROMPTS.copy()
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration completeness"""
        required_sections = ['WINDOW_CONFIG', 'OLLAMA_CONFIG', 'MODEL_CONFIG', 'UI_CONFIG', 'COLORS', 'AI_PROMPTS']
        
        for section in required_sections:
            if not hasattr(cls, section):
                return False
            
            section_data = getattr(cls, section)
            if not section_data or not isinstance(section_data, dict):
                return False
        
        return True


# Global configuration instance
config = AppConfig()

# Validate configuration on import
if not config.validate_config():
    raise RuntimeError("Invalid configuration detected")