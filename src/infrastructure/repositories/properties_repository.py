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

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                self.data.update(loaded)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                logger.error(f"File content: {open(self.file_path, 'r', encoding='utf-8').read()}")
            except Exception as e:
                logger.error(f"Error loading properties: {e}")
                import traceback
                traceback.print_exc()

    def _clean(self):
        # Korrigiert nur Typen, entfernt aber keine benutzerdefinierten Keys
        DEFAULT_SCHEMA = {
            "session_files": dict,
# "dialog_geometry": dict,  # OBSOLETE - use dialogs.geometry
# "log_level": str,  # OBSOLETE - use dialogs.settings.logging.level
# "log_file": str,  # OBSOLETE - use dialogs.settings.logging.file
# "log_display_lines": int,  # OBSOLETE - use dialogs.settings.logging.display_lines
# "marker_enabled": bool,  # OBSOLETE - no longer used
            "marker_step": int,
            "downsample_step": int,
# "main_window_geometry": str  # OBSOLETE - use app.main_window.geometry
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
        """Get property value, supporting dot notation for nested keys"""
        if '.' in key:
            keys = key.split('.')
            current = self.data
            for k in keys:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    return default
            return current
        else:
            return self.data.get(key, default)

    def set(self, key, value):
        """Set property value, supporting dot notation for nested keys"""
        if '.' in key:
            keys = key.split('.')
            current = self.data
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            current[keys[-1]] = value
        else:
            self.data[key] = value
        self.save()

    # -------------------------------------------------------------

    def get_dialog_geometry(self, dialog_name):
        """Get dialog geometry from structured path"""
        return self.get(f"dialogs.geometry.{dialog_name}")

    def set_dialog_geometry(self, dialog_name, geometry):
        """Set dialog geometry to structured path without immediate save"""
        key = f"dialogs.geometry.{dialog_name}"
        if '.' in key:
            keys = key.split('.')
            current = self.data
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            current[keys[-1]] = geometry
        else:
            self.data[key] = geometry
        # Don't call save() here for dialog geometry to avoid loops
    
    def save_dialog_geometries(self):
        """Save all dialog geometries to file"""
        self.save()

    # -------------------------------------------------------------

    def get_or_create_file_reference(self, file_path):
        """Get existing reference number or create new one for file path"""
        session_files = self.get("files.session") or self.data.get("session_files", {})
        
        # Look for existing reference
        for ref_num, file_data in session_files.items():
            if file_data.get("path") == file_path:
                return int(ref_num)
        
        # Create new reference - always start from 1
        new_ref = 1
        while str(new_ref) in session_files:
            new_ref += 1
        session_files[str(new_ref)] = {"path": file_path, "settings": {}}
        self.set("files.session", session_files)
        return new_ref
    
    def get_file_settings_by_reference(self, ref_num):
        """Get file settings by reference number"""
        session_files = self.get("files.session") or self.data.get("session_files", {})
        file_data = session_files.get(str(ref_num))
        return file_data.get("settings") if file_data else None
    
    def save_file_settings_by_reference(self, ref_num, settings):
        """Save file settings by reference number"""
        session_files = self.get("files.session") or self.data.get("session_files", {})
        ref_str = str(ref_num)
        
        if ref_str not in session_files:
            session_files[ref_str] = {"path": "", "settings": {}}
        
        session_files[ref_str]["settings"] = settings
        self.set("files.session", session_files)

    # -------------------------------------------------------------

    def get_file_path_by_reference(self, ref_num):
        """Get file path by reference number"""
        session_files = self.data.get("session_files", {})
        file_data = session_files.get(str(ref_num))
        return file_data.get("path") if file_data else None

    # -------------------------------------------------------------

    def get_main_window_geometry(self):
        return self.data.get("main_window_geometry")

    def set_main_window_geometry(self, geometry):
        self.data["main_window_geometry"] = geometry
        self.save()

    def remove_file_from_session(self, ref_num):
        """Remove file from session files"""
        ref_str = str(ref_num)
        
        # Try both old and new paths for compatibility
        session_files_old = self.data.get("session_files", {})
        session_files_new = self.data.get("files", {}).get("session", {})
        
        removed = False
        
        # Check old path first
        if ref_str in session_files_old:
            del session_files_old[ref_str]
            self.data["session_files"] = session_files_old
            removed = True
            logger.debug(f"Removed file reference {ref_num} from session_files (old path)")
        
        # Check new path
        elif ref_str in session_files_new:
            del session_files_new[ref_str]
            self.data["files"]["session"] = session_files_new
            removed = True
            logger.debug(f"Removed file reference {ref_num} from files.session (new path)")
        
        if removed:
            self.save()
            logger.debug(f"File reference {ref_num} removed successfully")
        else:
            logger.warning(f"File reference {ref_num} not found in any session path")
