#!/usr/bin/env python3
"""
Final test of recent files functionality
"""

import sys
import logging
sys.path.insert(0, '.')

# Enable debug logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

def test_final_recent():
    """Final test of recent files functionality"""
    print("=== Final Recent Files Test ===")
    
    try:
        from app import TomsGPXEditor
        import os
        
        app = TomsGPXEditor()
        
        # Create test file
        test_file = "W:/Navigation/Touren/test/final_test.gpx"
        gpx_content = '<?xml version="1.0"?><gpx version="1.1"><trk><trkseg><trkpt lat="51" lon="10"/></trkseg></trk></gpx>'
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(gpx_content)
        
        print("Before adding:")
        print("Recent files:", len(app.recent_files_manager.recent_files))
        
        # Add file
        entry = app.gpx_file_manager.add_file_to_ui(test_file)
        print("Entry created:", entry is not None)
        
        print("After adding (before reload):")
        print("Recent files:", len(app.recent_files_manager.recent_files))
        print("Test file in recent files:", test_file in app.recent_files_manager.recent_files)
        
        # Check timestamps
        timestamps = app.properties.get('app.recent_files_timestamps', {})
        print("Test file in timestamps:", test_file in timestamps)
        
        # Check if reload is needed
        if test_file not in app.recent_files_manager.recent_files and test_file in timestamps:
            print("RELOAD NEEDED: File in timestamps but not in recent files list")
        
        os.remove(test_file)
        
        return test_file in app.recent_files_manager.recent_files
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_final_recent()
    if success:
        print("\nSUCCESS: Recent files work without reload!")
    else:
        print("\nFAILED: Recent files need reload!")
