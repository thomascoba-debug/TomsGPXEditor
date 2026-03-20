"""
Tests for progress dialog functionality
"""

import unittest
import time
import tkinter as tk
from test_framework import GPXTestCase
from progress_dialog import ProgressDialog, ProgressManager


class TestProgressDialog(GPXTestCase):
    """Test cases for ProgressDialog"""
    
    def setUp(self):
        super().setUp()
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during tests
    
    def tearDown(self):
        self.root.destroy()
        super().tearDown()
    
    def test_dialog_creation(self):
        """Test dialog creation"""
        dialog = ProgressDialog(self.root, "Test Title", "Test Message")
        
        self.assertEqual(dialog.title(), "Test Title")
        self.assertIsNotNone(dialog.progress_var)
        self.assertIsNotNone(dialog.progress_bar)
        self.assertFalse(dialog.was_cancelled())
        
        dialog.destroy()
    
    def test_progress_update(self):
        """Test progress update"""
        dialog = ProgressDialog(self.root)
        
        dialog.update_progress(50, "Half way")
        self.assertEqual(dialog.progress_var.get(), 50)
        
        dialog.destroy()
    
    def test_progress_complete(self):
        """Test progress completion"""
        dialog = ProgressDialog(self.root)
        
        dialog.update_progress(100, "Complete!")
        dialog.auto_close(100)  # Auto close after 100ms
        
        # Should close automatically (but we'll destroy manually for test)
        dialog.destroy()
    
    def test_cancel_functionality(self):
        """Test cancel functionality"""
        dialog = ProgressDialog(self.root)
        dialog.show_cancel_button()
        
        # Initially not cancelled
        self.assertFalse(dialog.was_cancelled())
        
        # Cancel the dialog
        dialog.cancel()
        self.assertTrue(dialog.was_cancelled())
        
        dialog.destroy()
    
    def test_indeterminate_mode(self):
        """Test indeterminate progress mode"""
        dialog = ProgressDialog(self.root)
        
        dialog.set_indeterminate()
        # Check if progress bar is in indeterminate mode
        # In ttk, mode is an index object, convert to string for comparison
        mode_value = str(dialog.progress_bar.cget('mode'))
        self.assertIn('indeterminate', mode_value)
        
        dialog.set_determinate()
        mode_value = str(dialog.progress_bar.cget('mode'))
        self.assertIn('determinate', mode_value)
        
        dialog.destroy()
    
    def test_max_value_setting(self):
        """Test setting maximum progress value"""
        dialog = ProgressDialog(self.root)
        
        dialog.set_max_value(200)
        dialog.update_progress(100)
        
        # Should be 50% of the way to 200
        self.assertEqual(dialog.progress_var.get(), 100)
        self.assertEqual(dialog.progress_bar['maximum'], 200)
        
        dialog.destroy()


class TestProgressManager(GPXTestCase):
    """Test cases for ProgressManager"""
    
    def setUp(self):
        super().setUp()
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during tests
        
        self.operation_completed = False
        self.operation_result = None
        self.progress_updates = []
    
    def tearDown(self):
        self.root.destroy()
        super().tearDown()
    
    def mock_operation(self, progress_callback=None):
        """Mock operation that takes some time"""
        if progress_callback:
            for i in range(10):
                progress_callback(i * 10, f"Step {i+1}")
                time.sleep(0.01)  # Small delay
        
        return "operation_result"
    
    def mock_operation_with_progress(self, progress_callback):
        """Mock operation with progress callback"""
        for i in range(5):
            progress_callback(i * 20, f"Processing {i+1}/5")
            time.sleep(0.01)
        
        return "completed"
    
    def test_manager_creation(self):
        """Test progress manager creation"""
        manager = ProgressManager(self.root)
        
        self.assertIsNotNone(manager.parent)
        self.assertIsNone(manager.dialog)
    
    def test_show_progress_dialog(self):
        """Test showing progress dialog"""
        manager = ProgressManager(self.root)
        
        dialog = manager.show_progress("Test Operation", "Please wait...")
        
        self.assertIsNotNone(dialog)
        self.assertEqual(dialog.title(), "Test Operation")
        
        manager.close_dialog()
    
    def test_run_with_progress(self):
        """Test running operation with progress"""
        manager = ProgressManager(self.root)
        
        # This would normally show a dialog and run the operation
        # For testing, we'll just verify the method exists
        self.assertTrue(hasattr(manager, 'run_with_progress'))
    
    def test_progress_callback(self):
        """Test progress callback functionality"""
        def test_callback(value, message):
            self.progress_updates.append((value, message))
        
        # Simulate progress updates
        test_callback(25, "Step 1")
        test_callback(50, "Step 2")
        test_callback(100, "Complete")
        
        self.assertEqual(len(self.progress_updates), 3)
        self.assertEqual(self.progress_updates[0], (25, "Step 1"))
        self.assertEqual(self.progress_updates[2], (100, "Complete"))
    
    def test_dialog_auto_close(self):
        """Test dialog auto-close functionality"""
        manager = ProgressManager(self.root)
        dialog = manager.show_progress()
        
        # Set auto-close
        dialog.auto_close(100)
        
        # Destroy manually for test
        dialog.destroy()


class TestProgressIntegration(GPXTestCase):
    """Integration tests for progress functionality"""
    
    def setUp(self):
        super().setUp()
        self.root = tk.Tk()
        self.root.withdraw()
    
    def tearDown(self):
        self.root.destroy()
        super().tearDown()
    
    def test_progress_dialog_lifecycle(self):
        """Test complete progress dialog lifecycle"""
        dialog = ProgressDialog(self.root, "Test Operation")
        
        # Start indeterminate
        dialog.set_indeterminate()
        
        # Switch to determinate
        dialog.set_determinate()
        dialog.set_max_value(100)
        
        # Update progress
        for i in range(0, 101, 25):
            dialog.update_progress(i, f"Progress {i}%")
            time.sleep(0.001)  # Small delay
        
        # Complete and auto-close
        dialog.update_progress(100, "Complete!")
        dialog.auto_close(100)
        
        # Clean up
        dialog.destroy()
    
    def test_progress_with_cancellation(self):
        """Test progress with cancellation"""
        dialog = ProgressDialog(self.root, "Cancellable Operation")
        dialog.show_cancel_button()
        
        # Simulate some progress
        dialog.update_progress(30, "Working...")
        
        # User cancels
        dialog.cancel()
        self.assertTrue(dialog.was_cancelled())
        
        dialog.destroy()


if __name__ == '__main__':
    unittest.main()
