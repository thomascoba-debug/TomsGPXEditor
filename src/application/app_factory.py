"""
Application Factory

Factory for creating and configuring application components with dependency injection.
"""

from typing import Dict, Type, Any, Optional
from dataclasses import dataclass, field
import logging

# Placeholder imports - will be implemented in Phase 2
# from ..domain.services import GPXService, ConversionService, AnalysisService
# from ..domain.repositories import GPXRepository, SettingsRepository
# from ..infrastructure import PropertiesManager, MapRenderer
from .event_bus import EventBus


logger = logging.getLogger(__name__)


@dataclass
class Container:
    """Dependency injection container"""
    
    # Singletons
    _event_bus: Optional[EventBus] = None
    
    # Factories
    _services: Dict[str, Any] = field(default_factory=dict)
    _instances: Dict[str, Any] = field(default_factory=dict)
    
    def event_bus(self) -> EventBus:
        """Get or create event bus"""
        if self._event_bus is None:
            self._event_bus = EventBus()
        return self._event_bus
    
    def gpx_service(self):
        """Get or create GPX service"""
        if 'gpx_service' not in self._services:
            from .services.gpx_service import GPXEditController
            self._services['gpx_service'] = GPXEditController
        return self._services['gpx_service']
    
    def properties_manager(self):
        """Get or create properties manager"""
        if 'properties_manager' not in self._services:
            from ..infrastructure.repositories.properties_repository import AppProperties
            self._services['properties_manager'] = AppProperties()
        return self._services['properties_manager']
    
    def map_renderer(self):
        """Get or create map renderer"""
        if 'map_renderer' not in self._instances:
            from ..infrastructure.map_renderer import GPXCache
            self._instances['map_renderer'] = GPXCache()
        return self._instances['map_renderer']
    
    def conversion_service(self):
        """Get or create conversion service"""
        if 'conversion_service' not in self._services:
            from .services.conversion_service import route_to_track, track_to_route, convert_gpx_file, save_converted_gpx
            self._services['conversion_service'] = {
                'route_to_track': route_to_track,
                'track_to_route': track_to_route,
                'convert_gpx_file': convert_gpx_file,
                'save_converted_gpx': save_converted_gpx
            }
        return self._services['conversion_service']
    
    def analysis_service(self):
        """Get or create analysis service"""
        if 'analysis_service' not in self._services:
            # Placeholder for analysis service
            self._services['analysis_service'] = {
                'analyze_gpx': lambda gpx_data: {'tracks': len(gpx_data.tracks), 'routes': len(gpx_data.routes)}
            }
        return self._services['analysis_service']
    
    # Placeholder methods - will be implemented in Phase 2
    # def gpx_repository(self) -> GPXRepository:
    # def settings_repository(self) -> SettingsRepository:
    # def conversion_service(self) -> ConversionService:
    # def analysis_service(self) -> AnalysisService:


class AppFactory:
    """Factory for creating the complete application"""
    
    def __init__(self):
        self.container = Container()
    
    def create_application(self) -> 'TomsGPXEditor':
        """Create the main application with all dependencies"""
        # Create services
        # gpx_service = self.container.gpx_service()
        # conversion_service = self.container.conversion_service()
        # analysis_service = self.container.analysis_service()
        event_bus = self.container.event_bus()
        
        # Create main window
        # from ..ui.main_window import MainWindow
        # main_window = MainWindow(
        #     gpx_service=gpx_service,
        #     conversion_service=conversion_service,
        #     analysis_service=analysis_service,
        #     event_bus=event_bus,
        #     properties_manager=self.container.properties_manager()
        # )
        
        # return main_window
        return None  # Placeholder for Phase 1


# Global factory instance
_global_factory: Optional[AppFactory] = None


def get_app_factory() -> AppFactory:
    """Get or create global app factory instance"""
    global _global_factory
    if _global_factory is None:
        _global_factory = AppFactory()
    return _global_factory


def get_container() -> Container:
    """Get global container instance"""
    return get_app_factory().container


def get_event_bus() -> EventBus:
    """Get global event bus instance"""
    return get_container().event_bus()
    
    def get_container(self) -> Container:
        """Get the dependency container"""
        return self.container


# Global factory instance
_factory: Optional[AppFactory] = None


def get_app_factory() -> AppFactory:
    """Get the global application factory"""
    global _factory
    if _factory is None:
        _factory = AppFactory()
    return _factory


def set_app_factory(factory: AppFactory) -> None:
    """Set the global application factory (useful for testing)"""
    global _factory
    _factory = factory
