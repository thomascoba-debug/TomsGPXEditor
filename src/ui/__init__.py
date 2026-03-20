"""
UI Layer

Contains all user interface components following MVP pattern.
"""

from .base import PersistentDialog
from .dialogs import *
from .widgets import *

# MVP Components (Phase 3)
from .models import *
from .views import *
from .presenters import *
from .main_window import MainWindow

# Legacy components (will be phased out)
# from .file_entry import FileEntry
# from .gpx_table_editor import GPXTableEditor

__all__ = [
    'PersistentDialog',
    'LoggingSettingsDialog', 'MarkerSettingsDialog', 'PropertiesEditorDialog', 'RenderingSettingsDialog',
    'FileEntry', 'GPXTableEditor', 'ProgressManager',
    'FileSearchFrame', 'FileSearchEngine', 'AdvancedSearchDialog',
    'ContextMenuManager', 'AutoSaveManager', 'KeyboardShortcutManager', 'QuickActionsManager',
    # MVP Components
    'MainWindowModel', 'MainWindowView', 'MainWindowViewImpl', 'MainWindowPresenter',
    'MainWindow'
]
