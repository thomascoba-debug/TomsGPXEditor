"""
Tests for Application Factory

Unit tests for dependency injection container and app factory.
"""

import pytest
from unittest.mock import Mock, patch

from .app_factory import Container, AppFactory
from .event_bus import EventBus, set_event_bus


class TestContainer:
    """Test dependency injection container"""
    
    def setup_method(self):
        """Setup for each test"""
        self.container = Container()
    
    def test_event_bus_singleton(self):
        """Test that event bus is singleton"""
        bus1 = self.container.event_bus()
        bus2 = self.container.event_bus()
        
        assert bus1 is bus2
        assert isinstance(bus1, EventBus)
    
    def test_services_are_created_once(self):
        """Test that services are created only once"""
        service1 = self.container.gpx_service()
        service2 = self.container.gpx_service()
        
        assert service1 is service2
    
    def test_different_services_are_different(self):
        """Test that different services are different instances"""
        gpx_service = self.container.gpx_service()
        conversion_service = self.container.conversion_service()
        analysis_service = self.container.analysis_service()
        
        assert gpx_service is not conversion_service
        assert gpx_service is not analysis_service
        assert conversion_service is not analysis_service
    
    @patch('src.infrastructure.PropertiesManager')
    def test_properties_manager_creation(self, mock_properties):
        """Test properties manager creation"""
        mock_properties.return_value = Mock()
        
        props = self.container.properties_manager()
        
        mock_properties.assert_called_once()
        assert props is mock_properties.return_value
    
    def test_map_renderer_is_instance(self):
        """Test map renderer creation"""
        with patch('src.infrastructure.PropertiesManager'):
            renderer = self.container.map_renderer()
            # Should be a real instance (not mocked)
            assert renderer is not None


class TestAppFactory:
    """Test application factory"""
    
    def setup_method(self):
        """Setup for each test"""
        # Clear global event bus
        set_event_bus(None)
        self.factory = AppFactory()
    
    def test_get_container(self):
        """Test getting container from factory"""
        container = self.factory.get_container()
        
        assert isinstance(container, Container)
        assert container is self.factory.container
    
    def test_create_application(self):
        """Test application creation"""
        with patch('src.infrastructure.PropertiesManager'), \
             patch('src.domain.repositories.GPXFileRepository'), \
             patch('src.domain.repositories.SettingsFileRepository'), \
             patch('src.ui.main_window.MainWindow') as mock_main_window:
            
            app = self.factory.create_application()
            
            mock_main_window.assert_called_once()
            assert app is mock_main_window.return_value
    
    def test_dependencies_injected(self):
        """Test that dependencies are properly injected"""
        with patch('src.infrastructure.PropertiesManager'), \
             patch('src.domain.repositories.GPXFileRepository'), \
             patch('src.domain.repositories.SettingsFileRepository'), \
             patch('src.ui.main_window.MainWindow') as mock_main_window:
            
            self.factory.create_application()
            
            # Check that MainWindow was called with dependencies
            call_args = mock_main_window.call_args
            assert call_args is not None
            
            kwargs = call_args.kwargs
            assert 'gpx_service' in kwargs
            assert 'conversion_service' in kwargs
            assert 'analysis_service' in kwargs
            assert 'event_bus' in kwargs
            assert 'properties_manager' in kwargs


class TestGlobalFactory:
    """Test global factory functions"""
    
    def test_get_app_factory_creates_instance(self):
        """Test that get_app_factory creates instance"""
        from .app_factory import get_app_factory, set_app_factory
        
        # Clear global instance
        set_app_factory(None)
        
        factory = get_app_factory()
        assert isinstance(factory, AppFactory)
        
        # Should return same instance
        factory2 = get_app_factory()
        assert factory is factory2
    
    def test_set_app_factory(self):
        """Test setting global app factory"""
        from .app_factory import get_app_factory, set_app_factory
        
        custom_factory = AppFactory()
        set_app_factory(custom_factory)
        
        retrieved_factory = get_app_factory()
        assert retrieved_factory is custom_factory


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
