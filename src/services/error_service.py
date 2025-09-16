import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
from ..interfaces.base import IErrorTracker
import logging

logger = logging.getLogger(__name__)

class ErrorMemoryService(IErrorTracker):
    def __init__(self, errors_file_path: Path):
        self.errors_file = errors_file_path
        self.errors_memory = self._load_errors()
    
    def _load_errors(self) -> Dict[str, Any]:
        """Carga errores desde archivo"""
        try:
            if self.errors_file.exists():
                with open(self.errors_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading errors: {e}")
            return {}
    
    def _save_errors(self) -> None:
        """Guarda errores en archivo"""
        try:
            with open(self.errors_file, "w", encoding="utf-8") as f:
                json.dump(self.errors_memory, f, ensure_ascii=False, indent=4)
            logger.info("Errors saved successfully")
        except Exception as e:
            logger.error(f"Error saving errors: {e}")
    
    def register_error(self, original: str, correction: str) -> None:
        """Registra un error gramatical"""
        key = correction.lower()
        if key not in self.errors_memory:
            self.errors_memory[key] = {
                "veces": 0,
                "ultima_fecha": None,
                "originales": []
            }
        
        self.errors_memory[key]["veces"] += 1
        self.errors_memory[key]["ultima_fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.errors_memory[key]["originales"].append(original)
        self._save_errors()
        logger.info(f"Error registered: {original} -> {correction}")
    
    def get_frequent_errors(self, threshold: int = 3) -> Dict[str, Any]:
        """Obtiene errores frecuentes"""
        return {
            correction: data 
            for correction, data in self.errors_memory.items() 
            if data["veces"] >= threshold
        }
    
    def check_improvement(self, text: str) -> bool:
        """Verifica si el usuario mejoró un error previo"""
        for correction, data in self.errors_memory.items():
            if text.lower() == correction and data["veces"] > 0:
                data["veces"] -= 1
                self._save_errors()
                return True
        return False
    
    def get_session_summary(self) -> Dict[str, int]:
        """Genera resumen de errores de la sesión"""
        frequent_errors = len([e for e in self.errors_memory.values() if e["veces"] >= 3])
        occasional_errors = len([e for e in self.errors_memory.values() if 0 < e["veces"] < 3])
        
        return {
            "frequent": frequent_errors,
            "occasional": occasional_errors,
            "total": len(self.errors_memory)
        }