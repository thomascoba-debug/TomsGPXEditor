#!/usr/bin/env python3
"""
Test script for app startup with DI Container
"""

import sys
sys.path.insert(0, '.')

def test_app_startup():
    """Test app startup without GUI"""
    print("=== Testing App Startup ===")
    
    try:
        # Test imports
        print("Testing imports...")
        from src.infrastructure.di_container import DIContainer
        from src.infrastructure.container_config import configure_container
        from src.application.gpx_file_manager import GPXFileManager
        from src.application.map_controller import MapController
        from src.application.dialog_controller import DialogController
        print("SUCCESS: All imports successful")
        
        # Test container configuration
        print("Testing container configuration...")
        class MockApp:
            def __init__(self):
                self.map_widget = 'mock_map_widget'
                self.main_grid = 'mock_main_grid'
                self.properties = None
                
            def _update_conversion_buttons(self):
                print("Button update called")
                
            def _update_editable_buttons_only(self):
                print("Editable update called")
                
            def _update_map(self):
                print("Map update called")
                
            def _update_visibility_only(self):
                print("Visibility update called")
                
            def _save_properties(self):
                print("Save properties called")
        
        app = MockApp()
        container = configure_container(app)
        container.register_singleton('map_widget', app.map_widget)
        container.register_singleton('main_grid', app.main_grid)
        print("SUCCESS: Container configured")
        
        # Test controller creation
        print("Testing controller creation...")
        gpx_manager = GPXFileManager.create_from_container(container)
        print(f"SUCCESS: GPX Manager created: {type(gpx_manager)}")
        
        map_controller = MapController.create_from_container(container)
        print(f"SUCCESS: Map Controller created: {type(map_controller)}")
        
        dialog_controller = DialogController.create_from_container(container)
        print(f"SUCCESS: Dialog Controller created: {type(dialog_controller)}")
        
        print("SUCCESS: All tests passed!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_app_startup()
