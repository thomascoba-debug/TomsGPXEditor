#!/usr/bin/env python3
"""
Fix Remaining Hardcoded German Texts in Dialogs

This script fixes the remaining hardcoded German texts in dialogs
that should use language_manager.t() for proper translation.
"""

import os
import re

def fix_route_to_track_dialog():
    """Fix Route to Track dialog hardcoded texts"""
    
    print("FIXING ROUTE TO TRACK DIALOG")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/route_to_track_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Add language manager import if missing
        if 'from src.i18n.language_manager import get_language_manager' not in content:
            content = re.sub(
                r'import tkinter as tk',
                'import tkinter as tk\nfrom src.i18n.language_manager import get_language_manager',
                content
            )
        
        # Add language manager initialization if missing
        if 'self.language_manager = get_language_manager()' not in content:
            # Find __init__ method and add language manager
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'def __init__' in line:
                    # Add after the next line
                    lines.insert(i + 2, '        self.language_manager = get_language_manager()')
                    break
            content = '\n'.join(lines)
        
        # Fix hardcoded texts
        replacements = [
            (r'text="Ausgewählte Dateien"', 'text=self.language_manager.t("dialog.selected_files")'),
            (r'text="Alle auswählen"', 'text=self.language_manager.t("dialog.select_all")'),
            (r'text="Alle abwählen"', 'text=self.language_manager.t("dialog.deselect_all")'),
            (r'text="Ausgewählte entfernen"', 'text=self.language_manager.t("dialog.remove_selected")'),
            (r'text="Keine Dateien ausgewählt"', 'text=self.language_manager.t("dialog.no_files_selected")'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.final_fix_backup"
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
    """Fix Track Downsampling dialog hardcoded texts"""
    
    print("\nFIXING TRACK DOWNSAMPLING DIALOG")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/track_downsampling_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Add language manager import if missing
        if 'from src.i18n.language_manager import get_language_manager' not in content:
            content = re.sub(
                r'import tkinter as tk',
                'import tkinter as tk\nfrom src.i18n.language_manager import get_language_manager',
                content
            )
        
        # Add language manager initialization if missing
        if 'self.language_manager = get_language_manager()' not in content:
            # Find __init__ method and add language manager
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'def __init__' in line:
                    # Add after the next line
                    lines.insert(i + 2, '        self.language_manager = get_language_manager()')
                    break
            content = '\n'.join(lines)
        
        # Fix hardcoded texts
        replacements = [
            (r'text="Alle auswählen"', 'text=self.language_manager.t("dialog.select_all")'),
            (r'text="Alle abwählen"', 'text=self.language_manager.t("dialog.deselect_all")'),
            (r'text="Ausgewählte entfernen"', 'text=self.language_manager.t("dialog.remove_selected")'),
            (r'text="Ausgewählte Dateien downsamplen"', 'text=self.language_manager.t("dialog.track_downsampling.downsample_selected_files")'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.final_fix_backup"
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

def fix_track_to_route_dialog():
    """Fix Track to Route dialog hardcoded texts"""
    
    print("\nFIXING TRACK TO ROUTE DIALOG")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/dialogs/track_to_route_dialog.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix hardcoded texts
        replacements = [
            (r'text="Alle auswählen"', 'text=self.language_manager.t("dialog.select_all")'),
            (r'text="Alle abwählen"', 'text=self.language_manager.t("dialog.deselect_all")'),
            (r'text="Ausgewählte entfernen"', 'text=self.language_manager.t("dialog.remove_selected")'),
            (r'text="Schließen"', 'text=self.language_manager.t("dialog.close")'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.final_fix_backup"
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

def main():
    """Main function"""
    
    print("FIXING REMAINING HARDCODED GERMAN TEXTS")
    print("=" * 60)
    
    success1 = fix_route_to_track_dialog()
    success2 = fix_track_downsampling_dialog()
    success3 = fix_track_to_route_dialog()
    
    print("\n" + "=" * 60)
    print("FINAL FIX SUMMARY")
    print("=" * 60)
    
    if success1 and success2 and success3:
        print("SUCCESS: All remaining hardcoded German texts fixed!")
        print("\nChanges made:")
        print("  - Route to Track: All buttons now use language_manager.t()")
        print("  - Track Downsampling: All buttons now use language_manager.t()")
        print("  - Track to Route: All buttons now use language_manager.t()")
        print("\nNow when language is set to English, all dialogs should show English text!")
    else:
        print("FAILED: Some fixes failed. Check errors above.")

if __name__ == "__main__":
    main()
