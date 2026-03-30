#!/usr/bin/env python3
"""
Script to check translation completeness and consistency
"""

import json

def load_translations():
    """Load both language files"""
    with open('src/i18n/translations/de.json', 'r', encoding='utf-8') as f:
        de_data = json.load(f)

    with open('src/i18n/translations/en.json', 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    return de_data, en_data

def get_all_keys(data, prefix=''):
    """Get all nested keys as flat list"""
    keys = set()
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f'{prefix}.{key}' if prefix else key
            keys.add(full_key)
            if isinstance(value, dict):
                keys.update(get_all_keys(value, full_key))
    return keys

def get_value(data, key_path):
    """Get value by nested key path"""
    keys = key_path.split('.')
    value = data
    for k in keys:
        value = value.get(k)
    return value

def check_translations():
    """Check translation completeness"""
    de_data, en_data = load_translations()
    
    # Get all keys
    de_keys = get_all_keys(de_data)
    en_keys = get_all_keys(en_data)
    
    # Find missing keys
    missing_in_en = de_keys - en_keys
    missing_in_de = en_keys - de_keys
    
    print('=== SPRACHDATEIEN-VERGLEICH ===')
    print(f'Deutsch: {len(de_keys)} Keys')
    print(f'Englisch: {len(en_keys)} Keys')
    print()
    
    if missing_in_en:
        print('FEHLENDE Keys in Englisch:')
        for key in sorted(missing_in_en):
            print(f'  - {key}')
        print()
    
    if missing_in_de:
        print('FEHLENDE Keys in Deutsch:')
        for key in sorted(missing_in_de):
            print(f'  - {key}')
        print()
    
    # Check for empty or untranslated values
    empty_values = []
    same_values = []
    
    for key in sorted(de_keys):
        de_val = get_value(de_data, key)
        en_val = get_value(en_data, key)
        
        if not de_val or not str(de_val).strip():
            empty_values.append(f'DE: {key}')
        if not en_val or not str(en_val).strip():
            empty_values.append(f'EN: {key}')
        elif de_val == en_val and str(de_val).strip():
            same_values.append(key)
    
    print('=== UEBERSETZUNGS-CHECK ===')
    print(f'Gesamt: {len(de_keys)} Keys')
    print()
    
    if empty_values:
        print('LEERE Werte:')
        for item in sorted(empty_values):
            print(f'  - {item}')
        print()
    
    if same_values:
        print('GLEICHE Werte (vielleicht unuebersetzt):')
        for key in sorted(same_values):
            de_val = get_value(de_data, key)
            print(f'  - {key}: \"{de_val}\"')
        print()
    
    # Summary
    total_issues = len(missing_in_en) + len(missing_in_de) + len(empty_values) + len(same_values)
    
    if total_issues == 0:
        print('OK: Alle Werte sind ausgefuellt und unterschiedlich!')
    else:
        print(f'WARNUNG: {len(missing_in_en) + len(missing_in_de)} fehlende, {len(empty_values)} leere, {len(same_values)} gleiche Werte')
        print(f'Gesamt: {total_issues} Probleme')
    
    return total_issues == 0

if __name__ == "__main__":
    check_translations()
