"""
File Utilities - Utilidades para manejo de archivos
"""

import os
import json
from typing import Dict, Any, Optional

def ensure_directory(path: str) -> str:
    """"""Asegura que un directorio existe""""""
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def load_json(file_path: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """"""Carga un archivo JSON""""""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    return default or {}

def save_json(data: Dict[str, Any], file_path: str) -> bool:
    """"""Guarda datos en un archivo JSON""""""
    try:
        ensure_directory(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except (IOError, TypeError):
        return False
