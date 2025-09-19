"""
Custom Exceptions - Excepciones personalizadas de la aplicación
"""

class LanguageAssistantException(Exception):
    """"""Excepción base para la aplicación""""""
    pass

class ServiceException(LanguageAssistantException):
    """"""Excepción para errores en servicios""""""
    pass

class UIException(LanguageAssistantException):
    """"""Excepción para errores en la interfaz""""""
    pass

class ConfigurationException(LanguageAssistantException):
    """"""Excepción para errores de configuración""""""
    pass

class DataException(LanguageAssistantException):
    """"""Excepción para errores de datos""""""
    pass
