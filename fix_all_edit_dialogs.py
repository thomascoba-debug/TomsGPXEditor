#!/usr/bin/env python3
"""
Fix All Edit Dialog Button Texts

This script fixes all remaining hardcoded English texts in Edit dialogs
to use German language constants.
"""

import os
import re

def fix_track_to_route_dialog():
    """Fix Track to Route dialog"""
    
    print("FIXING TRACK TO ROUTE DIALOG")
    print("=" * 40)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/track_to_route_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix all hardcoded texts
        replacements = [
            (r'text="Convert Routes to Tracks"', 'text=self.language_manager.t("dialog.track_to_route.title")'),
            (r'text="Selected Files"', 'text=self.language_manager.t("dialog.selected_files")'),
            (r'text="Select All"', 'text=self.language_manager.t("dialog.select_all")'),
            (r'text="Deselect All"', 'text=self.language_manager.t("dialog.deselect_all")'),
            (r'text="Remove Selected"', 'text=self.language_manager.t("dialog.remove_selected")'),
            (r'text="Convert to Tracks"', 'text=self.language_manager.t("dialog.convert_to_tracks")'),
            (r'text="No files selected"', 'text=self.language_manager.t("dialog.no_files_selected")'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.complete_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed Track to Route dialog")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def fix_route_to_track_dialog():
    """Fix Route to Track dialog"""
    
    print("\nFIXING ROUTE TO TRACK DIALOG")
    print("=" * 40)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/route_to_track_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix all hardcoded texts
        replacements = [
            (r'text="Downsample Tracks"', 'text=self.language_manager.t("dialog.downsample_tracks")'),
            (r'text="Convert to Routes"', 'text=self.language_manager.t("dialog.convert_to_routes")'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.complete_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed Route to Track dialog")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def fix_track_downsampling_dialog():
    """Fix Track Downsampling dialog"""
    
    print("\nFIXING TRACK DOWNSAMPLING DIALOG")
    print("=" * 40)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/track_downsampling_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix all hardcoded texts
        replacements = [
            (r'text="Select All"', 'text=self.language_manager.t("dialog.select_all")'),
            (r'text="Deselect All"', 'text=self.language_manager.t("dialog.deselect_all")'),
            (r'text="Remove Selected"', 'text=self.language_manager.t("dialog.remove_selected")'),
            (r'text="Downsample Selected Files"', 'text=self.language_manager.t("dialog.downsample_selected_files")'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.complete_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed Track Downsampling dialog")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def add_missing_dialog_translations():
    """Add missing dialog translations"""
    
    print("\nADDING MISSING DIALOG TRANSLATIONS")
    print("=" * 40)
    
    # Missing dialog translations
    missing_translations = {
        "de": {
            "dialog": {
                "track_to_route": {
                    "title": "Routen in Tracks umwandeln",
                    "selected_files": "Ausgewählte Dateien",
                    "select_all": "Alle auswählen",
                    "deselect_all": "Alle abwählen",
                    "remove_selected": "Ausgewählte entfernen",
                    "convert_to_tracks": "In Tracks umwandeln",
                    "no_files_selected": "Keine Dateien ausgewählt"
                },
                "route_to_track": {
                    "downsample_tracks": "Tracks downsamplen",
                    "convert_to_routes": "In Routen umwandeln"
                },
                "track_downsampling": {
                    "downsample_selected_files": "Ausgewählte Dateien downsamplen"
                }
            }
        },
        "en": {
            "dialog": {
                "track_to_route": {
                    "title": "Convert Routes to Tracks",
                    "selected_files": "Selected Files",
                    "select_all": "Select All",
                    "deselect_all": "Deselect All",
                    "remove_selected": "Remove Selected",
                    "convert_to_tracks": "Convert to Tracks",
                    "no_files_selected": "No files selected"
                },
                "route_to_track": {
                    "downsample_tracks": "Downsample Tracks",
                    "convert_to_routes": "Convert to Routes"
                },
                "track_downsampling": {
                    "downsample_selected_files": "Downsample Selected Files"
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
            
            # Merge translations
            for key, value in translations.items():
                if key not in current_data:
                    current_data[key] = value
                else:
                    for subkey, subvalue in value.items():
                        if subkey not in current_data[key]:
                            current_data[key][subkey] = subvalue
                        else:
                            for subsubkey, subsubvalue in subvalue.items():
                                if subsubkey not in current_data[key][subkey]:
                                    current_data[key][subkey][subsubkey] = subsubvalue
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, indent=2, ensure_ascii=False)
            
            print(f"  Updated {lang} dialog translations")
            
        except Exception as e:
            print(f"  Error updating {lang} translations: {e}")
    
    return True

def main():
    """Main function"""
    
    print("FIXING ALL EDIT DIALOG BUTTON TEXTS")
    print("=" * 60)
    
    success1 = fix_track_to_route_dialog()
    success2 = fix_route_to_track_dialog()
    success3 = fix_track_downsampling_dialog()
    success4 = add_missing_dialog_translations()
    
    print("\n" + "=" * 60)
    print("DIALOG FIX SUMMARY")
    print("=" * 60)
    
    if success1 and success2 and success3 and success4:
        print("SUCCESS: All Edit dialogs fixed with German text!")
        print("\nFixed dialogs:")
        print("  - Track to Route: All buttons now German")
        print("  - Route to Track: All buttons now German")
        print("  - Track Downsampling: All buttons now German")
        print("\nAll Edit dialogs should now show complete German text!")
    else:
        print("FAILED: Some dialog fixes failed. Check errors above.")

if __name__ == "__main__":
    main()
