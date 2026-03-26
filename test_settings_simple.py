#!/usr/bin/env python3
"""
Simple Unit Test für GPX Settings Funktionalität
"""

import os
import sys
import tempfile
import json
from src.infrastructure.repositories.properties_repository import AppProperties

def test_settings():
    print("=== TESTING SETTINGS PERSISTENCE ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
        
        # Test-Daten
        test_data = {
            "files": {
                "session": {
                    "1": {
                        "path": "/test/file1.gpx",
                        "settings": {
                            "visible": False,
                            "editable": True,
                            "color": "#ff0000"
                        }
                    }
                }
            }
        }
        
        with open(temp_path, 'w') as f:
            json.dump(test_data, f, indent=4)
        
        print(f"Created test file: {temp_path}")
        
        # Properties laden
        props = AppProperties(temp_path)
        
        # Test 1: Settings laden
        print("\n--- Test 1: Settings Loading ---")
        settings1 = props.get_file_settings_by_reference(1)
        print(f"File 1 settings: {settings1}")
        
        expected = {'visible': False, 'editable': True, 'color': '#ff0000'}
        assert settings1 == expected, f"Expected {expected}, got {settings1}"
        print("Settings loading: PASSED")
        
        # Test 2: Settings speichern
        print("\n--- Test 2: Settings Saving ---")
        new_settings = {'visible': True, 'editable': False, 'color': '#0000ff'}
        props.save_file_settings_by_reference(1, new_settings)
        print(f"Saved new settings: {new_settings}")
        
        # Test 3: Neustart simulieren
        print("\n--- Test 3: Restart Simulation ---")
        props2 = AppProperties(temp_path)
        loaded_settings = props2.get_file_settings_by_reference(1)
        print(f"Loaded settings after save: {loaded_settings}")
        
        assert loaded_settings == new_settings, f"Expected {new_settings}, got {loaded_settings}"
        print("Settings persistence: PASSED")
        
        print("\n=== ALL TESTS PASSED ===")
        return True

if __name__ == "__main__":
    try:
        test_settings()
        print("\nALL TESTS SUCCESSFUL! Settings functionality works correctly.")
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        try:
            os.unlink(temp_path)
        except:
            pass
