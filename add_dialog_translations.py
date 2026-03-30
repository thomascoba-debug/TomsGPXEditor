#!/usr/bin/env python3
"""
Add Missing Dialog Translations

This script adds the missing dialog section to the translation files
using a direct file manipulation approach.
"""

import json
import os

def add_dialog_translations():
    """Add missing dialog translations"""
    
    print("ADDING MISSING DIALOG TRANSLATIONS")
    print("=" * 50)
    
    # Define the dialog section
    dialog_section = {
        "ok": "OK",
        "cancel": "Abbrechen",
        "apply": "Anwenden",
        "save": "Speichern",
        "delete": "Löschen",
        "add": "Hinzufügen",
        "remove": "Entfernen",
        "browse": "Durchsuchen",
        "yes": "Ja",
        "no": "Nein",
        "close": "Schließen",
        "update": "Aktualisieren",
        "refresh": "Aktualisieren"
    }
    
    # Update German translations
    de_file = "W:/TomsGPXEditor/src/i18n/translations/de.json"
    
    try:
        with open(de_file, 'r', encoding='utf-8') as f:
            de_data = json.load(f)
        
        # Add dialog section if not exists
        if "dialog" not in de_data:
            de_data["dialog"] = dialog_section
            print("Added dialog section to German translations")
        else:
            print("Dialog section already exists in German translations")
        
        # Write back
        with open(de_file, 'w', encoding='utf-8') as f:
            json.dump(de_data, f, indent=2, ensure_ascii=False)
        
        print("German translations updated successfully")
        
    except Exception as e:
        print(f"Error updating German translations: {e}")
        return False
    
    # Update English translations
    en_file = "W:/TomsGPXEditor/src/i18n/translations/en.json"
    
    try:
        with open(en_file, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
        
        # Add dialog section if not exists
        if "dialog" not in en_data:
            en_data["dialog"] = dialog_section
            print("Added dialog section to English translations")
        else:
            print("Dialog section already exists in English translations")
        
        # Write back
        with open(en_file, 'w', encoding='utf-8') as f:
            json.dump(en_data, f, indent=2, ensure_ascii=False)
        
        print("English translations updated successfully")
        
    except Exception as e:
        print(f"Error updating English translations: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = add_dialog_translations()
    
    if success:
        print("\nSUCCESS: Dialog translations added!")
        print("The application should now find the missing translations.")
    else:
        print("\nFAILED: Could not add dialog translations.")
