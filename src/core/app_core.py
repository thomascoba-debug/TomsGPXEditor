#!/usr/bin/env python3
"""
Core Application Management
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
from ..config.app_config import AppConfig
from ..infrastructure.stability_manager import get_stability_manager, run_stability_check
from ..infrastructure.error_handler import setup_global_error_handler

logger = logging.getLogger(__name__)

class AppCore:
    """Core application management with stability features"""
    
    def __init__(self):
        self.stability_manager = get_stability_manager()
        self.properties_data = {}
        self._initialized = False
        
        # Setup global error handling
        setup_global_error_handler()
        
        # Ensure directories exist
        AppConfig.ensure_directories()
    
    def initialize(self) -> bool:
        """Initialize core application"""
        try:
            logger.info("Initializing application core...")
            
            # Run stability check first
            stability_issues = run_stability_check()
            
            if stability_issues:
                logger.warning(f"Stability issues found: {len(stability_issues)}")
                self._handle_stability_issues(stability_issues)
            
            # Create backup before any changes
            self.stability_manager.create_backup()
            
            # Load properties
            self._load_properties()
            
            self._initialized = True
            logger.info("Application core initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize application core: {e}")
            return False
    
    def _handle_stability_issues(self, issues: Dict[str, Any]) -> None:
        """Handle stability issues"""
        for category, details in issues.items():
            if category == "json_structure":
                logger.warning(f"JSON structure issues detected and auto-fixed")
            elif category == "invalid_references":
                logger.warning(f"Invalid file references found: {len(details)}")
            elif category == "circular_dependencies":
                logger.warning(f"Circular dependencies detected")
            else:
                logger.warning(f"Unknown stability issue: {category}")
    
    def _load_properties(self) -> Dict[str, Any]:
        """Load properties with fallback to defaults"""
        properties_file = AppConfig.get_properties_path()
        
        if properties_file.exists():
            try:
                import json
                with open(properties_file, 'r', encoding='utf-8') as f:
                    self.properties_data = json.load(f)
                logger.info("Properties loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load properties: {e}")
                self.properties_data = AppConfig.get_default_settings()
                logger.info("Using default properties")
        else:
            logger.info("Properties file not found, using defaults")
            self.properties_data = AppConfig.get_default_settings()
        
        return self.properties_data
    
    def get_properties(self) -> Dict[str, Any]:
        """Get current properties"""
        if not self._initialized:
            self.initialize()
        return self.properties_data
    
    def save_properties(self) -> bool:
        """Save properties with validation"""
        if not self._initialized:
            logger.warning("Application core not initialized")
            return False
        
        try:
            import json
            properties_file = AppConfig.get_properties_path()
            
            with open(properties_file, 'w', encoding='utf-8') as f:
                json.dump(self.properties_data, f, indent=2, ensure_ascii=False)
            
            logger.info("Properties saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save properties: {e}")
            return False
    
    def validate_file_path(self, file_path: str) -> bool:
        """Validate file path"""
        return AppConfig.validate_file_path(file_path)
    
    def get_setting(self, category: str, setting: Optional[str] = None, default: Any = None) -> Any:
        """Get setting value"""
        if not self._initialized:
            self.initialize()
        
        key = AppConfig.get_setting_path(category, setting)
        
        try:
            keys = key.split('.')
            current = self.properties_data
            
            for k in keys:
                current = current[k]
            
            return current
            
        except (KeyError, TypeError):
            return default
    
    def set_setting(self, category: str, setting: Optional[str], value: Any) -> bool:
        """Set setting value"""
        if not self._initialized:
            self.initialize()
        
        key = AppConfig.get_setting_path(category, setting)
        
        try:
            keys = key.split('.')
            current = self.properties_data
            
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            
            current[keys[-1]] = value
            return self.save_properties()
            
        except Exception as e:
            logger.error(f"Failed to set setting {key}: {e}")
            return False
    
    def cleanup_invalid_references(self) -> int:
        """Clean up invalid file references"""
        cleaned_count = 0
        
        # Clean session files
        session_files = self.properties_data.get(AppConfig.SESSION_FILES_KEY, {})
        valid_session_files = {}
        
        for ref_num, file_data in session_files.items():
            file_path = file_data.get("path")
            if file_path and Path(file_path).exists():
                valid_session_files[ref_num] = file_data
            else:
                cleaned_count += 1
                logger.debug(f"Removed invalid session reference: {file_path}")
        
        if cleaned_count > 0:
            self.properties_data[AppConfig.SESSION_FILES_KEY] = valid_session_files
            self.save_properties()
            logger.info(f"Cleaned up {cleaned_count} invalid session references")
        
        return cleaned_count
    
    def run_maintenance(self) -> None:
        """Run maintenance tasks"""
        logger.info("Running maintenance tasks...")
        
        # Clean invalid references
        self.cleanup_invalid_references()
        
        # Clean old backups
        self.stability_manager.cleanup_old_backups()
        
        # Run stability check
        run_stability_check()
        
        logger.info("Maintenance completed")
    
    def shutdown(self) -> None:
        """Shutdown application core"""
        try:
            logger.info("Shutting down application core...")
            
            if self._initialized:
                # Save current state
                self.save_properties()
                
                # Create final backup
                self.stability_manager.create_backup()
                
                logger.info("Application core shutdown completed")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

# Global app core instance
_app_core = AppCore()

def get_app_core() -> AppCore:
    """Get global app core instance"""
    return _app_core

def initialize_app_core() -> bool:
    """Initialize application core"""
    return _app_core.initialize()
