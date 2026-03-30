#!/usr/bin/env python3
"""
Fix English Dialog Translations

This script fixes the English dialog translations that currently contain German text.
"""

import json

def fix_english_dialog_translations():
    """Fix English dialog translations"""
    
    print("FIXING ENGLISH DIALOG TRANSLATIONS")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/i18n/translations/en.json"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("Current dialog section (should be English):")
        if 'dialog' in data:
            for key, value in data['dialog'].items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for subkey, subvalue in value.items():
                        print(f"    {subkey}: {subvalue}")
                else:
                    print(f"  {key}: {value}")
        
        # Fix the dialog section with proper English translations
        data['dialog'] = {
            "ok": "OK",
            "cancel": "Cancel",
            "apply": "Apply",
            "save": "Save",
            "delete": "Delete",
            "add": "Add",
            "remove": "Remove",
            "browse": "Browse",
            "yes": "Yes",
            "no": "No",
            "close": "Close",
            "update": "Update",
            "refresh": "Refresh",
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
        
        # Create backup
        backup_path = f"{file_path}.english_fix_backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Write fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\nFixed dialog section (now English):")
        for key, value in data['dialog'].items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for subkey, subvalue in value.items():
                    print(f"    {subkey}: {subvalue}")
            else:
                print(f"  {key}: {value}")
        
        print(f"\nBackup created: {backup_path}")
        print("English dialog translations fixed!")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function"""
    
    print("FIXING ENGLISH DIALOG TRANSLATIONS")
    print("=" * 60)
    
    success = fix_english_dialog_translations()
    
    print("\n" + "=" * 60)
    print("ENGLISH TRANSLATIONS FIX SUMMARY")
    print("=" * 60)
    
    if success:
        print("SUCCESS: English dialog translations fixed!")
        print("\nChanges made:")
        print("  - Fixed dialog.ok, dialog.cancel, etc. to English")
        print("  - Fixed track_to_route dialog texts to English")
        print("  - Fixed route_to_track dialog texts to English")
        print("  - Fixed track_downsampling dialog texts to English")
        print("  - Created backup before changes")
        print("\nNow when language is set to English, all buttons should show English text!")
    else:
        print("FAILED: Could not fix English translations. Check errors above.")

if __name__ == "__main__":
    main()
