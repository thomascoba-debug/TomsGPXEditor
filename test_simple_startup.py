#!/usr/bin/env python3
"""
Simple app startup test
"""

import sys
sys.path.insert(0, '.')

def test_simple_startup():
    """Test simple app startup without GUI"""
    print("=== Testing Simple App Startup ===")
    
    try:
        # Test imports first
        print("Testing imports...")
        from app import TomsGPXEditor
        print("Imports successful!")
        
        # Test app creation (but don't start mainloop)
        print("Creating app instance...")
        app = TomsGPXEditor()
        print("App instance created successfully!")
        
        # Test basic attributes
        print("Testing basic attributes...")
        print(f"  Has properties: {hasattr(app, 'properties')}")
        print(f"  Has recent_files_manager: {hasattr(app, 'recent_files_manager')}")
        print(f"  Has gpx_file_manager: {hasattr(app, 'gpx_file_manager')}")
        print(f"  Has map_controller: {hasattr(app, 'map_controller')}")
        
        # Test recent files
        print("Testing recent files...")
        recent = app.recent_files_manager.get_recent_files()
        print(f"  Recent files count: {len(recent)}")
        
        print("SUCCESS: Simple startup test completed!")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_startup()
    if success:
        print("\nApp basic initialization works!")
        print("The issue might be with GUI startup or tkintermapview.")
    else:
        print("\nApp basic initialization failed!")
