import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.ui.base import PersistentDialog
import os
import logging
import gpxpy

# Get logger for this module
logger = logging.getLogger(__name__)


class RouteToTrackDialog(PersistentDialog):

    def __init__(self, parent, entries, properties):
        super().__init__(parent, properties, "RouteToTrackDialog")
        
        self.title("Route to Track")
        self.entries = entries
        self.properties = properties
        
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(frame, text="Convert Routes to Tracks", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Info text
        info_text = "Selected editable files will be converted from routes to tracks."
        info_label = ttk.Label(frame, text=info_text)
        info_label.pack(pady=(0, 10))
        
        # Files list
        files_frame = ttk.LabelFrame(frame, text="Selected Files")
        files_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Create scrollable frame
        canvas = tk.Canvas(files_frame, height=200)
        scrollbar = ttk.Scrollbar(files_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Store references for rebuild
        self.canvas = canvas
        self.scrollable_frame = scrollable_frame
        
        # Add files with checkboxes
        self.selected_files = {}  # Track selected files
        editable_count = 0
        for entry in self.entries:
            if entry.editable_var.get():
                try:
                    # Check if file has routes
                    with open(entry.path, 'r', encoding='utf-8') as f:
                        gpx = gpxpy.parse(f)
                    
                    if gpx.routes and len(gpx.routes) > 0:
                        editable_count += 1
                        file_frame = ttk.Frame(scrollable_frame)
                        file_frame.pack(fill="x", padx=5, pady=2)
                        
                        # Checkbox for file selection
                        var = tk.BooleanVar(value=True)
                        self.selected_files[entry.path] = var
                        
                        # File info
                        route_count = len(gpx.routes)
                        total_points = sum(len(route.points) for route in gpx.routes)
                        file_info = f"{os.path.basename(entry.path)} ({route_count} routes, {total_points} points)"
                        
                        checkbox = ttk.Checkbutton(
                            file_frame, 
                            text=file_info,
                            variable=var
                        )
                        checkbox.pack(side="left")
                        
                except Exception as e:
                    logger.warning(f"Error analyzing file {entry.path}: {e}")
                    continue
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Status label
        self.status_label = ttk.Label(frame, text="", foreground="blue")
        self.status_label.pack(pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x")
        
        # Select All button
        select_all_button = ttk.Button(
            button_frame, 
            text="Select All",
            command=self._select_all
        )
        select_all_button.pack(side="left", padx=(0, 5))
        
        # Deselect All button
        deselect_all_button = ttk.Button(
            button_frame, 
            text="Deselect All",
            command=self._deselect_all
        )
        deselect_all_button.pack(side="left", padx=(0, 5))
        
        # Remove button
        remove_button = ttk.Button(
            button_frame, 
            text="Remove Selected",
            command=self._remove_selected
        )
        remove_button.pack(side="left", padx=(0, 5))
        
        # Convert button
        convert_button = ttk.Button(
            button_frame, 
            text="Convert to Tracks",
            command=self._convert_to_tracks
        )
        convert_button.pack(side="left", padx=(0, 5))
        
        # Close button
        close_button = ttk.Button(button_frame, text="Close", command=self._on_close)
        close_button.pack(side="right")
        
        # Store button references
        self.convert_button = convert_button
        self.close_button = close_button
        
        # Update status
        self._update_status()

    def _on_close(self):
        """Close dialog - ALWAYS save geometry"""
        # Save geometry (handled by PersistentDialog base class)
        super()._on_close()

    def _select_all(self):
        """Select all files"""
        for var in self.selected_files.values():
            var.set(True)
        self._update_status()

    def _deselect_all(self):
        """Deselect all files"""
        for var in self.selected_files.values():
            var.set(False)
        self._update_status()

    def _remove_selected(self):
        """Remove selected files from the list"""
        selected_files = [path for path, var in self.selected_files.items() if var.get()]
        
        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one file to remove.")
            return
        
        # Confirm removal
        result = messagebox.askyesno(
            "Remove Files",
            f"Remove {len(selected_files)} file(s) from the list?\n\n"
            "This will not delete the actual files, just remove them from this dialog.",
            icon="question"
        )
        
        if not result:
            return
        
        # Remove selected files
        for file_path in selected_files:
            del self.selected_files[file_path]
        
        # Rebuild the file list
        self._rebuild_file_list()
        self._update_status()

    def _rebuild_file_list(self):
        """Rebuild the file list display"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Re-add files
        for file_path, var in self.selected_files.items():
            file_frame = ttk.Frame(self.scrollable_frame)
            file_frame.pack(fill="x", padx=5, pady=2)
            
            # Get file info
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    gpx = gpxpy.parse(f)
                
                route_count = len(gpx.routes)
                total_points = sum(len(route.points) for route in gpx.routes)
                file_info = f"{os.path.basename(file_path)} ({route_count} routes, {total_points} points)"
                
            except Exception as e:
                file_info = f"{os.path.basename(file_path)} (error reading file)"
            
            checkbox = ttk.Checkbutton(
                file_frame, 
                text=file_info,
                variable=var
            )
            checkbox.pack(side="left")
        
        # Update canvas scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _update_status(self):
        """Update status label"""
        selected_count = sum(1 for var in self.selected_files.values() if var.get())
        total_count = len(self.selected_files)
        
        if selected_count == 0:
            self.status_label.config(text="No files selected", foreground="red")
            self.convert_button.config(state="disabled")
        else:
            self.status_label.config(
                text=f"{selected_count} of {total_count} file(s) selected for conversion", 
                foreground="green"
            )
            self.convert_button.config(state="normal")

    def _convert_to_tracks(self):
        """Convert selected routes to tracks"""
        selected_files = [path for path, var in self.selected_files.items() if var.get()]
        
        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one file for conversion.")
            return
        
        try:
            converted_count = 0
            error_count = 0
            
            for file_path in selected_files:
                try:
                    logger.debug(f"Converting routes to tracks: {file_path}")
                    
                    # Load GPX file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        gpx = gpxpy.parse(f)
                    
                    # Convert routes to tracks
                    if gpx.routes:
                        for route in gpx.routes:
                            track = gpxpy.gpx.GPXTrack()
                            if route.name:
                                track.name = route.name
                            
                            segment = gpxpy.gpx.GPXTrackSegment()
                            for point in route.points:
                                segment.points.append(point)
                            
                            track.segments.append(segment)
                            gpx.tracks.append(track)
                        
                        # Remove original routes
                        gpx.routes = []
                    
                    # Save converted file
                    original_name = os.path.splitext(os.path.basename(file_path))[0]
                    suggested_name = f"{original_name}_converted_tracks.gpx"
                    original_dir = os.path.dirname(file_path)
                    
                    save_path = filedialog.asksaveasfilename(
                        parent=self,
                        title="Save Converted GPX File",
                        initialdir=original_dir,
                        initialfile=suggested_name,
                        defaultextension=".gpx",
                        filetypes=[("GPX files", "*.gpx"), ("All files", "*.*")]
                    )
                    
                    if save_path:
                        with open(save_path, 'w', encoding='utf-8') as f:
                            f.write(gpx.to_xml())
                        
                        converted_count += 1
                        logger.info(f"Converted file saved to: {save_path}")
                    else:
                        logger.debug("User cancelled save dialog")
                        
                except Exception as e:
                    error_count += 1
                    logger.error(f"Error converting file {file_path}: {e}")
            
            # Show result
            if error_count == 0:
                messagebox.showinfo(
                    "Success", 
                    f"Successfully converted {converted_count} file(s)."
                )
            else:
                messagebox.showwarning(
                    "Partial Success",
                    f"Converted {converted_count} file(s) successfully,\n"
                    f"but {error_count} file(s) had errors."
                )
                
        except Exception as e:
            logger.error(f"Error in conversion process: {e}")
            messagebox.showerror("Error", f"Error during conversion:\n{str(e)}")
