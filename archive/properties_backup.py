import json
import os
import logging

# Configure logger
logger = logging.getLogger(__name__)

class AppProperties:
    def __init__(self, file_path="properties.json"):
        self.file_path = file_path
        self.data = {}
        self.load()
        self._clean()

    def _clean(self):
        # Korrigiert nur Typen, entfernt aber keine benutzerdefinierten Keys
        DEFAULT_SCHEMA = {
            "session_files": dict,
            "dialog_geometry": dict,
            "log_level": str,
            "log_file": str,
            "marker_enabled": bool,
            "marker_step": int,
            "marker_icon_size": list,
            "marker_icon_path": str,
            "zoom_scaling_enabled": bool,
            "downsample_step": int,
            "main_window_geometry": str
        }
        
        for key in list(self.data.keys()):
            if key in DEFAULT_SCHEMA:
                typ = DEFAULT_SCHEMA[key]
                value = self.data[key]
                
                # Typkorrektur wie bisher, aber nur wenn wirklich nötig
                if typ == dict and not isinstance(value, dict):
                    self.data[key] = {}
                elif typ == list and not isinstance(value, list):
                    self.data[key] = []
                elif typ == bool and not isinstance(value, bool):
                    self.data[key] = False
                elif typ == int and not isinstance(value, int):
                    self.data[key] = 0
                elif typ == str and not isinstance(value, str):
                    self.data[key] = ""
        
        self.save()

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        # Remove debug logging to avoid log-level dependency
        result = self.data.get(key, default)
        return result

    def set(self, key, value):
        self.data[key] = value

    # -------------------------------------------------------------

    def get_dialog_geometry(self, dialog_name):

        geo = self.data.get("dialog_geometry", {})
        return geo.get(dialog_name)

    def set_dialog_geometry(self, dialog_name, geometry):

        geo = self.data.get("dialog_geometry", {})
        geo[dialog_name] = geometry
        self.data["dialog_geometry"] = geo
        self.save()

    # -------------------------------------------------------------

    def get_or_create_file_reference(self, file_path):
        """Get existing reference number or create new one for file path"""
        session_files = self.data.get("session_files", {})
        file_data = session_files.get(str(ref_num))
        return file_data.get("path") if file_data else None
    
    def get_file_settings_by_reference(self, ref_num):
        """Get file settings by reference number"""
        session_files = self.data.get("session_files", {})
        file_data = session_files.get(str(ref_num))
        return file_data.get("settings") if file_data else None
    
    def save_file_settings_by_reference(self, ref_num, settings):
        """Save file settings by reference number"""
        session_files = self.data.get("session_files", {})
        ref_str = str(ref_num)
        
        if ref_str not in session_files:
            session_files[ref_str] = {"path": "", "settings": {}}
        
        session_files[ref_str]["settings"] = settings
        self.data["session_files"] = session_files
        self.save()

    # -------------------------------------------------------------

    def get_file_path_by_reference(self, ref_num):
        """Get file path by reference number"""
        session_files = self.data.get("session_files", {})
        file_data = session_files.get(str(ref_num))
        return file_data.get("path") if file_data else None
    
    def get_file_settings_by_reference(self, ref_num):
        """Get file settings by reference number"""
        session_files = self.data.get("session_files", {})
        file_data = session_files.get(str(ref_num))
        return file_data.get("settings") if file_data else None

    def save_file_settings_by_reference(self, ref_num, settings):
        """Save file settings by reference number"""
        session_files = self.data.get("session_files", {})
        ref_str = str(ref_num)
        
        if ref_str not in session_files:
            session_files[ref_str] = {"path": "", "settings": {}}
        
        session_files[ref_str]["settings"] = settings
        self.data["session_files"] = session_files
        self.save()

    # -------------------------------------------------------------

    def get_main_window_geometry(self):
        return self.data.get("main_window_geometry")

    def set_main_window_geometry(self, geometry):
        self.data["main_window_geometry"] = geometry
        self.save()
