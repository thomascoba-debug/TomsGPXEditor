#!/usr/bin/env python3
"""
GPXTableEditor Refactoring - Split God Object into focused components

This script refactors the GPXTableEditor class from a God Object (23 methods)
into smaller, focused components following Single Responsibility Principle.
"""

import os
import shutil
from datetime import datetime

class GPXTableEditorRefactorer:
    def __init__(self):
        self.backup_dir = "W:/TomsGPXEditor/backup_before_refactor"
        self.source_file = "W:/TomsGPXEditor/src/ui/widgets/gpx_table_editor.py"
        
    def create_backup(self):
        """Create backup before refactoring"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{self.backup_dir}/gpx_table_editor_{timestamp}.py"
        
        shutil.copy2(self.source_file, backup_file)
        print(f"✅ Backup created: {backup_file}")
        
    def analyze_responsibilities(self):
        """Analyze and categorize the responsibilities"""
        responsibilities = {
            "ui_setup": [
                "setup_ui",
                "setup_keyboard_shortcuts"
            ],
            "data_management": [
                "load_data",
                "load_current_page",
                "_create_document_copy"
            ],
            "pagination": [
                "first_page",
                "previous_page", 
                "next_page",
                "last_page",
                "update_page_info",
                "on_page_size_changed"
            ],
            "point_operations": [
                "delete_point",
                "move_point_up",
                "move_point_down"
            ],
            "command_operations": [
                "apply_changes",
                "cancel_changes",
                "undo_action",
                "redo_action",
                "update_undo_redo_buttons"
            ],
            "dialog_management": [
                "close_editor"
            ]
        }
        
        print("📊 GPXTableEditor Responsibilities Analysis:")
        for category, methods in responsibilities.items():
            print(f"   {category}: {len(methods)} methods")
            for method in methods:
                print(f"     - {method}")
        
        return responsibilities
    
    def create_pagination_manager(self):
        """Create PaginationManager class"""
        content = '''"""
Pagination Manager - Handles all pagination logic for GPX table editor
"""
import tkinter as tk
from tkinter import ttk

class PaginationManager:
    """Handles pagination logic for large datasets"""
    
    def __init__(self, page_size=1000):
        self.page_size = page_size
        self.current_page = 0
        self.total_points = 0
        self.all_points = []
        self.page_size_var = None
        self.page_info_label = None
        
    def setup_ui(self, parent_frame):
        """Setup pagination UI controls"""
        # Pagination controls frame
        pagination_frame = ttk.Frame(parent_frame)
        pagination_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        # Page info label
        self.page_info_label = ttk.Label(pagination_frame, text="Page 1 of 1 (0 points)")
        self.page_info_label.pack(side="left", padx=(0, 20))
        
        # Navigation buttons
        ttk.Button(pagination_frame, text="⏮ First", command=self.first_page, width=8).pack(side="left", padx=2)
        ttk.Button(pagination_frame, text="◀ Previous", command=self.previous_page, width=10).pack(side="left", padx=2)
        ttk.Button(pagination_frame, text="Next ▶", command=self.next_page, width=10).pack(side="left", padx=2)
        ttk.Button(pagination_frame, text="Last ⏭", command=self.last_page, width=8).pack(side="left", padx=2)
        
        # Page size selector
        ttk.Label(pagination_frame, text="Page size:").pack(side="left", padx=(20, 5))
        self.page_size_var = tk.StringVar(value=str(self.page_size))
        page_size_combo = ttk.Combobox(pagination_frame, textvariable=self.page_size_var,
                                     values=["100", "500", "1000", "2000", "5000"],
                                     width=8, state="readonly")
        page_size_combo.pack(side="left")
        page_size_combo.bind("<<ComboboxSelected>>", self.on_page_size_changed)
        
        return pagination_frame
    
    def set_data(self, all_points):
        """Set the complete dataset"""
        self.all_points = all_points
        self.total_points = len(all_points)
        self.current_page = 0
        self.update_page_info()
    
    def get_current_page_data(self):
        """Get data for current page"""
        start_idx = self.current_page * self.page_size
        end_idx = min(start_idx + self.page_size, self.total_points)
        
        if start_idx >= self.total_points:
            return []
        
        return self.all_points[start_idx:end_idx]
    
    def first_page(self):
        """Go to first page"""
        if self.current_page != 0:
            self.current_page = 0
            return True
        return False
    
    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            return True
        return False
    
    def next_page(self):
        """Go to next page"""
        total_pages = (self.total_points + self.page_size - 1) // self.page_size
        if self.current_page < total_pages - 1:
            self.current_page += 1
            return True
        return False
    
    def last_page(self):
        """Go to last page"""
        total_pages = (self.total_points + self.page_size - 1) // self.page_size
        if total_pages > 0:
            self.current_page = total_pages - 1
            return True
        return False
    
    def on_page_size_changed(self, event):
        """Handle page size change"""
        try:
            new_page_size = int(self.page_size_var.get())
            if new_page_size > 0:
                self.page_size = new_page_size
                self.current_page = 0  # Reset to first page
                return True
        except ValueError:
            pass
        return False
    
    def update_page_info(self):
        """Update page information label"""
        total_pages = max(1, (self.total_points + self.page_size - 1) // self.page_size)
        current_page_display = self.current_page + 1  # Convert to 1-based
        
        start_point = self.current_page * self.page_size + 1
        end_point = min((self.current_page + 1) * self.page_size, self.total_points)
        
        info_text = f"Page {current_page_display} of {total_pages} ({self.total_points} points: {start_point}-{end_point})"
        if self.page_info_label:
            self.page_info_label.config(text=info_text)
'''
        
        with open("W:/TomsGPXEditor/src/ui/widgets/pagination_manager.py", "w") as f:
            f.write(content)
        
        print("✅ Created: PaginationManager class")
    
    def create_table_ui_manager(self):
        """Create TableUIManager class"""
        content = '''"""
