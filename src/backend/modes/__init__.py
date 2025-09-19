"""
Conversation Modes - Modos de conversación
"""

try:
    from .conversation_mode import ConversationMode
    from .smart_chat_mode import SmartChatMode
    from .training_mode import TrainingMode
    from .interactive_mode import InteractiveMode
    __all__ = ['ConversationMode', 'SmartChatMode', 'TrainingMode', 'InteractiveMode']
except ImportError:
    __all__ = []
