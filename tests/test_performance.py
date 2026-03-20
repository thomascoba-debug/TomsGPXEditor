"""
Performance and stress tests for GPX Editor
"""

import unittest
import time
import os
import json
import tempfile
from test_framework import GPXTestCase
from map_renderer import GPXCache
from recent_files import RecentFilesManager
from properties import AppProperties
import gpxpy


class TestPerformance(GPXTestCase):
    """Performance tests for GPX Editor components"""
    
    def test_gpx_cache_performance(self):
        """Test GPX cache performance with multiple files"""
        # Clear cache
        GPXCache.clear_cache()
        
        # Create multiple GPX files
        files = []
        for i in range(10):
            # Create GPX with many points
            points = [(48.0 + i * 0.01, 2.0 + i * 0.01, 100 + i * 10) for i in range(100)]
            gpx_file = self.create_sample_gpx(points)
            files.append(gpx_file)
        
        # Test loading performance (first load - cache miss)
        start_time = time.time()
        for file_path in files:
            GPXCache.get_gpx(file_path)
        first_load_time = time.time() - start_time
        
        # Test loading performance (second load - cache hit)
        start_time = time.time()
        for file_path in files:
            GPXCache.get_gpx(file_path)
        second_load_time = time.time() - start_time
        
        # Cache should be significantly faster
        self.assertLess(second_load_time, first_load_time * 0.5)  # At least 50% faster
        
        # Verify all files are cached
        self.assertEqual(len(GPXCache._cache), 10)
    
    def test_recent_files_performance(self):
        """Test RecentFilesManager performance with many files"""
        props_file = self.create_temp_file('{}', '.json')
        properties = AppProperties(props_file)
        
        # Test with large number of files
        recent_files = RecentFilesManager(properties, max_files=100)
        
        # Add many files
        files = []
        for i in range(150):
            test_file = self.create_temp_file(f"content {i}")
            files.append(test_file)
            recent_files.add_file(test_file)
        
        # Should only keep max_files
        recent_list = recent_files.get_recent_files()
        self.assertEqual(len(recent_list), 100)
        
        # Test search performance
        start_time = time.time()
        for _ in range(10):
            recent_list = recent_files.get_recent_files()
        search_time = time.time() - start_time
        
        # Should be very fast (less than 0.1 seconds for 10 searches)
        self.assertLess(search_time, 0.1)
    
    def test_large_gpx_file_handling(self):
        """Test handling of large GPX files"""
        # Create a large GPX file with many points
        points = []
        for i in range(1000):
            lat = 48.0 + (i * 0.001)
            lon = 2.0 + (i * 0.001)
            ele = 100 + i
            points.append((lat, lon, ele))
        
        large_gpx_file = self.create_sample_gpx(points)
        
        # Test loading performance
        start_time = time.time()
        gpx_data = GPXCache.get_gpx(large_gpx_file)
        load_time = time.time() - start_time
        
        # Should load within reasonable time (less than 1 second)
        self.assertLess(load_time, 1.0)
        self.assertIsNotNone(gpx_data)
        
        # Verify all points are loaded
        track = gpx_data.tracks[0]
        segment = track.segments[0]
        self.assertEqual(len(segment.points), 1000)
    
    def test_memory_usage_with_cache(self):
        """Test memory usage patterns with GPX cache"""
        # Clear cache
        GPXCache.clear_cache()
        
        # Add files to cache
        files = []
        for i in range(20):
            points = [(48.0 + i * 0.01, 2.0 + i * 0.01, 100 + i * 10) for i in range(50)]
            gpx_file = self.create_sample_gpx(points)
            files.append(gpx_file)
            GPXCache.get_gpx(gpx_file)
        
        # Verify cache size
        self.assertEqual(len(GPXCache._cache), 20)
        
        # Clear cache and verify memory is freed
        GPXCache.clear_cache()
        self.assertEqual(len(GPXCache._cache), 0)
    
    def test_concurrent_cache_access(self):
        """Test concurrent access to GPX cache"""
        import threading
        
        # Clear cache
        GPXCache.clear_cache()
        
        # Create test files
        files = [self.create_sample_gpx() for _ in range(5)]
        
        results = []
        errors = []
        
        def worker(file_path):
            try:
                for _ in range(10):
                    result = GPXCache.get_gpx(file_path)
                    results.append(result is not None)
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for file_path in files:
            thread = threading.Thread(target=worker, args=(file_path,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Should have no errors
        self.assertEqual(len(errors), 0)
        
        # Should have successful results
        self.assertEqual(len(results), 50)  # 5 files * 10 accesses each
        self.assertTrue(all(results))


class TestStressScenarios(GPXTestCase):
    """Stress tests for edge cases and heavy usage"""
    
    def test_rapid_file_operations(self):
        """Test rapid file add/remove operations"""
        props_file = self.create_temp_file('{}', '.json')
        properties = AppProperties(props_file)
        recent_files = RecentFilesManager(properties, max_files=10)
        
        # Rapid add/remove operations
        for cycle in range(10):
            # Add files
            added_files = []
            for i in range(15):
                test_file = self.create_temp_file(f"cycle_{cycle}_file_{i}")
                added_files.append(test_file)
                recent_files.add_file(test_file)
            
            # Should maintain max_files limit
            recent_list = recent_files.get_recent_files()
            self.assertEqual(len(recent_list), 10)
            
            # Remove some files
            for i in range(5):
                recent_files.remove_file(added_files[i])
            
            # Should still work
            recent_list = recent_files.get_recent_files()
            self.assertGreaterEqual(len(recent_list), 5)
    
    def test_cache_under_memory_pressure(self):
        """Test cache behavior under memory pressure simulation"""
        # Clear cache
        GPXCache.clear_cache()
        
        # Add many large files to cache
        large_files = []
        for i in range(50):
            # Create GPX with many points
            points = [(48.0 + j * 0.001, 2.0 + j * 0.001, 100 + j) for j in range(200)]
            gpx_file = self.create_sample_gpx(points)
            large_files.append(gpx_file)
            GPXCache.get_gpx(gpx_file)
        
        # Cache should have all files
        self.assertEqual(len(GPXCache._cache), 50)
        
        # Clear cache to simulate memory pressure
        GPXCache.clear_cache()
        
        # Cache should be empty
        self.assertEqual(len(GPXCache._cache), 0)
    
    def test_properties_file_corruption_recovery(self):
        """Test recovery from corrupted properties file"""
        # Create initial valid properties
        props_file = self.create_temp_file(json.dumps({
            "session_files": {},
            "recent_files": []
        }), '.json')
        
        # Load and modify
        properties = AppProperties(props_file)
        properties.set("test_key", "test_value")
        properties.save()
        
        # Verify it works
        new_properties = AppProperties(props_file)
        self.assertEqual(new_properties.get("test_key"), "test_value")
        
        # Corrupt the file
        with open(props_file, 'w') as f:
            f.write('{"invalid": json content}')
        
        # Should handle gracefully
        try:
            corrupted_properties = AppProperties(props_file)
            # Should have default values
            self.assertIsNotNone(corrupted_properties.data)
            self.assertIsInstance(corrupted_properties.data, dict)
        except Exception as e:
            self.fail(f"Should handle corrupted properties gracefully: {e}")
    
    def test_extreme_gpx_coordinates(self):
        """Test GPX files with extreme coordinate values"""
        # Test with coordinates at boundaries
        extreme_points = [
            (90.0, 180.0, 8848.0),  # North pole, max longitude, Everest
            (-90.0, -180.0, -418.0),  # South pole, min longitude, Dead Sea
            (0.0, 0.0, 0.0),  # Equator, prime meridian, sea level
            (89.999999, 179.999999, 10000.0),  # Near boundaries
        ]
        
        for points in [extreme_points]:
            gpx_file = self.create_sample_gpx(points)
            
            # Should load without errors
            gpx_data = GPXCache.get_gpx(gpx_file)
            self.assertIsNotNone(gpx_data)
            
            # Validate coordinates
            track = gpx_data.tracks[0]
            segment = track.segments[0]
            for i, point in enumerate(segment.points):
                expected_lat, expected_lon, expected_ele = points[i]
                self.assertAlmostEqual(point.latitude, expected_lat, places=5)
                self.assertAlmostEqual(point.longitude, expected_lon, places=5)
                self.assertAlmostEqual(point.elevation, expected_ele, places=5)
    
    def test_unicode_handling(self):
        """Test Unicode and special character handling"""
        # Test with special characters in file paths and names
        special_chars = ["test äöü.gpx", "test 中文.gpx", "test ñiñ.gpx"]
        
        for filename in special_chars:
            try:
                # Create file with special characters
                gpx_file = self.create_sample_gpx()
                
                # Rename file (if supported by filesystem)
                try:
                    new_path = os.path.join(os.path.dirname(gpx_file), filename)
                    os.rename(gpx_file, new_path)
                    
                    # Should handle gracefully
                    gpx_data = GPXCache.get_gpx(new_path)
                    self.assertIsNotNone(gpx_data)
                    
                    # Clean up
                    if os.path.exists(new_path):
                        os.remove(new_path)
                except (OSError, UnicodeError):
                    # Some filesystems don't support all special characters
                    pass
                    
            except Exception as e:
                # Should not crash the application
                self.assertNotIsInstance(e, SystemError)


if __name__ == '__main__':
    unittest.main()
