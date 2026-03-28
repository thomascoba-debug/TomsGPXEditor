#!/usr/bin/env python3
"""
Test script for DI Container implementation
"""

import sys
sys.path.insert(0, '.')

from src.infrastructure.di_container import DIContainer
from src.infrastructure.container_config import configure_container

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

def test_di_container():
    """Test DI Container functionality"""
    print("=== Testing DI Container ===")
    
    # Create mock app
    app = MockApp()
    
    # Configure container
    try:
        container = configure_container(app)
        print("SUCCESS: Container configured successfully")
        
        # Register UI components manually for test
        container.register_singleton('map_widget', app.map_widget)
        container.register_singleton('main_grid', app.main_grid)
        print("SUCCESS: UI components registered")
        
        # Test service retrieval
        print("SUCCESS: Testing service retrieval:")
        print(f"   - App: {container.get('app')}")
        print(f"   - Properties: {type(container.get('properties'))}")
        print(f"   - Button callback: {container.get('button_update_callback')}")
        
        # Test factory services
        print("SUCCESS: Testing factory services:")
        gpx_manager = container.get('gpx_file_manager')
        print(f"   - GPX Manager: {type(gpx_manager)}")
        
        map_controller = container.get('map_controller')
        print(f"   - Map Controller: {type(map_controller)}")
        
        dialog_controller = container.get('dialog_controller')
        print(f"   - Dialog Controller: {type(dialog_controller)}")
        
        print("SUCCESS: All tests passed!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_di_container()
