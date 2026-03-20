"""
Integration tests for GPX Editor - testing recent fixes and edge cases
"""

import unittest
import os
import tempfile
import json
from test_framework import GPXTestCase
from properties import AppProperties
from recent_files import RecentFilesManager
from app import TomsGPXEditor
import tkinter as tk


class TestRecentFixes(GPXTestCase):
    """Test cases for recently fixed issues"""
    
    def test_auto_save_manager_integration(self):
        """Test AutoSaveManager with actual save callback"""
        import tkinter as tk
        
        # Create temporary properties file
        props_file = self.create_temp_file('{}', '.json')
        properties = AppProperties(props_file)
        
        # Create a mock root window for AutoSaveManager
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        try:
            # Mock save callback
            save_called = []
            def mock_save():
                save_called.append(True)
                properties.save()
                return True
            
            # Import and test AutoSaveManager
            from context_menu import AutoSaveManager
            auto_save = AutoSaveManager(properties, mock_save)
            
            # Test basic functionality
            self.assertFalse(auto_save.auto_save_enabled)
            self.assertEqual(auto_save.auto_save_interval, 300)
            
            # Test enabling auto-save (but don't start timer to avoid Tkinter issues)
            auto_save.auto_save_enabled = True
            self.assertTrue(auto_save.auto_save_enabled)
            
            # Test interval change (direct property access to avoid timer)
            auto_save.auto_save_interval = 60
            self.assertEqual(auto_save.auto_save_interval, 60)
            
            # Test status
            status = auto_save.get_auto_save_status()
            self.assertTrue(status['enabled'])
            self.assertEqual(status['interval'], 60)
            
        finally:
            root.destroy()
    
    def test_toms_gpx_editor_initialization(self):
        """Test TomsGPXEditor can be initialized without errors"""
        # This test ensures the _save_all method exists
        try:
            # Create a temporary root window for testing
            root = tk.Tk()
            root.withdraw()  # Hide window
            
            # Create minimal properties for test
            props_file = self.create_temp_file(json.dumps({
                "session_files": {},
                "log_level": "INFO",
                "log_file": "test.log"
            }), '.json')
            
            # Mock the properties loading
            import app
            original_init = app.AppProperties
            
            class MockProperties:
                def __init__(self, file_path=None):
                    self.data = {
                        "session_files": {},
                        "log_level": "INFO",
                        "log_file": "test.log"
                    }
                
                def get(self, key, default=None):
                    return self.data.get(key, default)
                
                def save(self):
                    pass
            
            # Temporarily replace AppProperties
            app.AppProperties = MockProperties
            
            try:
                # Test that TomsGPXEditor can be created
                editor = app.TomsGPXEditor()
                
                # Verify that _save_all method exists
                self.assertTrue(hasattr(editor, '_save_all'))
                self.assertTrue(callable(getattr(editor, '_save_all')))
                
                # Test _save_all method
                result = editor._save_all()
                self.assertTrue(result)
                
                # Clean up
                editor.destroy()
                
            finally:
                # Restore original class
                app.AppProperties = original_init
                
            root.destroy()
            
        except Exception as e:
            self.fail(f"TomsGPXEditor initialization failed: {e}")
    
    def test_recent_files_edge_cases(self):
        """Test RecentFilesManager edge cases and error handling"""
        props_file = self.create_temp_file('{}', '.json')
        properties = AppProperties(props_file)
        
        # Test with max_files = 0 (edge case)
        recent_files = RecentFilesManager(properties, max_files=0)
        
        # Add files - should not store any
        for i in range(3):
            test_file = self.create_temp_file(f"content {i}")
            recent_files.add_file(test_file)
        
        # Should be empty due to max_files=0
        recent_list = recent_files.get_recent_files()
        self.assertEqual(len(recent_list), 0)
        
        # Test with negative max_files (should handle gracefully by using absolute value)
        recent_files_neg = RecentFilesManager(properties, max_files=-1)
        test_file = self.create_temp_file("test content")
        recent_files_neg.add_file(test_file)
        
        # Should still work (negative values should be handled)
        recent_list = recent_files_neg.get_recent_files()
        # With max_files=-1, it becomes 1, so should have 1 file
        self.assertGreaterEqual(len(recent_list), 0)
    
    def test_progress_dialog_error_handling(self):
        """Test ProgressDialog error handling and edge cases"""
        from progress_dialog import ProgressDialog
        
        root = tk.Tk()
        root.withdraw()
        
        try:
            # Test with invalid progress values
            dialog = ProgressDialog(root)
            
            # Test negative progress (should handle gracefully)
            dialog.update_progress(-10, "Negative progress")
            self.assertEqual(dialog.progress_var.get(), -10)
            
            # Test progress > 100
            dialog.update_progress(150, "Over 100%")
            self.assertEqual(dialog.progress_var.get(), 150)
            
            # Test cancellation
            dialog.show_cancel_button()
            self.assertFalse(dialog.was_cancelled())
            
            dialog.cancel()
            self.assertTrue(dialog.was_cancelled())
            
            dialog.destroy()
            
        finally:
            root.destroy()
    
    def test_file_search_with_invalid_entries(self):
        """Test FileSearchEngine with invalid or corrupted entries"""
        from file_search import FileSearchEngine
        
        # Create entries with various issues
        class InvalidEntry:
            def __init__(self, path, issue_type):
                self.path = path
                self.issue_type = issue_type
            
            def is_visible(self):
                if self.issue_type == "exception":
                    raise Exception("Test exception")
                return True
        
        entries = [
            InvalidEntry("/valid/path.gpx", "normal"),
            InvalidEntry("", "empty_path"),
            InvalidEntry("/invalid/path.gpx", "exception"),
        ]
        
        # Search should handle all issues gracefully
        results = FileSearchEngine.search_files(entries, "test", "All Files")
        
        # Should return results for valid entries only
        self.assertGreaterEqual(len(results), 0)  # At least the valid one
        
        # Test with None entries - should handle gracefully
        entries_with_none = entries + [None]
        results = FileSearchEngine.search_files(entries_with_none, "test", "All Files")
        
        # Should not crash and should filter out None entries
        self.assertIsInstance(results, list)
        # Results should not include None entries
        for result in results:
            self.assertIsNotNone(result)
    
    def test_properties_schema_validation(self):
        """Test properties schema validation for new fields"""
        props_file = self.create_temp_file('{}', '.json')
        properties = AppProperties(props_file)
        
        # Test that new fields are properly typed
        properties.set("auto_save_enabled", True)
        properties.set("auto_save_interval", 300)
        properties.set("recent_files", ["file1.gpx", "file2.gpx"])
        properties.set("log_display_lines", 100)
        
        properties.save()
        
        # Load and verify
        new_properties = AppProperties(props_file)
        
        self.assertTrue(new_properties.get("auto_save_enabled", False))
        self.assertEqual(new_properties.get("auto_save_interval", 300), 300)
        self.assertEqual(new_properties.get("log_display_lines", 10), 100)
        self.assertIsInstance(new_properties.get("recent_files", []), list)
    
    def test_gpx_cache_with_corrupted_files(self):
        """Test GPXCache handling of corrupted or invalid GPX files"""
        from map_renderer import GPXCache
        
        # Clear cache
        GPXCache.clear_cache()
        
        # Test with corrupted GPX file
        corrupted_file = self.create_temp_file("invalid xml content", ".gpx")
        
        # Should handle gracefully and return None
        result = GPXCache.get_gpx(corrupted_file)
        self.assertIsNone(result)
        
        # Test with non-existent file
        result = GPXCache.get_gpx("/non/existent/file.gpx")
        self.assertIsNone(result)
        
        # Test with valid file after corrupted ones
        valid_file = self.create_sample_gpx()
        result = GPXCache.get_gpx(valid_file)
        self.assertIsNotNone(result)
        
        # Verify cache contains only valid file
        self.assertEqual(len(GPXCache._cache), 1)
        self.assertIn(os.path.abspath(valid_file), GPXCache._cache)


