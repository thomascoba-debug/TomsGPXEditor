#!/usr/bin/env python3
"""
Regression Tests for TomsGPXEditor

Tests for regression detection after major refactoring:
- FileEntry vs FileEntryBuilder compatibility
- Properties structure consistency
- Controller integration
- Map rendering functionality
- Error handling
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

class TestGPXEditorRegression(unittest.TestCase):
    """Regression tests for GPX Editor after refactoring"""
    
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
        
        # Create test properties with new structure
        self.test_properties = {
            "files": {
                "session": {}
            },
            "dialogs": {
                "settings": {
                    "logging": {
                        "level": "INFO",
                        "file": "test.log"
                    },
                    "rendering": {
                        "line_width": 3,
                        "color_scheme": "default"
                    }
                }
            },
            "app": {
                "main_window": {
                    "geometry": "800x600+100+100"
                },
                "recent_files_timestamps": {}
            }
        }
        
        with open(self.test_properties_file, 'w') as f:
            json.dump(self.test_properties, f)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_no_old_fileentry_imports(self):
        """Regression test: Ensure old FileEntry imports are removed"""
        try:
            # This should fail - old FileEntry should not be importable
            from src.ui.widgets.file_entry import FileEntry
            self.fail("Old FileEntry should not be importable after refactoring")
        except ImportError:
            # This is expected
            pass
        
        # But FileEntryBuilder should be importable
        try:
            from src.ui.widgets.file_entry_builder import FileEntryBuilder
        except ImportError as e:
            self.fail(f"FileEntryBuilder should be importable: {e}")
    
    def test_no_di_container_imports(self):
        """Regression test: Ensure DI container imports are removed"""
        try:
            from src.infrastructure.di_container import DIContainer
            self.fail("DIContainer should not be importable after refactoring")
        except ImportError:
            # This is expected
            pass
        
        try:
            from src.infrastructure.container_config import ContainerConfig
            self.fail("ContainerConfig should not be importable after refactoring")
        except ImportError:
            # This is expected
            pass
    
    def test_no_app_factory_imports(self):
        """Regression test: Ensure AppFactory imports are removed"""
        try:
            from src.application.app_factory import AppFactory
            self.fail("AppFactory should not be importable after refactoring")
        except ImportError:
            # This is expected
            pass
    
    def test_properties_structure_consistency(self):
        """Regression test: Ensure properties structure is consistent"""
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Load properties
        props = AppProperties(self.test_properties_file)
        props.load()
        
        # Test new structure exists
        self.assertIn("files", props.data)
        self.assertIn("session", props.data["files"])
        self.assertIn("dialogs", props.data)
        self.assertIn("app", props.data)
        
        # Test old structure does not exist
        self.assertNotIn("session_files", props.data)
        self.assertNotIn("dialog_geometry", props.data)
        
        # Test file reference functionality works
        ref_num = props.get_or_create_file_reference(self.test_gpx_file)
        self.assertIsInstance(ref_num, int)
        
        settings = {"visible": True, "editable": False}
        props.save_file_settings_by_reference(ref_num, settings)
        
        loaded_settings = props.get_file_settings_by_reference(ref_num)
        self.assertEqual(loaded_settings, settings)
    
    def test_file_entry_builder_functionality(self):
        """Regression test: Ensure FileEntryBuilder works correctly"""
        from src.ui.widgets.file_entry_builder import FileEntryBuilder
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Create mock parent frame
        root = tk.Tk()
        root.withdraw()
        
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
            
            # Test that create_from_container method is removed
            self.assertFalse(hasattr(builder, 'create_from_container'))
            
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
            self.assertTrue(hasattr(entry, 'get_path'))
            
        finally:
            root.destroy()
    
    def test_controller_initialization_without_container(self):
        """Regression test: Controllers should work without DI container"""
        from src.application.map_controller import MapController
        from src.application.gpx_file_manager import GPXFileManager
        from src.application.dialog_controller import DialogController
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Create mock UI components
        root = tk.Tk()
        root.withdraw()
        
        try:
            mock_map_widget = Mock()
            mock_map_widget.winfo_exists.return_value = True
            frame = tk.Frame(root)
            mock_app = Mock()
            mock_app._save_properties = Mock()
            
            # Create properties
            props = AppProperties(self.test_properties_file)
            props.load()
            
            # Test MapController
            map_controller = MapController(mock_map_widget, props)
            self.assertIsNotNone(map_controller)
            self.assertFalse(hasattr(map_controller, 'create_from_container'))
            
            # Test DialogController
            dialog_controller = DialogController(mock_app, props, mock_app._save_properties)
            self.assertIsNotNone(dialog_controller)
            self.assertFalse(hasattr(dialog_controller, 'create_from_container'))
            
            # Test GPXFileManager
            file_manager = GPXFileManager(
                properties=props,
                map_widget=mock_map_widget,
                main_grid=frame,
                button_update_callback=Mock(),
                editable_update_callback=Mock(),
                recent_files_manager=Mock()
            )
            self.assertIsNotNone(file_manager)
            self.assertFalse(hasattr(file_manager, 'create_from_container'))
            
        finally:
            root.destroy()
    
    def test_app_initialization_without_container(self):
        """Regression test: App should initialize without DI container"""
        # Test that app.py doesn't try to use container
        # This is a smoke test - if it fails, there are still container references
        
        try:
            # Import should work
            import app
            self.assertTrue(hasattr(app, 'TomsGPXEditor'))
            
            # Check that no container-related imports are at the top level
            import inspect
            source = inspect.getsource(app)
            
            # These should not be in the source
            self.assertNotIn('di_container', source)
            self.assertNotIn('container_config', source)
            self.assertNotIn('AppFactory', source)
            
        except Exception as e:
            self.fail(f"App module should be importable without container dependencies: {e}")
    
    def test_ui_imports_consistency(self):
        """Regression test: UI imports should be consistent"""
        try:
            # Test that UI widgets import correctly
            from src.ui.widgets import FileEntryBuilder
            from src.ui.widgets import GPXTableEditor
            from src.ui.widgets import ProgressManager
            
            # Test that old FileEntry is not in UI widgets
            import src.ui.widgets as widgets_module
            self.assertNotIn('FileEntry', widgets_module.__all__)
            self.assertIn('FileEntryBuilder', widgets_module.__all__)
            
        except ImportError as e:
            self.fail(f"UI widgets should import correctly: {e}")
    
    def test_error_handling_after_refactoring(self):
        """Regression test: Error handling should still work after refactoring"""
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Test with corrupted properties file
        corrupted_file = os.path.join(self.test_dir, 'corrupted.json')
        with open(corrupted_file, 'w') as f:
            f.write('{"incomplete": json')
        
        props = AppProperties(corrupted_file)
        
        # Should handle gracefully
        try:
            props.load()
            # Should have default data structure
            self.assertIsInstance(props.data, dict)
        except Exception as e:
            self.fail(f"Properties loading should handle corrupted files gracefully: {e}")
    
    def test_gpx_file_operations_after_refactoring(self):
        """Regression test: GPX file operations should work after refactoring"""
        from src.application.gpx_file_manager import GPXFileManager
        from src.infrastructure.repositories.properties_repository import AppProperties
        
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
            
            # Test file operations
            entry = manager.add_file_to_ui(self.test_gpx_file)
            self.assertIsNotNone(entry)
            
            # Test file analysis
            analysis = manager.load_gpx_file(self.test_gpx_file)
            self.assertIsNotNone(analysis)
            self.assertIn('file_type', analysis)
            
            # Test entry management
            entries = manager.get_all_entries()
            self.assertEqual(len(entries), 1)
            
            # Test removal
            manager.remove_file_from_ui(entry)
            entries_after = manager.get_all_entries()
            self.assertEqual(len(entries_after), 0)
            
        finally:
            root.destroy()
    
    def test_map_rendering_after_refactoring(self):
        """Regression test: Map rendering should work after refactoring"""
        from src.infrastructure.map_renderer import GPXCache
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Test GPX cache
        gpx_data = GPXCache.get_gpx(self.test_gpx_file)
        self.assertIsNotNone(gpx_data)
        
        # Test that map renderer uses correct properties structure
        props = AppProperties(self.test_properties_file)
        props.load()
        
        # Add file to properties
        ref_num = props.get_or_create_file_reference(self.test_gpx_file)
        settings = {"visible": True, "editable": False}
        props.save_file_settings_by_reference(ref_num, settings)
        
        # Verify structure
        session_data = props.data.get('files', {}).get('session', {})
        self.assertIn(str(ref_num), session_data)
        self.assertEqual(session_data[str(ref_num)]['settings'], settings)


class TestPerformanceRegression(unittest.TestCase):
    """Performance regression tests"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_properties_file = os.path.join(self.test_dir, 'test_properties.json')
        
        # Create larger test GPX file
        self.test_gpx_file = os.path.join(self.test_dir, 'large_test.gpx')
        with open(self.test_gpx_file, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?><gpx version="1.1"><trk><name>Large Test Track</name><trkseg>')
            for i in range(100):
                lat = 51.0 + i * 0.001
                lon = 10.0 + i * 0.001
                f.write(f'<trkpt lat="{lat}" lon="{lon}"></trkpt>')
            f.write('</trkseg></trk></gpx>')
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_file_loading_performance(self):
        """Test that file loading performance hasn't regressed"""
        import time
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Create properties
        props = AppProperties(self.test_properties_file)
        with open(self.test_properties_file, 'w') as f:
            json.dump({"files": {"session": {}}}, f)
        props.load()
        
        # Test file reference creation performance
        start_time = time.time()
        for i in range(10):
            ref_num = props.get_or_create_file_reference(self.test_gpx_file)
        end_time = time.time()
        
        # Should complete quickly (less than 1 second for 10 operations)
        self.assertLess(end_time - start_time, 1.0, "File reference creation should be fast")


if __name__ == '__main__':
    # Configure logging for tests
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    # Run tests
    unittest.main(verbosity=2)
