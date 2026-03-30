#!/usr/bin/env python3
"""
Dialog Language Migration Tool

This script migrates hardcoded literals in dialog files to use language constants.
"""

import os
import re

def migrate_dialog_files():
    """Migrate dialog files to use language constants"""
    
    print("MIGRATING DIALOG FILES TO LANGUAGE CONSTANTS")
    print("=" * 60)
    
    # Files to migrate
    dialog_files = [
        "src/application/dialog_controller.py",
        "src/ui/dialogs/route_to_track_dialog.py",
        "src/ui/dialogs/track_downsampling_dialog.py",
        "src/ui/dialogs/settings_properties_dialog.py",
        "src/ui/widgets/gpx_table_editor.py",
        "src/ui/widgets/progress_dialog.py",
        "src/ui/widgets/file_search.py"
    ]
    
    migration_rules = [
        # Menu items
        (r'label="File"', 'label=lang_manager.get_text(MenuConstants.FILE)'),
        (r'label="Edit"', 'label=lang_manager.get_text(MenuConstants.EDIT)'),
        (r'label="Settings"', 'label=lang_manager.get_text(MenuConstants.SETTINGS)'),
        (r'label="Help"', 'label=lang_manager.get_text(MenuConstants.HELP)'),
        (r'label="Close"', 'label=lang_manager.get_text(DialogConstants.CLOSE)'),
        (r'label="OK"', 'label=lang_manager.get_text(DialogConstants.OK)'),
        (r'label="Cancel"', 'label=lang_manager.get_text(DialogConstants.CANCEL)'),
        (r'label="Apply"', 'label=lang_manager.get_text(DialogConstants.APPLY)'),
        (r'label="Save"', 'label=lang_manager.get_text(DialogConstants.SAVE)'),
        (r'label="Delete"', 'label=lang_manager.get_text(DialogConstants.DELETE)'),
        (r'label="Add"', 'label=lang_manager.get_text(DialogConstants.ADD)'),
        (r'label="Remove"', 'label=lang_manager.get_text(DialogConstants.REMOVE)'),
        (r'label="Browse"', 'label=lang_manager.get_text(DialogConstants.BROWSE)'),
        (r'text="Close"', 'text=lang_manager.get_text(DialogConstants.CLOSE)'),
        (r'text="OK"', 'text=lang_manager.get_text(DialogConstants.OK)'),
        (r'text="Cancel"', 'text=lang_manager.get_text(DialogConstants.CANCEL)'),
        (r'text="Apply"', 'text=lang_manager.get_text(DialogConstants.APPLY)'),
        (r'text="Save"', 'text=lang_manager.get_text(DialogConstants.SAVE)'),
        (r'text="Delete"', 'text=lang_manager.get_text(DialogConstants.DELETE)'),
        (r'text="Search"', 'text=lang_manager.get_text(MenuConstants.FILE_OPEN_GPX)'),
        (r'text="Clear"', 'text=lang_manager.get_text(MenuConstants.FILE_CLEAR_RECENT)'),
    ]
    
    total_migrations = 0
    
    for file_path in dialog_files:
        full_path = f"W:/TomsGPXEditor/{file_path}"
        
        if not os.path.exists(full_path):
            print(f"File not found: {file_path}")
            continue
        
        print(f"\nProcessing: {file_path}")
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Add necessary imports if not present
            if 'from src.i18n.constants import' not in content:
                # Find the first import line and add after it
                lines = content.split('\n')
                import_added = False
                
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        # Add language imports after the first import
                        lines.insert(i + 1, 'from src.i18n.constants import MenuConstants, DialogConstants')
                        lines.insert(i + 2, 'from src.i18n.language_manager import LanguageManager')
                        import_added = True
                        break
                
                if import_added:
                    content = '\n'.join(lines)
                    print("  Added language imports")
            
            # Add language manager initialization if not present
            if 'LanguageManager()' not in content and 'self.language_manager' not in content:
                # Find the __init__ method
                lines = content.split('\n')
                init_found = False
                
                for i, line in enumerate(lines):
                    if 'def __init__' in line:
                        # Find the next non-empty line and add language manager
                        j = i + 1
                        while j < len(lines) and (not lines[j].strip() or lines[j].strip().startswith('#')):
                            j += 1
                        
                        if j < len(lines):
                            lines.insert(j, '        self.language_manager = LanguageManager()')
                            content = '\n'.join(lines)
                            print("  Added language manager initialization")
                            init_found = True
                            break
                
                if not init_found:
                    print("  Warning: Could not find __init__ method")
            
            # Apply migration rules
            file_migrations = 0
            for pattern, replacement in migration_rules:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    file_migrations += 1
            
            if content != original_content:
                # Create backup
                backup_path = f"{full_path}.language_migration_backup"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write migrated content
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  Migrated {file_migrations} literals")
                print(f"  Backup created: {backup_path}")
                total_migrations += file_migrations
            else:
                print("  No migrations needed")
                
        except Exception as e:
            print(f"  Error processing {file_path}: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"MIGRATION SUMMARY")
    print(f"Total files processed: {len(dialog_files)}")
    print(f"Total migrations: {total_migrations}")
    print(f"\nNEXT STEPS:")
    print(f"1. Test the migrated files")
    print(f"2. Check for any missing constants")
    print(f"3. Add any new constants as needed")
    print(f"4. Test language switching functionality")

if __name__ == "__main__":
    migrate_dialog_files()
