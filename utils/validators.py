"""
Validation utilities
"""
from typing import Any, Dict


def validate_message(message: str) -> bool:
    """Validate message content"""
    if not isinstance(message, str):
        return False
    
    if not message.strip():
        return False
    
    if len(message.strip()) > 1000:  # Max message length
        return False
    
    return True


def validate_url(url: str) -> bool:
    """Validate URL format"""
    if not isinstance(url, str):
        return False
    
    if not url.startswith(('http://', 'https://')):
        return False
    
    return True


def validate_config_section(section: Dict[str, Any], required_keys: list) -> bool:
    """Validate configuration section"""
    if not isinstance(section, dict):
        return False
    
    for key in required_keys:
        if key not in section:
            return False
    
    return True


def validate_model_name(model_name: str) -> bool:
    """Validate model name format"""
    if not isinstance(model_name, str):
        return False
    
    if not model_name.strip():
        return False
    
    # Basic validation - can be extended
    return True