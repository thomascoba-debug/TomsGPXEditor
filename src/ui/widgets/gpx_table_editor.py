import tkinter as tk
from src.ui.base import PersistentDialog
from src.i18n import t
from tkinter import ttk
from tkinter import messagebox
import logging
import traceback
import copy
import gpxpy
from gpxpy.gpx import GPXTrackPoint, GPXTrackSegment
from src.application.services.command_service import CommandManager, PointMoveCommand, PointEditCommand

# Get logger for this module
logger = logging.getLogger(__name__)


class GPXTableEditor(PersistentDialog):
    
    def __init__(self, parent, document, update_callback, save_callback, properties):
        super().__init__(parent, properties, "GPXTableEditor", modal=False)
        
        self.title(t("dialogs.track_table.title"))
        # Geometry will be restored by PersistentDialog
        
        self.original_document = document
        self.update_callback = update_callback
        self.save_callback = save_callback
        
        # Initialize command manager for undo/redo
        self.command_manager = CommandManager()
        
        # Pagination settings
        self.page_size = 1000  # Points per page
        self.current_page = 0
        self.total_points = 0
        self.all_points = []  # Cache all points for pagination
        
        # Create a deep copy of the document for editing
        self.working_document = self._create_document_copy(document)
        self.has_changes = False
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview for track points
        columns = ("index", "lat", "lon", "ele", "time")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
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
        v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Pagination controls frame
        pagination_frame = ttk.Frame(main_frame)
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
        page_size_combo.pack(side="left", padx=2)
        page_size_combo.bind("<<ComboboxSelected>>", self.on_page_size_changed)
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Button frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # Navigation buttons frame
        nav_frame = ttk.Frame(button_frame)
        nav_frame.pack(side="left", padx=5)
        
        ttk.Button(nav_frame, text="↑", command=self.move_point_up, width=3).pack(side="left", padx=2)
        ttk.Button(nav_frame, text="↓", command=self.move_point_down, width=3).pack(side="left", padx=2)
        
        # Undo/Redo buttons
        undo_frame = ttk.Frame(button_frame)
        undo_frame.pack(side="left", padx=10)
        
        self.undo_button = ttk.Button(undo_frame, text="↶ Undo", command=self.undo_action, state="disabled")
        self.undo_button.pack(side="left", padx=2)
        
        self.redo_button = ttk.Button(undo_frame, text="↷ Redo", command=self.redo_action, state="disabled")
        self.redo_button.pack(side="left", padx=2)
        
        ttk.Button(button_frame, text=t("buttons.apply"), command=self.apply_changes).pack(side="left", padx=5)
        ttk.Button(button_frame, text=t("buttons.cancel"), command=self.cancel_changes).pack(side="left", padx=5)
        ttk.Button(button_frame, text=t("buttons.delete"), command=self.delete_point).pack(side="left", padx=5)
        ttk.Button(button_frame, text=t("buttons.close"), command=self.close_editor).pack(side="right", padx=5)
        
        # Setup keyboard shortcuts
        self.setup_keyboard_shortcuts()
    
    def _create_document_copy(self, original_document):
        """Create a deep copy of the GPX document for editing"""
        try:
            # Deep copy the GPX data
            copied_gpx = copy.deepcopy(original_document.gpx)
            
            # Create new document with copied data
            from src.application.services.gpx_service import GPXDocument
            copied_document = GPXDocument(copied_gpx, original_document.path)
            
            logger.debug(f"Created working copy of GPX document: {original_document.path}")
            return copied_document
            
        except Exception as e:
            logger.error(f"Failed to create document copy: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            raise ValueError(f"Failed to create working copy: {str(e)}")
    
    def load_data(self):
        """Load data from working document into table with pagination"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get first segment from working document
        segment = self.working_document.get_first_segment()
        if not segment:
            messagebox.showinfo("Info", "No track data found in this file")
            return
        
        # Cache all points for pagination
        self.all_points = segment.points
        self.total_points = len(self.all_points)
        
        # Reset to first page if we're out of bounds
        if self.current_page * self.page_size >= self.total_points:
            self.current_page = 0
        
        # Load current page
        self.load_current_page()
        self.update_page_info()
    
    def load_current_page(self):
        """Load the current page of points"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Calculate page boundaries
        start_idx = self.current_page * self.page_size
        end_idx = min(start_idx + self.page_size, self.total_points)
        
        # Load points for current page
        for i in range(start_idx, end_idx):
            point = self.all_points[i]
            lat = f"{point.latitude:.6f}"
            lon = f"{point.longitude:.6f}"
            ele = f"{point.elevation:.2f}" if point.elevation else ""
            time = str(point.time) if point.time else ""
            
            # Use 1-based index for display
            display_index = i + 1
            self.tree.insert("", "end", values=(display_index, lat, lon, ele, time))
    
    def update_page_info(self):
        """Update page information label"""
        total_pages = max(1, (self.total_points + self.page_size - 1) // self.page_size)
        current_page_display = self.current_page + 1  # Convert to 1-based
        
        start_point = self.current_page * self.page_size + 1
        end_point = min((self.current_page + 1) * self.page_size, self.total_points)
        
        info_text = f"Page {current_page_display} of {total_pages} ({self.total_points} points: {start_point}-{end_point})"
        self.page_info_label.config(text=info_text)
    
    def first_page(self):
        """Go to first page"""
        if self.current_page != 0:
            self.current_page = 0
            self.load_current_page()
            self.update_page_info()
    
    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_current_page()
            self.update_page_info()
    
    def next_page(self):
        """Go to next page"""
        total_pages = (self.total_points + self.page_size - 1) // self.page_size
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.load_current_page()
            self.update_page_info()
    
    def last_page(self):
        """Go to last page"""
        total_pages = (self.total_points + self.page_size - 1) // self.page_size
        if total_pages > 0:
            self.current_page = total_pages - 1
            self.load_current_page()
            self.update_page_info()
    
    def on_page_size_changed(self, event):
        """Handle page size change"""
        try:
            new_page_size = int(self.page_size_var.get())
            if new_page_size != self.page_size:
                self.page_size = new_page_size
                self.current_page = 0  # Reset to first page
                self.load_current_page()
                self.update_page_info()
                logger.debug(f"Page size changed to {new_page_size}")
        except ValueError:
            logger.error(f"Invalid page size: {self.page_size_var.get()}")
            self.page_size_var.set(str(self.page_size))  # Reset to valid value
    
    def delete_point(self):
        """Delete selected track point"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a point to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete selected track point?"):
            try:
                segment = self.working_document.get_first_segment()
                if not segment:
                    logger.warning("No segment found for deletion")
                    messagebox.showwarning("Warning", "No track data found")
                    return
                
                # Get selected item and its index
                item = selection[0]
                values = self.tree.item(item, "values")
                
                try:
                    point_index = int(values[0]) - 1  # Convert from 1-based to 0-based
                except (ValueError, IndexError, TypeError) as e:
                    logger.error(f"Failed to parse point index from values: {values} - {str(e)}")
                    messagebox.showerror("Error", "Invalid point selection")
                    return
                
                # Validate index
                if not (0 <= point_index < len(segment.points)):
                    logger.error(f"Point index {point_index} out of range (0-{len(segment.points)-1})")
                    messagebox.showerror("Error", f"Point index {point_index + 1} is out of range")
                    return
                
                # Log point details before deletion
                point = segment.points[point_index]
                logger.debug(f"Deleting point {point_index + 1}: lat={point.latitude}, lon={point.longitude}")
                
                # Remove point from working document segment
                segment.points.pop(point_index)
                
                # Update the all_points cache
                self.all_points.pop(point_index)
                self.total_points -= 1
                
                # Adjust current page if necessary
                total_pages = (self.total_points + self.page_size - 1) // self.page_size
                if self.current_page >= total_pages and total_pages > 0:
                    self.current_page = total_pages - 1
                
                # Mark as having changes
                self.has_changes = True
                
                # Reload current page to refresh table
                self.load_current_page()
                self.update_page_info()
                
                logger.debug(f"Successfully deleted point {point_index + 1}")
                messagebox.showinfo("Success", "Point deleted successfully")
                
            except Exception as e:
                logger.error(f"Failed to delete point: {str(e)}")
                logger.error(f"Stack trace: {traceback.format_exc()}")
                messagebox.showerror("Error", f"Failed to delete point: {str(e)}\n\nDetails have been logged.")
    
    def move_point_up(self):
        """Move selected track point up in the list"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a point to move")
            return
        
        try:
            segment = self.working_document.get_first_segment()
            if not segment:
                logger.warning("No segment found for move operation")
                messagebox.showwarning("Warning", "No track data found")
                return
            
            # Get selected item and its index
            item = selection[0]
            values = self.tree.item(item, "values")
            
            try:
                point_index = int(values[0]) - 1  # Convert from 1-based to 0-based
            except (ValueError, IndexError, TypeError) as e:
                logger.error(f"Failed to parse point index for move up: {values} - {str(e)}")
                messagebox.showerror("Error", "Invalid point selection")
                return
            
            # Validate index
            if not (0 <= point_index < len(segment.points)):
                logger.error(f"Point index {point_index} out of range for move up")
                messagebox.showerror("Error", f"Point index {point_index + 1} is out of range")
                return
            
            # Can only move up if not already at the top
            if point_index <= 0:
                logger.debug(f"Point {point_index + 1} is already at the top")
                messagebox.showinfo("Info", "Point is already at the top")
                return
            
            # Log move operation
            logger.debug(f"Moving point {point_index + 1} up to position {point_index}")
            
            # Swap points in working document segment
            segment.points[point_index], segment.points[point_index - 1] = \
                segment.points[point_index - 1], segment.points[point_index]
            
            # Mark as having changes
            self.has_changes = True
            
            # Reload data to refresh table
            self.load_data()
            
            # Select the moved item
            items = self.tree.get_children()
            if point_index - 1 < len(items):
                self.tree.selection_set(items[point_index - 1])
                self.tree.see(items[point_index - 1])
            
            logger.debug(f"Successfully moved point from position {point_index + 1} to {point_index}")
            
        except Exception as e:
            logger.error(f"Failed to move point up: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            messagebox.showerror("Error", f"Failed to move point up: {str(e)}\n\nDetails have been logged.")
    
    def move_point_down(self):
        """Move selected track point down in the list"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a point to move")
            return
        
        try:
            segment = self.working_document.get_first_segment()
            if not segment:
                logger.warning("No segment found for move operation")
                messagebox.showwarning("Warning", "No track data found")
                return
            
            # Get selected item and its index
            item = selection[0]
            values = self.tree.item(item, "values")
            
            try:
                point_index = int(values[0]) - 1  # Convert from 1-based to 0-based
            except (ValueError, IndexError, TypeError) as e:
                logger.error(f"Failed to parse point index for move down: {values} - {str(e)}")
                messagebox.showerror("Error", "Invalid point selection")
                return
            
            # Validate index
            if not (0 <= point_index < len(segment.points)):
                logger.error(f"Point index {point_index} out of range for move down")
                messagebox.showerror("Error", f"Point index {point_index + 1} is out of range")
                return
            
            # Can only move down if not already at the bottom
            if point_index >= len(segment.points) - 1:
                logger.debug(f"Point {point_index + 1} is already at the bottom")
                messagebox.showinfo("Info", "Point is already at the bottom")
                return
            
            # Log move operation
            logger.debug(f"Moving point {point_index + 1} down to position {point_index + 2}")
            
            # Swap points in working document segment
            segment.points[point_index], segment.points[point_index + 1] = \
                segment.points[point_index + 1], segment.points[point_index]
            
            # Mark as having changes
            self.has_changes = True
            
            # Reload data to refresh table
            self.load_data()
            
            # Select the moved item
            items = self.tree.get_children()
            if point_index + 1 < len(items):
                self.tree.selection_set(items[point_index + 1])
                self.tree.see(items[point_index + 1])
            
            logger.debug(f"Successfully moved point from position {point_index + 1} to {point_index + 2}")
            
        except Exception as e:
            logger.error(f"Failed to move point down: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            messagebox.showerror("Error", f"Failed to move point down: {str(e)}\n\nDetails have been logged.")
    
    def apply_changes(self):
        """Apply changes from working document to original document"""
        try:
            segment = self.working_document.get_first_segment()
            if not segment:
                logger.warning("No segment found in working document")
                messagebox.showwarning("Warning", "No track data found in working document")
                return
            
            # Get all items from tree
            items = self.tree.get_children()
            logger.debug(f"Applying changes for {len(items)} items")
            
            # Update working document points with table data
            for i, item in enumerate(items):
                try:
                    values = self.tree.item(item, "values")
                    if len(values) < 3:
                        logger.warning(f"Item {i} has insufficient data: {values}")
                        continue
                    
                    if i >= len(segment.points):
                        logger.warning(f"Index {i} exceeds available points ({len(segment.points)})")
                        break
                    
                    point = segment.points[i]
                    
                    # Parse and validate latitude
                    try:
                        point.latitude = float(values[1])
                    except (ValueError, TypeError) as e:
                        logger.error(f"Invalid latitude at row {i}: {values[1]} - {str(e)}")
                        raise ValueError(f"Invalid latitude value at row {i+1}: {values[1]}")
                    
                    # Parse and validate longitude
                    try:
                        point.longitude = float(values[2])
                    except (ValueError, TypeError) as e:
                        logger.error(f"Invalid longitude at row {i}: {values[2]} - {str(e)}")
                        raise ValueError(f"Invalid longitude value at row {i+1}: {values[2]}")
                    
                    # Parse elevation if provided
                    if values[3]:
                        try:
                            point.elevation = float(values[3])
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Invalid elevation at row {i}: {values[3]} - {str(e)}")
                            messagebox.showwarning("Warning", f"Invalid elevation at row {i+1}, keeping original value")
                    
                    # Parse time if provided
                    if values[4]:
                        point.time = values[4]
                    
                except Exception as e:
                    logger.error(f"Error processing row {i}: {str(e)}")
                    raise ValueError(f"Error processing row {i+1}: {str(e)}")
            
            # Copy working document back to original document
            self.original_document.gpx = copy.deepcopy(self.working_document.gpx)
            
            # Call save callback
            if self.save_callback:
                logger.debug("Calling save callback")
                success, message = self.save_callback(self.original_document)
                if not success:
                    messagebox.showerror("Save Error", f"Failed to save file: {message}")
                    return
            
            # Call update callback to refresh map
            if self.update_callback:
                logger.debug("Calling update callback")
                self.update_callback()
            
            self.has_changes = False
            logger.debug("Changes applied successfully")
            messagebox.showinfo("Success", "Changes applied and saved successfully!")
            
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            logger.error(f"Unexpected error during apply: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            messagebox.showerror("Error", f"Failed to apply changes: {str(e)}\n\nDetails have been logged.")
    
    def cancel_changes(self):
        """Cancel all changes and reload original data"""
        if self.has_changes:
            if messagebox.askyesno("Cancel Changes", "Are you sure you want to discard all changes?"):
                try:
                    # Recreate working document from original
                    self.working_document = self._create_document_copy(self.original_document)
                    self.has_changes = False
                    self.load_data()
                    logger.debug("Changes cancelled, original data reloaded")
                    messagebox.showinfo("Info", "All changes have been discarded")
                except Exception as e:
                    logger.error(f"Error cancelling changes: {str(e)}")
                    messagebox.showerror("Error", f"Failed to cancel changes: {str(e)}")
        else:
            messagebox.showinfo("Info", "No changes to cancel")
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for common actions"""
        self.bind('<Control-z>', lambda e: self.undo_action())
        self.bind('<Control-y>', lambda e: self.redo_action())
        self.bind('<Control-Z>', lambda e: self.undo_action())  # Shift+Ctrl+Z for redo
        self.bind('<Control-s>', lambda e: self.apply_changes())
        self.bind('<Escape>', lambda e: self.cancel_changes())
        self.bind('<Delete>', lambda e: self.delete_point())
        self.bind('<Up>', lambda e: self.move_point_up())
        self.bind('<Down>', lambda e: self.move_point_down())
        
        # Pagination keyboard shortcuts
        self.bind('<Control-Home>', lambda e: self.first_page())
        self.bind('<Control-End>', lambda e: self.last_page())
        self.bind('<Control-Prior>', lambda e: self.previous_page())  # Page Up
        self.bind('<Control-Next>', lambda e: self.next_page())  # Page Down
        self.bind('<Alt-Left>', lambda e: self.previous_page())
        self.bind('<Alt-Right>', lambda e: self.next_page())
        
        logger.debug("Keyboard shortcuts setup completed")
    
    def update_undo_redo_buttons(self):
        """Update the state of undo/redo buttons based on command manager"""
        if self.command_manager.can_undo():
            self.undo_button.config(state="normal")
        else:
            self.undo_button.config(state="disabled")
            
        if self.command_manager.can_redo():
            self.redo_button.config(state="normal")
        else:
            self.redo_button.config(state="disabled")
    
    def undo_action(self):
        """Handle undo action"""
        if self.command_manager.undo():
            self.load_data()  # Refresh the table
            self.update_undo_redo_buttons()
            logger.debug("Undo action completed")
    
    def redo_action(self):
        """Handle redo action"""
        if self.command_manager.redo():
            self.load_data()  # Refresh the table
            self.update_undo_redo_buttons()
            logger.debug("Redo action completed")
    
    def move_point_up(self):
        """Move selected point up using command pattern"""
        selected = self.tree.selection()
        if not selected:
            return
        
        selected_item = selected[0]
        values = self.tree.item(selected_item)['values']
        current_index = int(values[0]) - 1  # Convert back to 0-based
        
        if current_index > 0:
            # Get point data for command
            point_data = self.all_points[current_index]
            
            # Create and execute command
            from command_manager import PointMoveCommand
            command = PointMoveCommand(self, current_index, current_index - 1, point_data)
            if self.command_manager.execute_command(command):
                # Update the all_points array
                point = self.all_points.pop(current_index)
                self.all_points.insert(current_index - 1, point)
                
                # Reload current page to reflect changes
                self.load_current_page()
                self.update_undo_redo_buttons()
                
                # Re-select moved item
                new_index = current_index - 1
                for item in self.tree.get_children():
                    item_values = self.tree.item(item)['values']
                    if int(item_values[0]) == new_index + 1:
                        self.tree.selection_set(item)
                        self.tree.see(item)
                        break
    
    def move_point_down(self):
        """Move selected point down using command pattern"""
        selected = self.tree.selection()
        if not selected:
            return
        
        selected_item = selected[0]
        values = self.tree.item(selected_item)['values']
        current_index = int(values[0]) - 1  # Convert back to 0-based
        
        if current_index < len(self.all_points) - 1:
            # Get point data for command
            point_data = self.all_points[current_index]
            
            # Create and execute command
            from command_manager import PointMoveCommand
            command = PointMoveCommand(self, current_index, current_index + 1, point_data)
            if self.command_manager.execute_command(command):
                # Update the all_points array
                point = self.all_points.pop(current_index)
                self.all_points.insert(current_index + 1, point)
                
                # Reload current page to reflect changes
                self.load_current_page()
                self.update_undo_redo_buttons()
                
                # Re-select moved item
                new_index = current_index + 1
                for item in self.tree.get_children():
                    item_values = self.tree.item(item)['values']
                    if int(item_values[0]) == new_index + 1:
                        self.tree.selection_set(item)
                        self.tree.see(item)
                        break
    
    def close_editor(self):
        """Close the editor with confirmation if there are changes"""
        if hasattr(self, 'has_changes') and self.has_changes:
            if messagebox.askyesno("Ungespeicherte Änderungen", "Sie haben ungespeicherte Änderungen. Möchten Sie diese vor dem Schließen speichern?"):
                self.apply_changes()
                return
            elif messagebox.askyesno("Änderungen verwerfen", "Möchten Sie alle Änderungen verwerfen und schließen?"):
                self._on_close()
                return
        else:
            self._on_close()

    def _on_close(self):
        """Handle dialog close - save geometry and destroy"""
        # Save geometry (handled by PersistentDialog base class)
        super()._on_close()
