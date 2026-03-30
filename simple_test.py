#!/usr/bin/env python3
"""
Simple Application Test Suite

This script performs a comprehensive test of TomsGPXEditor application
after refactoring to ensure all functionality works correctly.
"""

import os
import sys
import time
import json

class SimpleAppTest:
    def __init__(self):
        self.test_results = []
        
    def log_test(self, test_name, status, details=""):
        """Log a test result"""
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': time.time()
        }
        self.test_results.append(result)
        
        status_symbol = "PASS" if status == "PASS" else "FAIL" if status == "FAIL" else "WARN"
        print(f"{status_symbol}: {test_name}")
        if details:
            print(f"   {details}")
    
    def test_import_structure(self):
        """Test that all imports work correctly"""
        print("\nTESTING IMPORT STRUCTURE...")
        
        try:
            # Test main imports
            from app import TomsGPXEditor
            self.log_test("Main App Import", "PASS", "TomsGPXEditor imported successfully")
            
            # Test core components
            from src.application.gpx_file_manager import GPXFileManager
            self.log_test("GPX File Manager Import", "PASS", "GPXFileManager imported successfully")
            
            from src.ui.utils.color_utils import pick_color, update_color_button, validate_hex_color
            self.log_test("Color Utils Import", "PASS", "All color utilities imported successfully")
            
            from src.constants.property_keys import APP_RECENT_FILES, DIALOGS_SETTINGS_LOGGING_LEVEL
            self.log_test("Property Keys Import", "PASS", "Property keys imported successfully")
            
        except ImportError as e:
            self.log_test("Import Structure", "FAIL", f"Import error: {e}")
        except Exception as e:
            self.log_test("Import Structure", "FAIL", f"Unexpected error: {e}")
    
    def test_properties_structure(self):
        """Test properties.json structure"""
        print("\nTESTING PROPERTIES STRUCTURE...")
        
        try:
            properties_file = "W:/TomsGPXEditor/properties.json"
            
            if not os.path.exists(properties_file):
                self.log_test("Properties File", "FAIL", "properties.json not found")
                return
            
            with open(properties_file, 'r', encoding='utf-8') as f:
                properties = json.load(f)
            
            # Check structure
            checks = [
                ("Root logging section", 'logging' not in properties),
                ("dialogs.settings.logging exists", 'dialogs' in properties and 'settings' in properties.get('dialogs', {}) and 'logging' in properties['dialogs']['settings']),
                ("files.session exists", 'files' in properties and 'session' in properties['files']),
                ("app.recent_files exists", 'app' in properties and 'recent_files' in properties['app'])
            ]
            
            for check_name, condition in checks:
                status = "PASS" if condition else "FAIL"
                self.log_test(f"Properties: {check_name}", status)
            
        except Exception as e:
            self.log_test("Properties Structure", "FAIL", f"Error reading properties: {e}")
    
    def test_color_utilities(self):
        """Test color utility functions"""
        print("\nTESTING COLOR UTILITIES...")
        
        try:
            from src.ui.utils.color_utils import pick_color, update_color_button, validate_hex_color
            
            # Test color validation
            valid_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFFFF"]
            invalid_colors = ["FF0000", "#FF00", "#GGGGGG", "", None]
            
            for color in valid_colors:
                if validate_hex_color(color):
                    self.log_test(f"Color Validation: {color}", "PASS")
                else:
                    self.log_test(f"Color Validation: {color}", "FAIL", "Valid color rejected")
            
            for color in invalid_colors:
                if not validate_hex_color(color):
                    self.log_test(f"Color Validation: {color}", "PASS", "Invalid color correctly rejected")
                else:
                    self.log_test(f"Color Validation: {color}", "FAIL", "Invalid color accepted")
                    
        except Exception as e:
            self.log_test("Color Utilities", "FAIL", f"Error testing color utilities: {e}")
    
    def test_refactoring_results(self):
        """Test that refactoring goals were achieved"""
        print("\nTESTING REFACTORING RESULTS...")
        
        try:
            # Check that PaginationManager exists
            from src.ui.widgets.pagination_manager import PaginationManager
            self.log_test("PaginationManager Created", "PASS", "PaginationManager class exists")
            
            # Check that PropertyKeys was properly refactored
            try:
                from src.constants.property_keys import PropertyKeys
                self.log_test("PropertyKeys Class", "FAIL", "PropertyKeys class still exists")
            except ImportError:
                self.log_test("PropertyKeys Class", "PASS", "PropertyKeys class properly removed")
            
            # Check that constants are available
            from src.constants.property_keys import APP_RECENT_FILES, DIALOGS_SETTINGS_LOGGING_LEVEL
            self.log_test("Constants Available", "PASS", "Required constants are available")
            
        except Exception as e:
            self.log_test("Refactoring Results", "FAIL", f"Error testing refactoring: {e}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("COMPREHENSIVE APPLICATION TEST SUITE")
        print("=" * 60)
        print(f"Testing TomsGPXEditor after refactoring")
        print(f"Python version: {sys.version}")
        print(f"Working directory: {os.getcwd()}")
        print("=" * 60)
        
        # Run all test suites
        self.test_import_structure()
        self.test_properties_structure()
        self.test_color_utilities()
        self.test_refactoring_results()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        warning_tests = len([r for r in self.test_results if r['status'] == 'WARNING'])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Warnings: {warning_tests}")
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests == 0:
            print("\nALL TESTS PASSED!")
            print("The application is ready for use.")
        else:
            print(f"\n{failed_tests} tests failed.")
            print("Some issues need to be addressed.")
        
        # Save detailed results
        results_file = "W:/TomsGPXEditor/test_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\nDetailed results saved to: {results_file}")

if __name__ == "__main__":
    tester = SimpleAppTest()
    tester.run_all_tests()
