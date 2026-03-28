"""
Graceful Shutdown Manager for GPX Editor
Handles application shutdown with proper cleanup
"""

import logging
import signal
import threading
import time
import sys
from enum import Enum
from typing import Callable, List, Dict, Any, Optional
from functools import wraps

logger = logging.getLogger(__name__)

class ShutdownPriority(Enum):
    """Shutdown handler priorities"""
    CRITICAL = 1    # Core cleanup (save data, close resources)
    HIGH = 2       # UI cleanup (close windows)
    NORMAL = 3     # General cleanup
    LOW = 4        # Optional cleanup (cache, temp files)

class ShutdownManager:
    """Manages graceful application shutdown"""
    
    def __init__(self, timeout: float = 30.0):
        self._handlers: List[Dict[str, Any]] = []
        self._timeout = timeout
        self._shutdown_in_progress = False
        self._lock = threading.Lock()
        self._original_handlers = {}
    
    def register_handler(self, handler: Callable, priority: ShutdownPriority = ShutdownPriority.NORMAL, 
                        name: str = None, timeout: float = None):
        """Register a shutdown handler"""
        with self._lock:
            if self._shutdown_in_progress:
                logger.warning("Cannot register handler during shutdown")
                return
            
            handler_info = {
                'handler': handler,
                'priority': priority,
                'name': name or f"handler_{len(self._handlers)}",
                'timeout': timeout or 10.0
            }
            self._handlers.append(handler_info)
            
            # Sort by priority (lower number = higher priority)
            self._handlers.sort(key=lambda x: x['priority'].value)
            
            logger.debug(f"Registered shutdown handler: {handler_info['name']} (priority: {priority.name})")
    
    def shutdown(self):
        """Execute graceful shutdown"""
        with self._lock:
            if self._shutdown_in_progress:
                logger.warning("Shutdown already in progress")
                return
            
            self._shutdown_in_progress = True
        
        logger.info("Starting graceful shutdown...")
        start_time = time.time()
        
        failed_handlers = []
        
        # Execute handlers in priority order
        for handler_info in self._handlers:
            handler_name = handler_info['name']
            handler = handler_info['handler']
            timeout = handler_info['timeout']
            
            try:
                logger.debug(f"Executing shutdown handler: {handler_name}")
                
                # Run handler with timeout
                handler_thread = threading.Thread(target=handler, daemon=True)
                handler_thread.start()
                handler_thread.join(timeout=timeout)
                
                if handler_thread.is_alive():
                    logger.warning(f"Shutdown handler {handler_name} timed out")
                    failed_handlers.append(handler_name)
                else:
                    logger.debug(f"Shutdown handler {handler_name} completed")
                    
            except Exception as e:
                logger.error(f"Shutdown handler {handler_name} failed: {e}")
                failed_handlers.append(handler_name)
        
        total_duration = time.time() - start_time
        
        if failed_handlers:
            logger.error(f"Shutdown completed with {len(failed_handlers)} failed handlers: {failed_handlers}")
        else:
            logger.info(f"Graceful shutdown completed in {total_duration:.2f}s")
        
        # Restore original signal handlers
        self._restore_signal_handlers()
        
        # Force exit if still running
        if threading.active_count() > 1:
            logger.info(f"Still {threading.active_count() - 1} threads active, forcing exit")
            
            # Try to join remaining threads briefly
            main_thread = threading.main_thread()
            if main_thread.is_alive():
                try:
                    main_thread.join(timeout=1.0)
                except Exception:
                    pass
            
            # Force exit if threads are still hanging
            sys.exit(1)
    
    def _restore_signal_handlers(self):
        """Restore original signal handlers"""
        for sig, handler in self._original_handlers.items():
            try:
                signal.signal(sig, handler)
            except Exception as e:
                logger.error(f"Error restoring signal handler for {sig}: {e}")
    
    def is_shutting_down(self) -> bool:
        """Check if shutdown is in progress"""
        return self._shutdown_in_progress

def shutdown_handler(priority: ShutdownPriority = ShutdownPriority.NORMAL, name: str = None, timeout: float = None):
    """Decorator to register shutdown handlers"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Register the decorated function
        manager = get_shutdown_manager()
        manager.register_handler(wrapper, priority, name, timeout)
        
        return wrapper
    return decorator

# Global shutdown manager instance
_shutdown_manager: Optional[ShutdownManager] = None
_lock = threading.Lock()

def get_shutdown_manager() -> ShutdownManager:
    """Get the global shutdown manager instance"""
    global _shutdown_manager
    if _shutdown_manager is None:
        with _lock:
            if _shutdown_manager is None:
                _shutdown_manager = ShutdownManager()
    return _shutdown_manager

def initialize_graceful_shutdown():
    """Initialize graceful shutdown with signal handlers"""
    manager = get_shutdown_manager()
    
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown")
        manager.shutdown()
    
    # Register signal handlers
    try:
        manager._original_handlers[signal.SIGINT] = signal.signal(signal.SIGINT, signal_handler)
        manager._original_handlers[signal.SIGTERM] = signal.signal(signal.SIGTERM, signal_handler)
        logger.debug("Signal handlers registered")
    except Exception as e:
        logger.error(f"Error registering signal handlers: {e}")
    
    logger.info("Graceful shutdown initialized")
