"""
Simple Settings para Ollama
"""
from pathlib import Path

class SimpleSettings:
    def __init__(self):
        self.working_dir = Path.cwd()
        self.audio_file = "temp.wav"
        self.ollama_url = "http://localhost:11434"
        self.preferred_model = "mistral"
        
    def validate(self):
        return True

settings = SimpleSettings()
