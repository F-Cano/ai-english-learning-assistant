import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class AudioConfig:
    sample_rate: int = 16000
    silence_threshold: float = 0.01
    silence_duration: float = 1.2
    audio_file: str = "salida.mp3"

@dataclass
class ModelConfig:
    whisper_model: str = "base"
    chat_model: str = "microsoft/DialoGPT-medium"
    grammar_model: str = "prithivida/grammar_error_correcter_v1"
    translator_en_model: str = "Helsinki-NLP/opus-mt-es-en"
    translator_es_model: str = "Helsinki-NLP/opus-mt-en-es"

@dataclass
class PathConfig:
    working_dir: Path = Path.cwd()  # Use current working directory instead of hardcoded Windows path
    errors_file: str = "errores_memoria.json"
    logs_dir: Path = Path("logs")
    models_cache_dir: Optional[Path] = None

class Settings:
    def __init__(self):
        self.audio = AudioConfig()
        self.models = ModelConfig()
        self.paths = PathConfig()
        
    def validate(self) -> bool:
        """Valida la configuración"""
        if not self.paths.working_dir.exists():
            self.paths.working_dir.mkdir(parents=True, exist_ok=True)
        if not self.paths.logs_dir.exists():
            self.paths.logs_dir.mkdir(parents=True, exist_ok=True)
        return True