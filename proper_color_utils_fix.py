#!/usr/bin/env python3
"""
Proper Color Utils Fix - Structural solution

This script properly fixes the tkinter.colorchooser import issue
with the correct structural approach.
"""

import os

def fix_color_utils_properly():
    """Fix color_utils.py with proper import structure"""
    
    file_path = "W:/TomsGPXEditor/src/ui/utils/color_utils.py"
    
    # Read current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("PROPER COLOR UTILS FIX")
    print("=" * 50)
    
    # Check current imports
    print("Current imports:")
    lines = content.split('\n')
    for i, line in enumerate(lines[:15], 1):
        if 'import' in line:
            print(f"  Line {i}: {line.strip()}")
    
    # Check colorchooser usage
    colorchooser_usage = content.count('colorchooser.askcolor')
    tk_colorchooser_usage = content.count('tk.colorchooser.askcolor')
    
    print(f"\nColorchooser usage analysis:")
    print(f"  - colorchooser.askcolor: {colorchooser_usage}")
    print(f"  - tk.colorchooser.askcolor: {tk_colorchooser_usage}")
    
    # Determine the correct fix
    if tk_colorchooser_usage > 0:
        print("\nISSUE IDENTIFIED:")
        print("  - Using tk.colorchooser instead of direct colorchooser import")
        print("  - This causes the 'module tkinter has no attribute colorchooser' error")
        
        print("\nPROPER SOLUTION:")
        print("  1. Add explicit colorchooser import")
        print("  2. Update all tk.colorchooser references")
        print("  3. Ensure consistent import structure")
        
        # Apply the proper fix
        fixed_content = content
        
        # Add proper import if not present
        if 'from tkinter import colorchooser' not in fixed_content:
            # Find the tkinter import line
            for i, line in enumerate(lines):
                if 'import tkinter as tk' in line:
                    # Add colorchooser import after tkinter import
                    lines.insert(i + 1, 'from tkinter import colorchooser')
                    break
            
            fixed_content = '\n'.join(lines)
            print("  ✅ Added proper colorchooser import")
        
        # Fix usage
        if 'tk.colorchooser.askcolor' in fixed_content:
            fixed_content = fixed_content.replace('tk.colorchooser.askcolor', 'colorchooser.askcolor')
            print("  ✅ Fixed tk.colorchooser.askcolor references")
        
        # Write back the fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print("  ✅ Applied proper structural fix")
        
        # Verify the fix
        with open(file_path, 'r', encoding='utf-8') as f:
            verify_content = f.read()
        
        if 'from tkinter import colorchooser' in verify_content:
            print("  ✅ Proper import confirmed")
        else:
            print("  ❌ Import fix failed")
        
        if 'tk.colorchooser.askcolor' not in verify_content:
            print("  ✅ Usage fix confirmed")
        else:
            print("  ❌ Usage fix failed")
        
        return True
    else:
        print("\nNO ISSUES FOUND:")
        print("  - No tk.colorchooser usage detected")
        print("  - File may already be properly structured")
        return False

if __name__ == "__main__":
    success = fix_color_utils_properly()
    
    if success:
        print("\n✅ PROPER FIX COMPLETED!")
        print("The colorchooser import issue has been structurally resolved.")
        print("\n🚀 Try running: python main.py")
    else:
        print("\nℹ️  NO FIX NEEDED!")
        print("The color_utils.py file appears to be properly structured.")
