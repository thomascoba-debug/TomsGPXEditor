#!/usr/bin/env python3
"""
Correct Dialog Fixes - Fix what was actually reported

This script fixes the actual issues reported by the user.
"""

import os
import re

def fix_track_to_route_close_button():
    """Fix Close button in Track to Route dialog"""
    
    print("FIXING TRACK TO ROUTE CLOSE BUTTON")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/track_to_route_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix Close button
        content = re.sub(
            r'text="Close"',
            'text="Schließen"',
            content
        )
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.correct_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed Close button to German")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def fix_route_to_track_all_texts():
    """Fix all English texts in Route to Track dialog"""
    
    print("\nFIXING ROUTE TO TRACK ALL TEXTS")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/route_to_track_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix all hardcoded texts with German
        replacements = [
            (r'text="Convert Routes to Tracks"', 'text="Routen in Tracks umwandeln"'),
            (r'text="Selected Files"', 'text="Ausgewählte Dateien"'),
            (r'text="Select All"', 'text="Alle auswählen"'),
            (r'text="Deselect All"', 'text="Alle abwählen"'),
            (r'text="Remove Selected"', 'text="Ausgewählte entfernen"'),
            (r'text="Convert to Tracks"', 'text="In Tracks umwandeln"'),
            (r'text="No files selected"', 'text="Keine Dateien ausgewählt"'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.correct_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed all English texts to German")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def main():
    """Main function"""
    
    print("CORRECT DIALOG FIXES - WHAT WAS ACTUALLY REPORTED")
    print("=" * 60)
    
    success1 = fix_track_to_route_close_button()
    success2 = fix_route_to_track_all_texts()
    
    print("\n" + "=" * 60)
    print("CORRECT FIX SUMMARY")
    print("=" * 60)
    
    if success1 and success2:
        print("SUCCESS: Fixed the actual reported issues!")
        print("\nFixed issues:")
        print("  - Track to Route: Close button now German")
        print("  - Route to Track: All texts now German (except Close which was already German)")
        print("\nNow all Edit dialogs should show complete German text!")
    else:
        print("FAILED: Some fixes failed. Check errors above.")

if __name__ == "__main__":
    main()
