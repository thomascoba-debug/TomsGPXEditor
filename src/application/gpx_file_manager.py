
from src.constants.property_keys import SESSION_FILES
from src.constants.property_keys import FILES_SESSION, DIALOGS_SETTINGS
"""
GPX File Manager - Zentrale Verwaltung von GPX-Dateien

Dieser Controller kümmert sich um:
- Laden von GPX-Dateien
- Verwalten von Datei-Einträgen
- Session-Management
- UI-State für Datei-Liste
"""

import logging
import os
import gpxpy
from typing import List, Optional, Dict, Any
import tkinter as tk
from tkinter import ttk

from src.infrastructure.repositories.properties_repository import AppProperties
from src.infrastructure.map_renderer import GPXCache

logger = logging.getLogger(__name__)


class GPXFileManager:
    """Zentrale Verwaltung von GPX-Dateien und UI-Einträgen"""
    
    def __init__(self, properties: AppProperties, map_widget, main_grid, button_update_callback=None, editable_update_callback=None, recent_files_manager=None):
        self.properties = properties
        self.map_widget = map_widget
        self.main_grid = main_grid
        self.entries = []  # FileEntryBuilder creates entries
        self.current_row = 2  # Start nach Header
        self.button_update_callback = button_update_callback
        self.editable_update_callback = editable_update_callback
        self.recent_files_manager = recent_files_manager
        
    def load_gpx_file(self, path: str) -> Optional[Dict[str, Any]]:
        """Analysiere eine GPX-Datei und gib Metadaten zurück"""
        if not path or not isinstance(path, str):
            logger.error(f"Invalid file path provided: {path}")
            return None
        
        if not os.path.exists(path):
            logger.error(f"File does not exist: {path}")
            return None
        
        if not os.path.isfile(path):
            logger.error(f"Path is not a file: {path}")
            return None
        
        if not path.lower().endswith('.gpx'):
            logger.error(f"File is not a GPX file: {path}")
            return None
        
        try:
            # Check file size first
            file_size = os.path.getsize(path)
            if file_size == 0:
                logger.warning(f"GPX file is empty: {path}")
                return {
                    'file_type': 'empty',
                    'track_count': 0,
                    'route_count': 0,
                    'waypoint_count': 0
                }
            
            # Parse GPX file
            with open(path, 'r', encoding='utf-8') as f:
                gpx = gpxpy.parse(f)
            
            # Validate GPX structure
            if not gpx:
                logger.error(f"Invalid GPX structure in file: {path}")
                return {
                    'file_type': 'invalid',
                    'track_count': 0,
                    'route_count': 0,
                    'waypoint_count': 0
                }
            
            track_count = len(gpx.tracks)
            route_count = len(gpx.routes)
            waypoint_count = len(gpx.waypoints)
            
            if track_count > 0 and route_count > 0:
                file_type = 'mixed'
            elif track_count > 0:
                file_type = 'track'
            elif route_count > 0:
                file_type = 'route'
            elif waypoint_count > 0:
                file_type = 'waypoints'
            else:
                file_type = 'empty'
                logger.warning(f"GPX file contains no tracks, routes, or waypoints: {path}")
            
            return {
                'file_type': file_type,
                'track_count': track_count,
                'route_count': route_count,
                'waypoint_count': waypoint_count
            }
            
        except (FileNotFoundError, PermissionError) as e:
            logger.error(f"File access error analyzing {path}: {e}")
            return {
                'file_type': 'error',
                'track_count': 0,
                'route_count': 0,
                'waypoint_count': 0
            }
        except gpxpy.gpx.GPXXMLSyntaxException as e:
            logger.error(f"GPX XML syntax error in {path}: {e}")
            return {
                'file_type': 'invalid_xml',
                'track_count': 0,
                'route_count': 0,
                'waypoint_count': 0
            }
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error analyzing {path}: {e}")
            return {
                'file_type': 'encoding_error',
                'track_count': 0,
                'route_count': 0,
                'waypoint_count': 0
            }
        except Exception as e:
            logger.error(f"Unexpected error analyzing {path}: {e}", exc_info=True)
            return {
                'file_type': 'unknown',
                'track_count': 0,
                'route_count': 0,
                'waypoint_count': 0
            }
    
    def add_file_to_ui(self, path: str):
        """Füge eine GPX-Datei zur UI hinzu"""
        # Prüfe auf Duplikate
        existing_paths = [entry.get_path() for entry in self.entries]
        if path in existing_paths:
            logger.warning(f"File is already loaded: {path}")
            return None
        
        # Analysiere Datei
        file_analysis = self.load_gpx_file(path)
        if not file_analysis:
            return None
        
        # Hole Reference und Settings
        ref_num = self.properties.get_or_create_file_reference(path)
        settings = self.properties.get_file_settings_by_reference(ref_num)
        
        # Erstelle UI-Widgets
        from src.ui.widgets.file_entry_builder import FileEntryBuilder
        
        # Create FileEntryBuilder with direct callbacks
        builder = FileEntryBuilder(
            parent_frame=self.main_grid,
            row=self.current_row,
            button_update_callback=self.button_update_callback,
            editable_update_callback=self.editable_update_callback
        )
        entry = builder.create_file_entry(path, ref_num, file_analysis, settings, self.properties)
        
        if entry:
            self.entries.append(entry)
            self.current_row += 1
            
            # Speichere in Session (bereits durch get_or_create_file_reference oben erledigt)
            
            # Add to recent files
            if self.recent_files_manager:
                self.recent_files_manager.add_file(path)
                self.recent_files_manager.reload_recent_files()
                logger.debug(f"Added to recent files: {path}")
            
            logger.info(f"Added GPX file: {os.path.basename(path)} (ref: {ref_num})")
        
        return entry
    
    def remove_file_from_ui(self, entry) -> None:
        """Entferne eine Datei aus der UI"""
        if entry in self.entries:
            self.entries.remove(entry)
            entry.destroy()
            
            # Entferne aus Properties
            self.properties.remove_file_from_session(entry.ref_num)
            
            logger.info(f"Removed GPX file: {os.path.basename(entry.get_path())}")
    
    def get_all_entries(self):
        """Gib alle Einträge zurück"""
        return self.entries.copy()
    
    def get_editable_entries(self):
        """Gib alle editierbaren Einträge zurück"""
        return [entry for entry in self.entries if entry.is_editable()]
    
    def get_visible_entries(self):
        """Gib alle sichtbaren Einträge zurück"""
        return [entry for entry in self.entries if entry.is_visible()]
    
    def clear_all_entries(self) -> None:
        """Entferne alle Einträge"""
        for entry in self.entries.copy():
            self.remove_file_from_ui(entry)
        self.current_row = 2
        
        logger.info("Cleared all GPX file entries")
    
    def load_session_files(self) -> None:
        """Lade Session-Dateien mit Optimierung für große Dateien"""
        try:
            session_files = self.properties.get('files.session') or self.properties.data.get('files', {}).get('session', {})
            loaded_count = 0
            
            # Sortiere Reference-Nummern
            sorted_refs = sorted(session_files.keys(), key=int)
            
            for ref_num in sorted_refs:
                try:
                    file_data = session_files[ref_num]
                    file_path = file_data.get("path")
                    
                    if not file_path:
                        continue
                    
                    if os.path.exists(file_path):
                        try:
                            # Check file size for optimization
                            file_size = os.path.getsize(file_path)
                            logger.debug(f"Loading session file: {file_path} ({file_size/1024:.1f} KB)")
                            
                            entry = self.add_file_to_ui(file_path)
                            if entry:
                                loaded_count += 1
                                logger.debug(f"Successfully loaded session file {loaded_count}")
                        except Exception as e:
                            logger.error(f"Failed to load session file {file_path}: {str(e)}")
                            # Continue with other files
                    else:
                        logger.warning(f"Session file path does not exist: {file_path}")
                        # Remove from session files to clean up
                        self.properties.remove_file_from_session(ref_num)
                        
                except Exception as e:
                    logger.error(f"Error processing session file entry {ref_num}: {str(e)}")
                    # Continue with other files
            
            logger.info(f"Successfully loaded {loaded_count} session files")
            
        except Exception as e:
            logger.error(f"Error loading session files: {str(e)}")
            # Don't crash the app, just continue without session files
