"""
Setup script for IA English Assistant
Optional - helps with initial setup validation
"""
import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    if version < (3, 8):
        print(f"Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    
    print(f"Python version: {version.major}.{version.minor}.{version.micro} ✓")
    return True


def check_ollama_installation():
    """Check if Ollama is installed and accessible"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"Ollama installed: {result.stdout.strip()} ✓")
            return True
        else:
            print("Ollama not found or not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("Ollama not found in PATH")
        return False


def check_ollama_running():
    """Check if Ollama service is running"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"Ollama running with {len(models)} models ✓")
            if models:
                print("Available models:")
                for model in models[:5]:  # Show first 5 models
                    print(f"  - {model.get('name', 'Unknown')}")
            return True
        else:
            print("Ollama service not responding properly")
            return False
    except Exception as e:
        print(f"Cannot connect to Ollama service: {e}")
        return False


def install_dependencies():
    """Install required dependencies"""
    try:
        print("Installing dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("Dependencies installed ✓")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False


def create_structure():
    """Create any missing directories"""
    directories = ['logs', 'tests']
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(exist_ok=True)
            print(f"Created directory: {directory}")


def main():
    """Main setup function"""
    print("=" * 50)
    print("IA ENGLISH ASSISTANT")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Install dependencies
    if not install_dependencies():
        success = False
    
    # Create structure
    create_structure()
    
    # Check Ollama
    print("\nChecking Ollama...")
    if not check_ollama_installation():
        print("  Ollama not found. Please install from https://ollama.ai")
        success = False
    elif not check_ollama_running():
        print("  Ollama not running. Start with: ollama serve")
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print(" Setup completed successfully!")
        print("You can now run: python main.py")
    else:
        print(" Setup completed with warnings")
        print("Please resolve the issues above before running the application")
    print("=" * 50)


if __name__ == "__main__":
    main()