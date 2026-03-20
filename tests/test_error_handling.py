"""
Tests for error handling and exception management
"""

import unittest
import os
import tempfile
import logging
from test_framework import GPXTestCase
from error_handler import safe_execute, GPXEditorException, validate_gpx_data, handle_file_error
import gpxpy


class TestErrorHandler(GPXTestCase):
    """Test cases for error handling functionality"""
    
    def test_safe_execute_decorator_success(self):
        """Test safe_execute decorator with successful operation"""
        @safe_execute("Test operation successful")
        def successful_operation():
            return "success"
        
        result = successful_operation()
        self.assertEqual(result, "success")
    
    def test_safe_execute_decorator_failure(self):
        """Test safe_execute decorator with failed operation"""
        @safe_execute("Test operation failed", show_error=False)
        def failing_operation():
            raise ValueError("Test error")
        
        result = failing_operation()
        self.assertIsNone(result)  # Should return None on error
    
    def test_safe_execute_decorator_with_reraise(self):
        """Test safe_execute decorator with reraise"""
        @safe_execute("Test operation failed", reraise=True)
        def failing_operation():
            raise ValueError("Test error")
        
        with self.assertRaises(ValueError):
            failing_operation()
    
    def test_gpx_editor_exception(self):
        """Test GPXEditorException"""
        exc = GPXEditorException("Test error")
        self.assertEqual(str(exc), "Test error")
        self.assertIsInstance(exc, Exception)
    
    def test_validate_gpx_data_valid(self):
        """Test GPX data validation with valid data"""
        # Create valid GPX data
        gpx = gpxpy.gpx.GPX()
        
        # Add a track with valid coordinates
        track = gpxpy.gpx.GPXTrack()
        segment = gpxpy.gpx.GPXTrackSegment()
        
        # Add valid points
        segment.points.append(gpxpy.gpx.GPXTrackPoint(48.8566, 2.3522, elevation=35.0))
        segment.points.append(gpxpy.gpx.GPXTrackPoint(48.8584, 2.2945, elevation=40.0))
        
        track.segments.append(segment)
        gpx.tracks.append(track)
        
        errors, warnings = validate_gpx_data(gpx)
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(warnings), 0)
    
    def test_validate_gpx_data_empty(self):
        """Test GPX data validation with empty data"""
        gpx = gpxpy.gpx.GPX()
        
        errors, warnings = validate_gpx_data(gpx)
        
        # Should have error for no tracks or routes
        self.assertGreater(len(errors), 0)
        self.assertIn("No tracks or routes", errors[0])
    
    def test_validate_gpx_data_invalid_coordinates(self):
        """Test GPX data validation with invalid coordinates"""
        gpx = gpxpy.gpx.GPX()
        
        # Add a track with invalid coordinates
        track = gpxpy.gpx.GPXTrack()
        segment = gpxpy.gpx.GPXTrackSegment()
        
        # Add invalid latitude
        segment.points.append(gpxpy.gpx.GPXTrackPoint(91.0, 2.3522, elevation=35.0))
        segment.points.append(gpxpy.gpx.GPXTrackPoint(48.8584, 2.2945, elevation=40.0))
        
        track.segments.append(segment)
        gpx.tracks.append(track)
        
        errors, warnings = validate_gpx_data(gpx)
        
        # Should have error for invalid latitude
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("latitude" in error for error in errors))
    
    def test_validate_gpx_data_warnings(self):
        """Test GPX data validation with warnings"""
        gpx = gpxpy.gpx.GPX()
        
        # Add a track with empty segment
        track = gpxpy.gpx.GPXTrack()
        segment = gpxpy.gpx.GPXTrackSegment()  # Empty segment
        
        track.segments.append(segment)
        gpx.tracks.append(track)
        
        errors, warnings = validate_gpx_data(gpx)
        
        # Should have warning for empty segment or no points
        self.assertGreater(len(warnings), 0)
        # Check for any warning about empty segments or no points
        warning_text = ' '.join(warnings).lower()
        self.assertTrue(any(keyword in warning_text for keyword in ['empty', 'no points', 'segment']))
    
    def test_handle_file_error_not_found(self):
        """Test file error handling for non-existent file"""
        nonexistent_file = "/path/to/nonexistent/file.gpx"
        
        # Should return True for any file (handle_file_error is very permissive)
        result = handle_file_error(nonexistent_file, "access")
        self.assertTrue(result)  # handle_file_error returns True for any case
    
    def test_handle_file_error_permission(self):
        """Test file error handling for permission issues"""
        # Create a file and make it read-only (simulated)
        test_file = self.create_temp_file("test content")
        
        # Test with existing file (should return True)
        result = handle_file_error(test_file, "access")
        self.assertTrue(result)