Table UI Manager - Handles table setup and display
"""
import tkinter as tk
from tkinter import ttk

class TableUIManager:
    """Manages table UI setup and display"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.tree = None
        
    def setup_table(self):
        """Setup the treeview table"""
        # Treeview for track points
        columns = ("index", "lat", "lon", "ele", "time")
        self.tree = ttk.Treeview(self.parent_frame, columns=columns, show="headings")
        
        # Define headings
        self.tree.heading("index", text="#")
        self.tree.heading("lat", text="Latitude")
        self.tree.heading("lon", text="Longitude")
        self.tree.heading("ele", text="Elevation")
        self.tree.heading("time", text="Time")
        
        # Configure column widths
        self.tree.column("index", width=50)
        self.tree.column("lat", width=120)
        self.tree.column("lon", width=120)
        self.tree.column("ele", width=100)
        self.tree.column("time", width=200)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.parent_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        self.parent_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=1)
        
        return self.tree
    
    def clear_table(self):
        """Clear all data from table"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def load_data(self, points_data):
        """Load data into table"""
        self.clear_table()
        
        for i, point in enumerate(points_data):
            lat = getattr(point, 'latitude', 'N/A')
            lon = getattr(point, 'longitude', 'N/A')
            ele = getattr(point, 'elevation', 'N/A')
            time = getattr(point, 'time', 'N/A')
            
            display_index = i + 1
            self.tree.insert("", "end", values=(display_index, lat, lon, ele, time))
    
    def get_selection(self):
        """Get selected items from table"""
        return self.tree.selection()
    
    def see_item(self, item):
        """Ensure item is visible"""
        self.tree.see(item)
'''
        
        with open("W:/TomsGPXEditor/src/ui/widgets/table_ui_manager.py", "w") as f:
            f.write(content)
        
        print("✅ Created: TableUIManager class")
    
    def create_point_operations_manager(self):
        """Create PointOperationsManager class"""
        content = '''"""
