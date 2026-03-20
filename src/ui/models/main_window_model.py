"""
Main Window Model

Data model for the main application window following MVP pattern.
"""

from typing import List, Optional
from ...domain.entities import GPXFile


class MainWindowModel:
    """Main window data model"""
    
    def __init__(self):
        self.gpx_files: List[GPXFile] = []
        self.status_message: str = "Ready"
        self.selected_files: List[str] = []
        self._dirty: bool = False
    
    @property
    def has_editable_files(self) -> bool:
        """Check if any files are editable"""
        return any(file.is_editable for file in self.gpx_files)
    
    @property
    def editable_files_count(self) -> int:
        """Count of editable files"""
        return sum(1 for file in self.gpx_files if file.is_editable)
    
    def add_file(self, gpx_file: GPXFile):
        """Add a GPX file to the model"""
        self.gpx_files.append(gpx_file)
        self._dirty = True
    
    def remove_file(self, gpx_file: GPXFile):
        """Remove a GPX file from the model"""
        if gpx_file in self.gpx_files:
            self.gpx_files.remove(gpx_file)
            self._dirty = True
    
    def remove_file_by_path(self, file_path: str):
        """Remove a GPX file by path"""
        self.gpx_files = [f for f in self.gpx_files if f.path != file_path]
        self._dirty = True
    
    def get_file_by_path(self, file_path: str) -> Optional[GPXFile]:
        """Get a GPX file by path"""
        for file in self.gpx_files:
            if file.path == file_path:
                return file
        return None
    
    def update_file(self, gpx_file: GPXFile):
        """Update a GPX file in the model"""
        for i, file in enumerate(self.gpx_files):
            if file.path == gpx_file.path:
                self.gpx_files[i] = gpx_file
                self._dirty = True
                break
    
    def set_selected_files(self, file_paths: List[str]):
        """Set selected files"""
        self.selected_files = file_paths
        self._dirty = True
    
    def set_status(self, message: str):
        """Set status message"""
        self.status_message = message
        self._dirty = True
    
    def is_dirty(self) -> bool:
        """Check if model has unsaved changes"""
        return self._dirty
    
    def mark_clean(self):
        """Mark model as clean"""
        self._dirty = False
    
    def clear_files(self):
        """Clear all files"""
        self.gpx_files.clear()
        self.selected_files.clear()
        self.status_message = "Ready"
        self._dirty = True
    
    def get_file_count(self) -> int:
        """Get total file count"""
        return len(self.gpx_files)
    
    def get_track_count(self) -> int:
        """Get total track count"""
        return sum(len(file.tracks) for file in self.gpx_files)
    
    def get_route_count(self) -> int:
        """Get total route count"""
        return sum(len(file.routes) for file in self.gpx_files)
    
    def get_total_points(self) -> int:
        """Get total points across all files"""
        return sum(file.total_points for file in self.gpx_files)
