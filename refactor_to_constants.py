#!/usr/bin/env python3
"""
Refactor String Literals to Constants
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Property mappings
MAPPINGS = {
    # App level
    r'"app\.version"': 'APP_VERSION',
    r'"app\.main_window"': 'APP_MAIN_WINDOW',
    r'"app\.recent_files_timestamps"': 'APP_RECENT_FILES',
    
    # Session level
    r'"session_files"': 'SESSION_FILES',
    r'"files\.session"': 'FILES_SESSION',
    
    # Dialog level
    r'"dialogs\.geometry"': 'DIALOGS_GEOMETRY',
    r'"dialogs\.settings"': 'DIALOGS_SETTINGS',
    
    # Conversion level
    r'"dialogs\.settings\.conversion"': 'CONVERSION_ROOT',
    r'"downsample"': 'DOWNSAMPLE',
    r'"route_to_track"': 'ROUTE_TO_TRACK',
    r'"track_to_route"': 'TRACK_TO_ROUTE',
    
    # Rendering level
    r'"dialogs\.settings\.rendering"': 'RENDERING_ROOT',
    r'"waypoints"': 'WAYPOINTS',
    r'"trackpoints"': 'TRACKPOINTS',
    r'"routepoints"': 'ROUTEPOINTS',
    
    # Logging level
    r'"dialogs\.settings\.logging"': 'LOGGING_ROOT',
    r'"level"': 'LOG_LEVEL',
    r'"file"': 'LOG_FILE',
    
    # Map settings
    r'"track_to_route_points_per_100km"': 'TRACK_TO_ROUTE_POINTS_PER_100KM',
    r'"route_to_track\.points_per_100km"': 'ROUTE_TO_TRACK_POINTS_PER_100KM',
}

# Function to add import
IMPORT_TEMPLATE = """from src.constants.property_keys import {constant}"""

def find_string_literals_in_file(file_path: Path) -> List[Tuple[str, int, str]]:
    """Find string literals in a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        issues = []
        for line_num, line in enumerate(lines, 1):
            for pattern, constant in MAPPINGS.items():
                if re.search(pattern, line):
                    issues.append((str(file_path), line_num, line.strip()))
                    break
        
        return issues
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def generate_imports(used_constants: set) -> str:
    """Generate import statements for used constants"""
    imports = []
    for constant in used_constants:
        imports.append(IMPORT_TEMPLATE.format(constant=constant))
    return "\n".join(imports)

def update_file(file_path: Path, issues: List[Tuple[str, int, str]]) -> bool:
    """Update file with constants"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add imports at the top
        lines = content.split('\n')
        
        # Find insertion point after existing imports
        insert_line = 0
        for i, line in enumerate(lines):
            if line.startswith('from ') or line.startswith('import '):
                insert_line = i + 1
            elif line.strip() == '' and i > insert_line:
                break
        
        # Generate required imports
        used_constants = set()
        for pattern, constant in MAPPINGS.items():
            for _, _, line_content in issues:
                if re.search(pattern, line_content):
                    used_constants.add(constant)
        
        if used_constants:
            imports = generate_imports(used_constants)
            lines.insert(insert_line, imports)
            lines.insert(insert_line, '')  # Empty line after imports
        
        # Replace string literals with constants
        updated_lines = []
        for line in lines:
            updated_line = line
            for pattern, constant in MAPPINGS.items():
                updated_line = re.sub(pattern, f'PropertyKeys.APP.{constant}', updated_line)
            updated_lines.append(updated_line)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_lines))
        
        return True
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    """Main refactor function"""
    print("Refactoring String Literals to Constants...")
    
    src_dir = Path("src")
    
    # Find all Python files
    python_files = list(src_dir.rglob("*.py"))
    
    total_issues = 0
    total_files = 0
    
    for file_path in python_files:
        # Skip the constants file itself
        if file_path.name == "property_keys.py":
            continue
        
        print(f"Processing: {file_path}")
        issues = find_string_literals_in_file(file_path)
        
        if issues:
            print(f"  Found {len(issues)} issues in {file_path.name}")
            total_issues += len(issues)
            
            if update_file(file_path, issues):
                print(f"  Updated {file_path.name}")
            else:
                print(f"  Failed to update {file_path.name}")
        else:
            print(f"  No issues found in {file_path.name}")
        
        total_files += 1
    
    print(f"\nSummary:")
    print(f"  Files processed: {total_files}")
    print(f"  Total issues found: {total_issues}")
    print(f"  Files updated: {len([f for f in python_files if find_string_literals_in_file(f)])}")
    
    if total_issues > 0:
        print(f"\nRefactoring completed! {total_issues} string literals replaced with constants.")
        print("\nNext steps:")
        print("1. Review the changes")
        print("2. Test the application")
        print("3. Commit the changes")
    else:
        print("\nNo string literals found that need refactoring!")

if __name__ == "__main__":
    main()
