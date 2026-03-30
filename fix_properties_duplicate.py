#!/usr/bin/env python3
"""
Fix Properties.json Duplicate

This script removes the duplicate conversion section from properties.json
"""

import json
import os

def fix_properties_duplicate():
    """Remove duplicate conversion section from properties.json"""
    
    print("FIXING PROPERTIES.JSON DUPLICATE")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/properties.json"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("Original structure:")
        print(f"  - dialogs.settings.conversion.downsample: {'EXISTS' if 'conversion' in data.get('dialogs', {}).get('settings', {}) else 'MISSING'}")
        print(f"  - Root-level conversion: {'EXISTS' if 'conversion' in data else 'MISSING'}")
        
        # Remove the duplicate root-level conversion section
        if 'conversion' in data:
            del data['conversion']
            print("  Removed duplicate root-level conversion section")
        
        # Create backup
        backup_path = f"{file_path}.duplicate_fix_backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Write fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  Backup created: {backup_path}")
        print("  Fixed properties.json")
        
        # Verify the fix
        with open(file_path, 'r', encoding='utf-8') as f:
            fixed_data = json.load(f)
        
        print("\nFixed structure:")
        print(f"  - dialogs.settings.conversion.downsample: {'EXISTS' if 'conversion' in fixed_data.get('dialogs', {}).get('settings', {}) else 'MISSING'}")
        print(f"  - Root-level conversion: {'EXISTS' if 'conversion' in fixed_data else 'MISSING'}")
        
        return True
        
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    """Main function"""
    
    print("FIXING PROPERTIES.JSON DUPLICATE CONVERSION SECTION")
    print("=" * 60)
    
    success = fix_properties_duplicate()
    
    print("\n" + "=" * 60)
    print("DUPLICATE FIX SUMMARY")
    print("=" * 60)
    
    if success:
        print("SUCCESS: Duplicate conversion section removed!")
        print("\nChanges made:")
        print("  - Removed duplicate root-level 'conversion' section")
        print("  - Kept correct 'dialogs.settings.conversion' section")
        print("  - Created backup before changes")
        print("\nThe properties.json should now be clean and without duplicates!")
    else:
        print("FAILED: Could not fix properties.json. Check errors above.")

if __name__ == "__main__":
    main()
