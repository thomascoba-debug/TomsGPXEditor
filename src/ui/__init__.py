"""
UI Layer

Contains all user interface components.
"""

from .base import PersistentDialog
from .dialogs import *
from .widgets import *
from .utils.color_utils import pick_color, update_color_button, validate_color

# Legacy components
# from .file_entry import FileEntry
# from .gpx_table_editor import GPXTableEditor

__all__ = [
    'PersistentDialog',
    'LoggingSettingsDialog', 'MarkerSettingsDialog', 'PropertiesEditorDialog', 'RenderingSettingsDialog',
    'FileEntry', 'GPXTableEditor', 'ProgressManager',
    'FileSearchFrame', 'FileSearchEngine', 'AdvancedSearchDialog',
    'ContextMenuManager', 'AutoSaveManager', 'KeyboardShortcutManager', 'QuickActionsManager',
    'pick_color', 'update_color_button', 'validate_color'
]
