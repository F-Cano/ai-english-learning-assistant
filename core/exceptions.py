"""
Custom exceptions for the application
"""


class IAAssistantException(Exception):
    """Base exception for IA Assistant application"""
    pass


class ConfigurationError(IAAssistantException):
    """Configuration related errors"""
    pass


class OllamaConnectionError(IAAssistantException):
    """Ollama service connection errors"""
    pass


class OllamaTimeoutError(IAAssistantException):
    """Ollama service timeout errors"""
    pass


class ModelNotFoundError(IAAssistantException):
    """Model not available error"""
    pass


class TranslationError(IAAssistantException):
    """Translation service errors"""
    pass


class ValidationError(IAAssistantException):
    """Data validation errors"""
    pass


class UIError(IAAssistantException):
    """UI related errors"""
    pass


class StateError(IAAssistantException):
    """Application state errors"""
    pass