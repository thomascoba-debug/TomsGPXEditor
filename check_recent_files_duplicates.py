#!/usr/bin/env python3
"""
Check for recent files duplicates in JSON
"""

import sys
sys.path.insert(0, '.')

def check_recent_files_duplicates():
    """Check for recent files duplicates in properties"""
    print("=== Checking Recent Files Duplicates ===")
    
    try:
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        props = AppProperties()
        print("Top-level keys:")
        for key in sorted(props.data.keys()):
            value = props.data[key]
            if isinstance(value, dict):
                print(f"  {key}: {{dict}} with {len(value)} keys")
            elif isinstance(value, list):
                print(f"  {key}: [list] with {len(value)} items")
            else:
                print(f"  {key}: {type(value).__name__} = {str(value)[:50]}...")
        
        print("\nChecking for recent files duplicates:")
        
        # Check all possible recent files keys
        recent_keys = [
            'app.recent_files',
            'app.recent_files.with_timestamps', 
            'app.recent_files_timestamps',
            'recent_files',
            'recent_files_with_timestamps'
        ]
        
        found_keys = []
        for key in recent_keys:
            if key in props.data:
                value = props.data[key]
                print(f"  {key}: {type(value).__name__}")
                if isinstance(value, list):
                    print(f"    Length: {len(value)}")
                    if len(value) > 0:
                        print(f"    First item: {value[0]}")
                elif isinstance(value, dict):
                    print(f"    Keys: {list(value.keys())}")
                found_keys.append(key)
        
        print(f"\nFound {len(found_keys)} recent files keys: {found_keys}")
        
        # Check if app.recent_files exists and what it contains
        if 'app.recent_files' in props.data:
            app_recent = props.data['app.recent_files']
            print(f"\napp.recent_files details:")
            print(f"  Type: {type(app_recent)}")
            if isinstance(app_recent, list):
                print(f"  Length: {len(app_recent)}")
                for i, item in enumerate(app_recent[:3]):  # Show first 3
                    print(f"    {i}: {item}")
                if len(app_recent) > 3:
                    print(f"    ... and {len(app_recent) - 3} more")
        
        # Check if we need to clean up
        if len(found_keys) > 1:
            print(f"\nWARNING: Found {len(found_keys)} recent files keys - may need cleanup")
            print("Recommendation: Keep only one recent files mechanism")
        else:
            print(f"\nOK: Only one recent files key found")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_recent_files_duplicates()
