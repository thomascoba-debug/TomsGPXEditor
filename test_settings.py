#!/usr/bin/env python3
"""
Unit Test für GPX Settings Funktionalität
Testet das Laden und Speichern von Settings
"""

import os
import sys
import tempfile
import json
from src.infrastructure.repositories.properties_repository import AppProperties

def test_settings_persistence():
    """Testet ob Settings korrekt gespeichert und geladen werden"""
    print("=== TESTING SETTINGS PERSISTENCE ===")
    
    # Temporäre Properties-Datei erstellen
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
                    },
                    "2": {
                        "path": "/test/file2.gpx", 
                        "settings": {
                            "visible": True,
                            "editable": False,
                            "color": "#00ff00"
                        }
                    }
                }
            }
        }
        
        # Test-Daten schreiben
        with open(temp_path, 'w') as f:
            json.dump(test_data, f, indent=4)
        
        print(f"Created test file: {temp_path}")
        
        # Properties laden
        props = AppProperties(temp_path)
        
        # Test 1: Settings laden
        print("\n--- Test 1: Settings Loading ---")
        settings1 = props.get_file_settings_by_reference(1)
        settings2 = props.get_file_settings_by_reference(2)
        
        print(f"File 1 settings: {settings1}")
        print(f"File 2 settings: {settings2}")
        
        # Verify
        assert settings1 == {'visible': False, 'editable': True, 'color': '#ff0000'}, f"File 1 settings mismatch: {settings1}"
        assert settings2 == {'visible': True, 'editable': False, 'color': '#00ff00'}, f"File 2 settings mismatch: {settings2}"
        print("Settings loading: PASSED")
        
        # Test 2: Settings speichern
        print("\n--- Test 2: Settings Saving ---")
        
        # Settings ändern
        new_settings1 = {'visible': True, 'editable': False, 'color': '#0000ff'}
        new_settings2 = {'visible': False, 'editable': True, 'color': '#ff0000'}
        
        props.save_file_settings_by_reference(1, new_settings1)
        props.save_file_settings_by_reference(2, new_settings2)
        
        print(f"Saved new settings for file 1: {new_settings1}")
        print(f"Saved new settings for file 2: {new_settings2}")
        
        # Test 3: Settings nach Speichern überprüfen
        print("\n--- Test 3: Settings Verification ---")
        
        # Neue Properties-Instanz erstellen (simuliert Neustart)
        props2 = AppProperties(temp_path)
        
        loaded_settings1 = props2.get_file_settings_by_reference(1)
        loaded_settings2 = props2.get_file_settings_by_reference(2)
        
        print(f"Loaded settings after save for file 1: {loaded_settings1}")
        print(f"Loaded settings after save for file 2: {loaded_settings2}")
        
        # Verify
        assert loaded_settings1 == new_settings1, f"File 1 persistence failed: expected {new_settings1}, got {loaded_settings1}"
        assert loaded_settings2 == new_settings2, f"File 2 persistence failed: expected {new_settings2}, got {loaded_settings2}"
        print("✅ Settings persistence: PASSED")
        
        # Test 4: Nested Key Access
        print("\n--- Test 4: Nested Key Access ---")
        
        session_files = props.get("files.session")
        assert session_files is not None, "files.session should not be None"
        assert "1" in session_files, "Reference 1 not found in files.session"
        assert "2" in session_files, "Reference 2 not found in files.session"
        print("✅ Nested key access: PASSED")
        
        # Test 5: Fallback auf alte Struktur
        print("\n--- Test 5: Fallback Test ---")
        
        # Alte Struktur hinzufügen
        test_data["session_files"] = test_data["files"]["session"]
        
        with open(temp_path, 'w') as f:
            json.dump(test_data, f, indent=4)
        
        props3 = AppProperties(temp_path)
        session_files_new = props3.get("files.session")
        session_files_old = props3.get("session_files")
        
        print(f"New structure: {session_files_new is not None}")
        print(f"Old structure: {session_files_old is not None}")
        
        assert session_files_new is not None, "New structure should work"
        assert session_files_old is not None, "Old structure fallback should work"
        print("✅ Fallback mechanism: PASSED")
        
        print("\n=== ALL TESTS PASSED ===")
        return True

def test_edge_cases():
    """Testet Edge Cases"""
    print("\n=== TESTING EDGE CASES ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
        
        # Leere Properties
        empty_data = {}
        with open(temp_path, 'w') as f:
            json.dump(empty_data, f)
        
        props = AppProperties(temp_path)
        
        # Test mit nicht existenter Referenz
        settings = props.get_file_settings_by_reference(999)
        assert settings is None, f"Expected None for non-existent reference, got {settings}"
        print("✅ Non-existent reference: PASSED")
        
        # Test mit leerer Referenz
        props.save_file_settings_by_reference(999, {'visible': True})
        settings_after = props.get_file_settings_by_reference(999)
        assert settings_after == {'visible': True}, f"Expected saved settings, got {settings_after}"
        print("✅ Creating new reference: PASSED")

if __name__ == "__main__":
    try:
        test_settings_persistence()
        test_edge_cases()
        print("\n🎉 ALL TESTS SUCCESSFUL! Settings functionality works correctly.")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    
    finally:
        # Cleanup
        try:
            os.unlink(temp_path)
        except:
            pass
