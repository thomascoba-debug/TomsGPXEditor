#!/usr/bin/env python3
"""
Test drag and drop recent files functionality
"""

import sys
sys.path.insert(0, '.')

def test_drag_drop_recent():
    """Test drag and drop recent files functionality"""
    print("=== Testing Drag & Drop Recent Files ===")
    
    try:
        from app import TomsGPXEditor
        import os
        
        # Create app
        app = TomsGPXEditor()
        print("App created successfully")
        
        # Create test GPX file
        test_file = "W:/Navigation/Touren/test/drag_drop_test.gpx"
        gpx_content = '<?xml version="1.0"?><gpx version="1.1"><trk><trkseg><trkpt lat="51" lon="10"/></trkseg></trk></gpx>'
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(gpx_content)
        print(f"Created test file: {test_file}")
        
        # Check initial recent files
        initial_recent = app.recent_files_manager.get_recent_files()
        print(f"Initial recent files: {len(initial_recent)}")
        for i, f in enumerate(initial_recent):
            print(f"  {i+1}: {f}")
        
        # Simulate drag and drop by calling _on_drop
        print("\nSimulating drag and drop...")
        
        # Create a mock event with proper format
        class MockEvent:
            def __init__(self, data):
                self.data = data
        
        # Simulate dropping the test file (tkinter format)
        mock_event = MockEvent(f"{{{test_file}}}")
        app._on_drop(mock_event)
        
        # Check recent files after drag and drop
        updated_recent = app.recent_files_manager.get_recent_files()
        print(f"\nRecent files after drag and drop: {len(updated_recent)}")
        for i, f in enumerate(updated_recent):
            print(f"  {i+1}: {f}")
        
        # Check if test file is in recent files
        test_file_in_recent = test_file in updated_recent
        print(f"\nTest file in recent files: {test_file_in_recent}")
        
        # Clean up
        os.remove(test_file)
        print(f"\nCleaned up test file")
        
        if test_file_in_recent:
            print("SUCCESS: Drag and drop recent files update works!")
            return True
        else:
            print("FAILED: Test file not found in recent files")
            return False
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_drag_drop_recent()
    if success:
        print("\nDrag & Drop Recent Files Test PASSED!")
    else:
        print("\nDrag & Drop Recent Files Test FAILED!")
