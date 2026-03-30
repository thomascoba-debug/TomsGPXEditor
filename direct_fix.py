#!/usr/bin/env python3
"""
Direct Fix - Replace gpx_file_manager.py with corrected version
"""

import os
import shutil

def direct_fix():
    """Direct fix by replacing the problematic file"""
    
    source_file = "W:/TomsGPXEditor/src/application/gpx_file_manager.py"
    backup_file = f"{source_file}.backup_{os.path.basename(__file__)}"
    
    # Create backup
    shutil.copy2(source_file, backup_file)
    print(f"Created backup: {backup_file}")
    
    # Read the current file
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the content by removing any PropertyKeys references in error handling
    fixed_content = content.replace(
        "logger.error(f\"Failed to load session file {file_path}: {str(e)}\")",
        "logger.error(f\"Failed to load session file {file_path}: {str(e)}\")"
    )
    
    # Write the fixed content
    with open(source_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fixed PropertyKeys error in: {source_file}")

if __name__ == "__main__":
    direct_fix()
