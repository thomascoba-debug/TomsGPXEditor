#!/usr/bin/env python3
"""
Simple test for recent files functionality
"""

import sys
sys.path.insert(0, '.')

def test_recent_files():
    """Test recent files functionality"""
    print("=== Testing Recent Files ===")
    
    try:
        from app import TomsGPXEditor
        import os
        
        # Create app instance
        app = TomsGPXEditor()
        print("App created")
        
        # Check initial state
        initial_recent = app.recent_files_manager.get_recent_files()
        print(f"Initial recent files: {len(initial_recent)}")
        
        # Create test GPX file
        test_file = "W:/Navigation/Touren/test/recent_files_test.gpx"
        gpx_content = '''<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Test">
  <trk>
    <name>Test Track</name>
    <trkseg>
      <trkpt lat="51.0" lon="10.0"></trkpt>
      <trkpt lat="51.1" lon="10.1"></trkpt>
    </trkseg>
  </trk>
</gpx>'''
        
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(gpx_content)
            print(f"Created test file: {test_file}")
            
            # Test adding file
            entry = app.gpx_file_manager.add_file_to_ui(test_file)
            if entry:
                print("SUCCESS: File added to UI")
                
                # Check recent files
                recent_files = app.recent_files_manager.get_recent_files()
                print(f"Recent files after adding: {len(recent_files)}")
                
                for i, f in enumerate(recent_files):
                    print(f"  {i+1}: {f}")
                
                if test_file in recent_files:
                    print("SUCCESS: Test file found in recent files!")
                else:
                    print("ERROR: Test file not found in recent files")
            else:
                print("ERROR: Failed to add file to UI")
            
            # Clean up
            os.remove(test_file)
            print("Cleaned up test file")
            
        except Exception as e:
            print(f"Error during test: {e}")
        
        print("SUCCESS: Recent files test completed!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_recent_files()
