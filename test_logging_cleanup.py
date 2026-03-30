#!/usr/bin/env python3
"""
Test script to add flat logging keys and test cleanup
"""

import json
import os
import shutil
from datetime import datetime

def add_flat_logging_keys():
    """Add flat logging keys to test cleanup"""
    
    # Backup current properties
    if os.path.exists("properties.json"):
        backup_name = f"properties.json.logging_test_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2("properties.json", backup_name)
        print(f"Backup created: {backup_name}")
    
    # Load current properties
    with open("properties.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Add problematic flat logging keys
    print("Adding flat logging keys...")
    
    data["file"] = "app.log"
    data["display_lines"] = 1000
    data["dialogs.settings.logging.level"] = "DEBUG"
    data["dialogs.settings.logging.file"] = "app.log"
    
    # Save modified properties
    with open("properties.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Flat logging keys added!")
    print("Run the app or watchdog to test cleanup")

if __name__ == "__main__":
    add_flat_logging_keys()
