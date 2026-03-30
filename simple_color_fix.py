#!/usr/bin/env python3
"""
Simple Color Utils Fix - Basic fix without unicode

This script provides a simple fix for the colorchooser issue.
"""

import os

def simple_color_fix():
    """Simple fix for colorchooser issue"""
    
    file_path = "W:/TomsGPXEditor/src/ui/utils/color_utils.py"
    
    # Read current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("SIMPLE COLOR FIX")
    print("=" * 50)
    
    # Check if colorchooser import exists
    if 'from tkinter import colorchooser' in content:
        print("colorchooser import already exists")
        print("No fix needed")
        return True
    
    # Add colorchooser import
    lines = content.split('\n')
    
    # Find tkinter import line and add colorchooser import after it
    for i, line in enumerate(lines):
        if 'import tkinter as tk' in line:
            lines.insert(i + 1, 'from tkinter import colorchooser')
            break
    
    # Write back
    fixed_content = '\n'.join(lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Added colorchooser import")
    print("File updated successfully")
    
    return True

if __name__ == "__main__":
    success = simple_color_fix()
    
    if success:
        print("\nSIMPLE FIX COMPLETED!")
        print("The colorchooser import issue should be resolved.")
        print("\nTry running: python main.py")
