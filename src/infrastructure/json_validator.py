
#!/usr/bin/env python3
"""
JSON Validator and Sanitizer for Properties
"""


import json
import logging
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)

class JSONValidator:
    """Validates and sanitizes JSON properties"""
    
    def __init__(self, json_file: str):
        self.json_file = Path(json_file)
        self.data = {}
        self.errors = []
        self.warnings = []
    
    def load_and_validate(self) -> Dict[str, Any]:
        """Load and validate JSON file"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            self._validate_structure()
            self._sanitize_data()
            
            return self.data
            
        except Exception as e:
            logger.error(f"Failed to load JSON: {e}")
            raise
    
    def _validate_structure(self):
        """Validate JSON structure"""
        self.errors.clear()
        self.warnings.clear()
        
        # Check for known problematic patterns
        self._check_duplicate_keys()
        self._check_invalid_types()
        self._check_legacy_entries()
    
    def _check_duplicate_keys(self):
        """Check for duplicate or conflicting keys"""
        recent_files_keys = []
        
        def find_recent_keys(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    if "recent" in key.lower():
                        recent_files_keys.append(current_path)
                    
                    find_recent_keys(value, current_path)
        
        find_recent_keys(self.data)
        
        # Check for duplicates
        if len(recent_files_keys) > 1:
            self.warnings.append(f"Multiple recent files keys found: {recent_files_keys}")
    
    def _check_invalid_types(self):
        """Check for invalid data types"""
        def check_types(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Check for mixed types
                    if key in ["recent_files", "files.session"]:
                        if not isinstance(value, (dict, list)):
                            self.errors.append(f"Invalid type for {current_path}: expected dict or list, got {type(value)}")
                    
                    check_types(value, current_path)
        
        check_types(self.data)
    
    def _check_legacy_entries(self):
        """Check for legacy entries that should be cleaned up"""
        legacy_patterns = [
            "recent_files.with_timestamps",
            ["TRACK_TO_ROUTE"]  # flat version
        ]
        
        def find_legacy(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    if key in legacy_patterns:
                        self.warnings.append(f"Legacy entry found: {current_path}")
                    
                    find_legacy(value, current_path)
        
        find_legacy(self.data)
    
    def _sanitize_data(self):
        """Sanitize data by removing problematic entries"""
        if not self.warnings and not self.errors:
            return
        
        # Remove flat track_to_route_points_per_100km if structured exists
        if ["TRACK_TO_ROUTE"] in self.data:
            if "app" in self.data and "settings" in self.data["app"]:
                if "conversion" in self.data["app"]["settings"]:
                    if ["ROUTE_TO_TRACK"] in self.data["app"]["settings"]["conversion"]:
                        if "points_per_100km" in self.data["app"]["settings"]["conversion"][["ROUTE_TO_TRACK"]]:
                            del self.data[["TRACK_TO_ROUTE"]]
                            logger.info("Removed flat track_to_route_points_per_100km (structured version exists)")
        
        # Consolidate recent files entries
        self._consolidate_recent_files()
        
        # Clean up duplicate downsample settings
        self._cleanup_duplicate_downsample_settings()
    
    def _consolidate_recent_files(self):
        """Consolidate recent files to single source"""
        recent_sources = []
        
        # Find all recent files sources
        def find_recent_sources(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    if "recent" in key.lower() and isinstance(value, (dict, list)):
                        recent_sources.append((current_path, value))
                    
                    find_recent_sources(value, current_path)
        
        find_recent_sources(self.data)
        
        if len(recent_sources) > 1:
            # Keep only the structured version
            structured_path = APP_RECENT_FILES
            structured_data = None
            
            for path, data in recent_sources:
                if path == structured_path:
                    structured_data = data
                else:
                    # Remove other recent files entries
                    keys = path.split('.')
                    current = self.data
                    for key in keys[:-1]:
                        if key in current:
                            current = current[key]
                        else:
                            break
                    else:
                        if keys[-1] in current:
                            del current[keys[-1]]
                            logger.info(f"Removed duplicate recent files entry: {path}")
            
            if structured_data:
                # Ensure structured path exists
                if "app" not in self.data:
                    self.data["app"] = {}
                if "recent_files_timestamps" not in self.data["app"]:
                    self.data["app"]["recent_files_timestamps"] = structured_data
    
    def save_sanitized(self):
        """Save sanitized data back to file"""
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved sanitized JSON to {self.json_file}")
            
        except Exception as e:
            logger.error(f"Failed to save sanitized JSON: {e}")
            raise
    
    def get_report(self) -> str:
        """Get validation report"""
        report = []
        
        if self.errors:
            report.append(f"ERRORS ({len(self.errors)}):")
            for error in self.errors:
                report.append(f"  - {error}")
        
        if self.warnings:
            report.append(f"WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                report.append(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            report.append("✅ JSON structure is clean and valid")
        
        return "\n".join(report)

def validate_and_sanitize_properties(json_file: str) -> bool:
    """Validate and sanitize properties file"""
    validator = JSONValidator(json_file)
    
    try:
        validator.load_and_validate()
        
        # Print report
        report = validator.get_report()
        print("=== JSON Validation Report ===")
        print(report)
        
        # Save if there were issues
        if validator.errors or validator.warnings:
            validator.save_sanitized()
            print(f"\n✅ Sanitized JSON saved to {json_file}")
            return True
        else:
            print("\n✅ No issues found in JSON")
            return False
            
    except Exception as e:
        print(f"❌ Failed to validate JSON: {e}")
        return False

    def _cleanup_duplicate_downsample_settings(self):
        """Clean up duplicate flat downsample settings when structured versions exist"""
        flat_keys = [
            "downsample_points_per_100km",
            "downsample_keep_waypoints", 
            "downsample_overwrite_original"
        ]
        
        # Check if structured downsample settings exist
        structured_path = "dialogs.settings.conversion.downsample"
        if structured_path in self.data and isinstance(self.data[structured_path], dict):
            structured_settings = self.data[structured_path]
            
            # Remove flat keys if structured versions exist
            for flat_key in flat_keys:
                if flat_key in self.data:
                    structured_key = flat_key.replace("downsample_", "")
                    if structured_key in structured_settings:
                        del self.data[flat_key]
                        logger.info(f"Removed duplicate flat key '{flat_key}' (structured version exists)")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        validate_and_sanitize_properties(json_file)
    else:
        print("Usage: python json_validator.py <json_file>")
