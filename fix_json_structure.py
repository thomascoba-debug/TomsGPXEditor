#!/usr/bin/env python3
"""
Fix the confusing JSON structure with duplicate downsample entries
"""

import sys
import os
import json
import shutil
from datetime import datetime
sys.path.insert(0, '.')

def fix_json_structure():
    """Fix the duplicate JSON structure entries"""
    print("=== Fixing JSON Structure ===")
    
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
        
        # STEP 3: IDENTIFY PROBLEM
        problematic_key = "dialogs.settings.conversion.downsample"
        nested_path = ["dialogs", "settings", "conversion", "downsample"]
        
        has_flat_key = problematic_key in data
        has_nested_key = True
        
        # Check nested structure
        current = data
        for key in nested_path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                has_nested_key = False
                break
        
        print(f"Has flat key '{problematic_key}': {has_flat_key}")
        print(f"Has nested structure: {has_nested_key}")
        
        if has_flat_key and has_nested_key:
            # Get both values
            flat_value = data[problematic_key]
            nested_value = current
            
            print(f"Flat value: {flat_value}")
            print(f"Nested value: {nested_value}")
            
            # Check if they're the same
            if flat_value == nested_value:
                print("Values are identical - removing flat key")
                del data[problematic_key]
                print(f"Removed duplicate flat key: {problematic_key}")
            else:
                print("Values are different - keeping both")
                print("  This might indicate a configuration conflict")
        
        elif has_flat_key and not has_nested_key:
            print("Only flat key exists - this might be the correct one")
            print("  No action taken - keeping current structure")
        
        elif not has_flat_key and has_nested_key:
            print("Only nested structure exists - this is correct")
            print("  No action needed")
        
        else:
            print("Neither structure found - checking for other issues")
        
        # STEP 4: SAVE FIXED JSON
        if has_flat_key and has_nested_key and flat_value == nested_value:
            print("Saving fixed JSON...")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Fixed JSON saved: {json_file}")
            print(f"Keys after fix: {list(data.keys())}")
            
            # STEP 5: VERIFY
            with open(json_file, 'r', encoding='utf-8') as f:
                verify_data = json.load(f)
            
            if problematic_key not in verify_data:
                print("✅ Verification: Duplicate key successfully removed")
            else:
                print("❌ Verification: Duplicate key still present")
                return False
            
            # Check nested structure still exists
            current = verify_data
            for key in nested_path:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    print("❌ Verification: Nested structure broken")
                    return False
            
            print("✅ Verification: Nested structure intact")
            print(f"✅ Nested value: {current}")
            
        else:
            print("No changes needed - JSON structure is acceptable")
        
        print(f"\nSUCCESS: JSON structure analysis completed")
        print(f"Backup preserved: {backup_file}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_json_structure()
