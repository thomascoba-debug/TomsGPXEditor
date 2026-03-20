"""
Tests for map renderer functionality
"""

import unittest
import os
import time
from unittest.mock import Mock, patch
from test_framework import GPXTestCase
from map_renderer import GPXCache, render_tracks_on_map


class TestGPXCache(GPXTestCase):
    """Test cases for GPXCache"""
    
    def setUp(self):
        super().setUp()
        # Clear cache before each test
        GPXCache.clear_cache()
    
    def test_cache_miss_and_store(self):
        """Test cache miss and subsequent storage"""
        gpx_file = self.create_sample_gpx()
        
        # First call should load from file
        gpx_data = GPXCache.get_gpx(gpx_file)
        self.assertIsNotNone(gpx_data)
        
        # Verify cache contains the file
        cache_key = os.path.abspath(gpx_file)
        self.assertIn(cache_key, GPXCache._cache)
    
    def test_cache_hit(self):
        """Test cache hit"""
        gpx_file = self.create_sample_gpx()
        
        # Load file (cache miss)
        gpx_data1 = GPXCache.get_gpx(gpx_file)
        
        # Load again (cache hit)
        gpx_data2 = GPXCache.get_gpx(gpx_file)
        
        # Should be the same object (cached)
        self.assertIs(gpx_data1, gpx_data2)
    
    def test_cache_invalidation(self):
        """Test cache invalidation when file changes"""
        gpx_file = self.create_sample_gpx()
        
        # Load file
        gpx_data1 = GPXCache.get_gpx(gpx_file)
        
        # Modify file (simulate change)
        import time
        time.sleep(0.1)  # Ensure different timestamp
        with open(gpx_file, 'w') as f:
            f.write("modified content")
        
        # Should reload from file (cache invalidated)
        gpx_data2 = GPXCache.get_gpx(gpx_file)
        
        # Should be different objects
        self.assertIsNot(gpx_data1, gpx_data2)
    
    def test_cache_clear(self):
        """Test cache clearing"""
        gpx_file = self.create_sample_gpx()
        
        # Load file to populate cache
        GPXCache.get_gpx(gpx_file)
        self.assertEqual(len(GPXCache._cache), 1)
        
        # Clear cache
        GPXCache.clear_cache()
        self.assertEqual(len(GPXCache._cache), 0)
    
    def test_cache_remove_specific(self):
        """Test removing specific file from cache"""
        gpx_file1 = self.create_sample_gpx()
        gpx_file2 = self.create_sample_gpx()
        
        # Load both files
        GPXCache.get_gpx(gpx_file1)
        GPXCache.get_gpx(gpx_file2)
        
        self.assertEqual(len(GPXCache._cache), 2)
        
        # Remove specific file
        GPXCache.remove_from_cache(gpx_file1)
        self.assertEqual(len(GPXCache._cache), 1)
        
        # Verify correct file remains
        cache_key2 = os.path.abspath(gpx_file2)
        self.assertIn(cache_key2, GPXCache._cache)


class TestMapRenderer(GPXTestCase):
    """Test cases for map renderer"""
    
    def setUp(self):
        super().setUp()
        
        # Create mock map widget
        self.mock_map = Mock()
        self.mock_map.delete_all_path = Mock()
        self.mock_map.set_path = Mock()
        
        # Create mock file entries
        self.mock_entry1 = Mock()
        self.mock_entry1.is_visible.return_value = True
        self.mock_entry1.get_path.return_value = self.create_sample_gpx()
        self.mock_entry1.get_color.return_value = "#FF0000"
        
        self.mock_entry2 = Mock()
        self.mock_entry2.is_visible.return_value = False  # Hidden
        self.mock_entry2.get_path.return_value = self.create_sample_gpx()
        self.mock_entry2.get_color.return_value = "#00FF00"
        
        self.entries = [self.mock_entry1, self.mock_entry2]
        
        # Create mock properties
        self.mock_properties = Mock()
        self.mock_properties.get.return_value = 1  # downsample_step
    
    def test_render_tracks_basic(self):
        """Test basic track rendering"""
        render_tracks_on_map(self.mock_map, self.entries, self.mock_properties)
        
        # Should delete existing paths
        self.mock_map.delete_all_path.assert_called_once()
        
        # Should call set_path for visible entry only
        self.assertEqual(self.mock_map.set_path.call_count, 1)
        
        # Verify call arguments
        call_args = self.mock_map.set_path.call_args
        self.assertEqual(len(call_args[0][0]), 3)  # 3 points
        self.assertEqual(call_args[1]['color'], "#FF0000")
        self.assertEqual(call_args[1]['width'], 3)
    
    def test_render_tracks_with_downsampling(self):
        """Test track rendering with downsampling"""
        self.mock_properties.get.return_value = 2  # downsample every 2nd point
        
        render_tracks_on_map(self.mock_map, self.entries, self.mock_properties)
        
        # Should render fewer points due to downsampling
        call_args = self.mock_map.set_path.call_args
        coords = call_args[0][0]
        self.assertEqual(len(coords), 2)  # Every 2nd point (3 -> 2)
    
    def test_render_tracks_hidden_entry(self):
        """Test that hidden entries are not rendered"""
        render_tracks_on_map(self.mock_map, self.entries, self.mock_properties)
        
        # Only visible entry should be rendered
        self.mock_entry1.is_visible.assert_called_once()
        self.mock_entry2.is_visible.assert_called_once()
        
        # Only one set_path call (for visible entry)
        self.assertEqual(self.mock_map.set_path.call_count, 1)
    
    @patch('map_renderer.GPXCache.get_gpx')
    def test_render_tracks_with_cache_error(self, mock_get_gpx):
        """Test rendering when cache returns None (file error)"""
        mock_get_gpx.return_value = None  # Simulate cache error
        
        render_tracks_on_map(self.mock_map, self.entries, self.mock_properties)
        
        # Should not call set_path for any entry
        self.mock_map.set_path.assert_not_called()


if __name__ == '__main__':
    unittest.main()
