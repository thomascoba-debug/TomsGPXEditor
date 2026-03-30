#!/usr/bin/env python3
"""
Quick Fix Dialog Language Issues

This script quickly fixes the most critical dialog language issues.
"""

import os
import re

def fix_track_to_route_language_manager():
    """Fix language_manager initialization in Track to Route dialog"""
    
    print("FIXING TRACK TO ROUTE LANGUAGE MANAGER")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/track_to_route_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Check if language_manager is initialized
        if 'self.language_manager = get_language_manager()' not in content:
            # Find __init__ method and add language manager
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if 'def __init__' in line:
                    # Find the next non-empty line after __init__
                    j = i + 1
                    while j < len(lines) and (not lines[j].strip() or lines[j].strip().startswith('#')):
                        j += 1
                    
                    if j < len(lines):
                        # Add language manager initialization
                        lines.insert(j, '        self.language_manager = get_language_manager()')
                        content = '\n'.join(lines)
                        print("  Added language manager initialization")
                        break
        
        # Revert problematic language_manager calls back to hardcoded text temporarily
        content = re.sub(
            r'text=self\.language_manager\.t\("dialog\.select_all"\)',
            'text="Alle auswählen"',
            content
        )
        
        content = re.sub(
            r'text=self\.language_manager\.t\("dialog\.deselect_all"\)',
            'text="Alle abwählen"',
            content
        )
        
        content = re.sub(
            r'text=self\.language_manager\.t\("dialog\.remove_selected"\)',
            'text="Ausgewählte entfernen"',
            content
        )
        
        content = re.sub(
            r'text=self\.language_manager\.t\("dialog\.convert_to_tracks"\)',
            'text="In Tracks umwandeln"',
            content
        )
        
        content = re.sub(
            r'text=self\.language_manager\.t\("dialog\.no_files_selected"\)',
            'text="Keine Dateien ausgewählt"',
            content
        )
        
        # Fix title and other texts
        content = re.sub(
            r'text=self\.language_manager\.t\("dialog\.track_to_route\.title"\)',
            'text="Routen in Tracks umwandeln"',
            content
        )
        
        content = re.sub(
            r'text=self\.language_manager\.t\("dialog\.selected_files"\)',
            'text="Ausgewählte Dateien"',
            content
        )
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.quick_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed Track to Route dialog")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def fix_route_to_track_dialog():
    """Fix Route to Track dialog with German texts"""
    
    print("\nFIXING ROUTE TO TRACK DIALOG")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/route_to_track_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix hardcoded texts with German
        replacements = [
            (r'text="Downsample Tracks"', 'text="Tracks downsamplen"'),
            (r'text="Convert to Routes"', 'text="In Routen umwandeln"'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.quick_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed Route to Track dialog")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def fix_track_downsampling_dialog():
    """Fix Track Downsampling dialog with German texts"""
    
    print("\nFIXING TRACK DOWNSAMPLING DIALOG")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/track_downsampling_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix hardcoded texts with German
        replacements = [
            (r'text=self\.language_manager\.t\("dialog\.select_all"\)', 'text="Alle auswählen"'),
            (r'text=self\.language_manager\.t\("dialog\.deselect_all"\)', 'text="Alle abwählen"'),
            (r'text=self\.language_manager\.t\("dialog\.remove_selected"\)', 'text="Ausgewählte entfernen"'),
            (r'text=self\.language_manager\.t\("dialog\.downsample_selected_files"\)', 'text="Ausgewählte Dateien downsamplen"'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.quick_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed Track Downsampling dialog")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def fix_track_table_editor():
    """Fix Track Table Editor with German texts"""
    
    print("\nFIXING TRACK TABLE EDITOR")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/widgets/gpx_table_editor.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix hardcoded texts with German
        replacements = [
            (r'text="Apply Changes"', 'text="Änderungen anwenden"'),
            (r'text="Delete Point"', 'text="Punkt löschen"'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.quick_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed Track Table Editor")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def main():
    """Main function"""
    
    print("QUICK FIX DIALOG LANGUAGE ISSUES")
    print("=" * 60)
    
    success1 = fix_track_to_route_language_manager()
    success2 = fix_route_to_track_dialog()
    success3 = fix_track_downsampling_dialog()
    success4 = fix_track_table_editor()
    
    print("\n" + "=" * 60)
    print("QUICK FIX SUMMARY")
    print("=" * 60)
    
    if success1 and success2 and success3 and success4:
        print("SUCCESS: All critical dialog issues fixed!")
        print("\nFixed issues:")
        print("  - Track to Route: Added language_manager, German buttons")
        print("  - Route to Track: German buttons")
        print("  - Track Downsampling: German buttons")
        print("  - Track Table Editor: German buttons")
        print("\nAll Edit dialogs should now show German text!")
    else:
        print("FAILED: Some fixes failed. Check errors above.")

if __name__ == "__main__":
    main()