Point Operations Manager - Handles point manipulation operations
"""
import tkinter as tk
from tkinter import messagebox
import logging
import traceback

# Get logger for this module
logger = logging.getLogger(__name__)

class PointOperationsManager:
    """Manages point operations like delete, move up/down"""
    
    def __init__(self, tree, working_document, command_manager):
        self.tree = tree
        self.working_document = working_document
        self.command_manager = command_manager
    
    def delete_point(self):
        """Delete selected track point"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a point to delete.")
            return False
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected point?"):
            try:
                # Get the index from tree selection
                item = selection[0]
                point_index = int(self.tree.item(item)['values'][0]) - 1  # Convert to 0-based
                
                # Delete from working document
                segment = self.working_document.get_first_segment()
                if segment and point_index < len(segment.points):
                    segment.points.pop(point_index)
                    return True
                else:
                    messagebox.showerror("Error", "Invalid point index.")
                    return False
                    
            except Exception as e:
                logger.error(f"Failed to delete point: {str(e)}")
                logger.error(f"Stack trace: {traceback.format_exc()}")
                messagebox.showerror("Error", f"Failed to delete point: {str(e)}\\n\\nDetails have been logged.")
                return False
        
        return False
    
    def move_point_up(self, selection=None):
        """Move selected track point up in list"""
        if not selection:
            selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("No Selection", "Please select a point to move.")
            return False
        
        try:
            item = selection[0]
            point_index = int(self.tree.item(item)['values'][0]) - 1  # Convert to 0-based
            
            segment = self.working_document.get_first_segment()
            if segment and point_index > 0 and point_index < len(segment.points):
                # Swap points
                segment.points[point_index], segment.points[point_index - 1] = \
                    segment.points[point_index - 1], segment.points[point_index]
                
                # Update tree selection
                self.tree.selection_set(item)
                self.tree.see(item)
                return True
            else:
                messagebox.showerror("Error", "Cannot move point up (already at top).")
                return False
                
        except Exception as e:
            logger.error(f"Failed to move point up: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            messagebox.showerror("Error", f"Failed to move point up: {str(e)}\\n\\nDetails have been logged.")
            return False
    
    def move_point_down(self, selection=None):
        """Move selected track point down in list"""
        if not selection:
            selection = self.tree.selection()
        
        if not selection:
            messagebox.showwarning("No Selection", "Please select a point to move.")
            return False
        
        try:
            item = selection[0]
            point_index = int(self.tree.item(item)['values'][0]) - 1  # Convert to 0-based
            
            segment = self.working_document.get_first_segment()
            if segment and point_index < len(segment.points) - 1:
                # Swap points
                segment.points[point_index], segment.points[point_index + 1] = \
                    segment.points[point_index + 1], segment.points[point_index]
                
                # Update tree selection
                self.tree.selection_set(item)
                self.tree.see(item)
                return True
            else:
                messagebox.showerror("Error", "Cannot move point down (already at bottom).")
                return False
                
        except Exception as e:
            logger.error(f"Failed to move point down: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            messagebox.showerror("Error", f"Failed to move point down: {str(e)}\\n\\nDetails have been logged.")
            return False
'''
        
        with open("W:/TomsGPXEditor/src/ui/widgets/point_operations_manager.py", "w") as f:
            f.write(content)
        
        print("✅ Created: PointOperationsManager class")
    
    def create_refactored_gpx_table_editor(self):
        """Create the refactored GPXTableEditor"""
        content = '''"""
Refactored GPX Table Editor - Split into focused components

This refactored version follows Single Responsibility Principle by splitting
the God Object into focused managers for different responsibilities.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
import traceback
import copy
import gpxpy
from gpxpy.gpx import GPXTrackPoint, GPXTrackSegment

# Import the new manager classes
from .pagination_manager import PaginationManager
from .table_ui_manager import TableUIManager
from .point_operations_manager import PointOperationsManager
from src.application.services.command_service import CommandManager, PointMoveCommand, PointEditCommand

# Get logger for this module
logger = logging.getLogger(__name__)


class GPXTableEditor(tk.Toplevel):
    """
    Refactored GPX Table Editor with focused responsibilities
    
    Responsibilities split into:
    - PaginationManager: Handles pagination logic
    - TableUIManager: Manages table display
    - PointOperationsManager: Handles point operations
    """
    
    def __init__(self, parent, document, update_callback, save_callback):
        super().__init__(parent)
        
        self.title("Track Table Editor")
        self.geometry("800x600")
        
        self.original_document = document
        self.update_callback = update_callback
        self.save_callback = save_callback
        
        # Initialize managers
        self.command_manager = CommandManager()
        self.pagination_manager = PaginationManager()
        self.table_ui_manager = None
        self.point_operations_manager = None
        
        # Create a deep copy of document for editing
        self.working_document = self._create_document_copy(document)
        self.has_changes = False
        
        self.setup_ui()
        self.load_data()
        self.setup_keyboard_shortcuts()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Setup table UI
        self.table_ui_manager = TableUIManager(main_frame)
        tree = self.table_ui_manager.setup_table()
        
        # Setup point operations manager
        self.point_operations_manager = PointOperationsManager(
            tree, self.working_document, self.command_manager
        )
        
        # Setup pagination UI
        self.pagination_manager.setup_ui(main_frame)
    
    def _create_document_copy(self, original_document):
        """Create a deep copy of GPX document for editing"""
        try:
            # Deep copy the GPX data
            working_copy = copy.deepcopy(original_document)
            logger.debug(f"Created working copy with {len(working_copy.get_points())} points")
            return working_copy
        except Exception as e:
            logger.error(f"Failed to create working copy: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            raise ValueError(f"Failed to create working copy: {str(e)}")
    
    def load_data(self):
        """Load data from working document into table with pagination"""
        try:
            # Get all points from working document
            all_points = []
            for track in self.working_document.tracks:
                for segment in track.segments:
                    all_points.extend(segment.points)
            
            # Set data for pagination manager
            self.pagination_manager.set_data(all_points)
            
            # Load current page
            current_page_data = self.pagination_manager.get_current_page_data()
            self.table_ui_manager.load_data(current_page_data)
            
            self.has_changes = False
            logger.debug(f"Loaded {len(all_points)} points into table")
            
        except Exception as e:
            logger.error(f"Failed to load data: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            messagebox.showerror("Error", f"Failed to load data: {str(e)}\\n\\nDetails have been logged.")
    
    def refresh_display(self):
        """Refresh the table display"""
        current_page_data = self.pagination_manager.get_current_page_data()
        self.table_ui_manager.load_data(current_page_data)
        self.pagination_manager.update_page_info()
    
    def delete_point(self):
        """Delete selected track point"""
        if self.point_operations_manager.delete_point():
            self.refresh_display()
            self.has_changes = True
    
    def move_point_up(self):
        """Move selected track point up in list"""
        selection = self.table_ui_manager.get_selection()
        if self.point_operations_manager.move_point_up(selection):
            self.refresh_display()
            self.has_changes = True
    
    def move_point_down(self):
        """Move selected track point down in list"""
        selection = self.table_ui_manager.get_selection()
        if self.point_operations_manager.move_point_down(selection):
            self.refresh_display()
            self.has_changes = True
    
    def first_page(self):
        """Go to first page"""
        if self.pagination_manager.first_page():
            self.refresh_display()
    
    def previous_page(self):
        """Go to previous page"""
        if self.pagination_manager.previous_page():
            self.refresh_display()
    
    def next_page(self):
        """Go to next page"""
        if self.pagination_manager.next_page():
            self.refresh_display()
    
    def last_page(self):
        """Go to last page"""
        if self.pagination_manager.last_page():
            self.refresh_display()
    
    def on_page_size_changed(self, event):
        """Handle page size change"""
        if self.pagination_manager.on_page_size_changed(event):
            self.refresh_display()
    
    def apply_changes(self):
        """Apply changes from working document to original document"""
        try:
            segment = self.working_document.get_first_segment()
            if segment and len(segment.points) > 0:
                # Apply changes to original document
                original_segment = self.original_document.get_first_segment()
                if original_segment:
                    original_segment.points = copy.deepcopy(segment.points)
                
                self.has_changes = False
                self.save_callback(self.original_document)
                messagebox.showinfo("Success", "Changes have been applied successfully.")
                self.destroy()
            else:
                messagebox.showwarning("No Changes", "No changes to apply.")
                
        except Exception as e:
            logger.error(f"Failed to apply changes: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            messagebox.showerror("Error", f"Failed to apply changes: {str(e)}\\n\\nDetails have been logged.")
    
    def cancel_changes(self):
        """Cancel all changes and reload original data"""
        if self.has_changes:
            if messagebox.askyesno("Cancel Changes", "Are you sure you want to discard all changes?"):
                self.destroy()
        else:
            messagebox.showinfo("Info", "No changes to cancel")
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for common actions"""
        self.bind('<Control-z>', lambda e: self.undo_action())
        self.bind('<Control-y>', lambda e: self.redo_action())
        self.bind('<Delete>', lambda e: self.delete_point())
        self.bind('<Up>', lambda e: self.move_point_up())
        self.bind('<Down>', lambda e: self.move_point_down())
        self.bind('<Control-s>', lambda e: self.apply_changes())
        self.bind('<Escape>', lambda e: self.cancel_changes())
        
        logger.debug("Keyboard shortcuts setup completed")
    
    def undo_action(self):
        """Handle undo action"""
        if self.command_manager.undo():
            self.refresh_display()
            logger.debug("Undo action completed")
    
    def redo_action(self):
        """Handle redo action"""
        if self.command_manager.redo():
            self.refresh_display()
            logger.debug("Redo action completed")
    
    def close_editor(self):
        """Close editor with confirmation if there are changes"""
        if self.has_changes:
            if messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Do you want to save them before closing?"):
                self.apply_changes()
            else:
                self.destroy()
        else:
            self.destroy()
'''
        
        # Create backup of original
        original_backup = f"{self.source_file}.original_backup"
        shutil.copy2(self.source_file, original_backup)
        
        # Write refactored version
        with open(self.source_file, "w") as f:
            f.write(content)
        
        print("Refactored: GPXTableEditor (from 23 methods to ~15 methods)")

def main():
    """Main function to execute the refactoring"""
    refactorer = GPXTableEditorRefactorer()
    refactorer.refactor()

if __name__ == "__main__":
    main()
