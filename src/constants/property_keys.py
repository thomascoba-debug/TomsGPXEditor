#!/usr/bin/env python3
"""
Central Property Keys - Eliminates String Literals
"""

# App Level Keys
APP_VERSION = "app.version"
APP_MAIN_WINDOW = "app.main_window"
APP_RECENT_FILES = "app.recent_files"

# Session Management
SESSION_FILES = "session_files"

# Dialog System
DIALOGS = "dialogs"
DIALOGS_GEOMETRY = "dialogs.geometry"
DIALOGS_SETTINGS = "dialogs.settings"
DIALOGS_SETTINGS_LOGGING = "dialogs.settings.logging"

# Conversion Settings
CONVERSION = "conversion"
DOWNSAMPLE = "downsample"
ROUTE_TO_TRACK = "route_to_track"
TRACK_TO_ROUTE = "track_to_route"

# Rendering Settings
RENDERING = "rendering"
WAYPOINTS = "waypoints"
TRACKPOINTS = "trackpoints"
ROUTEPOINTS = "routepoints"

# Additional Constants for structured paths
DIALOGS_SETTINGS_RENDERING = "dialogs.settings.rendering"
FILES_SESSION = "files.session"

# Helper functions for building structured paths
def build_conversion_path(subkey):
    """Build structured path for conversion settings"""
    return f"dialogs.settings.conversion.{subkey}"
