#!/usr/bin/env python3
"""
SAFE JSON Properties File Cleanup
Follows security protocol: Backup -> Validate -> Modify -> Verify
"""

import sys
import os
import json
import shutil
from datetime import datetime
sys.path.insert(0, '.')

def safe_json_cleanup():
    """Safely clean up JSON properties file with full security protocol"""
    print("=== SAFE JSON Properties File Cleanup ===")
    
    try:
        # STEP 1: FILE VALIDATION
        json_file = "properties.json"
        if not os.path.exists(json_file):
            print(f"ERROR: {json_file} not found")
            return False
        
        print(f"Step 1: Validating {json_file}...")
        file_size = os.path.getsize(json_file)
        print(f"  File size: {file_size} bytes")
        
        # STEP 2: CREATE BACKUP
        print("Step 2: Creating backup...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{json_file}.backup_{timestamp}"
        
        shutil.copy2(json_file, backup_file)
        backup_size = os.path.getsize(backup_file)
        print(f"  Backup created: {backup_file}")
        print(f"  Backup size: {backup_size} bytes")
        print(f"  Backup integrity: {'OK' if file_size == backup_size else 'FAILED'}")
        
        # STEP 3: READ AND VALIDATE ORIGINAL
        print("Step 3: Reading and validating original JSON...")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                original_data = json.load(f)
            print(f"  JSON syntax: VALID")
            print(f"  Data keys: {len(original_data)}")
        except json.JSONDecodeError as e:
            print(f"  JSON syntax: INVALID - {e}")
            print("  ABORTING: Cannot proceed with invalid JSON")
            return False
        
        # STEP 4: IDENTIFY CHANGES
        print("Step 4: Identifying changes needed...")
        
        legacy_keys = [
            'downsample_keep_waypoints',
            'downsample_overwrite_original', 
            'downsample_points_per_100km'
        ]
        
        found_legacy = [key for key in legacy_keys if key in original_data]
        print(f"  Legacy entries found: {len(found_legacy)}")
        
        if not found_legacy:
            print("  No changes needed - JSON is already clean")
            print("  Cleaning up backup file...")
            os.remove(backup_file)
            print(f"  Backup removed: {backup_file}")
            return True
        
        for key in found_legacy:
            print(f"    - {key}: {original_data[key]}")
        
        # STEP 5: PREPARE MODIFICATIONS
        print("Step 5: Preparing modifications...")
        
        # Create working copy
        modified_data = json.loads(json.dumps(original_data))  # Deep copy
        
        # Ensure structured path exists
        structured_path = 'dialogs.settings.conversion.downsample'
        if structured_path not in modified_data:
            modified_data[structured_path] = {}
            print(f"  Created structured path: {structured_path}")
        elif not isinstance(modified_data[structured_path], dict):
            modified_data[structured_path] = {}
            print(f"  Reset structured path to dict: {structured_path}")
        
        # STEP 6: APPLY MODIFICATIONS
        print("Step 6: Applying modifications...")
        
        migrated_count = 0
        for key in found_legacy:
            # Map legacy to structured
            if key == 'downsample_keep_waypoints':
                structured_key = 'keep_waypoints'
            elif key == 'downsample_overwrite_original':
                structured_key = 'overwrite_original'
            elif key == 'downsample_points_per_100km':
                structured_key = 'points_per_100km'
            else:
                continue
            
            # Migrate
            legacy_value = modified_data[key]
            modified_data[structured_path][structured_key] = legacy_value
            del modified_data[key]
            migrated_count += 1
            
            print(f"  Migrated: {key} -> {structured_path}.{structured_key}")
            print(f"    Value: {legacy_value}")
        
        # STEP 7: VALIDATE MODIFIED DATA
        print("Step 7: Validating modified data...")
        
        # Check JSON serialization
        try:
            modified_json = json.dumps(modified_data, indent=2, ensure_ascii=False)
            print("  Modified data JSON syntax: VALID")
        except Exception as e:
            print(f"  Modified data JSON syntax: INVALID - {e}")
            print("  ABORTING: Modified data cannot be serialized")
            return False
        
        # Parse back to verify
        try:
            parsed_back = json.loads(modified_json)
            print("  Modified data round-trip: VALID")
        except Exception as e:
            print(f"  Modified data round-trip: INVALID - {e}")
            print("  ABORTING: Modified data cannot be parsed back")
            return False
        
        # STEP 8: CREATE TEMPORARY FILE
        print("Step 8: Creating temporary file...")
        
        temp_file = f"{json_file}.temp_{timestamp}"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(modified_json)
        
        temp_size = os.path.getsize(temp_file)
        print(f"  Temp file: {temp_file}")
        print(f"  Temp size: {temp_size} bytes")
        
        # STEP 9: VERIFY TEMPORARY FILE
        print("Step 9: Verifying temporary file...")
        
        try:
            with open(temp_file, 'r', encoding='utf-8') as f:
                verify_data = json.load(f)
            
            # Check key differences
            original_keys = set(original_data.keys())
            verify_keys = set(verify_data.keys())
            
            removed_keys = original_keys - verify_keys
            added_keys = verify_keys - original_keys
            
            print(f"  Keys removed: {len(removed_keys)}")
            for key in sorted(removed_keys):
                print(f"    - {key}")
            
            print(f"  Keys added: {len(added_keys)}")
            for key in sorted(added_keys):
                print(f"    + {key}")
            
            # Check legacy entries are gone
            remaining_legacy = [key for key in legacy_keys if key in verify_data]
            if remaining_legacy:
                print(f"  ERROR: Legacy entries still present: {remaining_legacy}")
                os.remove(temp_file)
                return False
            else:
                print("  Legacy entries: ALL REMOVED")
            
        except Exception as e:
            print(f"  Temp file verification FAILED: {e}")
            os.remove(temp_file)
            return False
        
        # STEP 10: ATOMIC REPLACE
        print("Step 10: Atomic replace...")
        
        # Replace original with temp file
        shutil.move(temp_file, json_file)
        final_size = os.path.getsize(json_file)
        print(f"  Original replaced: {json_file}")
        print(f"  Final size: {final_size} bytes")
        
        # STEP 11: FINAL VERIFICATION
        print("Step 11: Final verification...")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                final_data = json.load(f)
            
            # Check structured path exists
            if structured_path in final_data and isinstance(final_data[structured_path], dict):
                structured_data = final_data[structured_path]
                print(f"  Structured path verified: {structured_path}")
                print(f"  Structured keys: {len(structured_data)}")
                for key, value in sorted(structured_data.items()):
                    print(f"    {key}: {value}")
            else:
                print(f"  ERROR: Structured path not found in final file")
                return False
            
            # Check no legacy entries
            final_legacy = [key for key in legacy_keys if key in final_data]
            if final_legacy:
                print(f"  ERROR: Legacy entries in final file: {final_legacy}")
                return False
            else:
                print("  Legacy entries: ALL CLEARED")
            
        except Exception as e:
            print(f"  Final verification FAILED: {e}")
            print("  ATTEMPTING RESTORE FROM BACKUP...")
            shutil.copy2(backup_file, json_file)
            return False
        
        # SUCCESS
        print(f"\nSUCCESS: JSON cleanup completed safely!")
        print(f"  Files migrated: {migrated_count}")
        print(f"  Original backup: {backup_file}")
        print(f"  Final file: {json_file}")
        
        return True
        
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        print("  Attempting restore from backup...")
        try:
            if 'backup_file' in locals() and os.path.exists(backup_file):
                shutil.copy2(backup_file, json_file)
                print(f"  Restored from backup: {backup_file}")
        except Exception as restore_error:
            print(f"  Restore failed: {restore_error}")
        return False

if __name__ == "__main__":
    success = safe_json_cleanup()
    if success:
        print("\nJSON cleanup completed successfully!")
    else:
        print("\nJSON cleanup failed - original file preserved")
