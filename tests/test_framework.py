"""
Test framework utilities for GPX Editor
"""

import unittest
import tempfile
import os
import sys
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Disable logging for tests
logging.disable(logging.CRITICAL)


class GPXTestCase(unittest.TestCase):
    """Base test case for GPX Editor tests"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_files = []
        
    def tearDown(self):
        """Clean up test environment"""
        # Clean up temporary files
        for file_path in self.temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass
        
        # Clean up temp directory
        try:
            os.rmdir(self.temp_dir)
        except Exception:
            pass
    
    def create_temp_file(self, content, suffix=".gpx"):
        """Create a temporary file with given content"""
        file_path = os.path.join(self.temp_dir, f"test_{len(self.temp_files)}{suffix}")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.temp_files.append(file_path)
        return file_path
    
    def create_sample_gpx(self, points=None):
        """Create a sample GPX file for testing"""
        if points is None:
            points = [
                (48.8566, 2.3522, 35.0),  # Paris
                (48.8584, 2.2945, 40.0),  # Eiffel Tower
                (48.8606, 2.3376, 45.0),  # Near Eiffel Tower
            ]
        
        gpx_content = '''<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="GPX Editor Test">
  <trk>
    <name>Test Track</name>
    <trkseg>
'''
        
        for i, (lat, lon, ele) in enumerate(points):
            gpx_content += f'''      <trkpt lat="{lat}" lon="{lon}">
        <ele>{ele}</ele>
        <name>Point {i+1}</name>
      </trkpt>
'''
        
        gpx_content += '''    </trkseg>
  </trk>
</gpx>'''
        
        return self.create_temp_file(gpx_content)
    
    def assert_file_exists(self, file_path):
        """Assert that a file exists"""
        self.assertTrue(os.path.exists(file_path), f"File {file_path} should exist")
    
    def assert_file_not_exists(self, file_path):
        """Assert that a file does not exist"""
        self.assertFalse(os.path.exists(file_path), f"File {file_path} should not exist")


def run_tests():
    """Run all tests in the tests directory"""
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
