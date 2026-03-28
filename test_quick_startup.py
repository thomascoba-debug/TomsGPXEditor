#!/usr/bin/env python3
"""
Quick app startup test with timeout
"""

import sys
sys.path.insert(0, '.')

def test_quick_startup():
    """Test app startup with timeout"""
    print("=== Quick App Startup Test ===")
    
    try:
        from app import TomsGPXEditor
        import tkinter as tk
        
        print("Creating app...")
        app = TomsGPXEditor()
        print("App created successfully!")
        
        # Test that app window exists
        if app.winfo_exists():
            print("Window exists: YES")
        else:
            print("Window exists: NO")
            return False
        
        # Test basic components
        print(f"Map widget: {type(app.map_widget)}")
        print(f"GPX entries: {len(app.gpx_file_manager.get_all_entries())}")
        
        # Schedule app to close after 2 seconds
        app.after(2000, app.destroy)
        print("App will close automatically in 2 seconds...")
        
        # Start mainloop (will run for 2 seconds then close)
        app.mainloop()
        
        print("App completed successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_quick_startup()
    if success:
        print("\nApp startup test PASSED!")
    else:
        print("\nApp startup test FAILED!")
