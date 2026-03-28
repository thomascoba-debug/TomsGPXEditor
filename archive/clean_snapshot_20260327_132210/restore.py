#!/usr/bin/env python3
"""
Restore script for clean_snapshot_20260327_132210
This script restores the clean project state from the snapshot.
"""

import json
import os
import shutil
from datetime import datetime

def restore_snapshot():
    """Restore the clean snapshot state"""
    
    print(f"Restoring clean snapshot: clean_snapshot_20260327_132210")
    print("="*60)
    
    # Check if snapshot exists
    if not os.path.exists("archive/clean_snapshot_20260327_132210"):
        print("ERROR: Snapshot directory not found!")
        return False
    
    # 1. Restore properties.json
    print("1. Restoring properties.json...")
    if os.path.exists(f"archive/clean_snapshot_20260327_132210/properties.json"):
        shutil.copy2(f"archive/clean_snapshot_20260327_132210/properties.json", "properties.json")
        print("   ✓ properties.json restored")
    
    # 2. Verify file checksums
    print("2. Verifying file integrity...")
    with open(f"archive/clean_snapshot_20260327_132210/snapshot_metadata.json", 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    checksums = metadata.get("file_checksums", {})
    all_valid = True
    
    for file_path, expected_checksum in checksums.items():
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
                actual_checksum = hashlib.sha256(content).hexdigest()
                if actual_checksum == expected_checksum:
                    print(f"   ✓ src/infrastructure/map_renderer.py")
                else:
                    print(f"   ✗ src/infrastructure/map_renderer.py - MODIFIED")
                    all_valid = False
        else:
            print(f"   ✗ src/infrastructure/map_renderer.py - MISSING")
            all_valid = False
    
    # 3. Show snapshot info
    print(f"3. Snapshot Information:")
    print(f"   Created: {metadata['created_at']}")
    print(f"   Description: {metadata['description']}")
    print(f"   Features: {len(metadata['features'])} implemented")
    print(f"   Verified components: {len(metadata['verified_components'])}")
    
    if all_valid:
        print("\n✓ SUCCESS: Clean snapshot restored successfully!")
        print("✓ All files match the clean state")
        print("✓ Project is back to the clean, structured state")
    else:
        print("\n⚠ WARNING: Some files have been modified")
        print("⚠ You may need to manually review changes")
    
    return all_valid

if __name__ == "__main__":
    restore_snapshot()
