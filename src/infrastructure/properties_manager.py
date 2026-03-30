#!/usr/bin/env python3
"""
Properties Manager with automatic JSON validation
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from .json_validator import validate_and_sanitize_properties

logger = logging.getLogger(__name__)

class PropertiesManager:
    """Enhanced properties manager with automatic validation"""
    
    def __init__(self, json_file: str = "properties.json"):
        self.json_file = Path(json_file)
        self._data = None
        self._validation_enabled = True
    
    def load(self) -> Dict[str, Any]:
        """Load properties with automatic validation"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            
            # Auto-validate if enabled
            if self._validation_enabled:
                self._auto_validate()
            
            return self._data or {}
            
        except Exception as e:
            logger.error(f"Failed to load properties: {e}")
            self._data = {}
            return {}
    
    def _auto_validate(self):
        """Automatically validate and fix JSON issues"""
        try:
            # Validate and sanitize
            issues_found = validate_and_sanitize_properties(str(self.json_file))
            
            if issues_found:
                # Reload sanitized data
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
                logger.info("Reloaded sanitized properties after validation")
            
        except Exception as e:
            logger.error(f"Auto-validation failed: {e}")
    
    def save(self) -> bool:
        """Save properties with validation"""
        try:
            if self._data is None:
                logger.warning("No data to save")
                return False
            
            # Validate before saving
            if self._validation_enabled:
                temp_file = self.json_file.with_suffix('.temp.json')
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(self._data, f, indent=2, ensure_ascii=False)
                
                # Validate temp file
                from .json_validator import JSONValidator
                validator = JSONValidator(str(temp_file))
                validator.data = self._data
                validator._validate_structure()
                validator._sanitize_data()
                
                if validator.errors or validator.warnings:
                    validator.save_sanitized()
                    # Load sanitized data
                    with open(temp_file, 'r', encoding='utf-8') as f:
                        self._data = json.load(f)
                    logger.info("Properties sanitized during save")
                
                # Move temp to main file
                temp_file.replace(self.json_file)
            else:
                with open(self.json_file, 'w', encoding='utf-8') as f:
                    json.dump(self._data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save properties: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get property value with dot notation"""
        if self._data is None:
            self.load()
        
        keys = key.split('.')
        current = self._data
        
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """Set property value with validation"""
        if self._data is None:
            self.load()
        
        try:
            keys = key.split('.')
            current = self._data
            
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            
            current[keys[-1]] = value
            return self.save()
            
        except Exception as e:
            logger.error(f"Failed to set property {key}: {e}")
            return False
    
    def remove(self, key: str) -> bool:
        """Remove property key"""
        if self._data is None:
            self.load()
        
        try:
            keys = key.split('.')
            current = self._data
            
            for k in keys[:-1]:
                if k in current:
                    current = current[k]
                else:
                    return False  # Key doesn't exist
            
            if keys[-1] in current:
                del current[keys[-1]]
                return self.save()
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to remove property {key}: {e}")
            return False
    
    def enable_validation(self, enabled: bool = True):
        """Enable or disable automatic validation"""
        self._validation_enabled = enabled
        logger.info(f"JSON validation {'enabled' if enabled else 'disabled'}")
    
    def force_validation(self):
        """Force validation and cleanup"""
        logger.info("Forcing JSON validation and cleanup...")
        self._auto_validate()
    
    @property
    def data(self) -> Dict[str, Any]:
        """Get raw data (for compatibility)"""
        if self._data is None:
            self.load()
        return self._data
