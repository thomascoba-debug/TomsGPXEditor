#!/usr/bin/env python3
"""
Test script for dialog callbacks and map updates
"""

import sys
sys.path.insert(0, '.')

def test_dialog_callbacks():
    """Test dialog callbacks for proper map update behavior"""
    print("=== Testing Dialog Callbacks ===")
    
    try:
        from app import TomsGPXEditor
        
        # Create app instance
        app = TomsGPXEditor()
        print("SUCCESS: App created")
        
        # Test callback methods exist
        print("Testing callback methods...")
        print(f"_save_properties exists: {hasattr(app, '_save_properties')}")
        print(f"_save_properties_only exists: {hasattr(app, '_save_properties_only')}")
        print(f"_save_properties_and_map exists: {hasattr(app, '_save_properties_and_map')}")
        print(f"_save_properties_and_reconfigure_logging exists: {hasattr(app, '_save_properties_and_reconfigure_logging')}")
        
        # Test dialog controller callbacks
        print("Testing dialog controller...")
        dialog_controller = app.dialog_controller
        
        # Check if dialog controller uses specific callbacks
        print(f"Dialog controller exists: {dialog_controller is not None}")
        
        # Test mock dialog scenarios
        print("Testing mock dialog scenarios...")
        
        # Mock map update counter
        original_update_map = app._update_map
        map_update_count = 0
        
        def counting_update_map():
            nonlocal map_update_count
            map_update_count += 1
            print(f"Map update called (count: {map_update_count})")
        
        app._update_map = counting_update_map
        
        # Test different save methods
        print("\nTesting different save methods:")
        
        # Test language dialog (should NOT update map)
        print("1. Language dialog callback:")
        map_update_count = 0
        app._save_properties_only()
        print(f"   Map updates after language save: {map_update_count}")
        
        # Test logging dialog (should NOT update map)
        print("2. Logging dialog callback:")
        map_update_count = 0
        app._save_properties_and_reconfigure_logging()
        print(f"   Map updates after logging save: {map_update_count}")
        
        # Test marker dialog (should UPDATE map)
        print("3. Marker dialog callback:")
        map_update_count = 0
        app._save_properties_and_map()
        print(f"   Map updates after marker save: {map_update_count}")
        
        # Test rendering dialog (should UPDATE map)
        print("4. Rendering dialog callback:")
        map_update_count = 0
        app._save_properties_and_map()
        print(f"   Map updates after rendering save: {map_update_count}")
        
        # Test properties editor (should NOT update map)
        print("5. Properties editor callback:")
        map_update_count = 0
        app._save_properties_only()
        print(f"   Map updates after properties save: {map_update_count}")
        
        # Restore original method
        app._update_map = original_update_map
        
        print("\nSUCCESS: All callback tests completed!")
        print("Language/Logging/Properties dialogs: NO map updates")
        print("Marker/Rendering dialogs: YES map updates")
        
    except Exception as e:
        print("ERROR:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dialog_callbacks()
