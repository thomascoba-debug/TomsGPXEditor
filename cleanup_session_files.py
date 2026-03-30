#!/usr/bin/env python3
"""
Session Files Cleanup - Remove problematic session files

This script cleans up the session files that are causing PropertyKeys errors.
"""

import os
import json

def cleanup_session_files():
    """Clean up problematic session files"""
    
    properties_file = "W:/TomsGPXEditor/properties.json"
    
    # Read current properties
    try:
        with open(properties_file, 'r', encoding='utf-8') as f:
            properties = json.load(f)
    except Exception as e:
        print(f"Error reading properties: {e}")
        return
    
    # Clean up session files
    if 'files' in properties and 'session' in properties['files']:
        session_files = properties['files']['session']
        
        # Remove problematic files
        problematic_files = [
            "W:/Navigation/Touren/test/Iseo - Wenns.gpx",
            "W:/Navigation/Touren/test/bft Autowäsche, Obernburg a.Main - Sölden.gpx",
            "W:/Navigation/Touren/test/GW01_converted_tracks.gpx",
            "W:/Navigation/Touren/test/GW01.gpx",
            "W:/Navigation/Touren/test/GW01_downsampled.gpx"
        ]
        
        # Find and remove problematic entries
        refs_to_remove = []
        for ref_num, file_data in session_files.items():
            file_path = file_data.get('path', '')
            if file_path in problematic_files:
                refs_to_remove.append(ref_num)
                print(f"Marked for removal: {file_path}")
        
        # Remove problematic entries
        for ref_num in refs_to_remove:
            if ref_num in session_files:
                del session_files[ref_num]
                print(f"Removed from session: ref {ref_num}")
        
        # Update properties
        properties['files']['session'] = session_files
        
        # Save updated properties
        try:
            with open(properties_file, 'w', encoding='utf-8') as f:
                json.dump(properties, f, indent=2, ensure_ascii=False)
            print(f"Updated properties file, removed {len(refs_to_remove)} problematic entries")
        except Exception as e:
            print(f"Error saving properties: {e}")
    else:
        print("No session files found to clean up")

if __name__ == "__main__":
    cleanup_session_files()
