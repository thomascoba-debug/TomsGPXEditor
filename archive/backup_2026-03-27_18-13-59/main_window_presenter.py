"""
Main Window Presenter

MVP pattern presenter for the main application window.
"""

import logging
from typing import List, Optional
from ...application import EventBus
from ...domain.entities import GPXFile
from ...infrastructure import AppProperties
from ..models.main_window_model import MainWindowModel
from ..views.main_window_view import MainWindowView

logger = logging.getLogger(__name__)


class MainWindowPresenter:
    """Main window presenter implementing MVP pattern"""
    
    def __init__(self, event_bus: EventBus, properties: AppProperties):
        self.event_bus = event_bus
        self.properties = properties
        self.model = MainWindowModel()
        self.view: Optional[MainWindowView] = None
        
        # Subscribe to events
        self._setup_event_subscriptions()
    
    def set_view(self, view: 'MainWindowView'):
        """Set the view and initialize it"""
        self.view = view
        if view:
            view.set_presenter(self)
            self._initialize_view()
    
    def _setup_event_subscriptions(self):
        """Setup event subscriptions"""
        # File events
        from ...application.event_bus import FileLoadedEvent, FileEditableChangedEvent, FileRemovedEvent
        self.event_bus.subscribe(FileLoadedEvent, self._on_file_loaded)
        self.event_bus.subscribe(FileEditableChangedEvent, self._on_file_editable_changed)
        self.event_bus.subscribe(FileRemovedEvent, self._on_file_removed)
        
        # Application events
        from ...application.event_bus import ConversionCompletedEvent
        self.event_bus.subscribe(ConversionCompletedEvent, self._on_conversion_completed)
        
        # AnalysisCompletedEvent doesn't exist yet, skip for now
    
    def _initialize_view(self):
        """Initialize the view with current model state"""
        if self.view:
            self.view.update_file_list(self.model.gpx_files)
            self.view.update_conversion_buttons(self.model.has_editable_files)
            self.view.update_status(self.model.status_message)
    
    def load_gpx_file(self, file_path: str):
        """Load a GPX file"""
        try:
            import gpxpy
            from gpxpy.gpx import GPXXMLSyntaxException
            from ...infrastructure.error_handler import GPXEditorException
            
            # Check if file exists and is not empty
            import os
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"GPX file not found: {file_path}")
            
            if os.path.getsize(file_path) == 0:
                raise ValueError(f"GPX file is empty: {file_path}")
            
            # Load GPX file directly
            with open(file_path, "r", encoding="utf-8") as f:
                # Check if file starts with XML declaration or GPX tag
                content = f.read(100)
                f.seek(0)
                
                if not content.strip().startswith(('<?xml', '<gpx')):
                    raise ValueError(f"File does not appear to be a valid GPX file: {file_path}")
                
                gpx_data = gpxpy.parse(f)
            
            # Create GPXFile entity directly
            gpx_file = GPXFile.from_gpxpy(
                path=file_path,
                gpx_data=gpx_data,
                is_visible=True,
                is_editable=True,
                color="#80ffff"
            )
            
            self.model.add_file(gpx_file)
            self._update_view()
            
            # Publish event
            from ...application.event_bus import FileLoadedEvent
            self.event_bus.publish(FileLoadedEvent(
                file_path=file_path,
                gpx_file=gpx_file
            ))
            
            logger.info(f"Successfully loaded GPX file: {file_path}")
                
        except Exception as e:
            logger.error(f"Error loading GPX file {file_path}: {e}")
            self.model.set_status(f"Error loading file: {e}")
            self._update_view()
    
    def convert_route_to_track(self):
        """Convert all routes to tracks"""
        try:
            from ...application.services.conversion_service import route_to_track
            
            converted_files = []
            for gpx_file in self.model.gpx_files:
                if gpx_file.is_editable and gpx_file.routes:
                    converted = route_to_track(gpx_file.to_gpxpy())
                    converted_files.append(converted)
            
            if converted_files:
                self.model.set_status("Routes converted to tracks successfully")
                self.event_bus.publish('ConversionCompletedEvent', {
                    'type': 'route_to_track',
                    'files': converted_files
                })
            else:
                self.model.set_status("No routes to convert")
                
        except Exception as e:
            logger.error(f"Error converting routes to tracks: {e}")
            self.model.set_status(f"Error converting routes: {e}")
        
        self._update_view()
    
    def convert_track_to_route(self):
        """Convert all tracks to routes"""
        try:
            from ...application.services.conversion_service import track_to_route
            
            converted_files = []
            for gpx_file in self.model.gpx_files:
                if gpx_file.is_editable and gpx_file.tracks:
                    converted = track_to_route(gpx_file.to_gpxpy())
                    converted_files.append(converted)
            
            if converted_files:
                self.model.set_status("Tracks converted to routes successfully")
                self.event_bus.publish('ConversionCompletedEvent', {
                    'type': 'track_to_route',
                    'files': converted_files
                })
            else:
                self.model.set_status("No tracks to convert")
                
        except Exception as e:
            logger.error(f"Error converting tracks to routes: {e}")
            self.model.set_status(f"Error converting tracks: {e}")
        
        self._update_view()
    
    def analyze_gpx_files(self):
        """Analyze all loaded GPX files"""
        try:
            from ...application.services.gpx_service import GPXEditController
            
            analysis_results = []
            for gpx_file in self.model.gpx_files:
                if gpx_file.is_editable:
                    analysis = gpx_file.get_analysis()
                    analysis_results.append({
                        'file': gpx_file,
                        'analysis': analysis
                    })
            
            if analysis_results:
                self.model.set_status("GPX analysis completed")
                self.event_bus.publish('AnalysisCompletedEvent', {
                    'results': analysis_results
                })
            else:
                self.model.set_status("No editable files to analyze")
                
        except Exception as e:
            logger.error(f"Error analyzing GPX files: {e}")
            self.model.set_status(f"Error analyzing files: {e}")
        
        self._update_view()
    
    def delete_files(self):
        """Delete selected files"""
        try:
            # Implementation would depend on selection in view
            selected_files = self.view.get_selected_files() if self.view else []
            
            for file_path in selected_files:
                self.model.remove_file_by_path(file_path)
                self.event_bus.publish('FileRemovedEvent', {'path': file_path})
            
            self.model.set_status(f"Deleted {len(selected_files)} files")
            self._update_view()
            
        except Exception as e:
            logger.error(f"Error deleting files: {e}")
            self.model.set_status(f"Error deleting files: {e}")
            self._update_view()
    
    def _update_view(self):
        """Update the view with current model state"""
        if self.view:
            self.view.update_file_list(self.model.gpx_files)
            self.view.update_conversion_buttons(self.model.has_editable_files)
            self.view.update_status(self.model.status_message)
    
    # Event handlers
    def _on_file_loaded(self, event):
        """Handle file loaded event"""
        file_data = event.gpx_file
        if file_data:
            logger.info(f"File loaded: {file_data.path}")
    
    def _on_file_editable_changed(self, event):
        """Handle file editable changed event"""
        file_path = event.file_path
        is_editable = event.is_editable
        
        # Update model
        gpx_file = self.model.get_file_by_path(file_path)
        if gpx_file:
            gpx_file.is_editable = is_editable
            self._update_view()
    
    def _on_file_removed(self, event):
        """Handle file removed event"""
        file_path = event.file_path
        logger.info(f"File removed: {file_path}")
    
    def _on_conversion_completed(self, event):
        """Handle conversion completed event"""
        conversion_type = event.conversion_type
        logger.info(f"Conversion completed: {conversion_type}")
    
    def _on_analysis_completed(self, event):
        """Handle analysis completed event"""
        logger.info("Analysis completed")
