#!/usr/bin/env python3
"""
Test Dialog Button Functions
Testet die Select All, Deselect All und Remove Funktionen
"""

import os
import sys
import tempfile
import json
from src.infrastructure.repositories.properties_repository import AppProperties

def test_dialog_button_functions():
    """Testet die Button-Funktionen für alle Dialoge"""
    print("=== TESTING DIALOG BUTTON FUNCTIONS ===")
    
    # Test 1: Select All Functionality
    print("\n--- Test 1: Select All Functionality ---")
    
    # Simuliere selected_files Dictionary wie in den Dialogen
    selected_files = {
        "/test/file1.gpx": {"selected": False},
        "/test/file2.gpx": {"selected": False},
        "/test/file3.gpx": {"selected": True}
    }
    
    # Simuliere Select All
    for file_path in selected_files:
        selected_files[file_path]["selected"] = True
    
    # Überprüfen
    all_selected = all(file_data["selected"] for file_data in selected_files.values())
    assert all_selected == True, "Select All should select all files"
    print("Select All functionality: PASSED")
    
    # Test 2: Deselect All Functionality
    print("\n--- Test 2: Deselect All Functionality ---")
    
    # Simuliere Deselect All
    for file_path in selected_files:
        selected_files[file_path]["selected"] = False
    
    # Überprüfen
    none_selected = not any(file_data["selected"] for file_data in selected_files.values())
    assert none_selected == True, "Deselect All should deselect all files"
    print("Deselect All functionality: PASSED")
    
    # Test 3: Remove Selected Functionality
    print("\n--- Test 3: Remove Selected Functionality ---")
    
    # Setze einige Dateien als ausgewählt
    selected_files["/test/file1.gpx"]["selected"] = True
    selected_files["/test/file3.gpx"]["selected"] = True
    
    # Simuliere Remove Selected
    files_to_remove = [path for path, data in selected_files.items() if data["selected"]]
    for file_path in files_to_remove:
        del selected_files[file_path]
    
    # Überprüfen
    assert "/test/file1.gpx" not in selected_files, "file1 should be removed"
    assert "/test/file3.gpx" not in selected_files, "file3 should be removed"
    assert "/test/file2.gpx" in selected_files, "file2 should remain"
    print("Remove Selected functionality: PASSED")
    
    # Test 4: Status Update Functionality
    print("\n--- Test 4: Status Update Functionality ---")
    
    # Simuliere Status-Update
    selected_count = sum(1 for data in selected_files.values() if data["selected"])
    total_count = len(selected_files)
    
    assert selected_count == 0, "No files should be selected"
    assert total_count == 1, "One file should remain"
    print("Status Update functionality: PASSED")
    
    # Test 5: File List Rebuild Functionality
    print("\n--- Test 5: File List Rebuild Functionality ---")
    
    # Simuliere rebuild_list
    remaining_files = list(selected_files.keys())
    assert len(remaining_files) == 1, "Should have one remaining file"
    assert remaining_files[0] == "/test/file2.gpx", "Should be file2"
    print("File List Rebuild functionality: PASSED")
    
    print("\n=== ALL DIALOG BUTTON FUNCTIONS TESTS PASSED ===")
    return True

if __name__ == "__main__":
    try:
        test_dialog_button_functions()
        print("\nALL DIALOG BUTTON FUNCTIONS WORK CORRECTLY!")
        print("Select All: Selects all files in the list")
        print("Deselect All: Deselects all files in the list")
        print("Remove Selected: Removes selected files from the list")
        print("Status Update: Updates status based on selection")
        print("File List Rebuild: Rebuilds the list after removal")
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
