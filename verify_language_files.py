#!/usr/bin/env python3
"""
Systematic Language Files Verification

This script systematically verifies both language files (de.json and en.json)
to ensure consistency and completeness.
"""

import json
import os

def load_language_files():
    """Load both language files"""
    
    print("LOADING LANGUAGE FILES")
    print("=" * 50)
    
    de_file = "W:/TomsGPXEditor/src/i18n/translations/de.json"
    en_file = "W:/TomsGPXEditor/src/i18n/translations/en.json"
    
    try:
        with open(de_file, 'r', encoding='utf-8') as f:
            de_data = json.load(f)
        
        with open(en_file, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
        
        print("✅ German file loaded successfully")
        print("✅ English file loaded successfully")
        
        return de_data, en_data
        
    except Exception as e:
        print(f"❌ Error loading language files: {e}")
        return None, None

def extract_all_keys(data, prefix=""):
    """Recursively extract all keys from language data"""
    
    keys = {}
    
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                keys.update(extract_all_keys(value, full_key))
            else:
                keys[full_key] = value
    
    return keys

def compare_language_keys(de_keys, en_keys):
    """Compare keys between German and English translations"""
    
    print("\nCOMPARING LANGUAGE KEYS")
    print("=" * 50)
    
    de_key_set = set(de_keys.keys())
    en_key_set = set(en_keys.keys())
    
    # Find missing keys
    missing_in_en = de_key_set - en_key_set
    missing_in_de = en_key_set - de_key_set
    
    # Find common keys
    common_keys = de_key_set & en_key_set
    
    print(f"Total German keys: {len(de_key_set)}")
    print(f"Total English keys: {len(en_key_set)}")
    print(f"Common keys: {len(common_keys)}")
    
    if missing_in_en:
        print(f"\n❌ Missing in English ({len(missing_in_en)}):")
        for key in sorted(missing_in_en):
            print(f"  - {key}: {de_keys[key]}")
    
    if missing_in_de:
        print(f"\n❌ Missing in German ({len(missing_in_de)}):")
        for key in sorted(missing_in_de):
            print(f"  - {key}: {en_keys[key]}")
    
    if not missing_in_en and not missing_in_de:
        print("\n✅ All keys are present in both languages!")
    
    return missing_in_en, missing_in_de, common_keys

def verify_translations(de_keys, en_keys, common_keys):
    """Verify translations for consistency"""
    
    print("\nVERIFYING TRANSLATIONS")
    print("=" * 50)
    
    issues = []
    
    for key in sorted(common_keys):
        de_value = de_keys[key]
        en_value = en_keys[key]
        
        # Check for identical values (might indicate untranslated content)
        if de_value == en_value:
            issues.append(f"⚠️  Same value in both languages: {key} = '{de_value}'")
        
        # Check for empty values
        if not de_value.strip():
            issues.append(f"❌ Empty German value: {key}")
        
        if not en_value.strip():
            issues.append(f"❌ Empty English value: {key}")
        
        # Check for suspicious patterns (German text in English file)
        german_words = ['und', 'der', 'die', 'das', 'für', 'mit', 'von', 'zu', 'auf', 'in', 'an', 'den', 'dem', 'des', 'ein', 'eine', 'einer']
        en_lower = en_value.lower()
        
        if any(word in en_lower for word in german_words) and len(en_value) > 3:
            issues.append(f"⚠️  Possible German in English: {key} = '{en_value}'")
    
    if issues:
        print(f"Found {len(issues)} issues:")
        for issue in issues[:20]:  # Show first 20 issues
            print(f"  {issue}")
        
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more issues")
    else:
        print("✅ No translation issues found!")
    
    return issues

def check_menu_translations(de_data, en_data):
    """Specifically check menu translations"""
    
    print("\nCHECKING MENU TRANSLATIONS")
    print("=" * 50)
    
    menu_sections = ['menu', 'buttons', 'dialog']
    
    for section in menu_sections:
        print(f"\n{section.upper()}:")
        
        if section in de_data and section in en_data:
            de_section = de_data[section]
            en_section = en_data[section]
            
            if isinstance(de_section, dict) and isinstance(en_section, dict):
                for key in sorted(set(de_section.keys()) | set(en_section.keys())):
                    de_value = de_section.get(key, "MISSING")
                    en_value = en_section.get(key, "MISSING")
                    
                    status = "✅"
                    if de_value == "MISSING":
                        status = "❌ DE"
                    elif en_value == "MISSING":
                        status = "❌ EN"
                    elif de_value == en_value and len(de_value) > 3:
                        status = "⚠️"
                    
                    print(f"  {status} {key}: DE='{de_value}' | EN='{en_value}'")
            else:
                print(f"  ❌ Section {section} is not a dictionary")
        else:
            missing = []
            if section not in de_data:
                missing.append("DE")
            if section not in en_data:
                missing.append("EN")
            print(f"  ❌ Missing in: {', '.join(missing)}")

def generate_report(de_data, en_data, missing_in_en, missing_in_de, issues):
    """Generate a comprehensive verification report"""
    
    print("\n" + "=" * 60)
    print("VERIFICATION REPORT")
    print("=" * 60)
    
    report = {
        "timestamp": "2026-03-30 14:31:00",
        "total_keys": {
            "german": len(extract_all_keys(de_data)),
            "english": len(extract_all_keys(en_data))
        },
        "missing_keys": {
            "in_english": len(missing_in_en),
            "in_german": len(missing_in_de)
        },
        "issues_found": len(issues),
        "status": "PASS" if len(missing_in_en) == 0 and len(missing_in_de) == 0 and len(issues) == 0 else "FAIL"
    }
    
    print(f"Status: {report['status']}")
    print(f"Total Keys: DE={report['total_keys']['german']}, EN={report['total_keys']['english']}")
    print(f"Missing Keys: EN={report['missing_keys']['in_english']}, DE={report['missing_keys']['in_german']}")
    print(f"Issues Found: {report['issues_found']}")
    
    if report['status'] == "PASS":
        print("\n🎉 LANGUAGE FILES ARE PERFECT!")
        print("All translations are complete and consistent.")
    else:
        print(f"\n⚠️  LANGUAGE FILES NEED ATTENTION!")
        print(f"Please fix the {report['issues_found']} issues found.")
    
    return report

def main():
    """Main verification function"""
    
    print("SYSTEMATIC LANGUAGE FILES VERIFICATION")
    print("=" * 60)
    
    # Load language files
    de_data, en_data = load_language_files()
    
    if not de_data or not en_data:
        print("❌ Cannot proceed without language files")
        return
    
    # Extract all keys
    de_keys = extract_all_keys(de_data)
    en_keys = extract_all_keys(en_data)
    
    # Compare keys
    missing_in_en, missing_in_de, common_keys = compare_language_keys(de_keys, en_keys)
    
    # Verify translations
    issues = verify_translations(de_keys, en_keys, common_keys)
    
    # Check menu translations specifically
    check_menu_translations(de_data, en_data)
    
    # Generate report
    report = generate_report(de_data, en_data, missing_in_en, missing_in_de, issues)
    
    # Save report
    try:
        with open("W:/TomsGPXEditor/language_verification_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Report saved to: language_verification_report.json")
    except Exception as e:
        print(f"❌ Could not save report: {e}")

if __name__ == "__main__":
    main()
