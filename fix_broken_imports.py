#!/usr/bin/env python3
"""
Fix Broken Imports - Repair PropertyKeys imports after refactoring

This script fixes the broken imports caused by the PropertyKeys class removal.
"""

import os
import re

class ImportFixer:
    def __init__(self):
        self.src_dir = "W:/TomsGPXEditor/src"
        self.files_to_fix = [
            "ui/dialogs/settings_logging_dialog.py",
            "infrastructure/json_validator.py",
            "ui/dialogs/settings_rendering_dialog.py", 
            "infrastructure/stability_manager.py",
            "config/app_config.py"
        ]
        
    def fix_property_keys_imports(self):
        """Fix PropertyKeys imports in all affected files"""
        print("Fixing PropertyKeys imports...")
        
        for file_path in self.files_to_fix:
            full_path = os.path.join(self.src_dir, file_path)
            if os.path.exists(full_path):
                self._fix_file_imports(full_path)
    
    def _fix_file_imports(self, file_path):
        """Fix imports in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Remove PropertyKeys import
            content = re.sub(
                r'from src\.constants\.property_keys import PropertyKeys.*?\n',
                '',
                content
            )
            
            # Replace PropertyKeys.LOG usage with DIALOGS_SETTINGS_LOGGING
            content = re.sub(
                r'PropertyKeys\.LOG\["LEVEL"\]',
                'DIALOGS_SETTINGS_LOGGING_LEVEL',
                content
            )
            
            content = re.sub(
                r'PropertyKeys\.LOG\["FILE"\]',
                'DIALOGS_SETTINGS_LOGGING_FILE',
                content
            )
            
            content = re.sub(
                r'PropertyKeys\.LOG\["ROOT"\]',
                'DIALOGS_SETTINGS_LOGGING',
                content
            )
            
            # Replace PropertyKeys.APP usage
            content = re.sub(
                r'PropertyKeys\.APP\["RECENT_FILES"\]',
                'APP_RECENT_FILES',
                content
            )
            
            # Add new imports at the top
            if 'DIALOGS_SETTINGS_LOGGING' in content:
                import_addition = 'from src.constants.property_keys import DIALOGS_SETTINGS_LOGGING_LEVEL, DIALOGS_SETTINGS_LOGGING_FILE, DIALOGS_SETTINGS_LOGGING\n'
                content = import_addition + content
            
            if 'APP_RECENT_FILES' in content and 'APP_RECENT_FILES' not in content:
                if 'from src.constants.property_keys import' in content:
                    content = re.sub(
                        r'from src\.constants\.property_keys import (.+)\n',
                        r'from src.constants.property_keys import \1, APP_RECENT_FILES\n',
                        content
                    )
                else:
                    content = 'from src.constants.property_keys import APP_RECENT_FILES\n' + content
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  - Fixed: {file_path}")
            else:
                print(f"  - No changes needed: {file_path}")
                
        except Exception as e:
            print(f"  - Error fixing {file_path}: {e}")
    
    def add_missing_constants(self):
        """Add missing constants to property_keys.py"""
        print("Adding missing constants...")
        
        property_keys_file = os.path.join(self.src_dir, "constants/property_keys.py")
        
        with open(property_keys_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add missing constants if not present
        needed_constants = {
            'DIALOGS_SETTINGS_LOGGING_LEVEL': 'dialogs.settings.logging.level',
            'DIALOGS_SETTINGS_LOGGING_FILE': 'dialogs.settings.logging.file',
            'DIALOGS_SETTINGS_LOGGING': 'dialogs.settings.logging',
            'DIALOGS_SETTINGS_RENDERING': 'dialogs.settings.rendering',
            'FILES_SESSION': 'files.session'
        }
        
        for const_name, const_value in needed_constants.items():
            if const_name not in content:
                # Add constant at the end
                content += f'\n{const_name} = "{const_value}"'
                print(f"  - Added constant: {const_name}")
        
        # Write back
        with open(property_keys_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def fix_all_imports(self):
        """Fix all broken imports"""
        print("Starting import fixes...")
        
        # Step 1: Add missing constants
        self.add_missing_constants()
        
        # Step 2: Fix PropertyKeys imports
        self.fix_property_keys_imports()
        
        print("Import fixes complete!")

def main():
    """Main function"""
    fixer = ImportFixer()
    fixer.fix_all_imports()

if __name__ == "__main__":
    main()
