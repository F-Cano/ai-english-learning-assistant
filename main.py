"""
Entry point for IA English Assistant - SIMPLE VERSION
"""
import sys
import logging
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from core.logging_setup import setup_logging
from config import validate_environment, is_environment_valid


def main():
    """Main entry point"""
    logger = None
    
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger('main')
        logger.info("Starting IA English Assistant")
        
        # Validate environment
        if not is_environment_valid():
            issues = validate_environment()
            logger.error(f"Environment validation failed: {issues}")
            print(f"Environment issues: {issues}")
            return 1
        
        logger.info("Environment validation passed")
        
        # Import and start simple app
        from ui.simple_app import SimpleEnglishAssistantApp
        
        app = SimpleEnglishAssistantApp()
        app.run()
        
        return 0
        
    except KeyboardInterrupt:
        if logger:
            logger.info("Application interrupted by user")
        print("\nApplication interrupted by user")
        return 0
        
    except Exception as e:
        if logger:
            logger.error(f"Fatal application error: {e}")
            logger.error(f"Traceback: {e}", exc_info=True)
        
        print(f"Fatal error: {e}")
        print("Check the logs for more details")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)