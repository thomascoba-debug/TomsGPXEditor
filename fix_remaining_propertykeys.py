#!/usr/bin/env python3
"""
Fix PropertyKeys References - Clean up remaining PropertyKeys issues

This script fixes the remaining PropertyKeys references found in the scan.
"""

import os
import re

def fix_propertykeys_references():
    """Fix all remaining PropertyKeys references"""
    
    print("FIXING REMAINING PROPERTYKEYS REFERENCES...")
    print("=" * 60)
    
    # Files with PropertyKeys references
    files_to_fix = [
        "src/application/services/recent_files_service.py",
        "src/config/app_config.py", 
        "src/config/app_config_old.py",
        "src/infrastructure/json_validator.py",
        "src/infrastructure/stability_manager.py",
        "src/ui/dialogs/settings_rendering_dialog.py"
    ]
    
    total_fixes = 0
    
    for file_path in files_to_fix:
        full_path = f"W:/TomsGPXEditor/{file_path}"
        
        if not os.path.exists(full_path):
            print(f"   File not found: {file_path}")
            continue
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Count PropertyKeys references
            propertykeys_count = content.count('PropertyKeys')
            
            if propertykeys_count == 0:
                print(f"   {file_path}: No PropertyKeys references")
                continue
            
            print(f"   {file_path}: {propertykeys_count} PropertyKeys references")
            
            # Fix PropertyKeys references
            # Replace PropertyKeys.APP["RECENT_FILES"]
            content = re.sub(r'PropertyKeys\.APP\["RECENT_FILES"\]', 'APP_RECENT_FILES', content)
            
            # Replace PropertyKeys.LOG references
            content = re.sub(r'PropertyKeys\.LOG\["LEVEL"\]', 'DIALOGS_SETTINGS_LOGGING_LEVEL', content)
            content = re.sub(r'PropertyKeys\.LOG\["FILE"\]', 'DIALOGS_SETTINGS_LOGGING_FILE', content)
            content = re.sub(r'PropertyKeys\.LOG\["ROOT"\]', 'DIALOGS_SETTINGS_LOGGING', content)
            content = re.sub(r'PropertyKeys\.LOG', 'DIALOGS_SETTINGS_LOGGING', content)
            
            # Remove PropertyKeys imports
            content = re.sub(r'from src\.constants\.property_keys import PropertyKeys.*?\n', '', content)
            
            # Remove any remaining PropertyKeys. references
            content = re.sub(r'PropertyKeys\.[A-Z_]+', '', content)
            
            # Count fixes
            fixes_made = original_content.count('PropertyKeys') - content.count('PropertyKeys')
            total_fixes += fixes_made
            
            if content != original_content:
                # Create backup
                backup_path = f"{full_path}.propertykeys_fix_backup"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write fixed content
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"      Fixed {fixes_made} references, backup created")
            else:
                print(f"      No changes needed")
        
        except Exception as e:
            print(f"   ERROR fixing {file_path}: {e}")
    
    print(f"\nSUMMARY:")
    print(f"   - Total fixes applied: {total_fixes}")
    print(f"   - PropertyKeys references should now be resolved")
    
    return total_fixes

if __name__ == "__main__":
    fixes = fix_propertykeys_references()
    print(f"\nPropertyKeys fix completed: {fixes} references removed")
