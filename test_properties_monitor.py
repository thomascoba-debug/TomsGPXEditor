#!/usr/bin/env python3
"""
Test Properties Monitor - Creates duplicate entries to test the system
"""

import json
import os
import shutil
from datetime import datetime

def create_test_duplicates():
    """Create test duplicates in properties.json"""
    
    # Backup current properties
    if os.path.exists("properties.json"):
        backup_name = f"properties.json.test_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2("properties.json", backup_name)
        print(f"Backup created: {backup_name}")
    
    # Load current properties
    with open("properties.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Add duplicates
    print("Creating test duplicates...")
    
    # Add duplicate recent_files
    if 'app' not in data:
        data['app'] = {}
    
    # Add both recent_files entries
    data['app']['recent_files'] = {
        "test_file1.gpx": 1234567890,
        "test_file2.gpx": 1234567891
    }
    
    data['app']['recent_files_timestamps'] = {
        "test_file3.gpx": 1234567892,
        "test_file4.gpx": 1234567893
    }
    
    # Add duplicate conversion
    data['conversion'] = {
        "downsample": {
            "points_per_100km": 999,
            "keep_waypoints": True,
            "overwrite_original": False
        }
    }
    
    # Add ROOT entry
    data['ROOT'] = {
        "track_line": {
            "enabled": True,
            "width": 10
        },
        "route_line": {
            "enabled": True,
            "width": 8
        }
    }
    
    # Save modified properties
    with open("properties.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Test duplicates created!")
    print("Run the app to see the error message, or run:")
    print("python -c \"from src.infrastructure.properties_monitor import PropertiesMonitor; PropertiesMonitor.startup_check()\"")

if __name__ == "__main__":
    create_test_duplicates()
