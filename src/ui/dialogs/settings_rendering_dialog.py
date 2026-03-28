import tkinter as tk
from tkinter import ttk
from src.ui.base import PersistentDialog

# Get logger for this module
import logging
logger = logging.getLogger(__name__)


class RenderingSettingsDialog(PersistentDialog):

    def __init__(self, parent, properties, save_callback, modal=False):
        super().__init__(parent, properties, "RenderingSettingsDialog", modal=modal)
        
        self.title("Rendering Settings")
        self.properties = properties
        self.save_callback = save_callback

        # Get rendering settings from new structured path
        rendering_settings = self.properties.get("dialogs.settings.rendering", {})
        
        # Track line settings
        track_line = rendering_settings.get("track_line", {})
        self.track_line_enabled = tk.BooleanVar(value=track_line.get("enabled", True))
        self.track_line_width = tk.IntVar(value=track_line.get("width", 5))
        
        # Route line settings
        route_line = rendering_settings.get("route_line", {})
        self.route_line_enabled = tk.BooleanVar(value=route_line.get("enabled", True))
        self.route_line_width = tk.IntVar(value=route_line.get("width", 4))

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Track Line Settings
        track_frame = ttk.LabelFrame(frame, text="Track Line Settings")
        track_frame.grid(row=0, column=0, sticky="ew", pady=5)
        track_frame.columnconfigure(1, weight=1)
        
        ttk.Checkbutton(track_frame, text="Enabled", variable=self.track_line_enabled).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Label(track_frame, text="Line Width:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Spinbox(track_frame, from_=1, to=10, textvariable=self.track_line_width, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=2)

        # Route Line Settings
        route_frame = ttk.LabelFrame(frame, text="Route Line Settings")
        route_frame.grid(row=1, column=0, sticky="ew", pady=5)
        route_frame.columnconfigure(1, weight=1)
        
        ttk.Checkbutton(route_frame, text="Enabled", variable=self.route_line_enabled).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Label(route_frame, text="Line Width:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Spinbox(route_frame, from_=1, to=10, textvariable=self.route_line_width, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=2)

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, pady=10)

        def ok():
            """Save settings and close dialog"""
            # Get current rendering settings
            rendering_settings = self.properties.get("dialogs.settings.rendering", {})
            
            # Update track line settings
            if "track_line" not in rendering_settings:
                rendering_settings["track_line"] = {}
            rendering_settings["track_line"]["enabled"] = self.track_line_enabled.get()
            rendering_settings["track_line"]["width"] = self.track_line_width.get()
            
            # Update route line settings
            if "route_line" not in rendering_settings:
                rendering_settings["route_line"] = {}
            rendering_settings["route_line"]["enabled"] = self.route_line_enabled.get()
            rendering_settings["route_line"]["width"] = self.route_line_width.get()
            
            # Save structured settings
            self.properties.set("dialogs.settings.rendering", rendering_settings)
            self.properties.save()
            
            # Map Renderer über Properties-Update informieren
            if save_callback:
                save_callback()
            
            self._on_close()

        def cancel():
            """Close dialog without saving"""
            self._on_close()

        ttk.Button(button_frame, text="OK", command=ok).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel).pack(side="left", padx=5)