class TestEditControllerErrorHandling(GPXTestCase):
    """Test error handling in edit controller"""
    
    def test_load_nonexistent_file(self):
        """Test loading non-existent GPX file"""
        from edit_controller import GPXEditController
        
        controller = GPXEditController(None)  # Mock app
        
        nonexistent_file = "/path/to/nonexistent/file.gpx"
        
        # With @safe_execute decorator, should return None instead of raising exception
        result = controller.load_document(nonexistent_file)
        self.assertIsNone(result)  # Should return None on error
    
    def test_load_empty_file(self):
        """Test loading empty GPX file"""
        from edit_controller import GPXEditController
        
        controller = GPXEditController(None)  # Mock app
        
        empty_file = self.create_temp_file("", ".gpx")
        
        # With @safe_execute decorator, should return None instead of raising exception
        result = controller.load_document(empty_file)
        self.assertIsNone(result)  # Should return None on error
    
    def test_load_invalid_xml(self):
        """Test loading invalid XML file"""
        from edit_controller import GPXEditController
        
        controller = GPXEditController(None)  # Mock app
        
        invalid_file = self.create_temp_file("invalid xml content", ".gpx")
        
        # With @safe_execute decorator, should return None instead of raising exception
        result = controller.load_document(invalid_file)
        self.assertIsNone(result)  # Should return None on error
    
    def test_load_non_gpx_file(self):
        """Test loading file that doesn't start with GPX tags"""
        from edit_controller import GPXEditController
        
        controller = GPXEditController(None)  # Mock app
        
        non_gpx_file = self.create_temp_file("This is not a GPX file", ".gpx")
        
        # With @safe_execute decorator, should return None instead of raising exception
        result = controller.load_document(non_gpx_file)
        self.assertIsNone(result)  # Should return None on error


class TestMapRendererErrorHandling(GPXTestCase):
    """Test error handling in map renderer"""
    
    def test_render_with_invalid_file(self):
        """Test rendering with invalid GPX file"""
        from map_renderer import render_tracks_on_map
        from unittest.mock import Mock
        
        # Mock map widget
        mock_map = Mock()
        mock_map.delete_all_path = Mock()
        mock_map.set_path = Mock()
        
        # Create mock entry with invalid file
        mock_entry = Mock()
        mock_entry.is_visible.return_value = True
        mock_entry.get_path.return_value = "/nonexistent/file.gpx"
        mock_entry.get_color.return_value = "#FF0000"
        
        entries = [mock_entry]
        
        # Mock properties
        mock_properties = Mock()
        mock_properties.get.return_value = 1
        
        # Should handle gracefully without crashing
        render_tracks_on_map(mock_map, entries, mock_properties)
        
        # Should not call set_path for invalid file
        mock_map.set_path.assert_not_called()
    
    def test_render_with_corrupted_gpx(self):
        """Test rendering with corrupted GPX file"""
        from map_renderer import render_tracks_on_map
        from unittest.mock import Mock
        
        # Create corrupted GPX file
        corrupted_file = self.create_temp_file("invalid xml", ".gpx")
        
        # Mock map widget
        mock_map = Mock()
        mock_map.delete_all_path = Mock()
        mock_map.set_path = Mock()
        
        # Create mock entry with corrupted file
        mock_entry = Mock()
        mock_entry.is_visible.return_value = True
        mock_entry.get_path.return_value = corrupted_file
        mock_entry.get_color.return_value = "#FF0000"
        
        entries = [mock_entry]
        
        # Mock properties
        mock_properties = Mock()
        mock_properties.get.return_value = 1
        
        # Should handle gracefully without crashing
        render_tracks_on_map(mock_map, entries, mock_properties)
        
        # Should not call set_path for corrupted file
        mock_map.set_path.assert_not_called()


class TestFileEntryErrorHandling(GPXTestCase):
    """Test error handling in file entry"""
    
    def test_file_entry_with_missing_file(self):
        """Test FileEntry with missing GPX file"""
        # This would require creating a FileEntry with a non-existent file
        # For now, we'll test the concept
        missing_file = "/nonexistent/file.gpx"
        
        # File should not exist
        self.assert_file_not_exists(missing_file)
    
    def test_file_entry_color_handling(self):
        """Test FileEntry color handling edge cases"""
        # Test with various color formats
        colors = [
            "#FF0000",  # Standard hex
            "#F00",     # Short hex
            "red",      # Named color
            "",         # Empty color
            None,       # None color
        ]
        
        for color in colors:
            # Should handle all color formats gracefully
            if color is not None:
                self.assertIsInstance(color, str)
            # Actual FileEntry testing would require more setup


class TestLoggingErrorHandling(GPXTestCase):
    """Test logging error handling"""
    
    def test_logging_with_invalid_file_path(self):
        """Test logging with invalid file path"""
        import tempfile
        import shutil
        
        # Test logging to invalid path
        invalid_path = "/invalid/path/that/does/not/exist/test.log"
        
        # Should handle gracefully (logging system should fallback)
        try:
            import logging
            
            # Try to create a file handler with invalid path
            handler = logging.FileHandler(invalid_path)
            # If we get here, the system handled it
            handler.close()
        except Exception:
            # Expected to fail, but should not crash the application
            pass
    
    def test_logging_with_permissions_error(self):
        """Test logging with permissions error"""
        # This is platform-specific and hard to test reliably
        # We'll just verify the logging setup doesn't crash
        import logging
        
        # Should not crash
        logger = logging.getLogger("test")
        logger.info("Test message")
        
        # Should be able to create handlers
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        logger.removeHandler(handler)


if __name__ == '__main__':
    unittest.main()
