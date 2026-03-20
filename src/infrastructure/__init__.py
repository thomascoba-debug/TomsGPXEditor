"""
Infrastructure Layer

External dependencies, persistence, and technical concerns.
"""

from .repositories.properties_repository import AppProperties
from .map_renderer import GPXCache, render_tracks_on_map
from .error_handler import GPXEditorException, safe_execute, validate_gpx_data

# Alias for backward compatibility
PropertiesManager = AppProperties

__all__ = [
    'AppProperties', 'PropertiesManager', 'GPXCache', 'render_tracks_on_map',
    'GPXEditorException', 'safe_execute', 'validate_gpx_data'
]
