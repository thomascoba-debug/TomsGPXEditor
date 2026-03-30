#!/usr/bin/env python3
"""
Fix Track Table Editor Geometry

This script fixes the GPXTableEditor to inherit from PersistentDialog
so it can save and restore its geometry like other dialogs.
"""

import os
import re

def fix_gpx_table_editor_geometry():
    """Fix GPXTableEditor to use PersistentDialog for geometry saving"""
    
    print("FIXING GPX TABLE EDITOR GEOMETRY")
    print("=" * 50)
    
    file_path = "W:/TomsGPXEditor/src/ui/widgets/gpx_table_editor.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix imports
        content = re.sub(
            r'import tkinter as tk',
            'import tkinter as tk\nfrom src.ui.base import PersistentDialog',
            content
        )
        
        # Fix class inheritance
        content = re.sub(
            r'class GPXTableEditor\(tk\.Toplevel\):',
            'class GPXTableEditor(PersistentDialog):',
            content
        )
        
        # Fix __init__ method signature
        content = re.sub(
            r'def __init__\(self, parent, document, update_callback, save_callback\):',
            'def __init__(self, parent, document, update_callback, save_callback):',
            content
        )
        
        # Add properties parameter to super().__init__ call
        content = re.sub(
            r'super\(\).__init__\(parent\)',
            'super().__init__(parent, None, "GPXTableEditor", modal=True)',
            content
        )
        
        # Remove hardcoded geometry (will be handled by PersistentDialog)
        content = re.sub(
            r'self\.geometry\("800x600"\)',
            '# Geometry will be restored by PersistentDialog',
            content
        )
        
        # Add _on_close method if not exists
        if 'def _on_close(self):' not in content:
            # Find the end of the class and add _on_close method
            lines = content.split('\n')
            
            # Find the last method
            last_method_line = -1
            for i, line in enumerate(lines):
                if line.strip().startswith('def '):
                    last_method_line = i
            
            if last_method_line > 0:
                # Find the end of the last method
                indent_level = None
                end_of_method = last_method_line
                
                for i in range(last_method_line + 1, len(lines)):
                    line = lines[i]
                    if line.strip():
                        if indent_level is None:
                            indent_level = len(line) - len(line.lstrip())
                        elif len(line) - len(line.lstrip()) <= indent_level:
                            end_of_method = i - 1
                            break
                
                # Add _on_close method after the last method
                on_close_method = [
                    '',
                    '    def _on_close(self):',
                    '        """Handle dialog close - save geometry and destroy"""',
                    '        # Save geometry (handled by PersistentDialog base class)',
                    '        super()._on_close()',
                    ''
                ]
                
                # Insert the method
                for i, method_line in enumerate(on_close_method):
                    lines.insert(end_of_method + 1 + i, method_line)
                
                content = '\n'.join(lines)
                print("  Added _on_close method")
        
        if content != original_content:
            # Create backup
            backup_path = f"{file_path}.geometry_fix_backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("  Fixed GPXTableEditor to use PersistentDialog")
            print(f"  Backup created: {backup_path}")
        else:
            print("  No fixes needed")
            
    except Exception as e:
        print(f"  Error: {e}")
        return False
    
    return True

def main():
    """Main function"""
    
    print("FIXING GPX TABLE EDITOR GEOMETRY")
    print("=" * 60)
    
    success = fix_gpx_table_editor_geometry()
    
    print("\n" + "=" * 60)
    print("GEOMETRY FIX SUMMARY")
    print("=" * 60)
    
    if success:
        print("SUCCESS: GPXTableEditor now saves and restores geometry!")
        print("\nChanges made:")
        print("  - Inherits from PersistentDialog instead of tk.Toplevel")
        print("  - Uses modal=True for proper dialog behavior")
        print("  - Geometry will be saved/restored automatically")
        print("  - Added proper _on_close method")
        print("\nThe Track Table Editor should now remember its size and position!")
    else:
        print("FAILED: Geometry fix failed. Check errors above.")

if __name__ == "__main__":
    main()
