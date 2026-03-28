#!/usr/bin/env python3
"""
Test manual reload of recent files
"""

import sys
import logging
sys.path.insert(0, '.')

# Enable debug logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

def test_manual_reload():
    """Test manual reload of recent files"""
    print("=== Manual Reload Test ===")
    
    try:
        from app import TomsGPXEditor
        import os
        
        app = TomsGPXEditor()
        
        # Create test file
        test_file = "W:/Navigation/Touren/test/manual_reload_test.gpx"
        gpx_content = '<?xml version="1.0"?><gpx version="1.1"><trk><trkseg><trkpt lat="51" lon="10"/></trkseg></trk></gpx>'
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(gpx_content)
        
        print("Before adding:")
        print("Recent files:", len(app.recent_files_manager.recent_files))
        
        # Add file
        entry = app.gpx_file_manager.add_file_to_ui(test_file)
        print("Entry created:", entry is not None)
        
        print("After adding:")
        print("Recent files:", len(app.recent_files_manager.recent_files))
        print("Test file in recent files:", test_file in app.recent_files_manager.recent_files)
        
        # Manual reload
        print("Manual reload...")
        app.recent_files_manager.reload_recent_files()
        
        print("After manual reload:")
        print("Recent files:", len(app.recent_files_manager.recent_files))
        print("Test file in recent files:", test_file in app.recent_files_manager.recent_files)
        
        os.remove(test_file)
        
        return test_file in app.recent_files_manager.recent_files
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_manual_reload()
    if success:
        print("\nSUCCESS: Manual reload works!")
    else:
        print("\nFAILED: Manual reload failed!")
