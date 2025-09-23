"""
IA English Assistant - Main Application Entry Point
Modular architecture with complete separation of concerns
"""
import sys
import os
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from ui.app import EnglishAssistantApp
    from utils.logger import setup_logger
    from config import config
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all modules are properly installed and accessible")
    sys.exit(1)


def validate_environment():
    """Validate that the environment is properly set up"""
    errors = []
    
    # Check if configuration is valid
    try:
        if not config.validate_config():
            errors.append("Invalid configuration detected")
    except Exception as e:
        errors.append(f"Configuration error: {e}")
    
    # Check required directories exist
    required_dirs = ['core', 'models', 'services', 'ui', 'utils']
    for directory in required_dirs:
        if not (project_root / directory).exists():
            errors.append(f"Missing required directory: {directory}")
    
    # Check critical files exist
    critical_files = [
        'config.py',
        'core/events.py',
        'core/state.py',
        'services/chat_service.py',
        'ui/app.py'
    ]
    
    for file_path in critical_files:
        if not (project_root / file_path).exists():
            errors.append(f"Missing critical file: {file_path}")
    
    return errors


def show_startup_info():
    """Show application startup information"""
    print("=" * 60)
    print("IA ENGLISH ASSISTANT")
    print("=" * 60)
    print("Modular Architecture")
    print("- Event-driven communication")
    print("- Centralized state management") 
    print("- Independent service modules")
    print("- Reactive UI components")
    print("-" * 60)
    print("Features:")
    print("- Natural English conversation")
    print("- Smart translation with multiple models")
    print("- Real-time connection monitoring")
    print("- Session metrics and history")
    print("=" * 60)
    print()


def main():
    """Main application entry point"""
    
    # Show startup information
    show_startup_info()
    
    # Setup logging
    logger = setup_logger('main')
    logger.info("Starting IA English Assistant...")
    
    # Validate environment
    logger.info("Validating environment...")
    validation_errors = validate_environment()
    
    if validation_errors:
        logger.error("Environment validation failed:")
        for error in validation_errors:
            logger.error(f"  - {error}")
        
        print("\nEnvironment validation failed. Please check the following:")
        for error in validation_errors:
            print(f"  - {error}")
        
        input("\nPress Enter to exit...")
        return 1
    
    logger.info("Environment validation passed")
    
    # Create and run application
    try:
        logger.info("Initializing application...")
        app = EnglishAssistantApp()
        
        logger.info("Starting application...")
        app.run()
        
        logger.info("Application finished normally")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user (Ctrl+C)")
        print("\nApplication interrupted by user")
        return 0
        
    except Exception as e:
        logger.error(f"Fatal application error: {e}", exc_info=True)
        print(f"\nFatal error: {e}")
        print("Check the logs for more details")
        
        input("\nPress Enter to exit...")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"Critical startup error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)