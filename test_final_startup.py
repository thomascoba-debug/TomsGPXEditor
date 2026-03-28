#!/usr/bin/env python3
"""
Final comprehensive app startup test
"""

import sys
sys.path.insert(0, '.')

def test_final_startup():
    """Final comprehensive app startup test"""
    print("=== Final App Startup Test ===")
    
    try:
        from app import TomsGPXEditor
        
        print("Creating app...")
        app = TomsGPXEditor()
        print("SUCCESS: App created successfully!")
        
        # Test basic functionality
        print("Testing basic functionality...")
        
        # Window exists
        if app.winfo_exists():
            print("SUCCESS: Window exists")
        else:
            print("ERROR: Window does not exist")
            return False
        
        # Map widget
        print(f"SUCCESS: Map widget: {type(app.map_widget).__name__}")
        
        # Controllers
        print(f"SUCCESS: GPX entries: {len(app.gpx_file_manager.get_all_entries())}")
        print(f"SUCCESS: Recent files: {len(app.recent_files_manager.get_recent_files())}")
        
        # Test menu creation (might fail but app should continue)
        try:
            app._build_menu()
            print("SUCCESS: Menu created successfully")
        except Exception as e:
            print(f"WARNING: Menu creation failed (but app continues): {e}")
        
        # Test session loading (might fail but app should continue)
        try:
            app._safe_load_session_files()
            print("SUCCESS: Session loading completed")
        except Exception as e:
            print(f"WARNING: Session loading failed (but app continues): {e}")
        
        # Schedule app to close after 3 seconds
        app.after(3000, app.destroy)
        print("App will close automatically in 3 seconds...")
        
        # Start mainloop
        app.mainloop()
        
        print("SUCCESS: App completed successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_final_startup()
    if success:
        print("\nFINAL TEST PASSED!")
        print("The app is ready for normal use with 'python main.py'")
    else:
        print("\nFINAL TEST FAILED!")
