#!/usr/bin/env python3
"""
Test full app startup
"""

import sys
sys.path.insert(0, '.')

def test_full_startup():
    """Test full app startup"""
    print("=== Testing Full App Startup ===")
    
    try:
        from app import TomsGPXEditor
        import tkinter as tk
        
        print("Creating app...")
        app = TomsGPXEditor()
        print("App created successfully!")
        
        # Test basic functionality
        print("Testing basic functionality...")
        
        # Test recent files
        recent = app.recent_files_manager.get_recent_files()
        print(f"Recent files: {len(recent)}")
        
        # Test map controller
        entries = app.gpx_file_manager.get_all_entries()
        print(f"GPX entries: {len(entries)}")
        
        # Test menu creation
        print("Testing menu creation...")
        app._build_menu()
        print("Menu created successfully!")
        
        print("SUCCESS: Full app startup test completed successfully!")
        print("The app should start normally when you run 'python main.py'")
        
        # Don't start the GUI automatically, just test initialization
        # app.destroy()  # Don't destroy, let it finish naturally
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_full_startup()
    if success:
        print("\nApp is ready to start!")
    else:
        print("\nApp startup failed!")
