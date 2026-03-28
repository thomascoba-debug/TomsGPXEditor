#!/usr/bin/env python3
"""
Final drag and drop test with recent files
"""

import sys
sys.path.insert(0, '.')

def test_drag_drop_final():
    """Final drag and drop test with recent files"""
    print("=== Final Drag & Drop Test ===")
    
    try:
        from app import TomsGPXEditor
        import os
        
        # Create app
        app = TomsGPXEditor()
        print("App created successfully")
        
        # Create test GPX file
        test_file = "W:/Navigation/Touren/test/drag_drop_final_test.gpx"
        gpx_content = '<?xml version="1.0"?><gpx version="1.1"><trk><trkseg><trkpt lat="51" lon="10"/></trkseg></trk></gpx>'
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(gpx_content)
        print(f"Created test file: {test_file}")
        
        # Check initial recent files
        initial_recent = app.recent_files_manager.get_recent_files()
        print(f"Initial recent files: {len(initial_recent)}")
        for i, f in enumerate(initial_recent):
            print(f"  {i+1}: {f}")
        
        # Simulate drag and drop by calling the app methods directly
        print("\nSimulating drag and drop...")
        
        # Add file like drag and drop does
        entry = app.gpx_file_manager.add_file_to_ui(test_file)
        if entry:
            # Update map and recent files like drag and drop does
            app._update_map()
            app.recent_files_manager.reload_recent_files()
            app._update_recent_files_menu()
            print(f"File added successfully: {test_file}")
        else:
            print(f"Failed to add file: {test_file}")
        
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
            print("SUCCESS: Drag & Drop Recent Files works!")
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
    success = test_drag_drop_final()
    if success:
        print("\n🎉 Drag & Drop Recent Files Test PASSED!")
        print("The recent files should now update when you drag and drop GPX files!")
    else:
        print("\n💥 Drag & Drop Recent Files Test FAILED!")
