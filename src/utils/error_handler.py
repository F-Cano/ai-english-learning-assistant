"""
Centralized error handling utilities
"""
import logging
import traceback
from typing import Optional, Callable, Any
from functools import wraps

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Manejador centralizado de errores"""
    
    @staticmethod
    def log_error(error: Exception, context: str = "") -> None:
        """
        Registra un error con contexto
        
        Args:
            error: Excepción a registrar
            context: Contexto adicional sobre el error
        """
        error_msg = f"Error in {context}: {str(error)}"
        logger.error(error_msg)
        logger.debug(traceback.format_exc())
    
    @staticmethod
    def handle_service_error(service_name: str, error: Exception, fallback_value: Any = None) -> Any:
        """
        Maneja errores de servicios con fallback
        
        Args:
            service_name: Nombre del servicio que falló
            error: Excepción ocurrida
            fallback_value: Valor de respaldo a retornar
        
        Returns:
            Valor de respaldo
        """
        ErrorHandler.log_error(error, f"{service_name} service")
        print(f"⚠️  Error en {service_name}: {str(error)}")
        return fallback_value
    
    @staticmethod
    def safe_execute(func: Callable, *args, fallback_value: Any = None, context: str = "", **kwargs) -> Any:
        """
        Ejecuta una función de manera segura con manejo de errores
        
        Args:
            func: Función a ejecutar
            *args: Argumentos posicionales
            fallback_value: Valor de respaldo si hay error
            context: Contexto para el logging
            **kwargs: Argumentos con nombre
        
        Returns:
            Resultado de la función o valor de respaldo
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            ErrorHandler.log_error(e, context or func.__name__)
            return fallback_value


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorador para reintentar operaciones que fallan
    
    Args:
        max_retries: Número máximo de reintentos
        delay: Demora entre reintentos en segundos
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                        time.sleep(delay)
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}")
            
            # Si llegamos aquí, todos los intentos fallaron
            raise last_exception
        
        return wrapper
    return decorator


def graceful_shutdown(func: Callable):
    """
    Decorador para manejo graceful de interrupciones
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\n\n⚠️  Aplicación interrumpida por el usuario")
            logger.info("Application interrupted by user")
        except Exception as e:
            ErrorHandler.log_error(e, f"Critical error in {func.__name__}")
            print(f"❌ Error crítico: {e}")
            raise
    
    return wrapper