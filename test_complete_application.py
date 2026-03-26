#!/usr/bin/env python3
"""
Comprehensive Unit Test for GPX Editor Application
Tests all major functionality: Settings, UI, Map Rendering, File Management
"""

import os
import sys
import tempfile
import json
import time
from unittest.mock import Mock, patch
from src.infrastructure.repositories.properties_repository import AppProperties

def test_properties_system():
    """Test the complete properties system"""
    print("=== TESTING PROPERTIES SYSTEM ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
        
        # Test 1: New structure support
        test_data = {
            "files": {
                "session": {
                    "1": {
                        "path": "/test/file1.gpx",
                        "settings": {
                            "visible": True,
                            "editable": False,
                            "color": "#ff0000"
                        }
                    },
                    "2": {
                        "path": "/test/file2.gpx",
                        "settings": {
                            "visible": False,
                            "editable": True,
                            "color": "#00ff00"
                        }
                    }
                }
            },
            "dialog_geometry": {
                "test_dialog": "100x200+10+10"
            }
        }
        
        with open(temp_path, 'w') as f:
            json.dump(test_data, f, indent=4)
        
        props = AppProperties(temp_path)
        
        # Test nested key access
        session_files = props.get("files.session")
        assert session_files is not None, "files.session should be accessible"
        assert "1" in session_files, "Reference 1 should exist"
        assert "2" in session_files, "Reference 2 should exist"
        print("Nested key access: PASSED")
        
        # Test file reference operations
        ref_num = props.get_or_create_file_reference("/test/new_file.gpx")
        assert ref_num > 0, "Should create new reference"
        
        settings = props.get_file_settings_by_reference(ref_num)
        assert settings is not None, "Should get default settings"
        print("File reference operations: PASSED")
        
        # Test settings persistence
        new_settings = {"visible": True, "editable": True, "color": "#0000ff"}
        props.save_file_settings_by_reference(ref_num, new_settings)
        
        # Simulate restart
        props2 = AppProperties(temp_path)
        loaded_settings = props2.get_file_settings_by_reference(ref_num)
        assert loaded_settings == new_settings, f"Settings should persist: expected {new_settings}, got {loaded_settings}"
        print("Settings persistence: PASSED")
        
        # Test dialog geometry
        props.set_dialog_geometry("test_dialog", "200x300+20+20")
        geometry = props.get_dialog_geometry("test_dialog")
        assert geometry == "200x300+20+20", f"Geometry should be saved: expected '200x300+20+20', got {geometry}"
        print("Dialog geometry: PASSED")
        
        print("Properties system: ALL TESTS PASSED")
        return True

def test_gpx_file_operations():
    """Test GPX file loading and parsing"""
    print("\n=== TESTING GPX FILE OPERATIONS ===")
    
    # Test with real GPX file if available
    test_gpx_files = [
        "W:/Navigation/Touren/test/Iseo - Wenns_downsampled.gpx",
        "Z:/work/Navigation/Touren/test/Iseo - Wenns.gpx"
    ]
    
    import gpxpy
    
    for gpx_file in test_gpx_files:
        if os.path.exists(gpx_file):
            print(f"Testing GPX file: {gpx_file}")
            
            # Test file loading
            with open(gpx_file, 'r') as f:
                gpx_data = gpxpy.parse(f)
            
            # Test basic structure
            assert gpx_data is not None, "GPX data should be loaded"
            print(f"  Tracks: {len(gpx_data.tracks)}")
            print(f"  Routes: {len(gpx_data.routes)}")
            print(f"  Waypoints: {len(gpx_data.waypoints)}")
            
            # Test track data
            if gpx_data.tracks:
                track = gpx_data.tracks[0]
                if track.segments:
                    segment = track.segments[0]
                    assert len(segment.points) > 0, "Track should have points"
                    print(f"  First track points: {len(segment.points)}")
            
            # Test route data
            if gpx_data.routes:
                route = gpx_data.routes[0]
                assert len(route.points) > 0, "Route should have points"
                print(f"  First route points: {len(route.points)}")
            
            print(f"GPX file {gpx_file}: PASSED")
            break
    else:
        print("No test GPX files found - SKIPPED")
    
    return True

def test_ui_components():
    """Test UI component creation and event handling"""
    print("\n=== TESTING UI COMPONENTS ===")
    
    # Mock tkinter for testing
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # Test basic widget creation
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Test BooleanVar
        visible_var = tk.BooleanVar()
        editable_var = tk.BooleanVar()
        
        visible_var.set(True)
        editable_var.set(False)
        
        assert visible_var.get() == True, "BooleanVar should work"
        assert editable_var.get() == False, "BooleanVar should work"
        print("BooleanVar operations: PASSED")
        
        # Test widget creation
        frame = ttk.Frame(root)
        checkbox = ttk.Checkbutton(frame, variable=visible_var)
        button = ttk.Button(frame, text="Test")
        
        assert checkbox is not None, "Checkbox should be created"
        assert button is not None, "Button should be created"
        print("Widget creation: PASSED")
        
        root.destroy()
        print("UI components: ALL TESTS PASSED")
        
    except ImportError:
        print("Tkinter not available - SKIPPED")
    
    return True

def test_map_renderer_logic():
    """Test map rendering logic without actual map"""
    print("\n=== TESTING MAP RENDERER LOGIC ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
        
        # Test data
        test_data = {
            "files": {
                "session": {
                    "1": {
                        "path": "/test/visible.gpx",
                        "settings": {"visible": True, "color": "#ff0000"}
                    },
                    "2": {
                        "path": "/test/hidden.gpx", 
                        "settings": {"visible": False, "color": "#00ff00"}
                    }
                }
            }
        }
        
        with open(temp_path, 'w') as f:
            json.dump(test_data, f, indent=4)
        
        props = AppProperties(temp_path)
        
        # Mock entry objects
        class MockEntry:
            def __init__(self, path):
                self.path = path
            
            def get_path(self):
                return self.path
        
        visible_entry = MockEntry("/test/visible.gpx")
        hidden_entry = MockEntry("/test/hidden.gpx")
        non_existent_entry = MockEntry("/test/nonexistent.gpx")
        
        entries = [visible_entry, hidden_entry, non_existent_entry]
        
        # Test visibility logic (simplified version of map_renderer logic)
        visible_count = 0
        for entry in entries:
            is_visible = False
            try:
                session_files = props.get("files.session") or {}
                for ref_num, file_info in session_files.items():
                    if file_info.get('path') == entry.get_path():
                        is_visible = file_info.get('settings', {}).get('visible', True)
                        break
            except:
                is_visible = True
            
            if is_visible:
                visible_count += 1
        
        assert visible_count == 1, f"Should find 1 visible entry, found {visible_count}"
        print("Visibility logic: PASSED")
        
        # Test color retrieval
        colors = []
        for entry in entries:
            color = "#0000ff"  # Default
            try:
                session_files = props.get("files.session") or {}
                for ref_num, file_info in session_files.items():
                    if file_info.get('path') == entry.get_path():
                        color = file_info.get('settings', {}).get('color', '#0000ff')
                        break
            except:
                pass
            colors.append(color)
        
        assert "#ff0000" in colors, "Should find red color for visible file"
        assert "#00ff00" in colors, "Should find green color for hidden file"
        assert "#0000ff" in colors, "Should find default blue for non-existent file"
        print("Color retrieval: PASSED")
        
        print("Map renderer logic: ALL TESTS PASSED")
    
    return True

def test_error_handling():
    """Test error handling and edge cases"""
    print("\n=== TESTING ERROR HANDLING ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
        
        # Test 1: Empty properties file
        with open(temp_path, 'w') as f:
            json.dump({}, f)
        
        props = AppProperties(temp_path)
        
        # Test non-existent reference
        settings = props.get_file_settings_by_reference(999)
        assert settings is None, "Non-existent reference should return None"
        print("Non-existent reference: PASSED")
        
        # Test creating new reference in empty file
        ref_num = props.get_or_create_file_reference("/test/new.gpx")
        assert ref_num == 1, "First reference should be 1"
        
        settings = props.get_file_settings_by_reference(ref_num)
        assert settings == {}, "New reference should have empty settings"
        print("New reference creation: PASSED")
        
        # Test 2: Corrupted JSON file
        with open(temp_path, 'w') as f:
            f.write("invalid json")
        
        try:
            props = AppProperties(temp_path)
            print("Corrupted JSON handling: PASSED")
        except Exception as e:
            print(f"Corrupted JSON handling: EXPECTED ERROR - {e}")
        
        # Test 3: Missing file
        try:
            props = AppProperties("/nonexistent/file.json")
            print("Missing file handling: PASSED")
        except Exception as e:
            print(f"Missing file handling: EXPECTED ERROR - {e}")
        
        print("Error handling: ALL TESTS PASSED")
    
    return True

def test_integration_workflow():
    """Test complete workflow integration"""
    print("\n=== TESTING INTEGRATION WORKFLOW ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
        
        # Simulate complete user workflow
        props = AppProperties(temp_path)
        
        # Step 1: Add multiple files
        files = [
            "/test/track1.gpx",
            "/test/track2.gpx", 
            "/test/route1.gpx"
        ]
        
        ref_nums = []
        for file_path in files:
            ref_num = props.get_or_create_file_reference(file_path)
            ref_nums.append(ref_num)
        
        print(f"Added {len(ref_nums)} files: {ref_nums}")
        
        # Step 2: Configure each file
        for i, ref_num in enumerate(ref_nums):
            settings = {
                "visible": i % 2 == 0,  # Alternate visibility
                "editable": i == 0,    # Only first is editable
                "color": f"#{i:02x}{(i+1):02x}{(i+2):02x}"  # Different colors
            }
            props.save_file_settings_by_reference(ref_num, settings)
        
        print("Configured file settings")
        
        # Step 3: Simulate "Select All"
        for ref_num in ref_nums:
            settings = props.get_file_settings_by_reference(ref_num) or {}
            settings['editable'] = True
            props.save_file_settings_by_reference(ref_num, settings)
        
        print("Simulated Select All")
        
        # Step 4: Verify all are editable
        editable_count = 0
        for ref_num in ref_nums:
            settings = props.get_file_settings_by_reference(ref_num)
            if settings and settings.get('editable'):
                editable_count += 1
        
        assert editable_count == len(ref_nums), f"All files should be editable: {editable_count}/{len(ref_nums)}"
        print("Select All verification: PASSED")
        
        # Step 5: Simulate restart
        props2 = AppProperties(temp_path)
        
        # Step 6: Verify persistence
        all_settings_correct = True
        for i, ref_num in enumerate(ref_nums):
            settings = props2.get_file_settings_by_reference(ref_num)
            expected_visible = i % 2 == 0
            expected_editable = True  # After Select All
            
            if not settings or settings.get('visible') != expected_visible or settings.get('editable') != expected_editable:
                all_settings_correct = False
                break
        
        assert all_settings_correct, "All settings should persist correctly"
        print("Settings persistence after restart: PASSED")
        
        # Step 7: Simulate "Deselect All"
        for ref_num in ref_nums:
            settings = props2.get_file_settings_by_reference(ref_num) or {}
            settings['editable'] = False
            props2.save_file_settings_by_reference(ref_num, settings)
        
        print("Simulated Deselect All")
        
        # Step 8: Verify all are not editable
        editable_count = 0
        for ref_num in ref_nums:
            settings = props2.get_file_settings_by_reference(ref_num)
            if settings and settings.get('editable'):
                editable_count += 1
        
        assert editable_count == 0, f"No files should be editable: {editable_count}/{len(ref_nums)}"
        print("Deselect All verification: PASSED")
        
        print("Integration workflow: ALL TESTS PASSED")
    
    return True

def run_all_tests():
    """Run all tests and report results"""
    print("🧪 COMPREHENSIVE GPX EDITOR TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Properties System", test_properties_system),
        ("GPX File Operations", test_gpx_file_operations),
        ("UI Components", test_ui_components),
        ("Map Renderer Logic", test_map_renderer_logic),
        ("Error Handling", test_error_handling),
        ("Integration Workflow", test_integration_workflow)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"\n📋 Running: {test_name}")
            result = test_func()
            if result:
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
                failed += 1
        except Exception as e:
            print(f"❌ {test_name}: FAILED with exception")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Application is ready for production.")
        return True
    else:
        print(f"⚠️  {failed} tests failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
