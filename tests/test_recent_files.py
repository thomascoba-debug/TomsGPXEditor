"""
Tests for recent files functionality
"""

import unittest
import tempfile
import os
import json
from test_framework import GPXTestCase
from recent_files import RecentFilesManager
from properties import AppProperties


class TestRecentFilesManager(GPXTestCase):
    """Test cases for RecentFilesManager"""
    
    def setUp(self):
        super().setUp()
        # Create a temporary properties file
        self.properties_file = self.create_temp_file('{}', '.json')
        self.properties = AppProperties(self.properties_file)
        self.recent_files = RecentFilesManager(self.properties, max_files=5)
    
    def test_add_file(self):
        """Test adding a file to recent files"""
        test_file = self.create_temp_file("test content")
        
        self.recent_files.add_file(test_file)
        recent_list = self.recent_files.get_recent_files()
        
        self.assertEqual(len(recent_list), 1)
        self.assertEqual(recent_list[0], test_file)
    
    def test_add_nonexistent_file(self):
        """Test adding a non-existent file"""
        nonexistent_file = "/path/to/nonexistent/file.gpx"
        
        self.recent_files.add_file(nonexistent_file)
        recent_list = self.recent_files.get_recent_files()
        
        self.assertEqual(len(recent_list), 0)
    
    def test_remove_file(self):
        """Test removing a file from recent files"""
        test_file = self.create_temp_file("test content")
        
        self.recent_files.add_file(test_file)
        self.recent_files.remove_file(test_file)
        recent_list = self.recent_files.get_recent_files()
        
        self.assertEqual(len(recent_list), 0)
    
    def test_max_files_limit(self):
        """Test that recent files list respects max files limit"""
        # Add more files than the limit
        added_files = []
        for i in range(7):
            test_file = self.create_temp_file(f"content {i}")
            added_files.append(test_file)
            self.recent_files.add_file(test_file)
        
        recent_list = self.recent_files.get_recent_files()
        
        # Should only keep the 5 most recent files
        self.assertEqual(len(recent_list), 5)
        
        # The most recent file should be the last one added (index 6)
        most_recent_file = added_files[-1]  # content 6
        self.assertIn(most_recent_file, recent_list)
        
        # The oldest kept file should be the third from last (index 2)
        oldest_kept_file = added_files[-5]  # content 2
        self.assertIn(oldest_kept_file, recent_list)
        
        # Files 0 and 1 should not be in the list
        self.assertNotIn(added_files[0], recent_list)  # content 0
        self.assertNotIn(added_files[1], recent_list)  # content 1
    
    def test_move_to_front_on_duplicate(self):
        """Test that adding existing file moves it to front"""
        test_file1 = self.create_temp_file("content 1")
        test_file2 = self.create_temp_file("content 2")
        
        self.recent_files.add_file(test_file1)
        self.recent_files.add_file(test_file2)
        self.recent_files.add_file(test_file1)  # Add again
        
        recent_list = self.recent_files.get_recent_files()
        
        self.assertEqual(len(recent_list), 2)
        self.assertEqual(recent_list[0], test_file1)  # Should be at front
        self.assertEqual(recent_list[1], test_file2)
    
    def test_clear_recent_files(self):
        """Test clearing all recent files"""
        for i in range(3):
            test_file = self.create_temp_file(f"content {i}")
            self.recent_files.add_file(test_file)
        
        self.recent_files.clear_recent_files()
        recent_list = self.recent_files.get_recent_files()
        
        self.assertEqual(len(recent_list), 0)
    
    def test_filter_nonexistent_files(self):
        """Test that non-existent files are filtered out"""
        test_file1 = self.create_temp_file("content 1")
        test_file2 = self.create_temp_file("content 2")
        
        self.recent_files.add_file(test_file1)
        self.recent_files.add_file(test_file2)
        
        # Delete one file
        os.remove(test_file2)
        
        recent_list = self.recent_files.get_recent_files()
        
        self.assertEqual(len(recent_list), 1)
        self.assertEqual(recent_list[0], test_file1)
    
    def test_get_display_name(self):
        """Test display name generation"""
        test_file = os.path.join("/path/to/test", "myfile.gpx")
        display_name = self.recent_files.get_display_name(test_file)
        
        self.assertEqual(display_name, "test/myfile.gpx")
        
        # Test with just filename
        just_filename = "myfile.gpx"
        display_name = self.recent_files.get_display_name(just_filename)
        
        self.assertEqual(display_name, "myfile.gpx")
    
    def test_persistence(self):
        """Test that recent files are persisted to properties"""
        test_file = self.create_temp_file("test content")
        
        self.recent_files.add_file(test_file)
        
        # Create new manager with same properties
        new_manager = RecentFilesManager(self.properties, max_files=5)
        recent_list = new_manager.get_recent_files()
        
        self.assertEqual(len(recent_list), 1)
        self.assertEqual(recent_list[0], test_file)


if __name__ == '__main__':
    unittest.main()
