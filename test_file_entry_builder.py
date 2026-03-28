#!/usr/bin/env python3
"""
Test script for FileEntryBuilder with DI Container
"""

import sys
sys.path.insert(0, '.')

def test_file_entry_builder():
    """Test FileEntryBuilder with DI Container"""
    print("=== Testing FileEntryBuilder with DI Container ===")
    
    try:
        from src.infrastructure.di_container import DIContainer
        from src.ui.widgets.file_entry_builder import FileEntryBuilder
        from src.infrastructure.repositories.properties_repository import AppProperties
        
        # Create mock container
        container = DIContainer()
        container.register_singleton('button_update_callback', lambda: print('Button update'))
        container.register_singleton('editable_update_callback', lambda: print('Editable update'))
        
        # Test FileEntryBuilder creation
        print("Testing FileEntryBuilder creation...")
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        frame = tk.Frame(root)
        builder = FileEntryBuilder.create_from_container(frame, 1, container)
        print(f"SUCCESS: FileEntryBuilder created: {type(builder)}")
        
        # Test callback access
        print("Testing callback access...")
        print(f"Button callback exists: {hasattr(builder, 'button_update_callback')}")
        print(f"Editable callback exists: {hasattr(builder, 'editable_update_callback')}")
        
        # Test mini-container creation
        print("Testing mini-container creation...")
        mini_container = DIContainer()
        mini_container.register_singleton('button_update_callback', lambda: print('Mini button update'))
        mini_container.register_singleton('editable_update_callback', lambda: print('Mini editable update'))
        
        builder2 = FileEntryBuilder.create_from_container(frame, 2, mini_container)
        print(f"SUCCESS: Second FileEntryBuilder created: {type(builder2)}")
        
        root.destroy()
        print("SUCCESS: All tests passed!")
        
    except Exception as e:
        print("ERROR:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_file_entry_builder()
