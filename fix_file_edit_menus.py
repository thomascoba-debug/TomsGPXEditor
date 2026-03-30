#!/usr/bin/env python3
"""
Fix File and Edit Menu Constants

This script fixes the hardcoded strings in File and Edit menus
to use language constants like the Settings menu.
"""

import os
import re

def fix_file_menu():
    """Fix File menu in app.py"""
    
    print("FIXING FILE MENU")
    print("=" * 40)
    
    file_path = "W:/TomsGPXEditor/app.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Add language manager import if not present
        if 'from src.i18n import t' not in content:
            # Find imports section
            lines = content.split('\n')
            import_added = False
            
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    # Add language import after the first import
                    lines.insert(i + 1, 'from src.i18n import t')
                    import_added = True
                    break
            
            if import_added:
                content = '\n'.join(lines)
                print("  Added language import")
        
        # Fix File menu items
        content = re.sub(
            r'file_menu\.add_command\(label="Open GPX"',
            'file_menu.add_command(label=t("menu.file_open_gpx")',
            content
        )
        
        content = re.sub(
            r'file_menu\.add_cascade\(label="Recent Files"',
            'file_menu.add_cascade(label=t("menu.file_recent_files")',
            content
        )
        
        content = re.sub(
            r'file_menu\.add_command\(label="Exit"',
            'file_menu.add_command(label=t("menu.file_exit")',
            content
        )
        
        content = re.sub(
            r'menubar\.add_cascade\(label="File"',
            'menubar.add_cascade(label=t("menu.file")',
            content
        )
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.file_menu_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed File menu with language constants")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed for File menu")
            
    except Exception as e:
        print(f"  Error fixing File menu: {e}")
        return False
    
    return True

def fix_edit_menu():
    """Fix Edit menu in dialog_controller.py"""
    
    print("\nFIXING EDIT MENU")
    print("=" * 40)
    
    file_path = "W:/TomsGPXEditor/src/application/dialog_controller.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix Edit menu items
        content = re.sub(
            r'label="Open Track Table Editor"',
            'label=self.language_manager.t("menu.edit_open_table_editor")',
            content
        )
        
        content = re.sub(
            r'label="Track to Route"',
            'label=self.language_manager.t("menu.edit_track_to_route")',
            content
        )
        
        content = re.sub(
            r'label="Route to Track"',
            'label=self.language_manager.t("menu.edit_route_to_track")',
            content
        )
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.edit_menu_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed Edit menu with language constants")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed for Edit menu")
            
    except Exception as e:
        print(f"  Error fixing Edit menu: {e}")
        return False
    
    return True

def add_missing_menu_translations():
    """Add missing menu translations"""
    
    print("\nADDING MISSING MENU TRANSLATIONS")
    print("=" * 40)
    
    # Missing menu translations
    missing_translations = {
        "de": {
            "menu": {
                "edit_open_table_editor": "Track-Tabelle öffnen",
                "edit_track_to_route": "Track zu Route",
                "edit_route_to_track": "Route zu Track"
            }
        },
        "en": {
            "menu": {
                "edit_open_table_editor": "Open Track Table",
                "edit_track_to_route": "Track to Route",
                "edit_route_to_track": "Route to Track"
            }
        }
    }
    
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
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, indent=2, ensure_ascii=False)
            
            print(f"  Updated {lang} menu translations")
            
        except Exception as e:
            print(f"  Error updating {lang} translations: {e}")
    
    return True

def main():
    """Main function"""
    
    print("FIXING FILE AND EDIT MENU CONSTANTS")
    print("=" * 60)
    
    success1 = fix_file_menu()
    success2 = fix_edit_menu()
    success3 = add_missing_menu_translations()
    
    print("\n" + "=" * 60)
    print("MENU FIX SUMMARY")
    print("=" * 60)
    
    if success1 and success2 and success3:
        print("SUCCESS: All menus fixed with language constants!")
        print("\nFixed menus:")
        print("  - File menu: Open GPX, Recent Files, Exit")
        print("  - Edit menu: Open Track Table, Track to Route, Route to Track")
        print("\nThe application should now show German text in all menus!")
    else:
        print("FAILED: Some menu fixes failed. Check errors above.")

if __name__ == "__main__":
    import json
    main()
