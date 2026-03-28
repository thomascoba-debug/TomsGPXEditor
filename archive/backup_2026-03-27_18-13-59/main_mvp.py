"""
Main Entry Point for MVP Architecture

Uses the new MainWindow with MVP pattern.
"""

import logging
from src.ui.main_window import MainWindow
from src.application.app_factory import AppFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main entry point using MVP architecture"""
    
    # Create application using factory
    factory = AppFactory()
    event_bus = factory.container.event_bus()
    properties = factory.container.properties_manager()
    
    # Create main window with MVP pattern
    main_window = MainWindow(event_bus, properties)
    
    # Show and run the application
    main_window.show()
    
    # Start the tkinter main loop
    main_window.get_view().root.mainloop()
    
    # Cleanup
    main_window.destroy()

if __name__ == "__main__":
    main()
