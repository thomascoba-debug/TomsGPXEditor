#!/usr/bin/env python3
"""
Clean up track_to_route_points_per_100km redundancy
"""

import sys
import os
import json
import shutil
from datetime import datetime
sys.path.insert(0, '.')

def cleanup_track_redundancy():
    """Clean up track_to_route_points_per_100km redundancy"""
    print("=== Cleaning Up Track-to-Route Redundancy ===")
    
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
        
        # STEP 3: CHECK VALUES
        flat_value = data.get('track_to_route_points_per_100km', None)
        structured_value = None
        
        if 'dialogs' in data and isinstance(data['dialogs'], dict):
            if 'settings' in data['dialogs'] and isinstance(data['dialogs']['settings'], dict):
                if 'conversion' in data['dialogs']['settings'] and isinstance(data['dialogs']['settings']['conversion'], dict):
                    if 'track_to_route' in data['dialogs']['settings']['conversion'] and isinstance(data['dialogs']['settings']['conversion']['track_to_route'], dict):
                        structured_value = data['dialogs']['settings']['conversion']['track_to_route'].get('points_per_100km')
        
        print(f"\nValues found:")
        print(f"  Flat entry: track_to_route_points_per_100km = {flat_value}")
        print(f"  Structured entry: dialogs.settings.conversion.track_to_route.points_per_100km = {structured_value}")
        
        # STEP 4: REMOVE FLAT ENTRY (keep structured for consistency)
        if flat_value is not None:
            print(f"\nRemoving flat entry (keeping structured for consistency)")
            del data['track_to_route_points_per_100km']
            print("Removed flat entry")
        else:
            print("No flat entry to remove")
        
        # STEP 5: SAVE CLEANED JSON
        print(f"\nSaving cleaned JSON...")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Cleaned JSON saved: {json_file}")
        print(f"Final keys: {list(data.keys())}")
        
        # STEP 6: VERIFY
        with open(json_file, 'r', encoding='utf-8') as f:
            verify_data = json.load(f)
        
        # Check final state
        final_flat = verify_data.get('track_to_route_points_per_100km', None)
        final_structured = None
        
        if 'dialogs' in verify_data and isinstance(verify_data['dialogs'], dict):
            if 'settings' in verify_data['dialogs'] and isinstance(verify_data['dialogs']['settings'], dict):
                if 'conversion' in verify_data['dialogs']['settings'] and isinstance(verify_data['dialogs']['settings']['conversion'], dict):
                    if 'track_to_route' in verify_data['dialogs']['settings']['conversion'] and isinstance(verify_data['dialogs']['settings']['conversion']['track_to_route'], dict):
                        final_structured = verify_data['dialogs']['settings']['conversion']['track_to_route'].get('points_per_100km')
        
        print(f"\nVerification:")
        print(f"  Flat entry: {final_flat}")
        print(f"  Structured entry: {final_structured}")
        
        if final_flat is None and final_structured is not None:
            print("SUCCESS: Only structured entry remains (consistent with other dialogs)")
        elif final_flat is not None and final_structured is None:
            print("WARNING: Only flat entry remains (inconsistent)")
        else:
            print("WARNING: Both entries still exist")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    cleanup_track_redundancy()
