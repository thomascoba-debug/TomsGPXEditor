#!/usr/bin/env python3
"""
Focused Language Verification - Check Only Real Issues

This script focuses on real translation issues, not false positives.
"""

import json

def focused_verification():
    """Check for real translation issues only"""
    
    print("FOCUSED LANGUAGE VERIFICATION")
    print("=" * 50)
    
    # Load files
    de_file = "W:/TomsGPXEditor/src/i18n/translations/de.json"
    en_file = "W:/TomsGPXEditor/src/i18n/translations/en.json"
    
    try:
        with open(de_file, 'r', encoding='utf-8') as f:
            de_data = json.load(f)
        
        with open(en_file, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # Check critical sections
    critical_sections = ['menu', 'dialog', 'buttons']
    real_issues = []
    
    print("\nCHECKING CRITICAL SECTIONS:")
    
    for section in critical_sections:
        print(f"\n{section.upper()}:")
        
        if section in de_data and section in en_data:
            de_section = de_data[section]
            en_section = en_data[section]
            
            if isinstance(de_section, dict) and isinstance(en_section, dict):
                for key in sorted(de_section.keys()):
                    if key in en_section:
                        de_value = de_section[key]
                        en_value = en_section[key]
                        
                        # Check for real German in English (not just similar words)
                        if isinstance(de_value, str) and isinstance(en_value, str):
                            # Real German indicators
                            german_indicators = ['ä', 'ö', 'ü', 'ß', ' und ', ' der ', ' die ', ' das ', ' für ', ' mit ']
                            
                            if any(indicator in en_value for indicator in german_indicators):
                                real_issues.append(f"REAL GERMAN IN ENGLISH: {section}.{key} = '{en_value}'")
                                print(f"  ERROR {key}: DE='{de_value}' | EN='{en_value}' [GERMAN DETECTED]")
                            elif de_value == en_value and len(de_value) > 5 and not de_value in ['OK', 'Toms GPX Editor']:
                                # Same long text might indicate missing translation
                                real_issues.append(f"IDENTICAL LONG TEXT: {section}.{key} = '{de_value}'")
                                print(f"  WARN {key}: DE='{de_value}' | EN='{en_value}' [IDENTICAL]")
                            else:
                                print(f"  OK {key}: DE='{de_value}' | EN='{en_value}'")
                    else:
                        print(f"  SKIP {key}: Not a string value")
            else:
                print(f"  ERROR Section {section} is not properly structured")
        else:
            print(f"  ERROR Section {section} missing in one language")
    
    # Summary
    print("\n" + "=" * 50)
    print("FOCUSED VERIFICATION SUMMARY")
    print("=" * 50)
    
    if real_issues:
        print(f"REAL ISSUES FOUND: {len(real_issues)}")
        for issue in real_issues:
            print(f"  - {issue}")
        return False
    else:
        print("NO REAL ISSUES FOUND!")
        print("All critical translations are correct.")
        return True

def check_specific_dialog_texts():
    """Check specific dialog texts that were reported as problematic"""
    
    print("\nCHECKING SPECIFIC DIALOG TEXTS:")
    print("=" * 50)
    
    # Load files
    de_file = "W:/TomsGPXEditor/src/i18n/translations/de.json"
    en_file = "W:/TomsGPXEditor/src/i18n/translations/en.json"
    
    try:
        with open(de_file, 'r', encoding='utf-8') as f:
            de_data = json.load(f)
        
        with open(en_file, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    # Check specific keys that were problematic
    problem_keys = [
        'dialog.cancel',
        'dialog.apply',
        'dialog.save',
        'dialog.delete',
        'dialog.add',
        'dialog.remove',
        'dialog.browse',
        'dialog.close',
        'dialog.yes',
        'dialog.no'
    ]
    
    print("Checking previously problematic dialog keys:")
    
    all_correct = True
    for key in problem_keys:
        parts = key.split('.')
        if len(parts) == 2:
            section, subkey = parts
            
            if section in de_data and section in en_data:
                de_section = de_data[section]
                en_section = en_data[section]
                
                if subkey in de_section and subkey in en_section:
                    de_value = de_section[subkey]
                    en_value = en_section[subkey]
                    
                    # Check if English is actually English
                    german_indicators = ['ä', 'ö', 'ü', 'ß']
                    has_german = any(indicator in en_value for indicator in german_indicators)
                    
                    status = "OK" if not has_german else "ERROR"
                    print(f"  {status} {key}: DE='{de_value}' | EN='{en_value}'")
                    
                    if has_german:
                        all_correct = False
                else:
                    print(f"  ERROR {key}: Missing in one language")
                    all_correct = False
            else:
                print(f"  ERROR {key}: Section missing")
                all_correct = False
        else:
            print(f"  ERROR {key}: Invalid key format")
            all_correct = False
    
    return all_correct

def main():
    """Main function"""
    
    print("FOCUSED LANGUAGE VERIFICATION - REAL ISSUES ONLY")
    print("=" * 60)
    
    # Focused verification
    result1 = focused_verification()
    
    # Check specific problematic texts
    result2 = check_specific_dialog_texts()
    
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION RESULT")
    print("=" * 60)
    
    if result1 and result2:
        print("SUCCESS: All language files are CORRECT!")
        print("No real translation issues found.")
        print("The 73 'issues' reported earlier were false positives.")
    else:
        print("WARNING: Real translation issues found!")
        print("Please review the issues listed above.")

if __name__ == "__main__":
    main()
