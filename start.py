"""
Iniciador Final - Solo Ollama
"""
import subprocess
import sys
import requests
import time

def check_ollama():
    """Verificar Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        return response.status_code == 200
    except:
        return False

def main():
    print("IA ENGLISH ASSISTANT - VERSION FINAL")
    print("Solo Ollama - Simple y confiable")
    print("=" * 50)
    
    if not check_ollama():
        print("Ollama no esta ejecutandose")
        print("\nPara iniciar Ollama:")
        print("   1. Abre una terminal")
        print("   2. Ejecuta: ollama serve")
        print("   3. Espera a que diga 'Listening on 127.0.0.1:11434'")
        print("\nSi no tienes Ollama: https://ollama.ai")
        input("\nPresiona Enter cuando Ollama este ejecutandose...")
        
        if not check_ollama():
            print("Ollama sigue sin responder")
            print("Asegurate de que este ejecutandose en puerto 11434")
            return
    
    print("Ollama detectado")
    print("Iniciando aplicacion...")
    
    try:
        subprocess.run([sys.executable, "main_final.py"])
    except Exception as e:
        print(f"Error: {e}")
        input("Presiona Enter para cerrar...")

if __name__ == "__main__":
    main()
