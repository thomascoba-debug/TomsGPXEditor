#!/usr/bin/env python3
"""
Script to clean up duplicate downsample properties
"""

import sys
sys.path.insert(0, '.')

def cleanup_downsample_duplicates():
    """Clean up duplicate downsample properties"""
    print("=== Cleaning Up Downsample Duplicates ===")
    
    try:
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Load properties
        properties = AppProperties()
        print(f"Loaded properties with {len(properties.data)} keys")
        
        # Check for duplicate entries
        legacy_keys = [
            'downsample_keep_waypoints',
            'downsample_overwrite_original', 
            'downsample_points_per_100km'
        ]
        
        structured_path = 'dialogs.settings.conversion.downsample'
        
        print("\nChecking for duplicate entries...")
        
        # Get structured values
        structured_values = {}
        if structured_path in properties.data:
            structured_data = properties.data[structured_path]
            if isinstance(structured_data, dict):
                structured_values = structured_data
        
        print(f"Structured values: {structured_values}")
        
        # Migrate legacy entries to structured format
        migrated_count = 0
        for key in legacy_keys:
            if key in properties.data:
                # Extract the corresponding structured key
                if key == 'downsample_keep_waypoints':
                    structured_key = 'keep_waypoints'
                elif key == 'downsample_overwrite_original':
                    structured_key = 'overwrite_original'
                elif key == 'downsample_points_per_100km':
                    structured_key = 'points_per_100km'
                else:
                    continue
                
                # Get legacy value
                legacy_value = properties.data[key]
                
                print(f"Migrating: {key} -> {structured_key}")
                print(f"  Value: {legacy_value}")
                
                # Ensure structured path exists
                if structured_path not in properties.data:
                    properties.data[structured_path] = {}
                elif not isinstance(properties.data[structured_path], dict):
                    properties.data[structured_path] = {}
                
                # Set structured value
                properties.data[structured_path][structured_key] = legacy_value
                
                # Remove legacy entry
                del properties.data[key]
                migrated_count += 1
                print(f"  -> Migrated and removed legacy entry")
        
        # Save cleaned properties
        if migrated_count > 0:
            properties.save()
            print(f"\nSUCCESS: Migrated {migrated_count} downsample entries to structured format")
        else:
            print("\nNo entries found to migrate")
        
        # Verify cleanup
        print("\nVerifying cleanup...")
        remaining_legacy = [key for key in legacy_keys if key in properties.data]
        if remaining_legacy:
            print(f"WARNING: Still have legacy entries: {remaining_legacy}")
        else:
            print("SUCCESS: All legacy downsample entries removed")
        
        # Show current structured settings
        if structured_path in properties.data:
            print(f"\nCurrent structured downsample settings:")
            structured_data = properties.data[structured_path]
            if isinstance(structured_data, dict):
                for key, value in sorted(structured_data.items()):
                    print(f"  {key}: {value}")
        
    except Exception as e:
        print("ERROR:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    cleanup_downsample_duplicates()
