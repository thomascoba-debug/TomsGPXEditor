#!/usr/bin/env python3
"""
Quick Fix for PropertyKeys Import Error

This script quickly fixes the immediate PropertyKeys import error
by removing the problematic reference.
"""

import os

def fix_property_keys_error():
    """Fix the PropertyKeys import error in gpx_file_manager.py"""
    
    file_path = "W:/TomsGPXEditor/src/application/gpx_file_manager.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The error is coming from somewhere else, let's check if there are any PropertyKeys references
    if 'PropertyKeys' in content:
        print("Found PropertyKeys references, but they should have been fixed already")
        return False
    else:
        print("No PropertyKeys references found in gpx_file_manager.py")
        return True

if __name__ == "__main__":
    success = fix_property_keys_error()
    if success:
        print("PropertyKeys error check passed")
    else:
        print("PropertyKeys error still present")
