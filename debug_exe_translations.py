#!/usr/bin/env python3
"""
Debug script for EXE translation issues
"""

import sys
import os

def test_pyinstaller_paths():
    """Test if PyInstaller paths work correctly"""
    print("=== PyInstaller Path Debug ===")
    print(f"sys.frozen: {getattr(sys, 'frozen', False)}")
    
    if getattr(sys, 'frozen', False):
        print(f"sys._MEIPASS: {sys._MEIPASS}")
        
        # Test translation file paths
        de_file = os.path.join(sys._MEIPASS, "src", "i18n", "translations", "de.json")
        en_file = os.path.join(sys._MEIPASS, "src", "i18n", "translations", "en.json")
        
        print(f"German file path: {de_file}")
        print(f"German file exists: {os.path.exists(de_file)}")
        
        print(f"English file path: {en_file}")
        print(f"English file exists: {os.path.exists(en_file)}")
        
        # List contents of translations directory
        trans_dir = os.path.join(sys._MEIPASS, "src", "i18n", "translations")
        if os.path.exists(trans_dir):
            print(f"Translation directory contents: {os.listdir(trans_dir)}")
        else:
            print(f"Translation directory does not exist: {trans_dir}")
            
        # List contents of src/i18n directory
        i18n_dir = os.path.join(sys._MEIPASS, "src", "i18n")
        if os.path.exists(i18n_dir):
            print(f"I18n directory contents: {os.listdir(i18n_dir)}")
            
        # List contents of src directory
        src_dir = os.path.join(sys._MEIPASS, "src")
        if os.path.exists(src_dir):
            print(f"Src directory contents: {os.listdir(src_dir)}")
            
        # List root contents
        print(f"Root directory contents: {os.listdir(sys._MEIPASS)}")
    else:
        print("Running in normal Python environment")

if __name__ == "__main__":
    test_pyinstaller_paths()
