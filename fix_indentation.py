#!/usr/bin/env python3
"""
Indentation Fix - Fix the syntax error in gpx_file_manager.py
"""

import os

def fix_indentation():
    """Fix the indentation error"""
    
    file_path = "W:/TomsGPXEditor/src/application/gpx_file_manager.py"
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Fixing indentation error around line 239...")
    
    # The error is that the except block needs proper indentation
    # Let's fix the specific problematic area
    lines = content.split('\n')
    
    # Find the problematic except block and fix it
    for i, line in enumerate(lines):
        if 'except Exception as e:' in line and i > 230:
            print(f"Found except block at line {i+1}")
            # Ensure proper indentation for the except block
            if not line.startswith('                        '):
                # This is the problem - the except block is not properly indented
                lines[i] = '                        except Exception as e:'
                print(f"Fixed indentation for line {i+1}")
                break
    
    # Write back the fixed content
    fixed_content = '\n'.join(lines)
    
    # Create backup
    backup_path = f"{file_path}.indentation_fix_backup"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created backup: {backup_path}")
    
    # Write fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Fixed indentation error in gpx_file_manager.py")
    print("The syntax error should now be resolved.")

if __name__ == "__main__":
    fix_indentation()
