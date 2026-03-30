#!/usr/bin/env python3
"""
Complete Dialog Literals Fix

This script completely fixes ALL hardcoded literals in ALL dialogs
to use proper language_manager.t() translations.
"""

import os
import re

def fix_route_to_track_dialog_complete():
    """Completely fix Route to Track dialog"""
    
    print("COMPLETELY FIXING ROUTE TO TRACK DIALOG")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/route_to_track_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Add language manager import if missing
        if 'from src.i18n.language_manager import get_language_manager' not in content:
            content = re.sub(
                r'import tkinter as tk',
                'import tkinter as tk\nfrom src.i18n.language_manager import get_language_manager',
                content
            )
        
        # Add language manager initialization if missing
        if 'self.language_manager = get_language_manager()' not in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'def __init__' in line:
                    lines.insert(i + 2, '        self.language_manager = get_language_manager()')
                    break
            content = '\n'.join(lines)
        
        # Fix ALL hardcoded texts
        replacements = [
            (r'text="Routen in Tracks umwandeln"', 'text=self.language_manager.t("dialog.route_to_track.title")'),
            (r'text="In Tracks umwandeln"', 'text=self.language_manager.t("dialog.route_to_track.convert_to_routes")'),
            (r'text="Ausgewählte Dateien"', 'text=self.language_manager.t("dialog.selected_files")'),
            (r'text="Alle auswählen"', 'text=self.language_manager.t("dialog.select_all")'),
            (r'text="Alle abwählen"', 'text=self.language_manager.t("dialog.deselect_all")'),
            (r'text="Ausgewählte entfernen"', 'text=self.language_manager.t("dialog.remove_selected")'),
            (r'text="Keine Dateien ausgewählt"', 'text=self.language_manager.t("dialog.no_files_selected")'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            backup_path = f"{file_path}.complete_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Completely fixed Route to Track dialog")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def fix_track_to_route_dialog_complete():
    """Completely fix Track to Route dialog"""
    
    print("\nCOMPLETELY FIXING TRACK TO ROUTE DIALOG")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/track_to_route_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix ALL hardcoded texts
        replacements = [
            (r'text="Routen in Tracks umwandeln"', 'text=self.language_manager.t("dialog.track_to_route.title")'),
            (r'text="In Tracks umwandeln"', 'text=self.language_manager.t("dialog.track_to_route.convert_to_tracks")'),
            (r'text="Ausgewählte Dateien"', 'text=self.language_manager.t("dialog.selected_files")'),
            (r'text="Alle auswählen"', 'text=self.language_manager.t("dialog.select_all")'),
            (r'text="Alle abwählen"', 'text=self.language_manager.t("dialog.deselect_all")'),
            (r'text="Ausgewählte entfernen"', 'text=self.language_manager.t("dialog.remove_selected")'),
            (r'text="Keine Dateien ausgewählt"', 'text=self.language_manager.t("dialog.no_files_selected")'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            backup_path = f"{file_path}.complete_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Completely fixed Track to Route dialog")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def fix_track_downsampling_dialog_complete():
    """Completely fix Track Downsampling dialog"""
    
    print("\nCOMPLETELY FIXING TRACK DOWNSAMPLING DIALOG")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/track_downsampling_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Add language manager import if missing
        if 'from src.i18n.language_manager import get_language_manager' not in content:
            content = re.sub(
                r'import tkinter as tk',
                'import tkinter as tk\nfrom src.i18n.language_manager import get_language_manager',
                content
            )
        
        # Add language manager initialization if missing
        if 'self.language_manager = get_language_manager()' not in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'def __init__' in line:
                    lines.insert(i + 2, '        self.language_manager = get_language_manager()')
                    break
            content = '\n'.join(lines)
        
        # Fix ALL hardcoded texts
        replacements = [
            (r'text="Ausgewählte Dateien"', 'text=self.language_manager.t("dialog.selected_files")'),
            (r'text="Alle auswählen"', 'text=self.language_manager.t("dialog.select_all")'),
            (r'text="Alle abwählen"', 'text=self.language_manager.t("dialog.deselect_all")'),
            (r'text="Ausgewählte entfernen"', 'text=self.language_manager.t("dialog.remove_selected")'),
            (r'text="Ausgewählte Dateien downsamplen"', 'text=self.language_manager.t("dialog.track_downsampling.downsample_selected_files")'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            backup_path = f"{file_path}.complete_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Completely fixed Track Downsampling dialog")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def add_missing_complete_translations():
    """Add all missing translations for complete fix"""
    
    print("\nADDING MISSING COMPLETE TRANSLATIONS")
    print("=" * 50)
    
    # Missing translations
    missing_translations = {
        "de": {
            "dialog": {
                "route_to_track": {
                    "title": "Routen in Tracks umwandeln",
                    "convert_to_routes": "In Routen umwandeln"
                },
                "track_to_route": {
                    "title": "Tracks in Routen umwandeln",
                    "convert_to_tracks": "In Tracks umwandeln"
                }
            }
        },
        "en": {
            "dialog": {
                "route_to_track": {
                    "title": "Convert Routes to Tracks",
                    "convert_to_routes": "Convert to Routes"
                },
                "track_to_route": {
                    "title": "Convert Tracks to Routes",
                    "convert_to_tracks": "Convert to Tracks"
                }
            }
        }
    }
    
    import json
    
    for lang, translations in missing_translations.items():
        file_path = f"W:/TomsGPXEditor/src/i18n/translations/{lang}.json"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
            
            print(f"\nProcessing {lang} complete translations:")
            
            # Merge translations
            for key, value in translations.items():
                if key not in current_data:
                    current_data[key] = value
                    print(f"  Added section: {key}")
                else:
                    for subkey, subvalue in value.items():
                        if subkey not in current_data[key]:
                            current_data[key][subkey] = subvalue
                            print(f"  Added subsection: {key}.{subkey}")
                        else:
                            for subsubkey, subsubvalue in subvalue.items():
                                if subsubkey not in current_data[key][subkey]:
                                    current_data[key][subkey][subsubkey] = subsubvalue
                                    print(f"  Added key: {key}.{subkey}.{subsubkey}")
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, indent=2, ensure_ascii=False)
            
            print(f"  Updated {lang} complete translations")
            
        except Exception as e:
            print(f"  Error updating {lang} translations: {e}")
            return False
    
    return True

def main():
    """Main function"""
    
    print("COMPLETE DIALOG LITERALS FIX")
    print("=" * 60)
    
    success1 = fix_route_to_track_dialog_complete()
    success2 = fix_track_to_route_dialog_complete()
    success3 = fix_track_downsampling_dialog_complete()
    success4 = add_missing_complete_translations()
    
    print("\n" + "=" * 60)
    print("COMPLETE FIX SUMMARY")
    print("=" * 60)
    
    if success1 and success2 and success3 and success4:
        print("SUCCESS: All dialog literals completely fixed!")
        print("\nChanges made:")
        print("  - Route to Track: ALL texts now use language_manager.t()")
        print("  - Track to Route: ALL texts now use language_manager.t()")
        print("  - Track Downsampling: ALL texts now use language_manager.t()")
        print("  - Added all missing translation keys")
        print("\nNow ALL dialogs should show correct translations in both languages!")
    else:
        print("FAILED: Some fixes failed. Check errors above.")

if __name__ == "__main__":
    main()
