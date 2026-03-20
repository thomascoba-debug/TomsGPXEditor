"""
Tests for file search functionality
"""

import unittest
import os
import tkinter as tk
from test_framework import GPXTestCase
from file_search import FileSearchEngine, FileSearchFrame


class MockFileEntry:
    """Mock file entry for testing"""
    
    def __init__(self, path, visible=True, editable=False, file_ref=1):
        self.path = path
        self._visible = visible
        # Create a mock BooleanVar without requiring a root window
        self.editable_var = MockBooleanVar(value=editable)
        self.file_ref = file_ref
    
    def is_visible(self):
        return self._visible


class MockBooleanVar:
    """Mock BooleanVar that doesn't require Tkinter root window"""
    
    def __init__(self, value=False):
        self._value = value
    
    def get(self):
        return self._value
    
    def set(self, value):
        self._value = value


class TestFileSearchEngine(GPXTestCase):
    """Test cases for FileSearchEngine"""
    
    def setUp(self):
        super().setUp()
        
        # Create mock file entries
        self.entries = [
            MockFileEntry("/path/to/track1.gpx", visible=True, editable=False, file_ref=1),
            MockFileEntry("/path/to/track2.gpx", visible=False, editable=True, file_ref=2),
            MockFileEntry("/another/path/route.gpx", visible=True, editable=False, file_ref=3),
            MockFileEntry("/path/to/hidden.gpx", visible=False, editable=False, file_ref=4),
        ]
    
    def test_search_all_files(self):
        """Test searching all files with no filter"""
        results = FileSearchEngine.search_files(self.entries, "", "All Files")
        
        self.assertEqual(len(results), 4)
    
    def test_filter_visible_only(self):
        """Test filtering visible files only"""
        results = FileSearchEngine.search_files(self.entries, "", "Visible Only")
        
        self.assertEqual(len(results), 2)
        self.assertTrue(all(entry.is_visible() for entry in results))
    
    def test_filter_hidden_only(self):
        """Test filtering hidden files only"""
        results = FileSearchEngine.search_files(self.entries, "", "Hidden Only")
        
        self.assertEqual(len(results), 2)
        self.assertTrue(all(not entry.is_visible() for entry in results))
    
    def test_filter_editable_only(self):
        """Test filtering editable files only"""
        results = FileSearchEngine.search_files(self.entries, "", "Editable Only")
        
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].editable_var.get())
    
    def test_search_by_filename(self):
        """Test searching by filename"""
        results = FileSearchEngine.search_files(self.entries, "track", "All Files")
        
        self.assertEqual(len(results), 2)
        self.assertTrue(all("track" in os.path.basename(entry.path) for entry in results))
    
    def test_search_by_path(self):
        """Test searching by path"""
        results = FileSearchEngine.search_files(self.entries, "another", "All Files")
        
        self.assertEqual(len(results), 1)
        self.assertIn("another", results[0].path)
    
    def test_search_by_reference(self):
        """Test searching by reference number"""
        results = FileSearchEngine.search_files(self.entries, "3", "All Files")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].file_ref, 3)
    
    def test_search_case_insensitive(self):
        """Test case insensitive search"""
        results_lower = FileSearchEngine.search_files(self.entries, "track", "All Files")
        results_upper = FileSearchEngine.search_files(self.entries, "TRACK", "All Files")
        
        self.assertEqual(len(results_lower), len(results_upper))
    
    def test_search_with_filter(self):
        """Test searching with filter applied"""
        results = FileSearchEngine.search_files(self.entries, "path", "Visible Only")
        
        # Should find visible files containing "path" in path
        # Both track1.gpx and route.gpx are visible and contain "path"
        # So we expect 2 results, not 1
        self.assertEqual(len(results), 2)
        self.assertTrue(all(entry.is_visible() for entry in results))
        self.assertTrue(all("path" in entry.path for entry in results))
    
    def test_search_no_results(self):
        """Test search with no results"""
        results = FileSearchEngine.search_files(self.entries, "nonexistent", "All Files")
        
        self.assertEqual(len(results), 0)
    
    def test_highlight_search_term(self):
        """Test search term highlighting"""
        text = "This is a test string"
        highlighted = FileSearchEngine.highlight_search_term(text, "test")
        
        self.assertIn("*test*", highlighted)
    
    def test_highlight_no_match(self):
        """Test highlighting with no match"""
        text = "This is a test string"
        highlighted = FileSearchEngine.highlight_search_term(text, "nonexistent")
        
        self.assertEqual(highlighted, text)
    
    def test_highlight_empty_term(self):
        """Test highlighting with empty term"""
        text = "This is a test string"
        highlighted = FileSearchEngine.highlight_search_term(text, "")
        
        self.assertEqual(highlighted, text)


class TestFileSearchFrame(GPXTestCase):
    """Test cases for FileSearchFrame"""
    
    def setUp(self):
        super().setUp()
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during tests
        
        self.search_callback_called = False
        self.search_args = None
    
    def search_callback(self, search_term, filter_type):
        """Mock search callback"""
        self.search_callback_called = True
        self.search_args = (search_term, filter_type)
        return ["result1", "result2"]
    
    def tearDown(self):
        self.root.destroy()
        super().tearDown()
    
    def test_frame_creation(self):
        """Test frame creation"""
        frame = FileSearchFrame(self.root, self.search_callback)
        
        self.assertIsNotNone(frame.search_var)
        self.assertIsNotNone(frame.filter_var)
        self.assertIsNotNone(frame.search_entry)
        self.assertIsNotNone(frame.filter_combo)
    
    def test_get_search_term(self):
        """Test getting search term"""
        frame = FileSearchFrame(self.root, self.search_callback)
        
        frame.search_var.set("test term")
        self.assertEqual(frame.get_search_term(), "test term")
    
    def test_get_filter_type(self):
        """Test getting filter type"""
        frame = FileSearchFrame(self.root, self.search_callback)
        
        frame.filter_var.set("Visible Only")
        self.assertEqual(frame.get_filter_type(), "Visible Only")
    
    def test_clear_search(self):
        """Test clearing search"""
        frame = FileSearchFrame(self.root, self.search_callback)
        
        frame.search_var.set("test term")
        frame.filter_var.set("Visible Only")
        
        frame.clear_search()
        
        self.assertEqual(frame.get_search_term(), "")
        self.assertEqual(frame.get_filter_type(), "All Files")


if __name__ == '__main__':
    unittest.main()
