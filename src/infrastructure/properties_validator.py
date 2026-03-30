#!/usr/bin/env python3
"""
Properties Validator - Prevents duplicate entries automatically
"""

import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

class PropertiesValidator:
    """Validates and cleans properties.json automatically"""
    
    DUPLICATE_PATTERNS = {
        'recent_files': ['app.recent_files', 'app.recent_files_timestamps'],
        'conversion': ['conversion', 'dialogs.settings.conversion'],
        'logging_flat': ['file', 'display_lines', 'dialogs.settings.logging.level', 'dialogs.settings.logging.file']
    }
    
    @staticmethod
    def validate_and_clean(properties_data: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """
        Validate properties and remove duplicates automatically
        
        Returns:
            Tuple[cleaned_data, was_changed]
        """
        changed = False
        cleaned_data = properties_data.copy()
        
        # Check for duplicate recent_files
        if PropertiesValidator._has_duplicate_recent_files(cleaned_data):
            cleaned_data = PropertiesValidator._fix_recent_files(cleaned_data)
            changed = True
            logger.warning("Auto-fixed duplicate recent_files entries")
        
        # Check for duplicate conversion
        if PropertiesValidator._has_duplicate_conversion(cleaned_data):
            cleaned_data = PropertiesValidator._fix_conversion(cleaned_data)
            changed = True
            logger.warning("Auto-fixed duplicate conversion entries")
        
        # Check for flat logging keys
        if PropertiesValidator._has_flat_logging_keys(cleaned_data):
            cleaned_data = PropertiesValidator._fix_flat_logging_keys(cleaned_data)
            changed = True
            logger.warning("Auto-fixed flat logging keys")
        
        # Check for ROOT entries
        if 'ROOT' in cleaned_data:
            cleaned_data = PropertiesValidator._fix_root_entries(cleaned_data)
            changed = True
            logger.warning("Auto-fixed ROOT entries")
        
        return cleaned_data, changed
    
    @staticmethod
    def _has_duplicate_recent_files(data: Dict[str, Any]) -> bool:
        """Check if both recent_files entries exist"""
        app_data = data.get('app', {})
        return 'recent_files' in app_data and 'recent_files_timestamps' in app_data
    
    @staticmethod
    def _has_flat_logging_keys(data: Dict[str, Any]) -> bool:
        """Check if flat logging keys exist"""
        flat_keys = ['file', 'display_lines']
        return any(key in data for key in flat_keys)
    
    @staticmethod
    def _fix_flat_logging_keys(data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove flat logging keys"""
        flat_keys = ['file', 'display_lines']
        for key in flat_keys:
            if key in data:
                del data[key]
        return data
    
    @staticmethod
    def _has_duplicate_conversion(data: Dict[str, Any]) -> bool:
        """Check if both conversion entries exist"""
        return 'conversion' in data and 'dialogs' in data and 'settings' in data.get('dialogs', {}) and 'conversion' in data.get('dialogs', {}).get('settings', {})
    
    @staticmethod
    def _fix_recent_files(data: Dict[str, Any]) -> Dict[str, Any]:
        """Keep only the structured recent_files entry"""
        app_data = data.get('app', {})
        
        # Prefer recent_files over recent_files_timestamps
        if 'recent_files' in app_data and 'recent_files_timestamps' in app_data:
            # Use the more recent timestamps
            recent_files = app_data['recent_files']
            timestamps = app_data['recent_files_timestamps']
            
            # Merge timestamps (keep newer)
            for file_path, timestamp in timestamps.items():
                if file_path not in recent_files or timestamp > recent_files[file_path]:
                    recent_files[file_path] = timestamp
            
            # Remove duplicate
            del app_data['recent_files_timestamps']
            data['app'] = app_data
        
        return data
    
    @staticmethod
    def _fix_conversion(data: Dict[str, Any]) -> Dict[str, Any]:
        """Keep only the structured conversion entry"""
        if 'conversion' in data:
            # Remove root-level conversion
            del data['conversion']
        
        return data
    
    @staticmethod
    def _fix_root_entries(data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove ROOT entries and move to correct structure"""
        if 'ROOT' in data:
            root_data = data['ROOT']
            
            # Move to dialogs.settings.rendering if it contains rendering data
            if 'track_line' in root_data or 'route_line' in root_data:
                if 'dialogs' not in data:
                    data['dialogs'] = {}
                if 'settings' not in data['dialogs']:
                    data['dialogs']['settings'] = {}
                data['dialogs']['settings']['rendering'] = root_data
            
            # Remove ROOT
            del data['ROOT']
        
        return data
    
    @staticmethod
    def log_validation_result(was_changed: bool):
        """Log validation result"""
        if was_changed:
            logger.info("Properties validation: Auto-cleaned duplicate entries")
        else:
            logger.debug("Properties validation: No issues found")
