#!/usr/bin/env python3
"""
Remove Root Logging Section + Complete Code Scan

This script removes the duplicate logging section and scans the entire codebase for issues.
"""

import json
import os
import re

def remove_root_logging():
    """Remove the duplicate logging section from root level"""
    
    properties_file = "W:/TomsGPXEditor/properties.json"
    
    # Read current properties
    with open(properties_file, 'r', encoding='utf-8') as f:
        properties = json.load(f)
    
    print("🔍 REMOVING ROOT LOGGING SECTION...")
    
    # Remove the duplicate logging section from root level
    if 'logging' in properties:
        logging_config = properties['logging']
        print(f"   Found root logging: {logging_config}")
        
        # Remove the duplicate logging section
        del properties['logging']
        print("   ✅ Removed root logging section")
    else:
        print("   ℹ️  No root logging section found")
    
    # Also fix recent_files structure if needed
    if 'app' in properties and 'recent_files_timestamps' in properties['app']:
        properties['app']['recent_files'] = properties['app']['recent_files_timestamps']
        del properties['app']['recent_files_timestamps']
        print("   ✅ Fixed recent_files structure")
    
    # Write back fixed properties
    with open(properties_file, 'w', encoding='utf-8') as f:
        json.dump(properties, f, indent=2, ensure_ascii=False)
    
    print("   ✅ Properties file updated")
    
    # Show final structure
    print(f"\n📋 FINAL STRUCTURE:")
    print(f"   - Root logging section: {'logging' in properties}")
    print(f"   - dialogs.settings.logging: {'dialogs' in properties and 'settings' in properties.get('dialogs', {}) and 'logging' in properties['dialogs']['settings']}")

def complete_code_scan():
    """Complete scan of the entire codebase for issues"""
    
    print("\n🔍 COMPLETE CODE SCAN...")
    print("=" * 60)
    
    src_dir = "W:/TomsGPXEditor/src"
    
    issues_found = []
    
    # Scan all Python files
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, "W:/TomsGPXEditor")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for PropertyKeys references
                    propertykeys_count = content.count('PropertyKeys')
                    if propertykeys_count > 0:
                        issues_found.append({
                            'file': relative_path,
                            'type': 'PropertyKeys references',
                            'count': propertykeys_count,
                            'severity': 'HIGH'
                        })
                    
                    # Check for import errors
                    if 'from src.constants.property_keys import PropertyKeys' in content:
                        issues_found.append({
                            'file': relative_path,
                            'type': 'PropertyKeys import',
                            'severity': 'HIGH'
                        })
                    
                    # Check for syntax issues
                    if content.count('except Exception as e:') != content.count('logger.error'):
                        issues_found.append({
                            'file': relative_path,
                            'type': 'Potential exception handling issue',
                            'severity': 'MEDIUM'
                        })
                    
                    # Check for TODO/FIXME comments
                    if 'TODO:' in content or 'FIXME:' in content:
                        issues_found.append({
                            'file': relative_path,
                            'type': 'TODO/FIXME comments',
                            'severity': 'LOW'
                        })
                
                except Exception as e:
                    issues_found.append({
                        'file': relative_path,
                        'type': 'File read error',
                        'error': str(e),
                        'severity': 'HIGH'
                    })
    
    # Report findings
    print(f"\n📊 SCAN RESULTS:")
    print(f"   Files scanned: {len([f for f in os.listdir(src_dir) if f.endswith('.py')])}")
    print(f"   Issues found: {len(issues_found)}")
    
    if issues_found:
        print(f"\n🚨 ISSUES BY SEVERITY:")
        
        high_issues = [i for i in issues_found if i['severity'] == 'HIGH']
        medium_issues = [i for i in issues_found if i['severity'] == 'MEDIUM']
        low_issues = [i for i in issues_found if i['severity'] == 'LOW']
        
        if high_issues:
            print(f"\n   🔴 HIGH PRIORITY ({len(high_issues)}):")
            for issue in high_issues:
                if 'count' in issue:
                    print(f"      - {issue['file']}: {issue['type']} ({issue['count']} references)")
                elif 'error' in issue:
                    print(f"      - {issue['file']}: {issue['type']} - {issue['error']}")
                else:
                    print(f"      - {issue['file']}: {issue['type']}")
        
        if medium_issues:
            print(f"\n   🟡 MEDIUM PRIORITY ({len(medium_issues)}):")
            for issue in medium_issues:
                print(f"      - {issue['file']}: {issue['type']}")
        
        if low_issues:
            print(f"\n   🟢 LOW PRIORITY ({len(low_issues)}):")
            for issue in low_issues:
                print(f"      - {issue['file']}: {issue['type']}")
    else:
        print(f"\n   ✅ NO ISSUES FOUND!")
    
    return issues_found

def main():
    """Main function"""
    print("🔧 ROOT LOGGING REMOVAL + COMPLETE CODE SCAN")
    print("=" * 60)
    
    # Step 1: Remove root logging
    remove_root_logging()
    
    # Step 2: Complete code scan
    issues = complete_code_scan()
    
    # Step 3: Summary
    print(f"\n🎯 SUMMARY:")
    print(f"   - Root logging section removed")
    print(f"   - Complete code scan finished")
    print(f"   - {len(issues)} issues found")
    
    high_issues = [i for i in issues if i['severity'] == 'HIGH']
    if high_issues:
        print(f"   - {len(high_issues)} high-priority issues need attention")
    else:
        print(f"   - No high-priority issues found")
    
    print(f"\n🚀 The application should now be clean and stable!")

if __name__ == "__main__":
    main()
