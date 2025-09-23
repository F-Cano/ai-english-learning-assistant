"""
UI constants and messages
"""

class UIMessages:
    """UI text messages and constants"""
    
    # Welcome messages
    WELCOME_TITLE = "¡Bienvenido a IA English Assistant!"
    WELCOME_DESCRIPTION = """¡Hola! Soy Alex, tu profesor personal de inglés interactivo.

🎯 Aprende con ejercicios personalizados:
• Práctica vocabulario con ejercicios
• Corrige gramática paso a paso  
• Mejora pronunciación con guías
• Evalúa tu progreso en tiempo real

💡 ¿Sabías que? Aprendes mejor cuando practicas activamente.
¡Empecemos con ejercicios divertidos!

¿Qué área quieres practicar hoy?"""
    
    # Status messages - mantener en español
    STATUS_INITIALIZING = "Inicializando..."
    STATUS_CONNECTING = "Conectando..."
    STATUS_ONLINE = "Conectado"
    STATUS_OFFLINE = "Desconectado"
    STATUS_ERROR = "Error"
    STATUS_DISCONNECTED = "Desconectado"
    
    # Button texts
    BUTTON_SEND = "Enviar"
    BUTTON_SENDING = "Enviando..."
    BUTTON_TRANSLATE = "Traducir"
    BUTTON_TRANSLATING = "Traduciendo..."
    
    # Error messages
    ERROR_NO_MESSAGE = "Por favor ingresa un mensaje"
    ERROR_CONNECTION = "Error de conexión"
    ERROR_TRANSLATION_FAILED = "Falló la traducción"
    ERROR_NO_RESPONSE_TO_TRANSLATE = "No hay respuesta para traducir"
    
    # Footer messages
    FOOTER_HELP = "Ctrl+Enter para enviar"
    FOOTER_OLLAMA_LINK = "Obtener Ollama"
    
    # Placeholders
    PLACEHOLDER_MESSAGE = "Escribe tu mensaje aquí..."


class UIConstants:
    """UI layout and behavior constants"""
    
    # Animation delays
    ANIMATION_DELAY = 100
    
    # Auto-scroll settings
    AUTO_SCROLL_DELAY = 50
    
    # Message limits
    MAX_MESSAGE_LENGTH = 1000
    MAX_HISTORY_DISPLAY = 100
    
    # Timeouts for UI updates
    UI_UPDATE_TIMEOUT = 5000  # 5 seconds