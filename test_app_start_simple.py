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
    
    print("Testing tkinter import...")
    import tkinter as tk
    print("Tkinter import successful")
    
    print("Testing app creation (without mainloop)...")
    root = tk.Tk()
    root.withdraw()  # Hide window initially
    
    app = TomsGPXEditor(root)
    print("App creation successful")
    
    print("Testing app initialization...")
    # Test if we can access basic properties
    print(f"  - Entries count: {len(app.entries)}")
    print(f"  - Properties loaded: {app.properties is not None}")
    print("App initialization successful")
    
    print("Testing menu state update...")
    app._update_edit_menu_state()
    print("Menu state update successful")
    
    root.destroy()
    print("ALL TESTS PASSED - App should start normally!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
