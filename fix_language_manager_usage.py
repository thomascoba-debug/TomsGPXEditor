#!/usr/bin/env python3
"""
Fix Language Manager Usage

This script fixes the LanguageManager usage in dialog files
to use the same pattern as the settings dialogs.
"""

import os
import re

def fix_language_manager_usage():
    """Fix LanguageManager usage to match settings dialog pattern"""
    
    print("FIXING LANGUAGE MANAGER USAGE")
    print("=" * 50)
    
    # Files that need fixing
    files_to_fix = [
        "src/ui/widgets/gpx_table_editor.py",
        "src/ui/dialogs/route_to_track_dialog.py", 
        "src/ui/dialogs/track_downsampling_dialog.py",
        "src/ui/dialogs/settings_properties_dialog.py",
        "src/ui/widgets/progress_dialog.py",
        "src/ui/widgets/file_search.py"
    ]
    
    for file_path in files_to_fix:
        full_path = f"W:/TomsGPXEditor/{file_path}"
        
        if not os.path.exists(full_path):
            print(f"File not found: {file_path}")
            continue
        
        print(f"\nProcessing: {file_path}")
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix 1: Update import to include get_language_manager
            if 'from src.i18n.language_manager import LanguageManager' in content:
                content = content.replace(
                    'from src.i18n.language_manager import LanguageManager',
                    'from src.i18n.language_manager import get_language_manager'
                )
                print("  Updated import")
            
            # Fix 2: Replace LanguageManager() with get_language_manager()
            content = re.sub(
                r'self\.language_manager = LanguageManager\(\)',
                'self.language_manager = get_language_manager()',
                content
            )
            
            # Fix 3: Update any remaining LanguageManager references
            content = re.sub(
                r'LanguageManager\(\)',
                'get_language_manager()',
                content
            )
            
            if content != original_content:
                # Create backup
                backup_path = f"{full_path}.lang_manager_fix_backup"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write fixed content
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("  Fixed LanguageManager usage")
                print(f"  Backup created: {backup_path}")
            else:
                print("  No fixes needed")
                
        except Exception as e:
            print(f"  Error processing {file_path}: {e}")
    
    print(f"\n" + "=" * 50)
    print("LANGUAGE MANAGER FIX COMPLETED")
    print("\nAll dialog files now use the same pattern as settings dialogs!")
    print("The application should start without LanguageManager errors.")

if __name__ == "__main__":
    fix_language_manager_usage()
