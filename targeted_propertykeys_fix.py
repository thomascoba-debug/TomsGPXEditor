#!/usr/bin/env python3
"""
Targeted PropertyKeys Fix - Find and remove the exact problematic reference

This script specifically targets the PropertyKeys error in gpx_file_manager.py
"""

import os
import re

def targeted_fix():
    """Targeted fix for PropertyKeys error"""
    
    file_path = "W:/TomsGPXEditor/src/application/gpx_file_manager.py"
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Searching for PropertyKeys references...")
    
    # Find all lines with PropertyKeys
    lines = content.split('\n')
    propertykeys_lines = []
    
    for i, line in enumerate(lines, 1):
        if 'PropertyKeys' in line and not line.strip().startswith('#'):
            propertykeys_lines.append((i, line.strip()))
    
    print(f"Found {len(propertykeys_lines)} PropertyKeys references:")
    for line_num, line_content in propertykeys_lines:
        print(f"  Line {line_num}: {line_content}")
    
    if not propertykeys_lines:
        print("No PropertyKeys references found - this is strange")
        return False
    
    # Fix each PropertyKeys reference
    fixed_lines = lines.copy()
    fixes_made = 0
    
    for line_num, line_content in propertykeys_lines:
        original_line = lines[line_num - 1]
        
        # Replace PropertyKeys references with appropriate constants
        fixed_line = original_line
        
        # Common replacements
        if 'PropertyKeys.APP["RECENT_FILES"]' in fixed_line:
            fixed_line = fixed_line.replace('PropertyKeys.APP["RECENT_FILES"]', 'APP_RECENT_FILES')
            fixes_made += 1
            print(f"Fixed: PropertyKeys.APP['RECENT_FILES'] -> APP_RECENT_FILES")
        
        elif 'PropertyKeys.LOG' in fixed_line:
            fixed_line = fixed_line.replace('PropertyKeys.LOG', 'DIALOGS_SETTINGS_LOGGING')
            fixes_made += 1
            print(f"Fixed: PropertyKeys.LOG -> DIALOGS_SETTINGS_LOGGING")
        
        elif 'PropertyKeys.' in fixed_line:
            # Generic PropertyKeys reference
            fixed_line = re.sub(r'PropertyKeys\.[A-Z_]+', '', fixed_line)
            fixes_made += 1
            print(f"Fixed: Generic PropertyKeys reference in line {line_num}")
        
        # Update the line
        fixed_lines[line_num - 1] = fixed_line
    
    if fixes_made > 0:
        # Write back the fixed content
        fixed_content = '\n'.join(fixed_lines)
        
        # Create backup
        backup_path = f"{file_path}.targeted_fix_backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created backup: {backup_path}")
        
        # Write fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✅ Applied {fixes_made} fixes to {file_path}")
        print("✅ File has been updated")
        
        # Verify the fix
        with open(file_path, 'r', encoding='utf-8') as f:
            verify_content = f.read()
        
        remaining_propertykeys = verify_content.count('PropertyKeys')
        if remaining_propertykeys == 0:
            print("✅ All PropertyKeys references removed!")
            return True
        else:
            print(f"⚠️  Still {remaining_propertykeys} PropertyKeys references remain")
            return False
    else:
        print("No fixes were needed")
        return True

if __name__ == "__main__":
    success = targeted_fix()
    
    if success:
        print("\n🎉 TARGETED FIX COMPLETED!")
        print("The PropertyKeys error should now be resolved.")
        print("\n🚀 Try running: python main.py")
    else:
        print("\n❌ TARGETED FIX FAILED!")
        print("Manual intervention may be required.")
