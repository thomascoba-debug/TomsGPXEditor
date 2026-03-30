#!/usr/bin/env python3
"""
Complete Syntax Fix - Restore the original file structure

This script restores the original file structure from backup and applies minimal fixes.
"""

import os
import shutil

def restore_and_fix():
    """Restore from backup and apply minimal fixes"""
    
    # Restore from the clean backup
    backup_file = "W:/TomsGPXEditor/src/application/gpx_file_manager.py.backup_direct_fix.py"
    target_file = "W:/TomsGPXEditor/src/application/gpx_file_manager.py"
    
    if os.path.exists(backup_file):
        shutil.copy2(backup_file, target_file)
        print(f"Restored from backup: {backup_file}")
    else:
        print("Backup file not found!")
        return False
    
    # Read the restored file
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Applying minimal fix...")
    
    # Only remove PropertyKeys references if they exist
    if 'PropertyKeys.' in content:
        content = content.replace('PropertyKeys.', '')
        print("Removed PropertyKeys references")
    
    # Write back
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Applied minimal fix to gpx_file_manager.py")
    return True

if __name__ == "__main__":
    success = restore_and_fix()
    
    if success:
        print("\nRESTORE AND FIX COMPLETED!")
        print("The file has been restored from backup with minimal fixes.")
        print("\nTry running: python main.py")
    else:
        print("\nRESTORE AND FIX FAILED!")
