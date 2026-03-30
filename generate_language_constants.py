#!/usr/bin/env python3
"""
Language Constants Generator

This script creates language constants from translation files
to replace hardcoded literals with constants.
"""

import json
import os

def generate_language_constants():
    """Generate language constants from translation files"""
    
    print("GENERATING LANGUAGE CONSTANTS")
    print("=" * 50)
    
    # Read translation files
    de_file = "W:/TomsGPXEditor/src/i18n/translations/de.json"
    en_file = "W:/TomsGPXEditor/src/i18n/translations/en.json"
    
    try:
        with open(de_file, 'r', encoding='utf-8') as f:
            de_translations = json.load(f)
        
        with open(en_file, 'r', encoding='utf-8') as f:
            en_translations = json.load(f)
        
        print("Translation files loaded successfully")
        
    except Exception as e:
        print(f"Error loading translation files: {e}")
        return False
    
    # Create constants file
    constants_file = "W:/TomsGPXEditor/src/i18n/constants.py"
    
    constants_content = '''"""
Language Constants

This file contains constants for all UI text strings
to replace hardcoded literals with translatable constants.
"""

class MenuConstants:
    """Menu text constants"""
    
    # File menu
    FILE = "menu.file"
    EDIT = "menu.edit"
    SETTINGS = "menu.settings"
    HELP = "menu.help"
    VISIBILITY = "menu.visibility"
    SETTINGS_CHOOSE = "menu.settings_choose"
    
    # File menu items
    FILE_OPEN_GPX = "menu.file_open_gpx"
    FILE_RECENT_FILES = "menu.file_recent_files"
    FILE_CLEAR_RECENT = "menu.file_clear_recent"
    FILE_EXIT = "menu.file_exit"
    
    # Edit menu items
    EDIT_OPEN_TABLE_EDITOR = "menu.edit_open_table_editor"
    EDIT_TRACK_TO_ROUTE = "menu.edit_track_to_route"
    EDIT_ROUTE_TO_TRACK = "menu.edit_route_to_track"
    EDIT_TRACK_DOWNSAMPLING = "menu.edit_track_downsampling"

class DialogConstants:
    """Dialog text constants"""
    
    # Common buttons
    OK = "dialog.ok"
    CANCEL = "dialog.cancel"
    APPLY = "dialog.apply"
    SAVE = "dialog.save"
    DELETE = "dialog.delete"
    ADD = "dialog.add"
    REMOVE = "dialog.remove"
    BROWSE = "dialog.browse"
    YES = "dialog.yes"
    NO = "dialog.no"
    CLOSE = "dialog.close"
    UPDATE = "dialog.update"
    REFRESH = "dialog.refresh"
    
    # Dialog titles
    LOGGING_TITLE = "dialog.logging.title"
    LOGGING_LEVEL = "dialog.logging.level"
    LOGGING_FILE = "dialog.logging.file"
    LOGGING_DISPLAY_LINES = "dialog.logging.display_lines"

class AppConstants:
    """Application text constants"""
    
    TITLE = "app.title"
    LOADING = "app.loading"
    ERROR = "app.error"
    WARNING = "app.warning"
    INFO = "app.info"
    SUCCESS = "app.success"

# Mapping of constants to translation keys
CONSTANT_MAPPING = {
    # Menu constants
    MenuConstants.FILE: ("Datei", "File"),
    MenuConstants.EDIT: ("Bearbeiten", "Edit"),
    MenuConstants.SETTINGS: ("Einstellungen", "Settings"),
    MenuConstants.HELP: ("Hilfe", "Help"),
    MenuConstants.VISIBILITY: ("Sichtbarkeit", "Visibility"),
    MenuConstants.SETTINGS_CHOOSE: ("Einstellungen wählen", "Choose Settings"),
    
    MenuConstants.FILE_OPEN_GPX: ("GPX öffnen", "Open GPX"),
    MenuConstants.FILE_RECENT_FILES: ("Zuletzt verwendet", "Recent Files"),
    MenuConstants.FILE_CLEAR_RECENT: ("Zuletzt verwendet löschen", "Clear Recent Files"),
    MenuConstants.FILE_EXIT: ("Beenden", "Exit"),
    
    MenuConstants.EDIT_OPEN_TABLE_EDITOR: ("Track-Tabelle öffnen", "Open Track Table"),
    MenuConstants.EDIT_TRACK_TO_ROUTE: ("Track zu Route", "Track to Route"),
    MenuConstants.EDIT_ROUTE_TO_TRACK: ("Route zu Track", "Route to Track"),
    
    # Dialog constants
    DialogConstants.OK: ("OK", "OK"),
    DialogConstants.CANCEL: ("Abbrechen", "Cancel"),
    DialogConstants.APPLY: ("Anwenden", "Apply"),
    DialogConstants.SAVE: ("Speichern", "Save"),
    DialogConstants.DELETE: ("Löschen", "Delete"),
    DialogConstants.ADD: ("Hinzufügen", "Add"),
    DialogConstants.REMOVE: ("Entfernen", "Remove"),
    DialogConstants.BROWSE: ("Durchsuchen", "Browse"),
    DialogConstants.YES: ("Ja", "Yes"),
    DialogConstants.NO: ("Nein", "No"),
    DialogConstants.CLOSE: ("Schließen", "Close"),
    DialogConstants.UPDATE: ("Aktualisieren", "Update"),
    DialogConstants.REFRESH: ("Aktualisieren", "Refresh"),
    
    # App constants
    AppConstants.TITLE: ("Toms GPX Editor", "Toms GPX Editor"),
    AppConstants.LOADING: ("Lade...", "Loading..."),
    AppConstants.ERROR: ("Fehler", "Error"),
    AppConstants.WARNING: ("Warnung", "Warning"),
    AppConstants.INFO: ("Information", "Information"),
    AppConstants.SUCCESS: ("Erfolg", "Success"),
}
'''
    
    try:
        with open(constants_file, 'w', encoding='utf-8') as f:
            f.write(constants_content)
        
        print(f"Language constants file created: {constants_file}")
        return True
        
    except Exception as e:
        print(f"Error creating constants file: {e}")
        return False

