#!/usr/bin/env python3
"""
Properties Watchdog - Monitors properties.json for corruption
Run this periodically to check for issues
"""

import json
import os
import logging
from datetime import datetime
from src.infrastructure.properties_validator import PropertiesValidator

def check_properties():
    """Check properties.json for issues"""
    try:
        with open("properties.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        cleaned_data, was_changed = PropertiesValidator.validate_and_clean(data)
        
        if was_changed:
            # Backup original
            backup_name = f"properties.json.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(backup_name, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Save cleaned version
            with open("properties.json", "w", encoding="utf-8") as f:
                json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
            
            print(f"FIXED: Properties had duplicates, backup saved as {backup_name}")
            return True
        else:
            print("OK: Properties are clean")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Properties Watchdog - Checking for duplicates...")
    check_properties()
