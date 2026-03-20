"""
Event Bus

Central event system for decoupled communication between components.
"""

from dataclasses import dataclass
from typing import Dict, List, Callable, Type, Any
from collections import defaultdict
import asyncio
import inspect
import logging

logger = logging.getLogger(__name__)


class Event:
    """Base event class"""
    pass


@dataclass
class FileLoadedEvent(Event):
    """Event fired when a GPX file is loaded"""
    file_path: str
    gpx_file: 'GPXFile'


@dataclass
class FileRemovedEvent(Event):
    """Event fired when a GPX file is removed"""
    file_path: str


@dataclass
class FileEditableChangedEvent(Event):
    """Event fired when file editable status changes"""
    file_path: str
    is_editable: bool


@dataclass
class FileVisibleChangedEvent(Event):
    """Event fired when file visible status changes"""
    file_path: str
    is_visible: bool


@dataclass
class FileColorChangedEvent(Event):
    """Event fired when file color changes"""
    file_path: str
    color: str


@dataclass
class ConversionCompletedEvent(Event):
    """Event fired when conversion is completed"""
    conversion_type: str  # 'route_to_track' or 'track_to_route'
    source_file: str
    target_file: str
    success: bool
    message: str


class EventBus:
    """Central event bus for application-wide communication"""
    
    def __init__(self):
        self._listeners: Dict[Type[Event], List[Callable]] = defaultdict(list)
        self._async_listeners: Dict[Type[Event], List[Callable]] = defaultdict(list)
    
    def subscribe(self, event_type: Type[Event], handler: Callable[[Event], None]) -> None:
        """Subscribe to synchronous events"""
        self._listeners[event_type].append(handler)
        event_name = event_type.__name__ if hasattr(event_type, '__name__') else str(event_type)
        logger.debug(f"Subscribed handler for {event_name}")
    
    def subscribe_async(self, event_type: Type[Event], 
                     handler: Callable[[Event], None]) -> None:
        """Subscribe to asynchronous events"""
        self._async_listeners[event_type].append(handler)
        event_name = event_type.__name__ if hasattr(event_type, '__name__') else str(event_type)
        logger.debug(f"Subscribed async handler for {event_name}")
    
    def unsubscribe(self, event_type: Type[Event], 
                  handler: Callable[[Event], None]) -> None:
        """Unsubscribe from events"""
        event_name = event_type.__name__ if hasattr(event_type, '__name__') else str(event_type)
        
        if handler in self._listeners[event_type]:
            self._listeners[event_type].remove(handler)
            logger.debug(f"Unsubscribed handler for {event_name}")
            
        if handler in self._async_listeners[event_type]:
            self._async_listeners[event_type].remove(handler)
            logger.debug(f"Unsubscribed async handler for {event_name}")
    
    def publish(self, event: Event) -> None:
        """Publish event to all subscribers"""
        event_type = type(event)
        
        # Synchronous handlers
        for handler in self._listeners[event_type]:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in event handler for {event_type.__name__}: {e}")
        
        # Asynchronous handlers
        if self._async_listeners[event_type]:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self._publish_async(event_type, event))
                else:
                    # Run synchronously if no event loop
                    asyncio.run(self._publish_async(event_type, event))
            except RuntimeError:
                # No event loop available, skip async handlers
                logger.debug(f"No event loop available for async handlers of {event_type.__name__}")
    
    async def _publish_async(self, event_type: Type[Event], event: Event) -> None:
        """Publish event to asynchronous handlers"""
        for handler in self._async_listeners[event_type]:
            try:
                if inspect.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error in async event handler for {event_type.__name__}: {e}")
    
    def clear_listeners(self) -> None:
        """Clear all event listeners (useful for testing)"""
        self._listeners.clear()
        self._async_listeners.clear()
        logger.debug("Cleared all event listeners")
    
    def get_listener_count(self, event_type: Type[Event]) -> int:
        """Get number of listeners for an event type"""
        return len(self._listeners[event_type]) + len(self._async_listeners[event_type])


# Global event bus instance
_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get the global event bus instance"""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


def set_event_bus(event_bus: EventBus) -> None:
    """Set the global event bus instance (useful for testing)"""
    global _event_bus
    _event_bus = event_bus
