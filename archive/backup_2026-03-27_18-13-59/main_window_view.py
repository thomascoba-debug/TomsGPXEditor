"""
Main Window View Interface

View interface for the main application window following MVP pattern.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Callable
from ...domain.entities import GPXFile


class MainWindowView(ABC):
    """Abstract base class for main window view"""
    
    @abstractmethod
    def set_presenter(self, presenter):
        """Set the presenter for this view"""
        pass
    
    @abstractmethod
    def update_file_list(self, files: List[GPXFile]):
        """Update the file list display"""
        pass
    
    @abstractmethod
    def update_conversion_buttons(self, enabled: bool):
        """Enable/disable conversion buttons based on editable files"""
        pass
    
    @abstractmethod
    def update_status(self, message: str):
        """Update the status bar message"""
        pass
    
    @abstractmethod
    def get_selected_files(self) -> List[str]:
        """Get list of selected file paths"""
        pass
    
    @abstractmethod
    def show_error(self, title: str, message: str):
        """Show error dialog"""
        pass
    
    @abstractmethod
    def show_info(self, title: str, message: str):
        """Show info dialog"""
        pass
    
    @abstractmethod
    def show_file_dialog(self, title: str, file_types: List[tuple]) -> Optional[str]:
        """Show file open dialog"""
        pass
    
    @abstractmethod
    def show_save_dialog(self, title: str, default_name: str, file_types: List[tuple]) -> Optional[str]:
        """Show file save dialog"""
        pass
    
    @abstractmethod
    def confirm_delete(self, file_count: int) -> bool:
        """Show delete confirmation dialog"""
        pass
    
    @abstractmethod
    def show_progress(self, message: str, maximum: int) -> 'ProgressManager':
        """Show progress dialog"""
        pass
    
    @abstractmethod
    def hide_progress(self):
        """Hide progress dialog"""
        pass
    
    @abstractmethod
    def refresh_map(self):
        """Refresh the map display"""
        pass
    
    @abstractmethod
    def add_file_to_map(self, gpx_file: GPXFile):
        """Add file to map display"""
        pass
    
    @abstractmethod
    def remove_file_from_map(self, file_path: str):
        """Remove file from map display"""
        pass
    
    @abstractmethod
    def update_file_on_map(self, gpx_file: GPXFile):
        """Update file on map display"""
        pass
    
    # Menu actions
    @abstractmethod
    def set_menu_callbacks(self, callbacks: dict):
        """Set menu action callbacks"""
        pass
    
    @abstractmethod
    def update_recent_files_menu(self, recent_files: List[str]):
        """Update recent files menu"""
        pass
    
    # Settings
    @abstractmethod
    def show_settings_dialog(self, dialog_type: str):
        """Show settings dialog"""
        pass
    
    # Application lifecycle
    @abstractmethod
    def show(self):
        """Show the main window"""
        pass
    
    @abstractmethod
    def hide(self):
        """Hide the main window"""
        pass
    
    @abstractmethod
    def destroy(self):
        """Destroy the main window"""
        pass
    
    @abstractmethod
    def get_geometry(self) -> str:
        """Get window geometry for persistence"""
        pass
    
    @abstractmethod
    def set_geometry(self, geometry: str):
        """Set window geometry from persistence"""
        pass
