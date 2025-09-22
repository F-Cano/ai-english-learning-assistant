"""
Settings - Configuracion minima
"""
class Settings:
    """Configuracion simple y directa"""
    
    def __init__(self):
        self.app_title = "IA English Assistant"
        self.app_version = "2.0 - Ollama Only"
        self.ollama_url = "http://localhost:11434"
        self.window_width = 1200
        self.window_height = 800
        self.theme = "dark"

# Instancia global
settings = Settings()
