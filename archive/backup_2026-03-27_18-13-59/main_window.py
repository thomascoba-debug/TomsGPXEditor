"""
Main Window

Main application window implementing MVP pattern with dependency injection.
"""

import logging
from typing import Optional

from ..application import EventBus, AppFactory
from ..infrastructure import AppProperties
from .presenters.main_window_presenter import MainWindowPresenter
from .views.main_window_view_impl import MainWindowViewImpl

logger = logging.getLogger(__name__)


class MainWindow:
    """Main application window with MVP pattern and dependency injection"""
    
    def __init__(self, event_bus: Optional[EventBus] = None, 
                 properties: Optional[AppProperties] = None):
        """Initialize main window with dependencies"""
        
        # Use dependency injection if provided, otherwise use global factory
        if event_bus is None:
            event_bus = AppFactory.get_event_bus()
        if properties is None:
            properties = AppFactory.get_container().properties_manager()
        
        self.event_bus = event_bus
        self.properties = properties
        
        # Setup MVP components
        self.view = MainWindowViewImpl()
        self.presenter = MainWindowPresenter(event_bus, properties)
        
        # Connect MVP
        self.view.set_presenter(self.presenter)
        self.presenter.set_view(self.view)
        
        # Load saved geometry
        self._load_geometry()
        
        logger.info("MainWindow initialized with MVP pattern")
    
    def _load_geometry(self):
        """Load saved window geometry"""
        try:
            geometry = self.properties.get("main_window_geometry")
            if geometry:
                self.view.set_geometry(geometry)
                logger.info(f"Loaded window geometry: {geometry}")
        except Exception as e:
            logger.error(f"Error loading window geometry: {e}")
    
    def _save_geometry(self):
        """Save window geometry"""
        try:
            geometry = self.view.get_geometry()
            if geometry:
                self.properties.set("main_window_geometry", geometry)
                self.properties.save()
                logger.info(f"Saved window geometry: {geometry}")
        except Exception as e:
            logger.error(f"Error saving window geometry: {e}")
    
    def show(self):
        """Show the main window"""
        self.view.show()
        logger.info("MainWindow shown")
    
    def hide(self):
        """Hide the main window"""
        self.view.hide()
        logger.info("MainWindow hidden")
    
    def destroy(self):
        """Destroy the main window"""
        self._save_geometry()
        self.view.destroy()
        logger.info("MainWindow destroyed")
    
    def get_view(self):
        """Get the view component"""
        return self.view
    
    def get_presenter(self):
        """Get the presenter component"""
        return self.presenter
    
    def get_event_bus(self):
        """Get the event bus"""
        return self.event_bus
    
    def get_properties(self):
        """Get the properties manager"""
        return self.properties
