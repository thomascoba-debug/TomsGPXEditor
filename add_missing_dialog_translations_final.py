#!/usr/bin/env python3
"""
Add Missing Dialog Translations

This script adds the missing dialog translations that are causing warnings.
"""

import json

def add_missing_dialog_translations():
    """Add missing dialog translations to both language files"""
    
    print("ADDING MISSING DIALOG TRANSLATIONS")
    print("=" * 50)
    
    # Missing translations
    missing_translations = {
        "de": {
            "dialog": {
                "select_all": "Alle auswählen",
                "deselect_all": "Alle abwählen",
                "remove_selected": "Ausgewählte entfernen",
                "selected_files": "Ausgewählte Dateien",
                "no_files_selected": "Keine Dateien ausgewählt",
                "track_downsampling": {
                    "downsample_selected_files": "Ausgewählte Dateien downsamplen"
                }
            }
        },
        "en": {
            "dialog": {
                "select_all": "Select All",
                "deselect_all": "Deselect All",
                "remove_selected": "Remove Selected",
                "selected_files": "Selected Files",
                "no_files_selected": "No files selected",
                "track_downsampling": {
                    "downsample_selected_files": "Downsample Selected Files"
                }
            }
        }
    }
    
    for lang, translations in missing_translations.items():
        file_path = f"W:/TomsGPXEditor/src/i18n/translations/{lang}.json"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
            
            print(f"\nProcessing {lang} translations:")
            
            # Merge translations
            for key, value in translations.items():
                if key not in current_data:
                    current_data[key] = value
                    print(f"  Added section: {key}")
                else:
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, dict):
                            if subkey not in current_data[key]:
                                current_data[key][subkey] = subvalue
                                print(f"  Added subsection: {key}.{subkey}")
                            else:
                                for subsubkey, subsubvalue in subvalue.items():
                                    if subsubkey not in current_data[key][subkey]:
                                        current_data[key][subkey][subsubkey] = subsubvalue
                                        print(f"  Added key: {key}.{subkey}.{subsubkey}")
                        else:
                            if subkey not in current_data[key]:
                                current_data[key][subkey] = subvalue
                                print(f"  Added key: {key}.{subkey}")
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, indent=2, ensure_ascii=False)
            
            print(f"  Updated {lang} translations")
            
        except Exception as e:
            print(f"  Error updating {lang} translations: {e}")
            return False
    
    return True

def main():
    """Main function"""
    
    print("ADDING MISSING DIALOG TRANSLATIONS")
    print("=" * 60)
    
    success = add_missing_dialog_translations()
    
    print("\n" + "=" * 60)
    print("TRANSLATIONS UPDATE SUMMARY")
    print("=" * 60)
    
    if success:
        print("SUCCESS: Missing dialog translations added!")
        print("\nAdded translations:")
        print("  - dialog.select_all: 'Alle auswählen' / 'Select All'")
        print("  - dialog.deselect_all: 'Alle abwählen' / 'Deselect All'")
        print("  - dialog.remove_selected: 'Ausgewählte entfernen' / 'Remove Selected'")
        print("  - dialog.selected_files: 'Ausgewählte Dateien' / 'Selected Files'")
        print("  - dialog.no_files_selected: 'Keine Dateien ausgewählt' / 'No files selected'")
        print("  - dialog.track_downsampling.downsample_selected_files")
        print("\nNow all dialogs should show correct translations in both languages!")
    else:
        print("FAILED: Could not add missing translations. Check errors above.")

if __name__ == "__main__":
    main()
