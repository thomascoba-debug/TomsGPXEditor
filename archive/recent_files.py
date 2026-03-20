"""
Recent files management for GPX Editor
"""

import os
import json
import logging
from typing import List, Optional
from collections import deque

logger = logging.getLogger(__name__)


class RecentFilesManager:
    """Manages recently opened files"""
    
    def __init__(self, properties, max_files=10):
        self.properties = properties
        # Ensure max_files is non-negative
        self.max_files = max(0, int(max_files))
        self.recent_files = self._load_recent_files()
    
    def _load_recent_files(self) -> deque:
        """Load recent files from properties"""
        recent_list = self.properties.get("recent_files", [])
        return deque(recent_list, maxlen=self.max_files)
    
    def _save_recent_files(self):
        """Save recent files to properties"""
        self.properties.set("recent_files", list(self.recent_files))
        self.properties.save()
        logger.debug(f"Saved {len(self.recent_files)} recent files")
    
    def add_file(self, file_path: str) -> None:
        """Add a file to recent files list"""
        if not os.path.exists(file_path):
            logger.warning(f"File does not exist, not adding to recent files: {file_path}")
            return
        
        # Remove if already exists (to move to front)
        try:
            self.recent_files.remove(file_path)
        except ValueError:
            pass
        
        # Add to front
        self.recent_files.appendleft(file_path)
        
        # Save
        self._save_recent_files()
        logger.debug(f"Added to recent files: {file_path}")
    
    def remove_file(self, file_path: str) -> None:
        """Remove a file from recent files list"""
        try:
            self.recent_files.remove(file_path)
            self._save_recent_files()
            logger.debug(f"Removed from recent files: {file_path}")
        except ValueError:
            pass  # File not in list
    
    def get_recent_files(self) -> List[str]:
        """Get list of recent files (only existing ones)"""
        # Filter out non-existent files
        existing_files = [f for f in self.recent_files if os.path.exists(f)]
        
        # Update if files were removed
        if len(existing_files) != len(self.recent_files):
            self.recent_files = deque(existing_files, maxlen=self.max_files)
            self._save_recent_files()
        
        return list(self.recent_files)
    
    def clear_recent_files(self) -> None:
        """Clear all recent files"""
        self.recent_files.clear()
        self._save_recent_files()
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
