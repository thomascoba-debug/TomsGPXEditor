"""
Resource Manager for GPX Editor
Manages file handles, temporary files, and other resources
"""

import logging
import threading
import tempfile
import os
from typing import Dict, Set, Any, Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class ResourceManager:
    """Manages application resources with thread safety"""
    
    def __init__(self):
        self._open_files: Dict[str, Any] = {}
        self._temp_files: Set[str] = set()
        self._resources: Dict[str, Any] = {}
        self._lock = threading.Lock()
    
    def register_file(self, file_path: str, file_handle: Any):
        """Register an open file handle"""
        with self._lock:
            self._open_files[file_path] = file_handle
            logger.debug(f"Registered file handle: {file_path}")
    
    def unregister_file(self, file_path: str):
        """Unregister and close a file handle"""
        with self._lock:
            if file_path in self._open_files:
                file_handle = self._open_files.pop(file_path)
                try:
                    if hasattr(file_handle, 'close'):
                        file_handle.close()
                    logger.debug(f"Closed file handle: {file_path}")
                except Exception as e:
                    logger.error(f"Error closing file {file_path}: {e}")
    
    def create_temp_file(self, suffix: str = "", prefix: str = "gpx_editor_") -> str:
        """Create a temporary file and track it"""
        temp_file = tempfile.NamedTemporaryFile(suffix=suffix, prefix=prefix, delete=False)
        temp_file.close()
        
        with self._lock:
            self._temp_files.add(temp_file.name)
            logger.debug(f"Created temp file: {temp_file.name}")
        
        return temp_file.name
    
    def cleanup_temp_file(self, temp_file_path: str):
        """Clean up a temporary file"""
        with self._lock:
            if temp_file_path in self._temp_files:
                try:
                    os.unlink(temp_file_path)
                    self._temp_files.remove(temp_file_path)
                    logger.debug(f"Cleaned up temp file: {temp_file_path}")
                except Exception as e:
                    logger.error(f"Error cleaning up temp file {temp_file_path}: {e}")
    
    def register_resource(self, name: str, resource: Any):
        """Register a generic resource"""
        with self._lock:
            self._resources[name] = resource
            logger.debug(f"Registered resource: {name}")
    
    def unregister_resource(self, name: str):
        """Unregister and cleanup a resource"""
        with self._lock:
            if name in self._resources:
                resource = self._resources.pop(name)
                try:
                    if hasattr(resource, 'cleanup'):
                        resource.cleanup()
                    elif hasattr(resource, 'close'):
                        resource.close()
                    logger.debug(f"Cleaned up resource: {name}")
                except Exception as e:
                    logger.error(f"Error cleaning up resource {name}: {e}")
    
    def cleanup_all(self):
        """Clean up all registered resources"""
        logger.info("Starting resource cleanup...")
        
        with self._lock:
            # Close all files
            for file_path in list(self._open_files.keys()):
                self.unregister_file(file_path)
            
            # Clean up temp files
            for temp_file in list(self._temp_files):
                self.cleanup_temp_file(temp_file)
            
            # Clean up resources
            for resource_name in list(self._resources.keys()):
                self.unregister_resource(resource_name)
        
        logger.info("Resource cleanup completed")
    
    @contextmanager
    def managed_file(self, file_path: str, mode: str = 'r'):
        """Context manager for file operations"""
        file_handle = None
        try:
            file_handle = open(file_path, mode, encoding='utf-8')
            self.register_file(file_path, file_handle)
            yield file_handle
        finally:
            if file_handle:
                self.unregister_file(file_path)
    
    @contextmanager
    def managed_temp_file(self, suffix: str = "", prefix: str = "gpx_editor_"):
        """Context manager for temporary files"""
        temp_file_path = None
        try:
            temp_file_path = self.create_temp_file(suffix, prefix)
            yield temp_file_path
        finally:
            if temp_file_path:
                self.cleanup_temp_file(temp_file_path)

# Global resource manager instance
_resource_manager: Optional[ResourceManager] = None
_lock = threading.Lock()

def get_resource_manager() -> ResourceManager:
    """Get the global resource manager instance"""
    global _resource_manager
    if _resource_manager is None:
        with _lock:
            if _resource_manager is None:
                _resource_manager = ResourceManager()
    return _resource_manager
