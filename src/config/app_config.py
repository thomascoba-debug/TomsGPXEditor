#!/usr/bin/env python3
"""
Central Application Configuration - Fixed Version
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging
from ..constants.property_keys import PropertyKeys, Defaults

logger = logging.getLogger(__name__)

class AppConfig:
    """Central application configuration management"""
    
    # Application constants
    APP_NAME = "TomsGPXEditor"
    VERSION = "1.0.0"
    
    # File paths
    BASE_DIR = Path(__file__).parent.parent.parent
    PROPERTIES_FILE = BASE_DIR / "properties.json"
    LOG_DIR = BASE_DIR / "logs"
    BACKUP_DIR = BASE_DIR / "backups"
    
    # Recent files configuration
    MAX_RECENT_FILES = 10
    
    # Session configuration
    SESSION_FILES_KEY = "session_files"
    
    # Dialog configuration
    DIALOG_GEOMETRY_KEY = "dialogs.geometry"
    DIALOG_SETTINGS_KEY = "dialogs.settings"
    
    # Map configuration
    MAP_DEFAULT_LAT = 51.0
    MAP_DEFAULT_LON = 10.0
    MAP_DEFAULT_ZOOM = 5
    
    # File extensions
    GPX_EXTENSION = ".gpx"
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist"""
        directories = [
            cls.LOG_DIR,
            cls.BACKUP_DIR
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")
    
    @classmethod
    def get_properties_path(cls) -> Path:
        """Get properties file path"""
        return cls.PROPERTIES_FILE
    
    @classmethod
    def get_backup_path(cls, filename: str) -> Path:
        """Get backup file path"""
        return cls.BACKUP_DIR / filename
    
    @classmethod
    def validate_file_path(cls, file_path: str) -> bool:
        """Validate if file path is acceptable"""
        path = Path(file_path)
        
        # Check extension
        if path.suffix.lower() != cls.GPX_EXTENSION:
            return False
        
        # Check if file exists
        if not path.exists():
            return False
        
        return True
    
    @classmethod
    def get_default_settings(cls) -> Dict[str, Any]:
        """Get default application settings"""
        return {
            "app": {
                "version": cls.VERSION,
                "main_window": {
                    "geometry": "800x600+100+100"
                },
                "app.recent_files_timestamps": {}
            },
            "dialogs": {
                "geometry": {},
                "settings": {
                    "conversion": {
                        "downsample": {
                            "enabled": False,
                            "max_points": 1000
                        },
                        "route_to_track": {
                            "points_per_100km": 10
                        },
                        "track_to_route": {
                            "points_per_100km": 10
                        }
                    },
                    "logging": {
                        "level": "INFO",
                        "file": "app.log"
                    }
                }
            },
            cls.SESSION_FILES_KEY: {}
        }
    
    @classmethod
    def get_setting_path(cls, category: str, setting: Optional[str] = None) -> str:
        """Get standardized setting path"""
        if setting:
            return f"{category}.{setting}"
        return category
    
    @classmethod
    def is_development_mode(cls) -> bool:
        """Check if running in development mode"""
        return os.environ.get("TGPX_DEV", "false").lower() == "true"
    
    @classmethod
    def get_log_level(cls) -> str:
        """Get appropriate log level"""
        if cls.is_development_mode():
            return "DEBUG"
        return "INFO"

# Initialize directories on import
AppConfig.ensure_directories()
