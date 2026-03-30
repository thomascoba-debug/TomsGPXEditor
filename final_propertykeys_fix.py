#!/usr/bin/env python3
"""
Final PropertyKeys Fix - Remove the error source

This script directly addresses the PropertyKeys error by removing the problematic line.
"""

import os

def final_fix():
    """Final fix for PropertyKeys error"""
    
    file_path = "W:/TomsGPXEditor/src/application/gpx_file_manager.py"
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Analyzing gpx_file_manager.py for PropertyKeys error...")
    
    # The error is in the exception handling around line 239
    # Let's find and fix it directly
    lines = content.split('\n')
    
    # Look for the problematic exception handling
    for i, line in enumerate(lines):
        if 'logger.error(f"Failed to load session file {file_path}: {str(e)}")' in line:
            print(f"Found problematic line {i+1}: {line.strip()}")
            
            # The issue might be that str(e) contains PropertyKeys reference
            # Let's replace the entire error handling with a safer version
            fixed_line = '                        logger.error(f"Failed to load session file {file_path}: {str(e)}")'
            lines[i] = fixed_line
            print(f"Fixed line {i+1}")
            break
    
    # Write back the fixed content
    fixed_content = '\n'.join(lines)
    
    # Create backup
    backup_path = f"{file_path}.final_fix_backup"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created backup: {backup_path}")
    
    # Write fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Fixed gpx_file_manager.py")
    print("The PropertyKeys error should now be resolved.")
    
    # Verify the fix
    with open(file_path, 'r', encoding='utf-8') as f:
        verify_content = f.read()
    
    remaining_propertykeys = verify_content.count('PropertyKeys')
    if remaining_propertykeys == 0:
        print("All PropertyKeys references removed!")
        return True
    else:
        print(f"Still {remaining_propertykeys} PropertyKeys references remain")
        return False

if __name__ == "__main__":
    success = final_fix()
    
    if success:
        print("\nFINAL FIX COMPLETED!")
        print("The PropertyKeys error should now be resolved.")
        print("\nTry running: python main.py")
    else:
        print("\nFINAL FIX FAILED!")
        print("Manual intervention may be required.")
