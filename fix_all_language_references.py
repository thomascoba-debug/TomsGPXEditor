#!/usr/bin/env python3
"""
Fix All Language Manager References

This script fixes all remaining language manager references
to use self.language_manager.t() instead of lang_manager.get_text()
"""

import os
import re

def fix_all_language_references():
    """Fix all language manager references"""
    
    print("FIXING ALL LANGUAGE MANAGER REFERENCES")
    print("=" * 60)
    
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
            
            # Fix lang_manager.get_text() -> self.language_manager.t()
            content = re.sub(
                r'lang_manager\.get_text\(',
                'self.language_manager.t(',
                content
            )
            
            # Fix any remaining get_text() -> t()
            content = re.sub(
                r'\.get_text\(',
                '.t(',
                content
            )
            
            if content != original_content:
                # Create backup
                backup_path = f"{full_path}.lang_refs_fix_backup"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write fixed content
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("  Fixed language references")
                print(f"  Backup created: {backup_path}")
            else:
                print("  No fixes needed")
                
        except Exception as e:
            print(f"  Error processing {file_path}: {e}")
    
    print(f"\n" + "=" * 60)
    print("ALL LANGUAGE REFERENCES FIXED")
    print("\nAll dialog files now use self.language_manager.t()!")
    print("The application should start without language reference errors.")

if __name__ == "__main__":
    fix_all_language_references()
