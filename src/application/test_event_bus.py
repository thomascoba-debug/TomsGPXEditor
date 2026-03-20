"""
Tests for Event Bus

Unit tests for the EventBus and event system.
"""

import pytest
from unittest.mock import Mock, AsyncMock
import asyncio

from .event_bus import (
    EventBus, Event, FileLoadedEvent, FileEditableChangedEvent,
    get_event_bus, set_event_bus
)


class TestEventBus:
    """Test EventBus functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        self.event_bus = EventBus()
    
    def test_subscribe_and_publish_sync(self):
        """Test synchronous event subscription and publishing"""
        handler = Mock()
        
        self.event_bus.subscribe(FileLoadedEvent, handler)
        event = FileLoadedEvent("/test/file.gpx", Mock())
        
        self.event_bus.publish(event)
        
        handler.assert_called_once_with(event)
    
    def test_subscribe_and_publish_async(self):
        """Test asynchronous event subscription and publishing"""
        handler = AsyncMock()
        
        self.event_bus.subscribe_async(FileLoadedEvent, handler)
        event = FileLoadedEvent("/test/file.gpx", Mock())
        
        # Run the async event processing
        asyncio.run(self.event_bus._publish_async(FileLoadedEvent, event))
        
        handler.assert_called_once_with(event)
    
    def test_multiple_handlers(self):
        """Test multiple handlers for same event"""
        handler1 = Mock()
        handler2 = Mock()
        handler3 = Mock()
        
        self.event_bus.subscribe(FileLoadedEvent, handler1)
        self.event_bus.subscribe(FileLoadedEvent, handler2)
        self.event_bus.subscribe_async(FileLoadedEvent, handler3)
        
        event = FileLoadedEvent("/test/file.gpx", Mock())
        self.event_bus.publish(event)
        
        # Run async processing
        asyncio.run(self.event_bus._publish_async(FileLoadedEvent, event))
        
        handler1.assert_called_once_with(event)
        handler2.assert_called_once_with(event)
        handler3.assert_called_once_with(event)
    
    def test_unsubscribe(self):
        """Test event unsubscription"""
        handler = Mock()
        
        self.event_bus.subscribe(FileLoadedEvent, handler)
        self.event_bus.unsubscribe(FileLoadedEvent, handler)
        
        event = FileLoadedEvent("/test/file.gpx", Mock())
        self.event_bus.publish(event)
        
        handler.assert_not_called()
    
    def test_handler_exception(self):
        """Test handling of exceptions in event handlers"""
        def failing_handler(event):
            raise ValueError("Test error")
        
        def working_handler(event):
            working_handler.called = True
        
        working_handler.called = False
        
        self.event_bus.subscribe(FileLoadedEvent, failing_handler)
        self.event_bus.subscribe(FileLoadedEvent, working_handler)
        
        event = FileLoadedEvent("/test/file.gpx", Mock())
        
        # Should not raise exception
        self.event_bus.publish(event)
        
        # Working handler should still be called
        assert working_handler.called is True
    
    def test_different_event_types(self):
        """Test different event types"""
        file_handler = Mock()
        editable_handler = Mock()
        
        self.event_bus.subscribe(FileLoadedEvent, file_handler)
        self.event_bus.subscribe(FileEditableChangedEvent, editable_handler)
        
        file_event = FileLoadedEvent("/test/file.gpx", Mock())
        editable_event = FileEditableChangedEvent("/test/file.gpx", True)
        
        self.event_bus.publish(file_event)
        self.event_bus.publish(editable_event)
        
        file_handler.assert_called_once_with(file_event)
        editable_handler.assert_called_once_with(editable_event)
    
    def test_get_listener_count(self):
        """Test getting listener count for event type"""
        handler1 = Mock()
        handler2 = Mock()
        
        self.event_bus.subscribe(FileLoadedEvent, handler1)
        self.event_bus.subscribe(FileLoadedEvent, handler2)
        self.event_bus.subscribe_async(FileLoadedEvent, Mock())
        
        count = self.event_bus.get_listener_count(FileLoadedEvent)
        assert count == 3
    
    def test_clear_listeners(self):
        """Test clearing all listeners"""
        handler = Mock()
        
        self.event_bus.subscribe(FileLoadedEvent, handler)
        self.event_bus.subscribe(FileEditableChangedEvent, handler)
        
        assert self.event_bus.get_listener_count(FileLoadedEvent) == 1
        assert self.event_bus.get_listener_count(FileEditableChangedEvent) == 1
        
        self.event_bus.clear_listeners()
        
        assert self.event_bus.get_listener_count(FileLoadedEvent) == 0
        assert self.event_bus.get_listener_count(FileEditableChangedEvent) == 0


class TestGlobalEventBus:
    """Test global event bus functions"""
    
    def test_get_event_bus_creates_instance(self):
        """Test that get_event_bus creates instance"""
        # Clear global instance
        set_event_bus(None)
        
        event_bus = get_event_bus()
        assert isinstance(event_bus, EventBus)
        
        # Should return same instance
        event_bus2 = get_event_bus()
        assert event_bus is event_bus2
    
    def test_set_event_bus(self):
        """Test setting global event bus"""
        custom_bus = EventBus()
        set_event_bus(custom_bus)
        
        retrieved_bus = get_event_bus()
        assert retrieved_bus is custom_bus


class TestEventTypes:
    """Test event type definitions"""
    
    def test_file_loaded_event(self):
        """Test FileLoadedEvent creation"""
        gpx_file = Mock()
        event = FileLoadedEvent("/test/file.gpx", gpx_file)
        
        assert event.file_path == "/test/file.gpx"
        assert event.gpx_file is gpx_file
    
    def test_file_editable_changed_event(self):
        """Test FileEditableChangedEvent creation"""
        event = FileEditableChangedEvent("/test/file.gpx", True)
        
        assert event.file_path == "/test/file.gpx"
        assert event.is_editable is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
