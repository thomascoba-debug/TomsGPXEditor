import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.ui.base import PersistentDialog
import os
import logging
import gpxpy
from src.application.services.conversion_service import convert_gpx_file, save_converted_gpx

# Get logger for this module
logger = logging.getLogger(__name__)


class TrackToRouteDialog(PersistentDialog):

    def __init__(self, parent, entries, properties):
        super().__init__(parent, properties, "TrackToRouteDialog")
        
        self.title("Track to Route")
        self.entries = entries
        self.properties = properties
        self.selected_files = {}  # Track selected files
        
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(frame, text="Convert Tracks to Routes", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Info text
        info_text = "Select GPX files and configure downsampling before conversion."
        info_label = ttk.Label(frame, text=info_text)
        info_label.pack(pady=(0, 10))
        
        # Files list with checkboxes
        files_frame = ttk.LabelFrame(frame, text="Select GPX Files")
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
        editable_count = 0
        for entry in self.entries:
            if entry.editable_var.get():
                editable_count += 1
                file_frame = ttk.Frame(scrollable_frame)
                file_frame.pack(fill="x", padx=5, pady=2)
                
                # Checkbox for file selection
                var = tk.BooleanVar(value=True)
                self.selected_files[entry.path] = var
                
                checkbox = ttk.Checkbutton(
                    file_frame, 
                    text=os.path.basename(entry.path),
                    variable=var
                )
                checkbox.pack(side="left")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Downsampling settings
        downsample_frame = ttk.LabelFrame(frame, text="Downsampling Settings")
        downsample_frame.pack(fill="x", pady=(0, 10))
        
        # Points per 100km
        points_frame = ttk.Frame(downsample_frame)
        points_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(points_frame, text="Points per 100km:").pack(side="left")
        
        # Entry for points
        self.points_var = tk.IntVar(value=100)
        points_entry = ttk.Entry(points_frame, textvariable=self.points_var, width=10)
        points_entry.pack(side="left", padx=(10, 5))
        
        # Slider for points
        self.points_slider = ttk.Scale(
            points_frame,
            from_=10,
            to=500,
            orient="horizontal",
            variable=self.points_var,
            command=self._on_slider_change
        )
        self.points_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        # Sync entry and slider
        points_entry.bind('<Return>', self._on_entry_change)
        
        # Status
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
        
        # Downsample button
        downsample_button = ttk.Button(
            button_frame, 
            text="Downsample Tracks",
            command=self._downsample_tracks
        )
        downsample_button.pack(side="left", padx=(0, 5))
        
        # Convert button
        convert_button = ttk.Button(
            button_frame, 
            text="Convert to Routes",
            command=self._convert_to_routes
        )
        convert_button.pack(side="left", padx=(0, 5))
        
        # Close button
        close_button = ttk.Button(button_frame, text="Close", command=self._on_close)
        close_button.pack(side="right")
        
        # Store button references
        self.downsample_button = downsample_button
        self.convert_button = convert_button
        self.close_button = close_button
        
        # Load settings
        self._load_settings()
        
        # Update status
        self._update_status()

    def _on_slider_change(self, value):
        """Handle slider change"""
        self.points_var.set(int(float(value)))

    def _on_entry_change(self, event):
        """Handle entry change"""
        try:
            value = int(self.points_var.get())
            if 10 <= value <= 500:
                self.points_slider.set(value)
        except ValueError:
            pass

    def _update_status(self):
        """Update status label"""
        selected_count = sum(1 for var in self.selected_files.values() if var.get())
        editable_count = len(self.selected_files)
        
        if selected_count == 0:
            status_text = "No files selected for conversion"
            self.status_label.config(text=status_text, foreground="red")
        else:
            status_text = f"{selected_count} of {editable_count} file(s) selected for conversion"
            self.status_label.config(text=status_text, foreground="green")

    def _downsample_tracks(self):
        """Downsample selected tracks"""
        selected_files = [path for path, var in self.selected_files.items() if var.get()]
        
        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one file for downsampling.")
            return
        
        points_per_100km = self.points_var.get()
        
        try:
            for file_path in selected_files:
                logger.debug(f"Downsampling track: {file_path}")
                
                # Load GPX file
                with open(file_path, 'r', encoding='utf-8') as f:
                    gpx = gpxpy.parse(f)
                
                # Downsample tracks
                if gpx.tracks:
                    for track in gpx.tracks:
                        for segment in track.segments:
                            if len(segment.points) > 2:
                                # Keep start and end points, downsample middle points
                                downsampled_points = self._downsample_points(segment.points, points_per_100km)
                                segment.points = downsampled_points
                
                # Save downsampled file
                original_name = os.path.splitext(os.path.basename(file_path))[0]
                suggested_name = f"{original_name}_downsampled.gpx"
                original_dir = os.path.dirname(file_path)  # Use original file directory
                
                save_path = filedialog.asksaveasfilename(
                    parent=self,
                    title="Save Downsampled GPX File",
                    initialdir=original_dir,  # Set default directory
                    initialfile=suggested_name,
                    defaultextension=".gpx",
                    filetypes=[("GPX files", "*.gpx"), ("All files", "*.*")]
                )
                
                if save_path:
                    with open(save_path, 'w', encoding='utf-8') as f:
                        f.write(gpx.to_xml())
                    
                    logger.info(f"Downsampled file saved to: {save_path}")
                    messagebox.showinfo("Success", f"Downsampled file saved to:\n{save_path}")
                else:
                    logger.debug("User cancelled save dialog for downsampled file")
                    
        except Exception as e:
            logger.error(f"Error downsampling tracks: {str(e)}")
            messagebox.showerror("Error", f"Error downsampling tracks:\n{str(e)}")

    def _downsample_points(self, points, points_per_100km):
        """Downsample points while keeping start and end points"""
        if len(points) <= 2:
            return points
        
        # Calculate total distance
        total_distance = 0
        for i in range(1, len(points)):
            total_distance += points[i-1].distance_2d(points[i])
        
        # Calculate target number of points
        if total_distance == 0:
            return points
        
        # Convert distance to km and calculate target points
        distance_km = total_distance / 1000  # Convert to km
        target_points = max(2, int((distance_km / 100) * points_per_100km))
        
        if target_points >= len(points):
            return points
        
        # Simple downsampling: keep start, end, and evenly distribute intermediate points
        downsampled = [points[0]]  # Keep start point
        
        if target_points > 2:
            step = (len(points) - 2) / (target_points - 2)
            for i in range(1, target_points - 1):
                index = int(i * step) + 1
                if index < len(points) - 1:
                    downsampled.append(points[index])
        
        downsampled.append(points[-1])  # Keep end point
        
        return downsampled

    def _convert_to_routes(self):
        """Convert selected tracks to routes"""
        selected_files = [path for path, var in self.selected_files.items() if var.get()]
        
        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one file for conversion.")
            return
        
        try:
            for file_path in selected_files:
                logger.debug(f"Converting file: {file_path}")
                
                # Convert using existing conversion service
                success, message, gpx_data = convert_gpx_file(file_path, 'track_to_route')
                
                if success:
                    # Save dialog for new file
                    original_name = os.path.splitext(os.path.basename(file_path))[0]
                    suggested_name = f"{original_name}_converted_routes.gpx"
                    original_dir = os.path.dirname(file_path)  # Use original file directory
                    
                    save_path = filedialog.asksaveasfilename(
                        parent=self,
                        title="Save Converted GPX File",
                        initialdir=original_dir,  # Set default directory
                        initialfile=suggested_name,
                        defaultextension=".gpx",
                        filetypes=[("GPX files", "*.gpx"), ("All files", "*.*")]
                    )
                    
                    if save_path:
                        # Save converted file
                        success_save, message_save = save_converted_gpx(gpx_data, save_path)
                        
                        if success_save:
                            logger.info(f"Successfully converted tracks to routes and saved to: {save_path}")
                            messagebox.showinfo("Success", f"Converted file saved to:\n{save_path}")
                        else:
                            logger.error(f"Failed to save converted file: {message_save}")
                            messagebox.showerror("Error", f"Failed to save converted file:\n{message_save}")
                    else:
                        logger.debug("User cancelled save dialog for converted file")
                else:
                    logger.error(f"Failed to convert {file_path}: {message}")
                    messagebox.showerror("Error", f"Failed to convert {os.path.basename(file_path)}:\n{message}")
                    
        except Exception as e:
            logger.error(f"Exception converting files: {str(e)}")
            messagebox.showerror("Error", f"Exception during conversion:\n{str(e)}")

    def _on_close(self):
        """Close dialog - ALWAYS save settings and geometry"""
        # Save settings before closing
        self._save_settings()
        # Save geometry (handled by PersistentDialog base class)
        super()._on_close()

    def _load_settings(self):
        """Load saved settings"""
        try:
            points_per_100km = self.properties.get("track_to_route_points_per_100km", 100)
            self.points_var.set(points_per_100km)
            logger.debug(f"Loaded track to route settings: points={points_per_100km}")
        except Exception as e:
            logger.error(f"Error loading track to route settings: {e}")

    def _save_settings(self):
        """Save current settings"""
        try:
            self.properties.set("track_to_route_points_per_100km", self.points_var.get())
            logger.debug(f"Saved track to route settings: points={self.points_var.get()}")
        except Exception as e:
            logger.error(f"Error saving track to route settings: {e}")

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
            
            checkbox = ttk.Checkbutton(
                file_frame, 
                text=os.path.basename(file_path),
                variable=var
            )
            checkbox.pack(side="left")
        
        # Update canvas scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
