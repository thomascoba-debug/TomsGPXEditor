#!/usr/bin/env python3
"""
Test App Start
Testet ob die Anwendung ohne GUI starten kann
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing basic imports...")
    from app import TomsGPXEditor
    print("App import successful")
    
    print("Testing app creation...")
    app = TomsGPXEditor()
    print("App creation successful")
    
    print("Testing app initialization...")
    # Test if we can access basic properties
    print(f"  - Entries count: {len(app.entries)}")
    print(f"  - Properties loaded: {app.properties is not None}")
    print("App initialization successful")
    
    print("Testing menu state update...")
    app._update_edit_menu_state()
    print("Menu state update successful")
    
    # Don't destroy - let it run briefly
    print("Testing window visibility...")
    app.after(1000, app.quit)  # Quit after 1 second
    app.mainloop()
    print("Window test successful")
    
    print("ALL TESTS PASSED - App should start normally!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
