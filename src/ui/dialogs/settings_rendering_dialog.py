import tkinter as tk
from tkinter import ttk
from src.ui.base import PersistentDialog

# Get logger for this module
import logging
logger = logging.getLogger(__name__)


class RenderingSettingsDialog(PersistentDialog):

    def __init__(self, parent, properties, save_callback):
        super().__init__(parent, properties, "RenderingSettingsDialog")
        
        self.title("Rendering Settings")
        self.properties = properties
        self.save_callback = save_callback

        # Linien-Dicke für Tracks
        self.track_line_enabled = tk.BooleanVar(value=properties.get("track_line_enabled", True))
        self.track_line_width = tk.IntVar(value=properties.get("track_line_width", 2))
        
        # Linien-Dicke für Routes
        self.route_line_enabled = tk.BooleanVar(value=properties.get("route_line_enabled", True))
        self.route_line_width = tk.IntVar(value=properties.get("route_line_width", 2))

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Track Linien-Dicke Sektion
        track_frame = ttk.LabelFrame(frame, text="Track Lines")
        track_frame.grid(row=0, column=0, sticky="ew", pady=5)
        track_frame.columnconfigure(1, weight=1)
        
        ttk.Checkbutton(track_frame, text="Enabled", variable=self.track_line_enabled).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Label(track_frame, text="Line Width:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        track_entry = ttk.Entry(track_frame, textvariable=self.track_line_width, width=10)
        track_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        track_slider = ttk.Scale(track_frame, from_=1, to=10, orient=tk.HORIZONTAL, 
                               variable=self.track_line_width, length=200,
                               command=lambda value: self.track_line_width.set(int(float(value))))
        track_slider.grid(row=1, column=2, sticky="w", padx=5, pady=2)

        # Route Linien-Dicke Sektion
        route_frame = ttk.LabelFrame(frame, text="Route Lines")
        route_frame.grid(row=1, column=0, sticky="ew", pady=5)
        route_frame.columnconfigure(1, weight=1)
        
        ttk.Checkbutton(route_frame, text="Enabled", variable=self.route_line_enabled).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Label(route_frame, text="Line Width:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        route_entry = ttk.Entry(route_frame, textvariable=self.route_line_width, width=10)
        route_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        route_slider = ttk.Scale(route_frame, from_=1, to=10, orient=tk.HORIZONTAL, 
                               variable=self.route_line_width, length=200,
                               command=lambda value: self.route_line_width.set(int(float(value))))
        route_slider.grid(row=1, column=2, sticky="w", padx=5, pady=2)

        # Explanation
        explanation_frame = ttk.Frame(frame)
        explanation_frame.grid(row=2, column=0, sticky="ew", pady=10)
        
        explanation_text = """Configure line width for tracks and routes.

Track Lines: Connect track points with lines
Route Lines: Connect route points with lines

Line Width: Thickness of the connecting lines (1-10 pixels)
Higher values = thicker lines, lower values = thinner lines"""
        
        explanation_label = ttk.Label(explanation_frame, text=explanation_text, 
                                 font=("TkDefaultFont", 9), foreground="gray", justify="left")
        explanation_label.pack(fill="both", expand=True)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, pady=10)

        def ok():
            """Save settings and close dialog"""
            properties.set("track_line_enabled", self.track_line_enabled.get())
            properties.set("track_line_width", self.track_line_width.get())
            properties.set("route_line_enabled", self.route_line_enabled.get())
            properties.set("route_line_width", self.route_line_width.get())
            
            # Properties explizit speichern
            properties.save()
            
            # Map Renderer über Properties-Update informieren
            if save_callback:
                save_callback()
            
            self._on_close()

        def cancel():
            """Close dialog without saving"""
            self._on_close()

        ttk.Button(button_frame, text="OK", command=ok).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side="left", padx=5)
