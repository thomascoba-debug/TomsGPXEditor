"""
Progress dialog for long-running operations
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import logging

logger = logging.getLogger(__name__)


class ProgressDialog(tk.Toplevel):
    """Progress dialog for long-running operations"""
    
    def __init__(self, parent, title="Processing", message="Please wait..."):
        super().__init__(parent)
        
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self._center_on_parent(parent)
        
        # Create UI
        self._create_ui(message)
        
        # Progress tracking
        self.current_value = 0
        self.max_value = 100
        self.is_cancelled = False
        
        # Auto-close timer
        self.auto_close_after = None
        self.start_time = time.time()
    
    def _center_on_parent(self, parent):
        """Center dialog on parent window"""
        parent.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        dialog_width = 400
        dialog_height = 150
        
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    def _create_ui(self, message):
        """Create the dialog UI"""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Message label
        self.message_label = ttk.Label(main_frame, text=message, wraplength=350)
        self.message_label.pack(pady=(0, 15))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame, 
            variable=self.progress_var,
            maximum=100,
            length=350
        )
        self.progress_bar.pack(pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Starting...")
        self.status_label.pack(pady=(0, 10))
        
        # Cancel button (optional)
        self.cancel_button = ttk.Button(
            main_frame, 
            text="Cancel", 
            command=self.cancel
        )
        self.cancel_button.pack()
        
        # Initially hide cancel button
        self.cancel_button.pack_forget()
    
    def update_progress(self, value, message=None):
        """Update progress value and optional message"""
        self.current_value = value
        self.progress_var.set(value)
        
        if message:
            self.status_label.config(text=message)
        
        # Update UI
        self.update_idletasks()
        
        # Check for auto-close
        if value >= 100 and self.auto_close_after:
            self.after(self.auto_close_after, self.destroy)
    
    def set_indeterminate(self):
        """Set progress bar to indeterminate mode"""
        self.progress_bar.config(mode='indeterminate')
        self.progress_bar.start(10)
    
    def set_determinate(self):
        """Set progress bar to determinate mode"""
        self.progress_bar.stop()
        self.progress_bar.config(mode='determinate')
    
    def set_max_value(self, max_value):
        """Set maximum progress value"""
        self.max_value = max_value
        self.progress_bar.config(maximum=max_value)
    
    def show_cancel_button(self):
        """Show the cancel button"""
        self.cancel_button.pack()
    
    def cancel(self):
        """Cancel the operation"""
        self.is_cancelled = True
        self.status_label.config(text="Cancelling...")
        self.cancel_button.config(state="disabled")
    
    def was_cancelled(self):
        """Check if operation was cancelled"""
        return self.is_cancelled
    
    def auto_close(self, milliseconds=1000):
        """Auto-close dialog after operation completes"""
        self.auto_close_after = milliseconds
    
    def close(self):
        """Close the dialog"""
        elapsed_time = time.time() - self.start_time
        logger.debug(f"Progress dialog closed after {elapsed_time:.2f} seconds")
        self.destroy()


class ProgressManager:
    """Manager for progress dialogs with threading support"""
    
    def __init__(self, parent):
        self.parent = parent
        self.dialog = None
    
    def show_progress(self, title="Processing", message="Please wait...", show_cancel=False):
        """Show progress dialog"""
        self.dialog = ProgressDialog(self.parent, title, message)
        
        if show_cancel:
            self.dialog.show_cancel_button()
        
        return self.dialog
    
    def run_with_progress(self, operation, title="Processing", message="Please wait...", 
                         show_cancel=False, progress_callback=None):
        """Run an operation with progress dialog"""
        result = None
        error = None
        
        def worker():
            nonlocal result, error
            try:
                if progress_callback:
                    result = operation(progress_callback)
                else:
                    result = operation()
                
                # Update UI from main thread
                self.parent.after(0, self._on_complete, result)
                
            except Exception as e:
                error = e
                logger.error(f"Error in progress operation: {e}")
                self.parent.after(0, self._on_error, e)
        
        # Show progress dialog
        dialog = self.show_progress(title, message, show_cancel)
        
        # Start worker thread
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        
        # Wait for completion or cancellation
        self.parent.wait_window(dialog)
        
        if error:
            raise error
        
        return result
    
    def _on_complete(self, result):
        """Handle operation completion"""
        if self.dialog and not self.dialog.was_cancelled():
            self.dialog.update_progress(100, "Complete!")
            self.dialog.auto_close(500)
    
    def _on_error(self, error):
        """Handle operation error"""
        if self.dialog:
            self.dialog.status_label.config(text=f"Error: {error}")
            self.dialog.cancel_button.config(text="Close")
    
    def close_dialog(self):
        """Close the progress dialog"""
        if self.dialog:
            self.dialog.close()
            self.dialog = None
