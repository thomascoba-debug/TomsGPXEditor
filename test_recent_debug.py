#!/usr/bin/env python3
"""
Debug recent files with detailed logging
"""

import sys
import logging
sys.path.insert(0, '.')

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

def test_recent_debug():
    """Test recent files with debug logging"""
    print("=== Recent Files Debug Test ===")
    
    try:
        from app import TomsGPXEditor
        import os
        
        # Create app
        app = TomsGPXEditor()
        print("App created")
        
        # Create test file
        test_file = "W:/Navigation/Touren/test/recent_files_test.gpx"
        gpx_content = '<?xml version="1.0"?><gpx version="1.1"><trk><trkseg><trkpt lat="51" lon="10"/></trkseg></trk></gpx>'
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(gpx_content)
        print(f"Created test file: {test_file}")
        
        # Check initial state
        print("\n=== Initial State ===")
        initial_recent = app.recent_files_manager.get_recent_files()
        print(f"Initial recent files count: {len(initial_recent)}")
        
        # Check if recent_files_manager exists in GPX manager
        print(f"\nGPX manager has recent_files_manager: {hasattr(app.gpx_file_manager, 'recent_files_manager')}")
        if hasattr(app.gpx_file_manager, 'recent_files_manager'):
            print(f"GPX manager recent_files_manager: {app.gpx_file_manager.recent_files_manager}")
            print(f"Same as app recent_files_manager: {app.gpx_file_manager.recent_files_manager is app.recent_files_manager}")
        
        # Add file
        print(f"\n=== Adding File ===")
        print(f"Adding file: {test_file}")
        entry = app.gpx_file_manager.add_file_to_ui(test_file)
        print(f"Entry result: {entry}")
        print(f"Entry type: {type(entry)}")
        
        # Check after adding
        print(f"\n=== After Adding ===")
        updated_recent = app.recent_files_manager.get_recent_files()
        print(f"Recent files count: {len(updated_recent)}")
        
        for i, f in enumerate(updated_recent):
            print(f"  {i+1}: {f}")
        
        print(f"Test file in recent files: {test_file in updated_recent}")
        
        # Check properties
        print(f"\n=== Properties Check ===")
        timestamps = app.properties.get("app.recent_files_timestamps", {})
        print(f"Timestamps in properties: {timestamps}")
        
        # Clean up
        os.remove(test_file)
        print(f"\nCleaned up test file")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_recent_debug()
