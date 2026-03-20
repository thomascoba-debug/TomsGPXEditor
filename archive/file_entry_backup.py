import tkinter as tk
from tkinter import ttk, colorchooser
import os
from debug_decorator import log_all_methods


@log_all_methods

class FileEntry(ttk.Frame):

    def __init__(self, parent, path, properties, change_callback):

        super().__init__(parent)

        self.path = path
        self.properties = properties
        self.change_callback = change_callback

        self.visible_var = tk.BooleanVar(value=True)
        self.editable_var = tk.BooleanVar(value=False)

        self.color = self._load_color()

        self._build()

    # ---------------------------------------------------------

    def _load_color(self):
        gpx_files = self.properties.get("gpx_files", {})
        # Reparatur: Falls gpx_files kein Dict ist, zurücksetzen
        if not isinstance(gpx_files, dict):
            gpx_files = {}
            self.properties.set("gpx_files", gpx_files)
            self.properties.save()
        entry = gpx_files.get(self.path, None)
        if isinstance(entry, dict):
            return entry.get("color", "#ff0000")
        elif isinstance(entry, str):
            # Automatisch reparieren und speichern
            new_entry = {"color": entry}
            gpx_files[self.path] = new_entry
            self.properties.set("gpx_files", gpx_files)
            self.properties.save()
            return new_entry["color"]
        return "#ff0000"

    # ---------------------------------------------------------

    def _save_color(self):
        gpx_files = self.properties.get("gpx_files", {})
        # Reparatur: Falls gpx_files kein Dict ist, zurücksetzen
        if not isinstance(gpx_files, dict):
            gpx_files = {}
        if self.path not in gpx_files or not isinstance(gpx_files[self.path], dict):
            gpx_files[self.path] = {}
        gpx_files[self.path]["color"] = self.color

        self.properties.set("gpx_files", gpx_files)
        self.properties.save()

    # ---------------------------------------------------------

    def _build(self):

        ttk.Checkbutton(
            self,
            variable=self.visible_var,
            command=self._changed
        ).grid(row=0, column=0, padx=3)

        ttk.Checkbutton(
            self,
            variable=self.editable_var,
            command=self._changed
        ).grid(row=0, column=1, padx=3)

        self.color_btn = tk.Button(
            self,
            bg=self.color,
            width=3,
            command=self._choose_color
        )

        self.color_btn.grid(row=0, column=2, padx=3)

        ttk.Label(
            self,
            text=os.path.basename(self.path)
        ).grid(row=0, column=3, sticky="w")

    # ---------------------------------------------------------

    def _choose_color(self):

        color = colorchooser.askcolor(self.color)[1]

        if color:

            self.color = color
            self.color_btn.configure(bg=color)

            self._save_color()

            self._changed()

    # ---------------------------------------------------------

    def _changed(self):

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


# Import at the end to avoid circular imports
try:
    from edit_controller import analyze_gpx_file
except ImportError:
    # Fallback if edit_controller is not available
    def analyze_gpx_file(path):
        return {'file_type': 'unknown', 'has_tracks': False, 'has_routes': False}