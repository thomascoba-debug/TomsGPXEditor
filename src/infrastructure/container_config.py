"""
Container Configuration
Central setup for dependency injection container
"""

import logging
from typing import Callable

from .di_container import DIContainer
from ..infrastructure.repositories.properties_repository import AppProperties

logger = logging.getLogger(__name__)


class ContainerConfig:
    """Configuration for dependency injection container"""
    
    def __init__(self, container: DIContainer):
        self.container = container
    
    def configure_core_services(self, app_instance):
        """Configure core application services"""
        # Register app instance as singleton
        self.container.register_singleton('app', app_instance)
        
        # Register properties
        properties = AppProperties()
        self.container.register_singleton('properties', properties)
        
        logger.debug("Core services configured")
    
    def configure_ui_components(self, app_instance):
        """Configure UI components"""
        # UI components will be registered after UI is built
        # This method is called from _build_ui after map widget is created
        if hasattr(app_instance, 'map_widget'):
            self.container.register_singleton('map_widget', app_instance.map_widget)
        if hasattr(app_instance, 'main_grid'):
            self.container.register_singleton('main_grid', app_instance.main_grid)
        
        logger.debug("UI components configured")
    
    def configure_callbacks(self, app_instance):
        """Configure callback functions"""
        # Register callback functions
        self.container.register_singleton('button_update_callback', app_instance._update_conversion_buttons)
        self.container.register_singleton('editable_update_callback', app_instance._update_editable_buttons_only)
        self.container.register_singleton('map_update_callback', app_instance._update_map)
        self.container.register_singleton('visibility_update_callback', app_instance._update_visibility_only)
        
        logger.debug("Callbacks configured")
    
    def configure_controllers(self, app_instance):
        """Configure business logic controllers"""
        # Register controllers as factories to create instances with dependencies
        def create_gpx_file_manager():
            from ..application.gpx_file_manager import GPXFileManager
            return GPXFileManager(
                properties=self.container.get('properties'),
                map_widget=self.container.get('map_widget'),
                main_grid=self.container.get('main_grid'),
                button_update_callback=self.container.get('button_update_callback'),
                editable_update_callback=self.container.get('editable_update_callback')
            )
        
        def create_map_controller():
            from ..application.map_controller import MapController
            return MapController(
                map_widget=self.container.get('map_widget'),
                properties=self.container.get('properties')
            )
        
        def create_dialog_controller():
            from ..application.dialog_controller import DialogController
            return DialogController(
                parent=self.container.get('app'),
                properties=self.container.get('properties'),
                save_callback=app_instance._save_properties
            )
        
        # Register as factories (new instance each time)
        self.container.register_factory('gpx_file_manager', create_gpx_file_manager)
        self.container.register_factory('map_controller', create_map_controller)
        self.container.register_factory('dialog_controller', create_dialog_controller)
        
        logger.debug("Controllers configured")
    
    def configure_services(self):
        """Configure application services"""
        # Register service factories
        def create_recent_files_manager():
            from ..application.services.recent_files_service import RecentFilesFromSessionManager
            return RecentFilesFromSessionManager(
                properties=self.container.get('properties'),
                max_files=10
            )
        
        def create_gpx_service():
            from ..application.services.gpx_service import GPXEditController
            return GPXEditController(self.container.get('app'))
        
        self.container.register_factory('recent_files_manager', create_recent_files_manager)
        self.container.register_factory('gpx_service', create_gpx_service)
        
        logger.debug("Services configured")
    
    def configure_all(self, app_instance):
        """Configure all dependencies"""
        self.configure_core_services(app_instance)
        self.configure_callbacks(app_instance)
        self.configure_controllers(app_instance)
        self.configure_services()
        # UI components will be configured later after UI is built
        
        logger.info("Container configuration completed (UI components pending)")
    
    def configure_ui_components_after_build(self, app_instance):
        """Configure UI components after UI is built"""
        self.configure_ui_components(app_instance)
        logger.debug("UI components configured after UI build")


def configure_container(app_instance) -> DIContainer:
    """Create and configure the dependency injection container"""
    container = DIContainer()
    config = ContainerConfig(container)
    config.configure_all(app_instance)
    return container
