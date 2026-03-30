#!/usr/bin/env python3
"""
Fix Properties Structure - Correct the logging configuration

This script fixes the properties.json structure to match the expected format.
"""

import json

def fix_properties():
    """Fix properties.json structure"""
    
    properties_file = "W:/TomsGPXEditor/properties.json"
    
    # Read current properties
    with open(properties_file, 'r', encoding='utf-8') as f:
        properties = json.load(f)
    
    print("Current properties structure loaded")
    
    # Fix the logging structure - move it under dialogs.settings
    if 'logging' in properties:
        logging_config = properties['logging']
        
        # Ensure dialogs.settings exists
        if 'dialogs' not in properties:
            properties['dialogs'] = {}
        if 'settings' not in properties['dialogs']:
            properties['dialogs']['settings'] = {}
        
        # Move logging under dialogs.settings
        properties['dialogs']['settings']['logging'] = logging_config
        
        # Remove the old logging section
        del properties['logging']
        
        print("✅ Moved logging section under dialogs.settings")
    
    # Clean up recent_files structure
    if 'app' in properties and 'recent_files_timestamps' in properties['app']:
        # Move recent_files under app
        properties['app']['recent_files'] = properties['app']['recent_files_timestamps']
        del properties['app']['recent_files_timestamps']
        
        print("✅ Fixed recent_files structure")
    
    # Ensure files.session exists
    if 'files' not in properties:
        properties['files'] = {}
    if 'session' not in properties['files']:
        properties['files']['session'] = {}
    
    print("✅ Ensured files.session structure exists")
    
    # Write back fixed properties
    with open(properties_file, 'w', encoding='utf-8') as f:
        json.dump(properties, f, indent=2, ensure_ascii=False)
    
    print("✅ Fixed properties.json structure")
    print("\n🎉 PROPERTIES STRUCTURE FIXED!")
    print("   - Logging moved under dialogs.settings")
    print("   - Recent files structure corrected")
    print("   - Files.session structure ensured")
    print("\n🚀 Try running: python main.py")

if __name__ == "__main__":
    fix_properties()
