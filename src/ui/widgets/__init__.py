"""
UI Widgets

Contains all UI widget components for GPX Editor.
"""

# Only use the modern FileEntryBuilder system
from .file_entry_builder import FileEntryBuilder
from .gpx_table_editor import GPXTableEditor
from .file_search import FileSearchFrame, FileSearchEngine, AdvancedSearchDialog
from .context_menu import ContextMenuManager, AutoSaveManager, KeyboardShortcutManager, QuickActionsManager

__all__ = [
    'FileEntryBuilder', 'GPXTableEditor',
    'FileSearchFrame', 'FileSearchEngine', 'AdvancedSearchDialog',
    'ContextMenuManager', 'AutoSaveManager', 'KeyboardShortcutManager', 'QuickActionsManager'
]
