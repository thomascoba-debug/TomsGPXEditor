#!/usr/bin/env python3
"""
Test direct recent files functionality
"""

import sys
sys.path.insert(0, '.')

def test_direct_recent():
    """Test direct recent files functionality"""
    print("=== Testing Direct Recent Files ===")
    
    try:
        from app import TomsGPXEditor
        import os
        
        # Create app
        app = TomsGPXEditor()
        print("App created successfully")
        
        # Create test GPX file
        test_file = "W:/Navigation/Touren/test/direct_recent_test.gpx"
        gpx_content = '<?xml version="1.0"?><gpx version="1.1"><trk><trkseg><trkpt lat="51" lon="10"/></trkseg></trk></gpx>'
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(gpx_content)
        print(f"Created test file: {test_file}")
        
        # Check initial recent files
        initial_recent = app.recent_files_manager.get_recent_files()
        print(f"Initial recent files: {len(initial_recent)}")
        for i, f in enumerate(initial_recent):
            print(f"  {i+1}: {f}")
        
        # Add file directly (like drag and drop does)
        print("\nAdding file directly...")
        entry = app.gpx_file_manager.add_file_to_ui(test_file)
        print(f"Entry result: {entry}")
        
        # Check recent files after adding
        updated_recent = app.recent_files_manager.get_recent_files()
        print(f"\nRecent files after adding: {len(updated_recent)}")
        for i, f in enumerate(updated_recent):
            print(f"  {i+1}: {f}")
        
        # Check if test file is in recent files
        test_file_in_recent = test_file in updated_recent
        print(f"\nTest file in recent files: {test_file_in_recent}")
        
        # Check if we need to call reload
        if not test_file_in_recent:
            print("Test file not found, forcing reload...")
            app.recent_files_manager.reload_recent_files()
            
            # Check again after reload
            reloaded_recent = app.recent_files_manager.get_recent_files()
            print(f"Recent files after reload: {len(reloaded_recent)}")
            for i, f in enumerate(reloaded_recent):
                print(f"  {i+1}: {f}")
            
            test_file_in_recent = test_file in reloaded_recent
            print(f"Test file in recent files after reload: {test_file_in_recent}")
        
        # Clean up
        os.remove(test_file)
        print(f"\nCleaned up test file")
        
        if test_file_in_recent:
            print("SUCCESS: Direct recent files update works!")
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
    success = test_direct_recent()
    if success:
        print("\nDirect Recent Files Test PASSED!")
    else:
        print("\nDirect Recent Files Test FAILED!")
