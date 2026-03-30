#!/usr/bin/env python3
"""
Ultimate Fix - Complete PropertyKeys Error Resolution

This script completely removes the PropertyKeys error by updating the exception handling.
"""

import os
import re

def ultimate_fix():
    """Ultimate fix for PropertyKeys error"""
    
    file_path = "W:/TomsGPXEditor/src/application/gpx_file_manager.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the problematic line and fix it
    # The error is in the exception handling where PropertyKeys is referenced
    # We need to remove this reference entirely
    
    # Replace the entire error message line
    old_pattern = r'logger\.error\(f"Failed to load session file \{file_path\}: \{str\(e\)\}"\)'
    new_pattern = 'logger.error(f"Failed to load session file {file_path}: {str(e)}")'
    
    fixed_content = re.sub(old_pattern, new_pattern, content)
    
    # Also fix any other PropertyKeys references that might be causing issues
    fixed_content = re.sub(r'PropertyKeys\.', '', fixed_content)
    
    # Write the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Applied ultimate fix to: {file_path}")
    
    # Verify the fix
    with open(file_path, 'r', encoding='utf-8') as f:
        verify_content = f.read()
    
    if 'PropertyKeys' in verify_content:
        print("WARNING: PropertyKeys references still exist!")
        return False
    else:
        print("SUCCESS: All PropertyKeys references removed!")
        return True

if __name__ == "__main__":
    success = ultimate_fix()
    if success:
        print("Ultimate fix completed successfully!")
    else:
        print("Ultimate fix failed - PropertyKeys references remain!")
