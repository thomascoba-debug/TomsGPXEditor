"""
Dependency Injection Container for GPX Editor
Provides centralized dependency management
"""

import logging
from typing import Dict, Any, Optional, Type
from typing import TypeVar

T = TypeVar('T')

logger = logging.getLogger(__name__)

class DIContainer:
    """Simple dependency injection container"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, callable] = {}
    
    def register_singleton(self, name: str, instance: Any):
        """Register a singleton instance"""
        self._singletons[name] = instance
        logger.debug(f"Registered singleton: {name}")
    
    def register_factory(self, name: str, factory: callable):
        """Register a factory function"""
        self._factories[name] = factory
        logger.debug(f"Registered factory: {name}")
    
    def register_transient(self, name: str, cls: Type[T]):
        """Register a transient class (new instance each time)"""
        self._services[name] = cls
        logger.debug(f"Registered transient: {name}")
    
    def get(self, name: str) -> Any:
        """Get a service instance"""
        # Check singletons first
        if name in self._singletons:
            return self._singletons[name]
        
        # Check factories
        if name in self._factories:
            return self._factories[name]()
        
        # Check transients
        if name in self._services:
            cls = self._services[name]
            return cls()
        
        raise ValueError(f"Service '{name}' not found in container")
    
    def get_typed(self, name: str, expected_type: Type[T]) -> T:
        """Get a service instance with type checking"""
        instance = self.get(name)
        if not isinstance(instance, expected_type):
            raise TypeError(f"Service '{name}' is not of expected type {expected_type}")
        return instance
    
    def has(self, name: str) -> bool:
        """Check if service is registered"""
        return name in self._singletons or name in self._factories or name in self._services
    
    def clear(self):
        """Clear all registrations"""
        self._services.clear()
        self._singletons.clear()
        self._factories.clear()
        logger.debug("Container cleared")

# Global container instance
_container: Optional[DIContainer] = None

def get_container() -> DIContainer:
    """Get the global container instance"""
    global _container
    if _container is None:
        _container = DIContainer()
    return _container

def configure_container(app_instance=None):
    """Configure the dependency injection container"""
    container = get_container()
    
    # Clear previous configuration
    container.clear()
    
    # Register app instance if provided
    if app_instance:
        container.register_singleton("app", app_instance)
    
    # Register core services
    try:
        from src.infrastructure.state_manager import get_state_manager
        container.register_factory("state_manager", get_state_manager)
    except ImportError:
        logger.warning("State manager not available")
    
    try:
        from src.infrastructure.resource_manager import get_resource_manager
        container.register_factory("resource_manager", get_resource_manager)
    except ImportError:
        logger.warning("Resource manager not available")
    
    try:
        from src.infrastructure.shutdown_manager import get_shutdown_manager
        container.register_factory("shutdown_manager", get_shutdown_manager)
    except ImportError:
        logger.warning("Shutdown manager not available")
    
    logger.info("DI Container configured")
