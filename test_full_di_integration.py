#!/usr/bin/env python3
"""
Test script for full DI Container integration
"""

import sys
sys.path.insert(0, '.')

def test_full_di_integration():
    """Test full DI Container integration"""
    print("=== Testing Full DI Container Integration ===")
    
    try:
        # Test all imports
        print("Testing imports...")
        from src.infrastructure.di_container import DIContainer
        from src.infrastructure.container_config import configure_container
        from src.application.gpx_file_manager import GPXFileManager
        from src.application.map_controller import MapController
        from src.application.dialog_controller import DialogController
        from src.ui.widgets.file_entry_builder import FileEntryBuilder
        print("SUCCESS: All imports successful")
        
        # Test app creation with container
        print("Testing app creation with container...")
        from app import TomsGPXEditor
        
        # Create app instance (this will initialize the container)
        app = TomsGPXEditor()
        print("SUCCESS: App created with DI Container")
        
        # Test container functionality
        print("Testing container functionality...")
        container = app.container
        
        # Test core services
        print("Testing core services...")
        properties = container.get('properties')
        print(f"SUCCESS: Properties: {type(properties)}")
        
        button_callback = container.get('button_update_callback')
        print(f"SUCCESS: Button callback: {type(button_callback)}")
        
        # Test UI components
        print("Testing UI components...")
        map_widget = container.get('map_widget')
        print(f"SUCCESS: Map widget: {type(map_widget)}")
        
        main_grid = container.get('main_grid')
        print(f"SUCCESS: Main grid: {type(main_grid)}")
        
        # Test controllers
        print("Testing controllers...")
        gpx_manager = app.gpx_file_manager
        print(f"SUCCESS: GPX Manager: {type(gpx_manager)}")
        
        map_controller = app.map_controller
        print(f"SUCCESS: Map Controller: {type(map_controller)}")
        
        dialog_controller = app.dialog_controller
        print(f"SUCCESS: Dialog Controller: {type(dialog_controller)}")
        
        # Test factory methods
        print("Testing factory methods...")
        gpx_manager2 = GPXFileManager.create_from_container(container)
        print(f"SUCCESS: GPX Manager from factory: {type(gpx_manager2)}")
        
        map_controller2 = MapController.create_from_container(container)
        print(f"SUCCESS: Map Controller from factory: {type(map_controller2)}")
        
        dialog_controller2 = DialogController.create_from_container(container)
        print(f"SUCCESS: Dialog Controller from factory: {type(dialog_controller2)}")
        
        print("SUCCESS: All tests passed!")
        print("DI Container integration is working correctly!")
        
    except Exception as e:
        print("ERROR:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_di_integration()
