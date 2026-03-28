"""
State Manager for GPX Editor
Provides centralized application state management
"""

import logging
import threading
from enum import Enum
from typing import Callable, Set, Optional

logger = logging.getLogger(__name__)

class ApplicationState(Enum):
    """Application states"""
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    ERROR = "error"

class StateManager:
    """Manages application state transitions"""
    
    def __init__(self):
        self._state = ApplicationState.INITIALIZING
        self._lock = threading.Lock()
        self._state_change_callbacks: Set[Callable[[ApplicationState, ApplicationState], None]] = set()
    
    @property
    def state(self) -> ApplicationState:
        """Get current state"""
        return self._state
    
    @state.setter
    def state(self, new_state: ApplicationState):
        """Set new state with validation"""
        with self._lock:
            old_state = self._state
            
            # Validate state transition
            if not self._is_valid_transition(old_state, new_state):
                logger.warning(f"Invalid state transition: {old_state} -> {new_state}")
                return
            
            self._state = new_state
            logger.info(f"State changed: {old_state.value} -> {new_state.value}")
            
            # Notify callbacks
            for callback in self._state_change_callbacks:
                try:
                    callback(old_state, new_state)
                except Exception as e:
                    logger.error(f"State change callback failed: {e}")
    
    def _is_valid_transition(self, from_state: ApplicationState, to_state: ApplicationState) -> bool:
        """Check if state transition is valid"""
        # Allow any transition to ERROR or SHUTTING_DOWN
        if to_state in [ApplicationState.ERROR, ApplicationState.SHUTTING_DOWN]:
            return True
        
        # Normal transitions
        valid_transitions = {
            ApplicationState.INITIALIZING: [ApplicationState.READY, ApplicationState.ERROR],
            ApplicationState.READY: [ApplicationState.RUNNING, ApplicationState.SHUTTING_DOWN, ApplicationState.ERROR],
            ApplicationState.RUNNING: [ApplicationState.READY, ApplicationState.SHUTTING_DOWN, ApplicationState.ERROR],
        }
        
        return to_state in valid_transitions.get(from_state, [])
    
    def register_state_change_callback(self, callback: Callable[[ApplicationState, ApplicationState], None]):
        """Register a callback for state changes"""
        self._state_change_callbacks.add(callback)
    
    def unregister_state_change_callback(self, callback: Callable[[ApplicationState, ApplicationState], None]):
        """Unregister a state change callback"""
        self._state_change_callbacks.discard(callback)
    
    def is_ready(self) -> bool:
        """Check if application is ready"""
        return self._state in [ApplicationState.READY, ApplicationState.RUNNING]
    
    def is_shutting_down(self) -> bool:
        """Check if application is shutting down"""
        return self._state == ApplicationState.SHUTTING_DOWN

# Global state manager instance
_state_manager: Optional[StateManager] = None
_lock = threading.Lock()

def get_state_manager() -> StateManager:
    """Get the global state manager instance"""
    global _state_manager
    if _state_manager is None:
        with _lock:
            if _state_manager is None:
                _state_manager = StateManager()
    return _state_manager
