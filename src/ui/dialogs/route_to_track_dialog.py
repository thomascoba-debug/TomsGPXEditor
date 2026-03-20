import tkinter as tk
from tkinter import ttk
from src.ui.base import PersistentDialog
import os
import logging

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
        
        # Add selected files
        editable_count = 0
        for entry in self.entries:
            if entry.editable_var.get():
                editable_count += 1
                file_label = ttk.Label(scrollable_frame, text=os.path.basename(entry.path))
                file_label.pack(anchor="w", padx=5, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Status
        if editable_count == 0:
            status_text = "No files selected for editing"
            status_label = ttk.Label(frame, text=status_text, foreground="red")
        else:
            status_text = f"{editable_count} file(s) will be converted"
            status_label = ttk.Label(frame, text=status_text, foreground="green")
        
        status_label.pack(pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x")
        
        close_button = ttk.Button(button_frame, text="Close", command=self._on_close)
        close_button.pack(side="right")
        
        # Store button reference for external access
        self.close_button = close_button

    def _on_close(self):
        """Close dialog"""
        self._save_geometry()
        self.destroy()
