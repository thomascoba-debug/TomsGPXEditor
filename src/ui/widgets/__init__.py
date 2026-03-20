"""
UI Widgets

Contains all UI widget components for GPX Editor.
"""

from .file_entry import FileEntry
from .gpx_table_editor import GPXTableEditor
from .progress_dialog import ProgressManager
from .file_search import FileSearchFrame, FileSearchEngine, AdvancedSearchDialog
from .context_menu import ContextMenuManager, AutoSaveManager, KeyboardShortcutManager, QuickActionsManager

__all__ = [
    'FileEntry', 'GPXTableEditor', 'ProgressManager',
    'FileSearchFrame', 'FileSearchEngine', 'AdvancedSearchDialog',
    'ContextMenuManager', 'AutoSaveManager', 'KeyboardShortcutManager', 'QuickActionsManager'
]
