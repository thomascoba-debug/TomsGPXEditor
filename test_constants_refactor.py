#!/usr/bin/env python3
"""
Test the constants refactoring
"""

import sys
sys.path.insert(0, '.')

def test_constants_import():
    """Test if constants can be imported"""
    try:
        from src.constants.property_keys import PropertyKeys, Defaults
        print("SUCCESS: Constants imported successfully")
        
        # Test some key constants
        print(f"APP.RECENT_FILES: {PropertyKeys.APP.RECENT_FILES}")
        print(f"SESSION.FILES: {PropertyKeys.SESSION.FILES}")
        print(f"DIALOGS.SETTINGS: {PropertyKeys.DIALOG.SETTINGS}")
        
        return True
    except Exception as e:
        print(f"ERROR: Failed to import constants: {e}")
        return False

def test_app_imports():
    """Test if app modules can import constants"""
    try:
        from src.application.services.recent_files_service import RecentFilesFromSessionManager
        from src.infrastructure.repositories.properties_repository import AppProperties
        from src.config.app_config import AppConfig
        
        print("SUCCESS: App modules import constants successfully")
        
        # Test instantiation
        props = AppProperties()
        recent_manager = RecentFilesFromSessionManager(props)
        
        print("SUCCESS: Module instantiation works")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to test app imports: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_startup():
    """Test if app starts with new constants"""
    try:
        from app import TomsGPXEditor
        
        print("Creating app with new constants...")
        app = TomsGPXEditor()
        
        print("SUCCESS: App created with new constants")
        
        # Test some basic functionality
        recent_files = app.recent_files_manager.get_recent_files()
        print(f"Recent files count: {len(recent_files)}")
        
        # Test properties access
        version = app.properties.get("app.version", "unknown")
        print(f"App version: {version}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to start app with new constants: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("=== Testing Constants Refactoring ===")
    
    tests = [
        ("Constants Import", test_constants_import),
        ("App Module Imports", test_app_imports),
        ("App Startup", test_app_startup),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    print(f"\n=== Test Results ===")
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\nALL TESTS PASSED! Constants refactoring successful!")
        return 0
    else:
        print("\nSOME TESTS FAILED! Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
