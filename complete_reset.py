#!/usr/bin/env python3
"""
Complete Reset - Clean slate approach

This script completely resets the problematic session files
and creates a clean starting state for the application.
"""

import os
import json
import shutil

def complete_reset():
    """Complete reset of problematic session files"""
    
    print("Starting complete reset...")
    
    # 1. Backup current properties
    properties_file = "W:/TomsGPXEditor/properties.json"
    backup_file = f"{properties_file}.backup_before_reset"
    
    if os.path.exists(properties_file):
        shutil.copy2(properties_file, backup_file)
        print(f"✅ Backed up properties to: {backup_file}")
    
    # 2. Create clean properties file
    clean_properties = {
        "files": {
            "session": {}
        },
        "dialogs": {
            "settings": {
                "logging": {"level": "INFO"},
                "rendering": {"line_width": 3},
                "marker": {"enabled": True}
            }
        },
        "app": {
            "main_window": {"geometry": "800x600+100+100"},
            "recent_files": {}
        }
    }
    
    with open(properties_file, 'w', encoding='utf-8') as f:
        json.dump(clean_properties, f, indent=2, ensure_ascii=False)
    
    print("✅ Created clean properties file")
    
    # 3. Remove any problematic session file references
    problematic_files = [
        "W:/Navigation/Touren/test/Iseo - Wenns.gpx",
        "W:/Navigation/Touren/test/bft Autowäsche, Obernburg a.Main - Sölden.gpx",
        "W:/Navigation/Touren/test/GW01_converted_tracks.gpx",
        "W:/Navigation/Touren/test/GW01.gpx",
        "W:/Navigation/Touren/test/GW01_downsampled.gpx"
    ]
    
    removed_count = 0
    for file_path in problematic_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed problematic file: {os.path.basename(file_path)}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {file_path}: {e}")
    
    print(f"✅ Removed {removed_count} problematic files")
    
    # 4. Verify gpx_file_manager.py has no PropertyKeys references
    gpx_file = "W:/TomsGPXEditor/src/application/gpx_file_manager.py"
    
    with open(gpx_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'PropertyKeys' in content:
        print("❌ WARNING: PropertyKeys references still exist in gpx_file_manager.py")
        print("   Manual intervention required!")
        return False
    else:
        print("✅ gpx_file_manager.py is clean")
    
    print("\n🎉 COMPLETE RESET FINISHED!")
    print("   - Clean properties file created")
    print("   - Problematic session files removed")
    print("   - Application should start cleanly now")
    print("\n🚀 Try running: python main.py")
    
    return True

if __name__ == "__main__":
    success = complete_reset()
    
    if success:
        print("\n✅ Reset completed successfully!")
        print("The application should now start without PropertyKeys errors.")
    else:
        print("\n❌ Reset completed with warnings!")
        print("Manual intervention may be required.")
