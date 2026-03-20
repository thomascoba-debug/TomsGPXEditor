"""
Example test showing how to use the test framework
"""

import unittest
from test_framework import GPXTestCase


class TestExample(GPXTestCase):
    """Example test class demonstrating framework usage"""
    
    def test_temp_file_creation(self):
        """Test creating temporary files"""
        # Create a temporary GPX file
        gpx_file = self.create_sample_gpx()
        
        # Verify file exists
        self.assert_file_exists(gpx_file)
        
        # Verify content
        with open(gpx_file, 'r') as f:
            content = f.read()
            self.assertIn('<gpx', content)
            self.assertIn('Test Track', content)
    
    def test_custom_temp_file(self):
        """Test creating custom temporary files"""
        # Create a temporary file with custom content
        custom_file = self.create_temp_file("custom content", ".txt")
        
        self.assert_file_exists(custom_file)
        
        with open(custom_file, 'r') as f:
            self.assertEqual(f.read(), "custom content")
    
    def test_sample_gpx_with_custom_points(self):
        """Test creating sample GPX with custom points"""
        points = [
            (50.0, 10.0, 100.0),
            (51.0, 11.0, 200.0),
            (52.0, 12.0, 300.0),
        ]
        
        gpx_file = self.create_sample_gpx(points)
        
        self.assert_file_exists(gpx_file)
        
        # Verify points are in the file
        with open(gpx_file, 'r') as f:
            content = f.read()
            self.assertIn('50.0', content)
            self.assertIn('10.0', content)
            self.assertIn('100.0', content)


if __name__ == '__main__':
    unittest.main()
