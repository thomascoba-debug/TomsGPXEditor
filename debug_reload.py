#!/usr/bin/env python3
"""
Debug recent files reload
"""

import sys
import logging
sys.path.insert(0, '.')

# Enable debug logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

def debug_reload():
    """Debug recent files reload"""
    print("=== Debug Recent Files Reload ===")
    
    try:
        from app import TomsGPXEditor
        import os
        
        app = TomsGPXEditor()
        
        # Create test file
        test_file = "W:/Navigation/Touren/test/debug_reload_test.gpx"
        gpx_content = '<?xml version="1.0"?><gpx version="1.1"><trk><trkseg><trkpt lat="51" lon="10"/></trkseg></trk></gpx>'
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(gpx_content)
        
        print("Before adding:")
        print("Recent files:", len(app.recent_files_manager.recent_files))
        for f in app.recent_files_manager.recent_files:
            print("  ", f)
        
        # Add file
        entry = app.gpx_file_manager.add_file_to_ui(test_file)
        print("Entry created:", entry is not None)
        
        print("After adding:")
        print("Recent files:", len(app.recent_files_manager.recent_files))
        for f in app.recent_files_manager.recent_files:
            print("  ", f)
        
        print("Test file in recent files:", test_file in app.recent_files_manager.recent_files)
        
        # Force reload
        print("Forcing reload...")
        app.recent_files_manager.reload_recent_files()
        
        print("After reload:")
        print("Recent files:", len(app.recent_files_manager.recent_files))
        for f in app.recent_files_manager.recent_files:
            print("  ", f)
        
        print("Test file in recent files after reload:", test_file in app.recent_files_manager.recent_files)
        
        # Check timestamps
        timestamps = app.properties.get('app.recent_files_timestamps', {})
        print("Timestamps:", len(timestamps))
        print("Test file in timestamps:", test_file in timestamps)
        
        os.remove(test_file)
        
        return test_file in app.recent_files_manager.recent_files
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_reload()
    if success:
        print("\nSUCCESS: Recent files reload works!")
    else:
        print("\nFAILED: Recent files reload failed!")
