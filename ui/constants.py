"""
UI constants and messages
"""

class UIMessages:
    """UI text messages and constants"""
    
    # Welcome messages
    WELCOME_TITLE = "Welcome to IA English Assistant!"
    WELCOME_DESCRIPTION = """
    Event-driven architecture
    Smart translation with multiple retries
    Centralized application state
    
    Let's practice English together!
    """
    
    # Status messages
    STATUS_INITIALIZING = "Initializing..."
    STATUS_CONNECTING = "Connecting..."
    STATUS_ONLINE = "Online"
    STATUS_OFFLINE = "Offline"
    STATUS_ERROR = "Error"
    STATUS_DISCONNECTED = "Disconnected"
    
    # Button texts
    BUTTON_SEND = "Send"
    BUTTON_SENDING = "Sending..."
    BUTTON_TRANSLATE = "Translate"
    BUTTON_TRANSLATING = "Translating..."
    
    # Error messages
    ERROR_NO_MESSAGE = "Please enter a message"
    ERROR_CONNECTION = "Connection error"
    ERROR_TRANSLATION_FAILED = "Translation failed"
    ERROR_NO_RESPONSE_TO_TRANSLATE = "No response to translate"
    
    # Footer messages
    FOOTER_HELP = "Ctrl+Enter to send"
    FOOTER_OLLAMA_LINK = "Get Ollama"
    
    # Placeholders
    PLACEHOLDER_MESSAGE = "Type your message here..."


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