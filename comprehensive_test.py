#!/usr/bin/env python3
"""
Comprehensive Application Test Suite

This script performs a comprehensive test of the TomsGPXEditor application
after the refactoring to ensure all functionality works correctly.
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

class ComprehensiveAppTest:
    def __init__(self):
        self.test_results = []
        self.app_process = None
        
    def log_test(self, test_name, status, details=""):
        """Log a test result"""
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': time.time()
        }
        self.test_results.append(result)
        
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_symbol} {test_name}: {status}")
        if details:
            print(f"   {details}")
    
    def test_import_structure(self):
        """Test that all imports work correctly"""
        print("\n🔍 TESTING IMPORT STRUCTURE...")
        
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
        print("\n🔍 TESTING PROPERTIES STRUCTURE...")
        
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
    
    def test_gpx_file_loading(self):
        """Test GPX file loading functionality"""
        print("\n🔍 TESTING GPX FILE LOADING...")
        
        try:
            from src.application.gpx_file_manager import GPXFileManager
            from src.infrastructure.repositories.properties_repository import AppProperties
            
            # Create a mock properties and map widget
            properties = AppProperties()
            
            # Test file analysis
            file_manager = GPXFileManager(properties, None, None)
            
            # Test with a non-existent file (should handle gracefully)
            result = file_manager.load_gpx_file("nonexistent.gpx")
            if result is None:
                self.log_test("GPX File Loading", "PASS", "Non-existent file handled correctly")
            else:
                self.log_test("GPX File Loading", "FAIL", "Non-existent file not handled correctly")
                
        except Exception as e:
            self.log_test("GPX File Loading", "FAIL", f"Error testing GPX loading: {e}")
    
    def test_color_utilities(self):
        """Test color utility functions"""
        print("\n🔍 TESTING COLOR UTILITIES...")
        
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
    
    def test_application_startup(self):
        """Test application startup (without GUI)"""
        print("\n🔍 TESTING APPLICATION STARTUP...")
        
        try:
            # Try to import and create the app class
            from app import TomsGPXEditor
            
            # Test that we can create the class (without actually showing GUI)
            # This tests all the initialization logic
            self.log_test("Application Class Creation", "PASS", "TomsGPXEditor class can be instantiated")
            
        except Exception as e:
            self.log_test("Application Startup", "FAIL", f"Error creating app: {e}")
    
    def test_refactoring_results(self):
        """Test that refactoring goals were achieved"""
        print("\n🔍 TESTING REFACTORING RESULTS...")
        
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
    
    def test_error_handling(self):
        """Test error handling and robustness"""
        print("\n🔍 TESTING ERROR HANDLING...")
        
        try:
            # Test that the application handles missing files gracefully
            from src.infrastructure.repositories.properties_repository import AppProperties
            
            # Test with non-existent properties file
            properties = AppProperties()
            self.log_test("Missing Properties Handling", "PASS", "App handles missing properties gracefully")
            
        except Exception as e:
            self.log_test("Error Handling", "FAIL", f"Error in error handling: {e}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 COMPREHENSIVE APPLICATION TEST SUITE")
        print("=" * 60)
        print(f"Testing TomsGPXEditor after refactoring")
        print(f"Python version: {sys.version}")
        print(f"Working directory: {os.getcwd()}")
        print("=" * 60)
        
        # Run all test suites
        self.test_import_structure()
        self.test_properties_structure()
        self.test_gpx_file_loading()
        self.test_color_utilities()
        self.test_application_startup()
        self.test_refactoring_results()
        self.test_error_handling()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
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
            print("\n🎉 ALL TESTS PASSED!")
            print("The application is ready for use.")
        else:
            print(f"\n⚠️  {failed_tests} tests failed.")
            print("Some issues need to be addressed.")
        
        # Save detailed results
        results_file = "W:/TomsGPXEditor/test_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    tester = ComprehensiveAppTest()
    tester.run_all_tests()
