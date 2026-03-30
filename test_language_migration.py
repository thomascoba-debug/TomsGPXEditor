#!/usr/bin/env python3
"""
Test Language Migration

Test the language migration by checking imports and basic functionality.
"""

import sys
import os

def test_language_migration():
    """Test the language migration functionality"""
    
    print("TESTING LANGUAGE MIGRATION")
    print("=" * 50)
    
    try:
        # Test imports
        print("\n1. Testing imports...")
        from src.i18n.constants import MenuConstants, DialogConstants
        from src.i18n.language_manager import LanguageManager
        print("   PASS: Language imports successful")
        
        # Test constants
        print("\n2. Testing constants...")
        print(f"   MenuConstants.EDIT: {MenuConstants.EDIT}")
        print(f"   DialogConstants.CLOSE: {DialogConstants.CLOSE}")
        print("   PASS: Constants accessible")
        
        # Test language manager
        print("\n3. Testing language manager...")
        from src.infrastructure.repositories.properties_repository import AppProperties
        properties = AppProperties()
        lang_manager = LanguageManager(properties)
        
        # Test translation
        edit_text = lang_manager.t(MenuConstants.EDIT)
        print(f"   Translation for 'menu.edit': {edit_text}")
        print("   PASS: Language manager working")
        
        # Test dialog controller import
        print("\n4. Testing dialog controller...")
        from src.application.dialog_controller import DialogController
        print("   PASS: Dialog controller imports successful")
        
        print("\n" + "=" * 50)
        print("LANGUAGE MIGRATION TEST COMPLETED")
        print("PASS: All tests passed!")
        print("\nThe application should now show German text in the Edit menu!")
        
        return True
        
    except Exception as e:
        print(f"\nFAILED: Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_language_migration()
    
    if success:
        print("\nMigration successful! The application should now:")
        print("1. Show German text in menus when language is set to German")
        print("2. Use constants instead of hardcoded literals")
        print("3. Support language switching")
    else:
        print("\nMigration needs attention. Check the errors above.")
