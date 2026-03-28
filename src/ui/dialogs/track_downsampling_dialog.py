#!/usr/bin/env python3
"""
Track Downsampling Dialog
Eigenständiger Dialog für das Downsampling von GPX-Tracks
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.ui.base import PersistentDialog
import os
import logging
import gpxpy

# Get logger for this module
logger = logging.getLogger(__name__)


class TrackDownsamplingDialog(PersistentDialog):

    def __init__(self, parent, entries, properties, modal=False):
        super().__init__(parent, properties, "TrackDownsamplingDialog", modal=modal)
        
        self.title("Track Downsampling")
        self.entries = entries
        self.properties = properties
        self.selected_files = {}  # Track selected files
        
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(frame, text="Downsample GPX Tracks", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Info text
        info_text = "Select editable GPX files with tracks and configure downsampling settings."
        info_label = ttk.Label(frame, text=info_text)
        info_label.pack(pady=(0, 10))
        
        # Files list with checkboxes
        files_frame = ttk.LabelFrame(frame, text="Select GPX Files with Tracks")
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
        
        # Add files with checkboxes (only editable files with tracks)
        editable_count = 0
        for entry in self.entries:
            if entry.editable_var.get():
                try:
                    # Check if file has tracks
                    with open(entry.path, 'r', encoding='utf-8') as f:
                        gpx = gpxpy.parse(f)
                    
                    if gpx.tracks and len(gpx.tracks) > 0:
                        editable_count += 1
                        file_frame = ttk.Frame(scrollable_frame)
                        file_frame.pack(fill="x", padx=5, pady=2)
                        
                        # Checkbox for file selection
                        var = tk.BooleanVar(value=True)
                        self.selected_files[entry.path] = var
                        
                        # File info
                        track_count = len(gpx.tracks)
                        total_points = sum(
                            len(segment.points) 
                            for track in gpx.tracks 
                            for segment in track.segments
                        )
                        file_info = f"{os.path.basename(entry.path)} ({track_count} tracks, {total_points} points)"
                        
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
        
        # Downsampling settings
        downsample_frame = ttk.LabelFrame(frame, text="Downsampling Settings")
        downsample_frame.pack(fill="x", pady=(0, 10))
        
        # Points per 100km
        points_frame = ttk.Frame(downsample_frame)
        points_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(points_frame, text="Points per 100km:").pack(side="left")
        
        # Entry for points
        self.points_var = tk.IntVar(value=20)
        points_entry = ttk.Entry(points_frame, textvariable=self.points_var, width=10)
        points_entry.pack(side="left", padx=(10, 5))
        
        # Slider for points
        self.points_slider = ttk.Scale(
            points_frame,
            from_=1,
            to=1000,
            orient="horizontal",
            variable=self.points_var,
            command=self._on_slider_change
        )
        self.points_slider.pack(side="left", fill="x", expand=True, padx=5)
        
        # Sync entry and slider
        points_entry.bind('<Return>', self._on_entry_change)
        
        # Options
        options_frame = ttk.Frame(downsample_frame)
        options_frame.pack(fill="x", padx=10, pady=5)
        
        self.keep_waypoints_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="Keep waypoints unchanged",
            variable=self.keep_waypoints_var
        ).pack(side="left")
        
        self.overwrite_original_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame,
            text="Overwrite original files",
            variable=self.overwrite_original_var
        ).pack(side="left", padx=(20, 0))
        
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
            text="Downsample Selected Files",
            command=self._downsample_files
        )
        downsample_button.pack(side="left", padx=(0, 5))
        
        # Close button
        close_button = ttk.Button(button_frame, text="Close", command=self._on_close)
        close_button.pack(side="right")
        
        # Store button references
        self.select_all_button = select_all_button
        self.downsample_button = downsample_button
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
            if 1 <= value <= 1000:
                self.points_slider.set(value)
        except ValueError:
            pass

    def _load_settings(self):
        """Load saved settings"""
        try:
            points_per_100km = self.properties.get("downsample_points_per_100km", 20)
            self.points_var.set(points_per_100km)
            
            keep_waypoints = self.properties.get("downsample_keep_waypoints", True)
            self.keep_waypoints_var.set(keep_waypoints)
            
            overwrite_original = self.properties.get("downsample_overwrite_original", False)
            self.overwrite_original_var.set(overwrite_original)
            
            logger.debug(f"Loaded downsampling settings: points={points_per_100km}, keep_waypoints={keep_waypoints}, overwrite={overwrite_original}")
            
        except Exception as e:
            logger.error(f"Error loading downsampling settings: {e}")

    def _save_settings(self):
        """Save current settings"""
        try:
            self.properties.set("downsample_points_per_100km", self.points_var.get())
            self.properties.set("downsample_keep_waypoints", self.keep_waypoints_var.get())
            self.properties.set("downsample_overwrite_original", self.overwrite_original_var.get())
            
            logger.debug(f"Saved downsampling settings: points={self.points_var.get()}, keep_waypoints={self.keep_waypoints_var.get()}, overwrite={self.overwrite_original_var.get()}")
            
        except Exception as e:
            logger.error(f"Error saving downsampling settings: {e}")

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
                
                track_count = len(gpx.tracks)
                total_points = sum(
                    len(segment.points) 
                    for track in gpx.tracks 
                    for segment in track.segments
                )
                file_info = f"{os.path.basename(file_path)} ({track_count} tracks, {total_points} points)"
                
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
            self.downsample_button.config(state="disabled")
        else:
            self.status_label.config(
                text=f"{selected_count} of {total_count} file(s) selected for downsampling", 
                foreground="green"
            )
            self.downsample_button.config(state="normal")

    def _downsample_files(self):
        """Downsample selected files"""
        selected_files = [path for path, var in self.selected_files.items() if var.get()]
        
        if not selected_files:
            messagebox.showwarning("No Selection", "Please select at least one file for downsampling.")
            return
        
        points_per_100km = self.points_var.get()
        keep_waypoints = self.keep_waypoints_var.get()
        overwrite_original = self.overwrite_original_var.get()
        
        # Safety check for overwrite
        if overwrite_original:
            result = messagebox.askyesno(
                "DANGER - Overwrite Original Files",
                f"WARNING: This will overwrite {len(selected_files)} original file(s)!\n\n"
                "This action cannot be undone.\n\n"
                "Are you absolutely sure you want to continue?",
                icon="warning"
            )
            if not result:
                return
        
        # Save settings
        self._save_settings()
        
        try:
            processed_count = 0
            error_count = 0
            
            for file_path in selected_files:
                try:
                    logger.info(f"Downsampling file: {file_path}")
                    
                    # Load GPX file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        gpx = gpxpy.parse(f)
                    
                    # Downsample tracks
                    if gpx.tracks:
                        for track in gpx.tracks:
                            for segment in track.segments:
                                if len(segment.points) > 2:
                                    downsampled_points = self._downsample_points(
                                        segment.points, points_per_100km
                                    )
                                    segment.points = downsampled_points
                    
                    # Remove waypoints if requested
                    if not keep_waypoints:
                        gpx.waypoints = []
                    
                    # Determine save path
                    if overwrite_original:
                        save_path = file_path
                    else:
                        original_name = os.path.splitext(os.path.basename(file_path))[0]
                        suggested_name = f"{original_name}_downsampled.gpx"
                        original_dir = os.path.dirname(file_path)
                        
                        save_path = filedialog.asksaveasfilename(
                            parent=self,
                            title="Save Downsampled GPX File",
                            initialdir=original_dir,
                            initialfile=suggested_name,
                            defaultextension=".gpx",
                            filetypes=[("GPX files", "*.gpx"), ("All files", "*.*")]
                        )
                    
                    if save_path:
                        # Save file
                        with open(save_path, 'w', encoding='utf-8') as f:
                            f.write(gpx.to_xml())
                        
                        processed_count += 1
                        logger.info(f"Downsampled file saved to: {save_path}")
                    else:
                        logger.debug("User cancelled save dialog")
                        
                except Exception as e:
                    error_count += 1
                    logger.error(f"Error downsampling file {file_path}: {e}")
            
            # Show result
            if error_count == 0:
                messagebox.showinfo(
                    "Success", 
                    f"Successfully downsampled {processed_count} file(s)."
                )
            else:
                messagebox.showwarning(
                    "Partial Success",
                    f"Processed {processed_count} file(s) successfully,\n"
                    f"but {error_count} file(s) had errors."
                )
                
        except Exception as e:
            logger.error(f"Error in downsampling process: {e}")
            messagebox.showerror("Error", f"Error during downsampling:\n{str(e)}")

    def _downsample_points(self, points, points_per_100km):
        """Downsample points while keeping start and end points"""
        if len(points) <= 2:
            return points
        
        # Calculate total distance
        total_distance = 0
        for i in range(1, len(points)):
            total_distance += points[i-1].distance_2d(points[i])
        
        # Calculate target points
        if total_distance == 0:
            return points
        
        # Convert distance to km and calculate target points
        distance_km = total_distance / 1000
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

    def _on_close(self):
        """Handle dialog close - ALWAYS save settings and geometry"""
        # Save settings before closing
        self._save_settings()
        # Save geometry (handled by PersistentDialog base class)
        super()._on_close()
