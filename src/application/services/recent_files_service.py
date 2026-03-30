
from src.constants.property_keys import SESSION_FILES
from src.constants.property_keys import APP_RECENT_FILES
"""
Recent files management based on session files with timestamp tracking
"""

import os
import json
import logging
import time
from typing import List, Dict
from collections import deque

logger = logging.getLogger(__name__)


class RecentFilesFromSessionManager:
    """Manages recent files based on session_files data with timestamp tracking"""
    
    def __init__(self, properties, max_files=10):
        self.properties = properties
        self.max_files = max_files
        self.recent_files = self._load_recent_files_with_timestamps()
    
    def _load_recent_files_with_timestamps(self) -> deque:
        """Load recent files from session_files with timestamp tracking"""
        session_files = self.properties.get('files.session') or self.properties.data.get('files', {}).get('session', {})
        # Use the nested path in app dict
        recent_files_data = self.properties.get(APP_RECENT_FILES, {})
        
        # Extract file paths with timestamps
        file_entries = []
        
        # First, add files from session_files
        for ref_num, file_data in session_files.items():
            file_path = file_data.get("path")
            if file_path and os.path.exists(file_path):
                # Get timestamp from recent_files_data, but don't use current time for old files
                if file_path in recent_files_data:
                    timestamp = recent_files_data[file_path]
                    file_entries.append((timestamp, file_path))
        
        # Then, add any additional files from timestamps that exist but aren't in session_files
        session_file_paths = {file_data.get("path") for file_data in session_files.values() if file_data.get("path")}
        
        for file_path, timestamp in recent_files_data.items():
            if file_path not in session_file_paths and os.path.exists(file_path):
                file_entries.append((timestamp, file_path))
        
        # Sort by timestamp (most recent first) and take only paths
        file_entries.sort(key=lambda x: x[0], reverse=True)
        file_paths = [path for _, path in file_entries[:self.max_files]]
        
        return deque(file_paths, maxlen=self.max_files)
    
    def _save_recent_files_with_timestamps(self):
        """Save recent files with timestamps to properties"""
        recent_files_data = {}
        
        # Create timestamp mapping
        for file_path in self.recent_files:
            recent_files_data[file_path] = time.time()
        
        # Use the nested path in app dict
        self.properties.set(APP_RECENT_FILES, recent_files_data)
        self.properties.save()
    
    def add_file(self, file_path: str) -> None:
        """Add a file to recent files list (updates timestamp)"""
        if not os.path.exists(file_path):
            logger.warning(f"File does not exist, not adding to recent files: {file_path}")
            return
        
        # Remove if already exists (to move to front)
        try:
            self.recent_files.remove(file_path)
        except ValueError:
            pass
        
        # Add to front with current timestamp
        self.recent_files.appendleft(file_path)
        
        # Save timestamps
        self._save_recent_files_with_timestamps()
        
        logger.debug(f"Added to recent files: {file_path}")
    
    def reload_recent_files(self):
        """Reload recent files from properties"""
        self.recent_files = self._load_recent_files_with_timestamps()
        logger.debug(f"Reloaded recent files: {len(self.recent_files)} files")
    
    def remove_file(self, file_path: str) -> None:
        """Remove a file from recent files list"""
        try:
            self.recent_files.remove(file_path)
            logger.debug(f"Removed from recent files: {file_path}")
        except ValueError:
            pass  # File not in list
        
        # Update timestamps
        self._save_recent_files_with_timestamps()
    
    def get_recent_files(self) -> List[str]:
        """Get list of recent files (only existing ones)"""
        # Filter out non-existent files and update if needed
        existing_files = [f for f in self.recent_files if os.path.exists(f)]
        
        # Update if files were removed
        if len(existing_files) != len(self.recent_files):
            self.recent_files = deque(existing_files, maxlen=self.max_files)
            self._save_recent_files_with_timestamps()
        
        return list(self.recent_files)
    
    def clear_recent_files(self) -> None:
        """Clear all recent files"""
        self.recent_files.clear()
        # Use the nested path in app dict
        self.properties.remove(APP_RECENT_FILES)
        self.properties.save()
        logger.debug("Cleared all recent files")
    
    def get_display_name(self, file_path: str) -> str:
        """Get display name for file (basename with directory)"""
        basename = os.path.basename(file_path)
        dirname = os.path.dirname(file_path)
        
        # Show parent directory name if available
        if dirname:
            parent_dir = os.path.basename(dirname)
            return f"{parent_dir}/{basename}"
        
        return basename
    
    def sync_with_session_files(self):
        """Sync recent files with current session files (maintains timestamps)"""
        # Load current timestamps
        # Use the nested path in app dict
        current_timestamps = self.properties.get(APP_RECENT_FILES, {})
        
        # Get current session files
        session_files = self.properties.get('files.session') or self.properties.data.get('files', {}).get('session', {})
        current_session_paths = set()
        
        for ref_num, file_data in session_files.items():
            file_path = file_data.get("path")
            if file_path and os.path.exists(file_path):
                current_session_paths.add(file_path)
        
        # Remove files from recent_files that are no longer in session
        filtered_files = deque()
        for file_path in self.recent_files:
            if file_path in current_session_paths:
                filtered_files.append(file_path)
        
        self.recent_files = filtered_files
        
        # Clean up timestamps for removed files
        for file_path in list(current_timestamps.keys()):
            if file_path not in current_session_paths:
                del current_timestamps[file_path]
        
        # Save updated timestamps
        # Use the nested path in app dict
        self.properties.set(APP_RECENT_FILES, current_timestamps)
        self.properties.save()
        
        logger.debug(f"Synced recent files with session files: {len(self.recent_files)} files")