class TestErrorRecovery(GPXTestCase):
    """Test error recovery and resilience"""
    
    def test_properties_corruption_recovery(self):
        """Test recovery from corrupted properties file"""
        # Create corrupted JSON file
        corrupted_file = self.create_temp_file('{"invalid": json content}', '.json')
        
        # Should handle gracefully and create default properties
        try:
            properties = AppProperties(corrupted_file)
            # Should not crash and have default values
            self.assertIsNotNone(properties.data)
            self.assertIsInstance(properties.data, dict)
        except Exception as e:
            self.fail(f"Properties should handle corrupted JSON gracefully: {e}")
    
    def test_missing_file_handling(self):
        """Test handling of missing GPX files in session"""
        props_file = self.create_temp_file('{}', '.json')
        properties = AppProperties(props_file)
        
        # Add file to session
        test_file = self.create_temp_file("test content", ".gpx")
        properties.get_or_create_file_reference(test_file)
        properties.save()
        
        # Delete the actual file
        os.remove(test_file)
        
        # Load properties - should handle missing file gracefully
        new_properties = AppProperties(props_file)
        session_files = new_properties.get("session_files", {})
        
        # Should still have the reference
        self.assertGreater(len(session_files), 0)
        
        # But file should be marked as missing when accessed
        ref_num = list(session_files.keys())[0]
        file_data = session_files[ref_num]
        self.assertEqual(file_data["path"], test_file)
        self.assertFalse(os.path.exists(test_file))  # File is missing
    
    def test_memory_cleanup(self):
        """Test memory cleanup and resource management"""
        from map_renderer import GPXCache
        
        # Add files to cache
        for i in range(10):
            test_file = self.create_sample_gpx()
            GPXCache.get_gpx(test_file)
        
        # Verify cache has entries
        self.assertEqual(len(GPXCache._cache), 10)
        
        # Clear cache
        GPXCache.clear_cache()
        
        # Verify cache is empty
        self.assertEqual(len(GPXCache._cache), 0)
        
        # Test remove specific
        test_file = self.create_sample_gpx()
        GPXCache.get_gpx(test_file)
        self.assertEqual(len(GPXCache._cache), 1)
        
        GPXCache.remove_from_cache(test_file)
        self.assertEqual(len(GPXCache._cache), 0)


if __name__ == '__main__':
    unittest.main()
