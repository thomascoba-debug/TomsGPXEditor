#!/usr/bin/env python3
"""
Debug recent files add functionality
"""

import sys
import logging
sys.path.insert(0, '.')

# Enable debug logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

def debug_recent_add():
    """Debug recent files add functionality"""
    print("=== Debug Recent Files Add ===")
    
    try:
        from app import TomsGPXEditor
        import os
        
        app = TomsGPXEditor()
        print("App created")
        
        # Create test file
        test_file = "W:/Navigation/Touren/test/debug_recent_test.gpx"
        gpx_content = '<?xml version="1.0"?><gpx version="1.1"><trk><trkseg><trkpt lat="51" lon="10"/></trkseg></trk></gpx>'
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(gpx_content)
        print(f"Test file created: {test_file}")
        
        # Check initial recent files
        initial_recent = app.recent_files_manager.get_recent_files()
        print(f"Initial recent files: {len(initial_recent)}")
        
        # Add file via GPX manager directly
        print("Adding file via gpx_file_manager...")
        entry = app.gpx_file_manager.add_file_to_ui(test_file)
        print(f"Entry result: {entry}")
        print(f"Entry type: {type(entry)}")
        
        # Check recent files after
        updated_recent = app.recent_files_manager.get_recent_files()
        print(f"Recent files after adding: {len(updated_recent)}")
        for i, f in enumerate(updated_recent):
            print(f"  {i+1}: {f}")
        
        print(f"Test file in recent files: {test_file in updated_recent}")
        
        # Check properties timestamps
        timestamps = app.properties.get('app.recent_files_timestamps', {})
        print(f"Timestamps in properties: {len(timestamps)} files")
        for f, ts in timestamps.items():
            print(f"  {f}: {ts}")
        
        # Check if test file is in timestamps
        test_file_in_timestamps = test_file in timestamps
        print(f"Test file in timestamps: {test_file_in_timestamps}")
        
        # Clean up
        os.remove(test_file)
        print("Cleaned up test file")
        
        return test_file in updated_recent
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_recent_add()
    if success:
        print("\nSUCCESS: Recent files add works!")
    else:
        print("\nFAILED: Recent files add failed!")
