"""
Properties Repository - Core properties data access
"""
import json
import os
from ..validators.properties_validator import PropertiesValidator

class PropertiesRepository:
    """Core properties data access"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        self.load()
    
    def load(self):
        """Load properties from file"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                
                # Validate loaded data
                is_valid, message = PropertiesValidator.validate_properties(self.data)
                if not is_valid:
                    raise ValueError(f"Invalid properties: {message}")
            else:
                # Create default structure
                self.data = self._get_default_schema()
        except Exception as e:
            raise ValueError(f"Failed to load properties: {str(e)}")
    
    def save(self):
        """Save properties to file"""
        try:
            # Validate before saving
            is_valid, message = PropertiesValidator.validate_properties(self.data)
            if not is_valid:
                raise ValueError(f"Invalid properties: {message}")
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Failed to save properties: {str(e)}")
    
    def get(self, key_path, default=None):
        """Get property value by key path"""
        keys = key_path.split('.')
        value = self.data
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path, value):
        """Set property value by key path"""
        keys = key_path.split('.')
        current = self.data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def _get_default_schema(self):
        """Get default properties schema"""
        return {
            "files": {
                "session": {}
            },
            "dialogs": {
                "settings": {
                    "logging": {"level": "INFO"},
                    "rendering": {"line_width": 3},
                    "marker": {"enabled": True}
                }
            },
            "app": {
                "main_window": {"geometry": "800x600+100+100"},
                "recent_files": {}
            }
        }
