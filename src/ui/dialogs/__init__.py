"""
UI Dialogs

Contains all dialog components for the GPX Editor.
"""

from .settings_logging_dialog import LoggingSettingsDialog
from .settings_marker_dialog import MarkerSettingsDialog
from .settings_properties_dialog import PropertiesEditorDialog
from .settings_rendering_dialog import RenderingSettingsDialog

__all__ = [
    'LoggingSettingsDialog',
    'MarkerSettingsDialog', 
    'PropertiesEditorDialog',
    'RenderingSettingsDialog'
]