def create_usage_examples():
    """Create usage examples for the constants"""
    
    examples_file = "W:/TomsGPXEditor/src/i18n/usage_examples.py"
    
    examples_content = '''"""
Language Constants Usage Examples

This file shows how to use the language constants
to replace hardcoded literals with translatable constants.
"""

from src.i18n.constants import MenuConstants, DialogConstants, AppConstants
from src.i18n.language_manager import LanguageManager

class ExampleUsage:
    """Example usage of language constants"""
    
    def __init__(self):
        self.language_manager = LanguageManager()
    
    def create_menu_example(self):
        """Example of creating a menu with constants"""
        
        # Instead of: menubar.add_cascade(label="File", menu=file_menu)
        # Use:
        file_text = self.language_manager.get_text(MenuConstants.FILE)
        menubar.add_cascade(label=file_text, menu=file_menu)
        
        # Instead of: file_menu.add_command(label="Open GPX", command=self.open_gpx)
        # Use:
        open_gpx_text = self.language_manager.get_text(MenuConstants.FILE_OPEN_GPX)
        file_menu.add_command(label=open_gpx_text, command=self.open_gpx)
    
    def create_dialog_example(self):
        """Example of creating a dialog with constants"""
        
        # Instead of: ttk.Button(dialog, text="OK", command=self.ok_clicked)
        # Use:
        ok_text = self.language_manager.get_text(DialogConstants.OK)
        ttk.Button(dialog, text=ok_text, command=self.ok_clicked)
        
        # Instead of: ttk.Button(dialog, text="Cancel", command=self.cancel_clicked)
        # Use:
        cancel_text = self.language_manager.get_text(DialogConstants.CANCEL)
        ttk.Button(dialog, text=cancel_text, command=self.cancel_clicked)
    
    def show_message_example(self):
        """Example of showing messages with constants"""
        
        # Instead of: messagebox.showinfo("Success", "File saved successfully")
        # Use:
        title = self.language_manager.get_text(AppConstants.SUCCESS)
        message = "File saved successfully"  # This would also be a constant
        messagebox.showinfo(title, message)

# Migration Guide
# -----------------
# 
# OLD CODE:
# menubar.add_cascade(label="File", menu=file_menu)
# ttk.Button(dialog, text="OK", command=self.ok_clicked)
# 
# NEW CODE:
# from src.i18n.constants import MenuConstants, DialogConstants
# from src.i18n.language_manager import LanguageManager
# 
# lang_manager = LanguageManager()
# file_text = lang_manager.get_text(MenuConstants.FILE)
# menubar.add_cascade(label=file_text, menu=file_menu)
# 
# ok_text = lang_manager.get_text(DialogConstants.OK)
# ttk.Button(dialog, text=ok_text, command=self.ok_clicked)
'''
    
    try:
        with open(examples_file, 'w', encoding='utf-8') as f:
            f.write(examples_content)
        
        print(f"Usage examples file created: {examples_file}")
        return True
        
    except Exception as e:
        print(f"Error creating examples file: {e}")
        return False

def main():
    """Main function"""
    print("LANGUAGE CONSTANTS GENERATOR")
    print("=" * 50)
    
    success1 = generate_language_constants()
    success2 = create_usage_examples()
    
    if success1 and success2:
        print("\nSUCCESS: Language constants and examples created!")
        print("\nNEXT STEPS:")
        print("1. Import constants in dialog files")
        print("2. Replace hardcoded literals with constants")
        print("3. Use LanguageManager.get_text() for translation")
        print("\nExample migration:")
        print("OLD: menubar.add_cascade(label='File', menu=file_menu)")
        print("NEW: menubar.add_cascade(label=lang_manager.get_text(MenuConstants.FILE), menu=file_menu)")
    else:
        print("\nFAILED: Could not create language files")

if __name__ == "__main__":
    main()
