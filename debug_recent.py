#!/usr/bin/env python3
"""
Debug recent files functionality
"""

import sys
import logging
sys.path.insert(0, '.')

# Enable debug logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def debug_recent_files():
    """Debug recent files functionality"""
    print("=== Debugging Recent Files ===")
    
    try:
        from app import TomsGPXEditor
        import os
        
        # Create app instance
        app = TomsGPXEditor()
        print("App created")
        
        # Check recent files manager
        print(f"Recent files manager: {app.recent_files_manager}")
        print(f"GPX manager has recent_files_manager: {hasattr(app.gpx_file_manager, 'recent_files_manager')}")
        if hasattr(app.gpx_file_manager, 'recent_files_manager'):
            print(f"GPX manager recent_files_manager: {app.gpx_file_manager.recent_files_manager}")
        
        # Create test file
        test_file = "W:/Navigation/Touren/test/recent_files_test.gpx"
        gpx_content = '<?xml version="1.0"?><gpx version="1.1"><trk><trkseg><trkpt lat="51" lon="10"/></trkseg></trk></gpx>'
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(gpx_content)
        print(f"Created test file: {test_file}")
        
        # Check initial recent files
        initial_recent = app.recent_files_manager.get_recent_files()
        print(f"Initial recent files: {len(initial_recent)}")
        
        # Add file
        print("Adding file to UI...")
        entry = app.gpx_file_manager.add_file_to_ui(test_file)
        print(f"Entry result: {entry}")
        
        # Check recent files after
        updated_recent = app.recent_files_manager.get_recent_files()
        print(f"Recent files after adding: {len(updated_recent)}")
        for i, f in enumerate(updated_recent):
            print(f"  {i+1}: {f}")
        
        # Check if test file is in recent files
        print(f"Test file in recent files: {test_file in updated_recent}")
        
        # Clean up
        os.remove(test_file)
        print("Cleaned up test file")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_recent_files()
