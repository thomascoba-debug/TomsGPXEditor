#!/usr/bin/env python3
"""
Stable Application Startup with Enhanced Error Handling
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.app_core import initialize_app_core, get_app_core
from config.app_config import AppConfig

def setup_logging():
    """Setup enhanced logging"""
    log_level = AppConfig.get_log_level()
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(AppConfig.LOG_DIR / "app.log", encoding='utf-8')
        ]
    )

def main():
    """Main entry point with enhanced stability"""
    print(f"🚀 Starting {AppConfig.APP_NAME} v{AppConfig.VERSION}")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize application core
        logger.info("Initializing application core...")
        if not initialize_app_core():
            logger.error("Failed to initialize application core")
            return 1
        
        app_core = get_app_core()
        
        # Run maintenance
        logger.info("Running maintenance tasks...")
        app_core.run_maintenance()
        
        # Import and create main application
        logger.info("Creating main application...")
        from app import TomsGPXEditor
        
        # Create app with enhanced error handling
        app = TomsGPXEditor()
        
        # Override properties with stable core
        app.properties = app_core
        
        logger.info("Application started successfully")
        print("✅ Application started successfully!")
        print("📊 Stability features enabled:")
        print("  - Automatic JSON validation")
        print("  - Error handling and recovery")
        print("  - Invalid reference cleanup")
        print("  - Automatic backups")
        print("  - Circular dependency detection")
        print("=" * 50)
        
        # Start main loop
        app.mainloop()
        
        # Cleanup on exit
        app_core.shutdown()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n👋 Application interrupted by user")
        return 0
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n💥 Fatal error: {e}")
        print("Check logs/error.log for details")
        return 1

if __name__ == "__main__":
    sys.exit(main())
