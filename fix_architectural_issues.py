#!/usr/bin/env python3
"""
Fix Architectural Issues - Empty Classes and Constants

This script fixes the 13 architectural issues found in the anomaly analysis:
- 11 empty Event classes (should be @dataclass)
- 2 empty constants classes (should be simple modules)
"""

import os
import re

class ArchitecturalIssueFixer:
    def __init__(self):
        self.event_bus_file = "W:/TomsGPXEditor/src/application/event_bus.py"
        self.property_keys_file = "W:/TomsGPXEditor/src/constants/property_keys.py"
        
    def fix_empty_event_classes(self):
        """Convert empty Event classes to @dataclass"""
        print("Fixing empty Event classes...")
        
        # Read the event bus file
        with open(self.event_bus_file, 'r') as f:
            content = f.read()
        
        # Find all empty Event classes
        event_class_pattern = r'class (\w+Event)\s*:\s*"""([^"]+)"""'
        matches = re.findall(event_class_pattern, content)
        
        fixed_content = content
        for class_name, docstring in matches:
            # Convert to @dataclass
            old_class = f'class {class_name}:\n    """{docstring}"""'
            new_dataclass = f'@dataclass\nclass {class_name}:\n    """{docstring}"""'
            
            fixed_content = fixed_content.replace(old_class, new_dataclass)
            print(f"  - Converted {class_name} to @dataclass")
        
        # Add dataclass import at the top
        if '@dataclass' in fixed_content and 'from dataclasses import dataclass' not in fixed_content:
            fixed_content = 'from dataclasses import dataclass\n\n' + fixed_content
        
        # Write back the fixed content
        with open(self.event_bus_file, 'w') as f:
            f.write(fixed_content)
        
        print(f"Fixed {len(matches)} empty Event classes")
    
    def fix_constants_classes(self):
        """Convert empty constants classes to simple modules"""
        print("Fixing empty constants classes...")
        
        # Read the property keys file
        with open(self.property_keys_file, 'r') as f:
            content = f.read()
        
        # Convert PropertyKeys and Defaults classes to simple constants
        fixed_content = content
        
        # Fix PropertyKeys class
        property_keys_pattern = r'class PropertyKeys\s*:.*?(?=class|\Z)'
        property_keys_replacement = '''# Property Keys - Centralized constants for property paths

# File-related keys
FILES_SESSION = "files.session"

# Dialog-related keys
DIALOGS_SETTINGS = "dialogs.settings"
DIALOGS_LOGGING = "dialogs.settings.logging"
DIALOGS_RENDERING = "dialogs.settings.rendering"
DIALOGS_MARKER = "dialogs.settings.marker"

# App-related keys
APP_MAIN_WINDOW = "app.main_window"
APP_RECENT_FILES = "app.recent_files"

# Session-related keys
SESSION_FILES = "files.session"
SESSION_LEGACY = "files.session.legacy"
'''
        
        matches = re.findall(property_keys_pattern, content, re.DOTALL)
        if matches:
            fixed_content = re.sub(property_keys_pattern, property_keys_replacement, fixed_content, flags=re.DOTALL)
            print("  - Converted PropertyKeys class to constants")
        
        # Fix Defaults class
        defaults_pattern = r'class Defaults\s*:.*?(?=\n\n|\Z)'
        defaults_replacement = '''# Default values for properties

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LINE_WIDTH = 3
DEFAULT_PAGE_SIZE = 1000
DEFAULT_ZOOM_LEVEL = 10
'''
        
        matches = re.findall(defaults_pattern, content, re.DOTALL)
        if matches:
            fixed_content = re.sub(defaults_pattern, defaults_replacement, fixed_content, flags=re.DOTALL)
            print("  - Converted Defaults class to constants")
        
        # Write back the fixed content
        with open(self.property_keys_file, 'w') as f:
            f.write(fixed_content)
        
        print("Fixed constants classes")
    
    def update_imports(self):
        """Update imports in files that use the old classes"""
        print("Updating imports...")
        
        files_to_check = [
            "W:/TomsGPXEditor/src/application/gpx_file_manager.py",
            "W:/TomsGPXEditor/src/infrastructure/map_renderer.py",
            "W:/TomsGPXEditor/src/infrastructure/repositories/properties_repository.py"
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Update PropertyKeys imports
                content = re.sub(
                    r'from src\.constants\.property_keys import PropertyKeys',
                    'from src.constants.property_keys import FILES_SESSION, DIALOGS_SETTINGS',
                    content
                )
                
                # Update PropertyKeys usage
                content = re.sub(r'PropertyKeys\.', '', content)
                
                # Write back
                with open(file_path, 'w') as f:
                    f.write(content)
                
                print(f"  - Updated imports in {os.path.basename(file_path)}")
    
    def fix_all_architectural_issues(self):
        """Fix all architectural issues"""
        print("Starting architectural issues fix...")
        
        # Fix empty Event classes
        self.fix_empty_event_classes()
        
        # Fix constants classes
        self.fix_constants_classes()
        
        # Update imports
        self.update_imports()
        
        print("Architectural issues fix complete!")

def main():
    """Main function to fix architectural issues"""
    fixer = ArchitecturalIssueFixer()
    fixer.fix_all_architectural_issues()

if __name__ == "__main__":
    main()
