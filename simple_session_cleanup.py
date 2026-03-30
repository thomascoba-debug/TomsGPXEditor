#!/usr/bin/env python3
"""
Simple Session Cleanup - Remove problematic session files only

This script only removes the problematic session files without touching the code.
"""

import json
import os

def simple_session_cleanup():
    """Simple cleanup of problematic session files"""
    
    properties_file = "W:/TomsGPXEditor/properties.json"
    
    # Read current properties
    with open(properties_file, 'r', encoding='utf-8') as f:
        properties = json.load(f)
    
    print("Cleaning up problematic session files...")
    
    # Remove problematic session files
    problematic_files = [
        "W:/Navigation/Touren/test/Iseo - Wenns.gpx",
        "W:/Navigation/Touren/test/bft Autowäsche, Obernburg a.Main - Sölden.gpx", 
        "W:/Navigation/Touren/test/GW01_converted_tracks.gpx",
        "W:/Navigation/Touren/test/GW01.gpx",
        "W:/Navigation/Touren/test/GW01_downsampled.gpx"
    ]
    
    # Find and remove problematic entries
    refs_to_remove = []
    if 'files' in properties and 'session' in properties['files']:
        session_files = properties['files']['session']
        
        for ref_num, file_data in session_files.items():
            file_path = file_data.get('path', '')
            if file_path in problematic_files:
                refs_to_remove.append(ref_num)
                print(f"Marked for removal: {file_path}")
    
    # Remove problematic entries
    for ref_num in refs_to_remove:
        if ref_num in properties['files']['session']:
            del properties['files']['session'][ref_num]
            print(f"Removed from session: ref {ref_num}")
    
    # Save updated properties
    with open(properties_file, 'w', encoding='utf-8') as f:
        json.dump(properties, f, indent=2, ensure_ascii=False)
    
    print(f"Removed {len(refs_to_remove)} problematic session files")
    print("The PropertyKeys errors should now be resolved!")

if __name__ == "__main__":
    simple_session_cleanup()
