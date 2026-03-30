import tkinter as tk
from tkinter import ttk
from src.ui.base import PersistentDialog
from src.i18n import t
from src.ui.utils.dialog_utils import create_tooltip

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
        track_frame = ttk.LabelFrame(frame, text=t("dialogs.rendering.track_line"))
        track_frame.grid(row=0, column=0, sticky="ew", pady=5)
        track_frame.columnconfigure(1, weight=1)
        
        ttk.Checkbutton(track_frame, text=t("dialogs.rendering.enabled"), variable=self.track_line_enabled).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Label(track_frame, text=t("dialogs.rendering.line_width")).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Spinbox(track_frame, from_=1, to=10, textvariable=self.track_line_width, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=2)

        # Route Line Settings
        route_frame = ttk.LabelFrame(frame, text=t("dialogs.rendering.route_line"))
        route_frame.grid(row=1, column=0, sticky="ew", pady=5)
        route_frame.columnconfigure(1, weight=1)
        
        ttk.Checkbutton(route_frame, text=t("dialogs.rendering.enabled"), variable=self.route_line_enabled).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Label(route_frame, text=t("dialogs.rendering.line_width")).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Spinbox(route_frame, from_=1, to=10, textvariable=self.route_line_width, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=2)

        # Downsampling Settings
        downsample_frame = ttk.LabelFrame(frame, text=t("dialogs.rendering.downsampling.title"))
        downsample_frame.grid(row=2, column=0, sticky="ew", pady=5)
        downsample_frame.columnconfigure(1, weight=1)
        
        # Get downsampling settings from properties
        rendering_settings = self.properties.get("dialogs.settings.rendering", {})
        downsampling_settings = rendering_settings.get('downsampling', {})
        
        self.downsampling_enabled = tk.BooleanVar(value=downsampling_settings.get('enabled', True))
        self.downsample_step = tk.IntVar(value=downsampling_settings.get('step', 1))
        
        # Downsampling enabled checkbox with tooltip
        downsample_check = ttk.Checkbutton(downsample_frame, text=t("dialogs.rendering.downsampling.enabled"), 
                       variable=self.downsampling_enabled)
        downsample_check.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        create_tooltip(downsample_check, t("dialogs.rendering.downsampling.enabled_tooltip"))
        
        # Downsample step with tooltip
        ttk.Label(downsample_frame, text=t("dialogs.rendering.downsampling.step")).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        downsample_step_spinbox = ttk.Spinbox(downsample_frame, from_=1, to=10, textvariable=self.downsample_step, width=10)
        downsample_step_spinbox.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        create_tooltip(downsample_step_spinbox, t("dialogs.rendering.downsampling.step_tooltip"))

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, pady=10)

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
            
            # Update downsampling settings
            if "downsampling" not in rendering_settings:
                rendering_settings["downsampling"] = {}
            rendering_settings["downsampling"]["enabled"] = self.downsampling_enabled.get()
            rendering_settings["downsampling"]["step"] = self.downsample_step.get()
            
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

        ttk.Button(button_frame, text=t("buttons.ok"), command=ok).pack(side="left", padx=5)
        ttk.Button(button_frame, text=t("buttons.cancel"), command=cancel).pack(side="left", padx=5)
