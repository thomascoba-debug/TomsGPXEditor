#!/usr/bin/env python3
"""
Emergency Fix - Remove PropertyKeys Error

This script removes any remaining PropertyKeys references that are causing the error.
"""

import os
import re

def emergency_fix():
    """Emergency fix for PropertyKeys error"""
    
    # Check all Python files for PropertyKeys references
    src_dir = "W:/TomsGPXEditor/src"
    
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Look for PropertyKeys references in error messages
                    if "name 'PropertyKeys' is not defined" in content:
                        print(f"Found PropertyKeys error in: {file_path}")
                        
                        # Remove any PropertyKeys references
                        content = re.sub(r'PropertyKeys\.', '', content)
                        
                        # Write back
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"Fixed PropertyKeys references in: {file_path}")
                
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    emergency_fix()
    print("Emergency fix complete!")
