#!/usr/bin/env python3
"""
Integration Tests for TomsGPXEditor - Updated Version

Tests the complete application workflow after refactoring:
- File loading and management
- UI interactions
- Map rendering
- Properties persistence
- Controller interactions
"""

import sys
import os
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestGPXEditorIntegration(unittest.TestCase):
    """Integration tests for the complete GPX Editor application"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_properties_file = os.path.join(self.test_dir, 'test_properties.json')
        
        # Create minimal test GPX file
        self.test_gpx_file = os.path.join(self.test_dir, 'test.gpx')
        with open(self.test_gpx_file, 'w') as f:
            f.write("""<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1">
  <trk>
    <name>Test Track</name>
    <trkseg>
      <trkpt lat="51.0" lon="10.0"></trkpt>
      <trkpt lat="51.1" lon="10.1"></trkpt>
    </trkseg>
  </trk>
</gpx>""")
        
        # Create test properties
        self.test_properties = {
            "files": {
                "session": {}
            },
            "dialogs": {
                "settings": {
                    "logging": {
                        "level": "INFO",
                        "file": "test.log"
                    }
                }
            }
        }
        
        with open(self.test_properties_file, 'w') as f:
            json.dump(self.test_properties, f)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_properties_repository_integration(self):
        """Test PropertiesRepository integration"""
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Test properties loading
        props = AppProperties(self.test_properties_file)
        props.load()
        
        # Test file reference creation
        ref_num = props.get_or_create_file_reference(self.test_gpx_file)
        self.assertIsInstance(ref_num, int)
        self.assertEqual(ref_num, 1)
        
        # Test settings save/load
        settings = {"visible": True, "editable": False, "color": "#ff0000"}
        props.save_file_settings_by_reference(ref_num, settings)
        
        loaded_settings = props.get_file_settings_by_reference(ref_num)
        self.assertEqual(loaded_settings, settings)
        
        # Test persistence
        props.save()
        props2 = AppProperties(self.test_properties_file)
        props2.load()
        
        loaded_settings2 = props2.get_file_settings_by_reference(ref_num)
        self.assertEqual(loaded_settings2, settings)
    
    def test_file_entry_builder_integration(self):
        """Test FileEntryBuilder integration"""
        from src.ui.widgets.file_entry_builder import FileEntryBuilder
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Create mock parent frame
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        try:
            frame = tk.Frame(root)
            
            # Create properties
            props = AppProperties(self.test_properties_file)
            props.load()
            
            # Create FileEntryBuilder
            builder = FileEntryBuilder(
                parent_frame=frame,
                row=0,
                button_update_callback=Mock(),
                editable_update_callback=Mock()
            )
            
            # Create file entry
            ref_num = props.get_or_create_file_reference(self.test_gpx_file)
            file_analysis = {'file_type': 'track', 'track_count': 1, 'route_count': 0}
            settings = {"visible": True, "editable": False}
            
            entry = builder.create_file_entry(
                path=self.test_gpx_file,
                ref_num=ref_num,
                file_analysis=file_analysis,
                settings=settings,
                properties=props
            )
            
            self.assertIsNotNone(entry)
            self.assertTrue(hasattr(entry, 'is_visible'))
            self.assertTrue(hasattr(entry, 'is_editable'))
            
            # Test checkbox functionality
            self.assertTrue(entry.is_visible())
            self.assertFalse(entry.is_editable())
            
        finally:
            root.destroy()
    
    def test_map_controller_integration(self):
        """Test MapController integration"""
        from src.application.map_controller import MapController
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Create mock map widget
        mock_map_widget = Mock()
        mock_map_widget.winfo_exists.return_value = True
        
        # Create properties
        props = AppProperties(self.test_properties_file)
        props.load()
        
        # Create map controller
        controller = MapController(mock_map_widget, props)
        
        # Test entry visibility check
        mock_entry = Mock()
        mock_entry.get_path.return_value = self.test_gpx_file
        
        # Add file to properties
        ref_num = props.get_or_create_file_reference(self.test_gpx_file)
        settings = {"visible": True}
        props.save_file_settings_by_reference(ref_num, settings)
        
        # Test visibility check
        is_visible = controller._is_entry_visible(mock_entry)
        self.assertTrue(is_visible)
    
    def test_gpx_file_manager_integration(self):
        """Test GPXFileManager integration"""
        from src.application.gpx_file_manager import GPXFileManager
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Create mock UI components
        root = tk.Tk()
        root.withdraw()
        
        try:
            mock_map_widget = Mock()
            mock_map_widget.winfo_exists.return_value = True
            
            frame = tk.Frame(root)
            
            # Create properties and manager
            props = AppProperties(self.test_properties_file)
            props.load()
            
            manager = GPXFileManager(
                properties=props,
                map_widget=mock_map_widget,
                main_grid=frame,
                button_update_callback=Mock(),
                editable_update_callback=Mock(),
                recent_files_manager=Mock()
            )
            
            # Test file addition
            entry = manager.add_file_to_ui(self.test_gpx_file)
            self.assertIsNotNone(entry)
            
            # Test file analysis
            analysis = manager.load_gpx_file(self.test_gpx_file)
            self.assertIsNotNone(analysis)
            self.assertEqual(analysis['file_type'], 'track')
            
            # Test entry management
            entries = manager.get_all_entries()
            self.assertEqual(len(entries), 1)
            
            visible_entries = manager.get_visible_entries()
            self.assertEqual(len(visible_entries), 1)
            
            # Test file removal
            manager.remove_file_from_ui(entry)
            entries_after = manager.get_all_entries()
            self.assertEqual(len(entries_after), 0)
            
        finally:
            root.destroy()
    
    def test_properties_consistency(self):
        """Test properties consistency across components"""
        from src.infrastructure.repositories.properties_repository import AppProperties
        from src.application.map_controller import MapController
        from src.application.gpx_file_manager import GPXFileManager
        
        # Create mock UI components
        root = tk.Tk()
        root.withdraw()
        
        try:
            mock_map_widget = Mock()
            mock_map_widget.winfo_exists.return_value = True
            frame = tk.Frame(root)
            
            # Create shared properties
            props = AppProperties(self.test_properties_file)
            props.load()
            
            # Add file to properties
            ref_num = props.get_or_create_file_reference(self.test_gpx_file)
            settings = {"visible": True, "editable": False, "color": "#00ff00"}
            props.save_file_settings_by_reference(ref_num, settings)
            
            # Test consistency across components
            manager = GPXFileManager(
                properties=props,
                map_widget=mock_map_widget,
                main_grid=frame,
                button_update_callback=Mock(),
                editable_update_callback=Mock(),
                recent_files_manager=Mock()
            )
            
            controller = MapController(mock_map_widget, props)
            
            # All components should see the same data
            settings1 = props.get_file_settings_by_reference(ref_num)
            self.assertEqual(settings1['visible'], True)
            
            # Test that changes are consistent
            settings['visible'] = False
            props.save_file_settings_by_reference(ref_num, settings)
            
            settings2 = props.get_file_settings_by_reference(ref_num)
            self.assertEqual(settings2['visible'], False)
            
        finally:
            root.destroy()
    
    def test_error_handling_integration(self):
        """Test error handling across the application"""
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Test with invalid properties file
        invalid_file = os.path.join(self.test_dir, 'invalid.json')
        with open(invalid_file, 'w') as f:
            f.write('invalid json content')
        
        # Should handle gracefully
        props = AppProperties(invalid_file)
        try:
            props.load()
            # Should have default values
            self.assertIsNotNone(props.data)
        except Exception as e:
            self.fail(f"Properties loading should handle errors gracefully: {e}")
        
        # Test with non-existent file
        non_existent = os.path.join(self.test_dir, 'non_existent.json')
        props2 = AppProperties(non_existent)
        props2.load()
        self.assertIsNotNone(props2.data)
    
    def test_full_workflow_integration(self):
        """Test complete workflow from file loading to map rendering"""
        from src.infrastructure.repositories.properties_repository import AppProperties
        from src.application.gpx_file_manager import GPXFileManager
        from src.application.map_controller import MapController
        
        # Create mock UI components
        root = tk.Tk()
        root.withdraw()
        
        try:
            mock_map_widget = Mock()
            mock_map_widget.winfo_exists.return_value = True
            frame = tk.Frame(root)
            
            # Create components
            props = AppProperties(self.test_properties_file)
            props.load()
            
            manager = GPXFileManager(
                properties=props,
                map_widget=mock_map_widget,
                main_grid=frame,
                button_update_callback=Mock(),
                editable_update_callback=Mock(),
                recent_files_manager=Mock()
            )
            
            controller = MapController(mock_map_widget, props)
            
            # Complete workflow
            # 1. Add file
            entry = manager.add_file_to_ui(self.test_gpx_file)
            self.assertIsNotNone(entry)
            
            # 2. Check visibility
            is_visible = controller._is_entry_visible(entry)
            self.assertTrue(is_visible)
            
            # 3. Update visibility
            ref_num = props.get_or_create_file_reference(self.test_gpx_file)
            settings = {"visible": False}
            props.save_file_settings_by_reference(ref_num, settings)
            
            # 4. Check updated visibility
            is_visible_after = controller._is_entry_visible(entry)
            self.assertFalse(is_visible_after)
            
            # 5. Remove file
            manager.remove_file_from_ui(entry)
            entries_after = manager.get_all_entries()
            self.assertEqual(len(entries_after), 0)
            
        finally:
            root.destroy()
    
    def test_application_startup_integration(self):
        """Test application can startup without errors"""
        try:
            # Test that main modules can be imported
            import app
            from src.infrastructure.repositories.properties_repository import AppProperties
            from src.application.gpx_file_manager import GPXFileManager
            from src.application.map_controller import MapController
            from src.application.dialog_controller import DialogController
            from src.ui.widgets.file_entry_builder import FileEntryBuilder
            
            # Test that no old modules can be imported
            with self.assertRaises(ImportError):
                from src.ui.widgets.file_entry import FileEntry
            
            with self.assertRaises(ImportError):
                from src.infrastructure.di_container import DIContainer
            
            with self.assertRaises(ImportError):
                from src.application.app_factory import AppFactory
            
        except Exception as e:
            self.fail(f"Application modules should be importable: {e}")


if __name__ == '__main__':
    # Configure logging for tests
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    # Run tests
    unittest.main(verbosity=2)
