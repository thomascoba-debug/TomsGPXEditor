#!/usr/bin/env python3
"""
Clean up recent files duplicates in JSON
"""

import sys
import os
import json
import shutil
from datetime import datetime
sys.path.insert(0, '.')

def cleanup_recent_files_json():
    """Clean up recent files duplicates in JSON"""
    print("=== Cleaning Up Recent Files JSON ===")
    
    try:
        # STEP 1: BACKUP
        json_file = "properties.json"
        if not os.path.exists(json_file):
            print(f"ERROR: {json_file} not found")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{json_file}.backup_{timestamp}"
        shutil.copy2(json_file, backup_file)
        print(f"Backup created: {backup_file}")
        
        # STEP 2: READ AND ANALYZE
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Original JSON keys: {list(data.keys())}")
        
        # STEP 3: IDENTIFY RECENT FILES ENTRIES
        recent_entries = {}
        
        # Check all possible recent files locations
        if 'app' in data and isinstance(data['app'], dict):
            if 'recent_files' in data['app']:
                recent_entries['app.recent_files'] = data['app']['recent_files']
            if 'recent_files_timestamps' in data['app']:
                recent_entries['app.recent_files_timestamps'] = data['app']['recent_files_timestamps']
        
        if 'app.recent_files.with_timestamps' in data:
            recent_entries['app.recent_files.with_timestamps'] = data['app.recent_files.with_timestamps']
        
        print(f"\nFound recent files entries:")
        for key, value in recent_entries.items():
            if isinstance(value, list):
                print(f"  {key}: [list] with {len(value)} items")
            elif isinstance(value, dict):
                print(f"  {key}: {{dict}} with {len(value)} keys")
            else:
                print(f"  {key}: {type(value).__name__}")
        
        # STEP 4: DECIDE WHICH TO KEEP
        # We want to keep the one with actual data (timestamps)
        target_key = None
        target_value = None
        
        # Prefer app.recent_files_timestamps (our new implementation)
        if 'app.recent_files_timestamps' in recent_entries:
            target_key = 'app.recent_files_timestamps'
            target_value = recent_entries['app.recent_files_timestamps']
        # Fallback to app.recent_files.with_timestamps
        elif 'app.recent_files.with_timestamps' in recent_entries:
            target_key = 'app.recent_files.with_timestamps'
            target_value = recent_entries['app.recent_files.with_timestamps']
        
        if not target_key:
            print("No recent files data found to keep")
            return True
        
        print(f"\nKeeping: {target_key}")
        print(f"  Data: {target_value}")
        
        # STEP 5: CLEAN UP JSON
        # Remove all recent files entries
        if 'app' in data and isinstance(data['app'], dict):
            if 'recent_files' in data['app']:
                del data['app']['recent_files']
                print("Removed: app.recent_files")
            if 'recent_files_timestamps' in data['app']:
                del data['app']['recent_files_timestamps']
                print("Removed: app.recent_files_timestamps")
        
        if 'app.recent_files.with_timestamps' in data:
            del data['app.recent_files.with_timestamps']
            print("Removed: app.recent_files.with_timestamps")
        
        # Add the clean entry back
        if target_key == 'app.recent_files_timestamps':
            if 'app' not in data:
                data['app'] = {}
            data['app']['recent_files_timestamps'] = target_value
            print(f"Restored: app.recent_files_timestamps")
        elif target_key == 'app.recent_files.with_timestamps':
            data['app.recent_files.with_timestamps'] = target_value
            print(f"Restored: app.recent_files.with_timestamps")
        
        # STEP 6: SAVE CLEANED JSON
        print(f"\nSaving cleaned JSON...")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Cleaned JSON saved: {json_file}")
        print(f"Final keys: {list(data.keys())}")
        
        # STEP 7: VERIFY
        with open(json_file, 'r', encoding='utf-8') as f:
            verify_data = json.load(f)
        
        # Count recent files entries again
        verify_recent = {}
        if 'app' in verify_data and isinstance(verify_data['app'], dict):
            if 'recent_files' in verify_data['app']:
                verify_recent['app.recent_files'] = verify_data['app']['recent_files']
            if 'recent_files_timestamps' in verify_data['app']:
                verify_recent['app.recent_files_timestamps'] = verify_data['app']['recent_files_timestamps']
        
        if 'app.recent_files.with_timestamps' in verify_data:
            verify_recent['app.recent_files.with_timestamps'] = verify_data['app.recent_files.with_timestamps']
        
        print(f"\nVerification - Recent files entries: {len(verify_recent)}")
        for key, value in verify_recent.items():
            print(f"  {key}: {type(value).__name__}")
        
        if len(verify_recent) == 1:
            print("SUCCESS: Only one recent files entry remains")
        else:
            print("WARNING: Multiple recent files entries still exist")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    cleanup_recent_files_json()
