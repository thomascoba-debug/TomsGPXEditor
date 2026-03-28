import tkinter as tk
from tkinter import ttk, colorchooser
import os
import logging

# Get logger for this module
logger = logging.getLogger(__name__)


# Import at the end to avoid circular imports
try:
    from src.application.services.gpx_service import analyze_gpx_file
except ImportError:
    # Fallback if gpx_service is not available
    def analyze_gpx_file(path):
        return {'file_type': 'unknown', 'has_tracks': False, 'has_routes': False}


class FileEntry(ttk.Frame):

    def __init__(self, parent, path, properties, change_callback):

        super().__init__(parent)

        self.path = path
        self.properties = properties
        self.change_callback = change_callback

        self.visible_var = tk.BooleanVar(value=True)
        self.editable_var = tk.BooleanVar(value=False)

        # Get or create file reference
        self.file_ref = self.properties.get_or_create_file_reference(path)
        
        # Load checkbox states from settings
        self._load_checkbox_states()
        
        self.color = self._load_color()
        
        # Analyze GPX file type
        self.file_analysis = analyze_gpx_file(self.path)

        self._build()
        self._create_tooltip()

    # ---------------------------------------------------------

    def _load_color(self):
        # Use integrated file settings only
        settings = self.properties.get_file_settings_by_reference(self.file_ref)
        
        if isinstance(settings, dict) and "color" in settings:
            return settings.get("color", "#ff0000")
        
        return "#ff0000"

    def _load_checkbox_states(self):
        """Load visible and editable states from settings"""
        settings = self.properties.get_file_settings_by_reference(self.file_ref)
        
        # Handle None or empty settings
        if not isinstance(settings, dict):
            settings = {}
        
        visible = settings.get("visible", True)
        editable = settings.get("editable", False)
        
        self.visible_var.set(visible)
        self.editable_var.set(editable)
        
        logger.debug(f"Loaded checkbox states for {self.path}: visible={visible}, editable={editable}")

    def _save_checkbox_states(self):
        """Save visible and editable states to settings"""
        settings = self.properties.get_file_settings_by_reference(self.file_ref)
        
        if not isinstance(settings, dict):
            settings = {}
        
        settings["visible"] = self.visible_var.get()
        settings["editable"] = self.editable_var.get()
        
        self.properties.save_file_settings_by_reference(self.file_ref, settings)
        
        logger.debug(f"Saved checkbox states for {self.path}: visible={settings['visible']}, editable={settings['editable']}")

    # ---------------------------------------------------------

    def _save_color(self):
        # Use integrated file settings only
        settings = self.properties.get_file_settings_by_reference(self.file_ref)
        settings["color"] = self.color
        self.properties.save_file_settings_by_reference(self.file_ref, settings)

    # ---------------------------------------------------------

    def _build(self):

        # Visible checkbox (V) - Column 0
        self.visible_cb = ttk.Checkbutton(
            self,
            variable=self.visible_var,
            command=self._changed,
            width=2
        )

        # Editable checkbox (E) - Column 1
        self.editable_cb = ttk.Checkbutton(
            self,
            variable=self.editable_var,
            command=self._changed,
            width=2
        )

        # Reference number (Nr) - Column 2
        self.ref_label = ttk.Label(
            self,
            text=f"[{self.file_ref}]",
            foreground="blue",
            font=("TkDefaultFont", 7),
            width=4
        )

        # Color button - Column 3
        self.color_btn = tk.Button(
            self,
            bg=self.color,
            width=3,
            command=self._choose_color
        )

        # Filename - Column 4
        self.filename_label = ttk.Label(
            self,
            text=os.path.basename(self.path)
        )
        
        # Add file type indicator
        file_type_text = self.file_analysis.get('file_type', 'unknown').upper()
        if self.file_analysis.get('file_type') == 'mixed':
            file_type_text = f"T+R ({self.file_analysis['track_count']},{self.file_analysis['route_count']})"
        elif self.file_analysis.get('file_type') == 'track':
            file_type_text = f"T ({self.file_analysis['track_count']})"
        elif self.file_analysis.get('file_type') == 'route':
            file_type_text = f"R ({self.file_analysis['route_count']})"
        
        self.filetype_label = ttk.Label(
            self,
            text=file_type_text,
            foreground="gray",
            font=("TkDefaultFont", 8)
        )
    
    def place_in_grid(self, parent, row):
        """Place this entry in the parent grid at specified row"""
        # Reparent widgets to main grid
        self.visible_cb.master = parent
        self.editable_cb.master = parent
        self.ref_label.master = parent
        self.color_btn.master = parent
        self.filename_label.master = parent
        self.filetype_label.master = parent
        
        # Place in grid
        self.visible_cb.grid(row=row, column=0, padx=3)
        self.editable_cb.grid(row=row, column=1, padx=3)
        self.ref_label.grid(row=row, column=2, padx=3)
        self.color_btn.grid(row=row, column=3, padx=3)
        self.filename_label.grid(row=row, column=4, sticky="w", padx=3)
        self.filetype_label.grid(row=row, column=5, sticky="w", padx=(5, 0))

    # ---------------------------------------------------------

    def _choose_color(self):
        """Öffne den Farbwahl-Dialog"""
        try:
            logger.debug(f"_choose_color called, current color: {self.color}")
            color = colorchooser.askcolor(self.color)[1]
            logger.debug(f"colorchooser result: {color}")
            
            if color:
                logger.debug(f"Setting color to: {color}")
                self.color = color
                self.color_btn.configure(bg=color)
                self._save_color()
                self._changed()
                logger.debug("Color changed successfully")
            else:
                logger.debug("Color chooser cancelled")
        except Exception as e:
            logger.error(f"_choose_color failed: {e}")
            import traceback
            traceback.print_exc()

    # ---------------------------------------------------------

    def _changed(self):
        """Handle checkbox changes"""
        # Save checkbox states
        self._save_checkbox_states()
        
        # Call change callback to update map and conversion buttons
        if self.change_callback:
            self.change_callback()

    # ---------------------------------------------------------

    def is_visible(self):
        return self.visible_var.get()

    def is_editable(self):
        return self.editable_var.get()

    def get_color(self):
        return self.color

    def get_path(self):
        return self.path
    
    def get_file_analysis(self):
        return self.file_analysis
    
    def get_file_reference(self):
        return self.file_ref
    
    def _create_tooltip(self):
        """Create tooltip for filename showing full path"""
        try:
            # Find the filename label
            filename_label = None
            for child in self.winfo_children():
                if isinstance(child, ttk.Label):
                    text = child.cget("text")
                    if text == os.path.basename(self.path):
                        filename_label = child
                        logger.debug(f"Found filename label: {text}")
                        break
            
            if filename_label:
                # Simple tooltip implementation
                self.tooltip = None
                
                def show_tooltip():
                    if not self.tooltip:
                        # Check if mouse is actually over this widget
                        try:
                            x, y = filename_label.winfo_pointerxy()
                            widget_x = filename_label.winfo_rootx()
                            widget_y = filename_label.winfo_rooty()
                            widget_width = filename_label.winfo_width()
                            widget_height = filename_label.winfo_height()
                            
                            # Only show tooltip if mouse is within widget bounds
                            if (widget_x <= x <= widget_x + widget_width and 
                                widget_y <= y <= widget_y + widget_height):
                                
                                self.tooltip = tk.Toplevel()
                                self.tooltip.wm_overrideredirect(True)
                                self.tooltip.wm_geometry(f"+{filename_label.winfo_rootx()+10}+{filename_label.winfo_rooty()+10}")
                                
                                # Create tooltip label
                                label = tk.Label(
                                    self.tooltip,
                                    text=self.path,
                                    background="lightyellow",
                                    relief="solid",
                                    borderwidth=1,
                                    font=("TkDefaultFont", 9),
                                    padx=8,
                                    pady=4
                                )
                                label.pack()
                                
                                logger.debug(f"Tooltip shown for: {self.path}")
                                
                        except Exception as e:
                            logger.debug(f"Error checking mouse position: {str(e)}")
                            # Fallback - show tooltip anyway
                            self.tooltip = tk.Toplevel()
                            self.tooltip.wm_overrideredirect(True)
                            self.tooltip.wm_geometry(f"+{filename_label.winfo_rootx()+10}+{filename_label.winfo_rooty()+10}")
                            
                            label = tk.Label(
                                self.tooltip,
                                text=self.path,
                                background="lightyellow",
                                relief="solid",
                                borderwidth=1,
                                font=("TkDefaultFont", 9),
                                padx=8,
                                pady=4
                            )
                            label.pack()
                            
                            logger.debug(f"Tooltip shown (fallback) for: {self.path}")
                
                def hide_tooltip():
                    if self.tooltip:
                        self.tooltip.destroy()
                        self.tooltip = None
                        logger.debug("Tooltip hidden")
                
                def on_enter(event):
                    # Show tooltip after short delay
                    filename_label.after(500, show_tooltip)
                
                def on_leave(event):
                    # Hide tooltip immediately
                    hide_tooltip()
                    # Cancel any pending show_tooltip
                    filename_label.after_cancel(show_tooltip)
                
                # Bind events
                filename_label.bind("<Enter>", on_enter)
                filename_label.bind("<Leave>", on_leave)
                logger.debug("Tooltip events bound successfully")
            else:
                logger.warning(f"Could not find filename label for: {os.path.basename(self.path)}")
                
        except Exception as e:
            logger.error(f"Failed to create tooltip: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
