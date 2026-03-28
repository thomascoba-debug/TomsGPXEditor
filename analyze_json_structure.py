#!/usr/bin/env python3
"""
Analyze the actual JSON structure to find downsample entries
"""

import sys
import os
import json
sys.path.insert(0, '.')

def analyze_json_structure():
    """Analyze the actual JSON file structure"""
    print("=== Analyzing JSON File Structure ===")
    
    try:
        # Read JSON file directly
        json_file = "properties.json"
        if not os.path.exists(json_file):
            print(f"ERROR: {json_file} not found")
            return
        
        print(f"Reading {json_file}...")
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"JSON loaded with {len(data)} top-level keys")
        
        # Show all keys
        print("\nAll top-level keys:")
        for key in sorted(data.keys()):
            value = data[key]
            if isinstance(value, dict):
                print(f"  {key}: {{dict}} with {len(value)} keys")
            elif isinstance(value, list):
                print(f"  {key}: [list] with {len(value)} items")
            else:
                print(f"  {key}: {type(value).__name__} = {str(value)[:50]}...")
        
        # Find ALL downsample entries
        print("\n=== FINDING ALL DOWNSAMPLE ENTRIES ===")
        
        def find_downsample_recursive(obj, path=""):
            """Recursively find all downsample entries"""
            entries = []
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    if 'downsample' in key.lower():
                        entries.append({
                            'path': current_path,
                            'key': key,
                            'value': value,
                            'type': type(value).__name__
                        })
                        print(f"FOUND: {current_path} = {value} ({type(value).__name__})")
                    
                    # Recurse into nested structures
                    if isinstance(value, (dict, list)):
                        entries.extend(find_downsample_recursive(value, current_path))
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{path}[{i}]" if path else f"[{i}]"
                    if isinstance(item, (dict, list)):
                        entries.extend(find_downsample_recursive(item, current_path))
            
            return entries
        
        all_downsample_entries = find_downsample_recursive(data)
        print(f"\nTotal downsample entries found: {len(all_downsample_entries)}")
        
        # Show detailed analysis
        print("\n=== DETAILED ANALYSIS ===")
        for entry in all_downsample_entries:
            print(f"Path: {entry['path']}")
            print(f"  Key: {entry['key']}")
            print(f"  Value: {entry['value']}")
            print(f"  Type: {entry['type']}")
            print()
        
        # Check for specific patterns
        print("=== PATTERN ANALYSIS ===")
        
        # Legacy flat entries
        legacy_patterns = [
            'downsample_keep_waypoints',
            'downsample_overwrite_original',
            'downsample_points_per_100km'
        ]
        
        print("Legacy flat entries:")
        for pattern in legacy_patterns:
            if pattern in data:
                print(f"  FOUND: {pattern} = {data[pattern]}")
            else:
                print(f"  MISSING: {pattern}")
        
        # Structured entries
        structured_patterns = [
            'dialogs.settings.conversion.downsample',
            'dialogs.settings.conversion.route_to_track.points_per_100km',
            'dialogs.settings.conversion.track_to_route.points_per_100km'
        ]
        
        print("\nStructured entries:")
        def get_nested_value(data, path):
            """Get value from nested dict using dot notation"""
            keys = path.split('.')
            current = data
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return None
            return current
        
        for pattern in structured_patterns:
            value = get_nested_value(data, pattern)
            if value is not None:
                print(f"  FOUND: {pattern} = {value}")
            else:
                print(f"  MISSING: {pattern}")
        
        # Compare with in-memory properties
        print("\n=== COMPARISON WITH IN-MEMORY PROPERTIES ===")
        try:
            from src.infrastructure.repositories.properties_repository import AppProperties
            app_props = AppProperties()
            
            print(f"In-memory properties keys: {len(app_props.data)}")
            print(f"JSON file keys: {len(data)}")
            
            # Find differences
            json_keys = set(data.keys())
            memory_keys = set(app_props.data.keys())
            
            only_in_json = json_keys - memory_keys
            only_in_memory = memory_keys - json_keys
            
            if only_in_json:
                print(f"Only in JSON: {sorted(only_in_json)}")
            if only_in_memory:
                print(f"Only in memory: {sorted(only_in_memory)}")
            
            if not only_in_json and not only_in_memory:
                print("JSON and in-memory properties are identical")
            
        except Exception as e:
            print(f"Could not compare with in-memory properties: {e}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_json_structure()
