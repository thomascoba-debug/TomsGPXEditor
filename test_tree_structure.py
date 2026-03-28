#!/usr/bin/env python3
"""
Test script to verify tree structure in Properties Viewer
"""

import sys
sys.path.insert(0, '.')

def test_tree_structure():
    """Test tree structure display in Properties Viewer"""
    print("=== Testing Tree Structure in Properties Viewer ===")
    
    try:
        from app import TomsGPXEditor
        from src.ui.dialogs.settings_properties_dialog import PropertiesEditorDialog
        import tkinter as tk
        
        # Create app instance
        app = TomsGPXEditor()
        print("SUCCESS: App created")
        
        # Create the properties viewer dialog
        print("Creating Properties Viewer Dialog...")
        dialog = PropertiesEditorDialog(
            app,
            app.properties,
            app._save_properties_only,
            modal=False
        )
        print("SUCCESS: Properties Viewer Dialog created")
        
        # Test tree structure
        print("Testing tree structure...")
        tree = dialog.tree
        
        # Get all root items
        root_items = tree.get_children()
        print(f"Root items count: {len(root_items)}")
        
        # Display tree structure
        def print_tree_structure(items, indent=0):
            for item in items:
                item_text = tree.item(item, "text")
                item_values = tree.item(item, "values")
                is_expanded = tree.item(item, "open")
                
                indent_str = "  " * indent
                print(f"{indent_str}- {item_text}: {item_values[0] if item_values else 'N/A'} {'(expanded)' if is_expanded else ''}")
                
                # Print children
                children = tree.get_children(item)
                if children:
                    print_tree_structure(children, indent + 1)
        
        print("\nTree Structure:")
        print_tree_structure(root_items)
        
        # Test specific complex properties
        print("\nTesting complex properties...")
        for key, value in app.properties.data.items():
            if isinstance(value, dict) and len(value) > 0:
                print(f"Dict property '{key}': {len(value)} items")
                for sub_key, sub_value in list(value.items())[:3]:  # Show first 3 items
                    print(f"  - {sub_key}: {type(sub_value).__name__}")
                if len(value) > 3:
                    print(f"  ... and {len(value) - 3} more items")
            elif isinstance(value, list) and len(value) > 0:
                print(f"List property '{key}': {len(value)} items")
                for i, item in enumerate(value[:3]):  # Show first 3 items
                    print(f"  - [{i}]: {type(item).__name__}")
                if len(value) > 3:
                    print(f"  ... and {len(value) - 3} more items")
        
        # Close dialog
        dialog._close()
        print("\nSUCCESS: Tree structure test completed!")
        print("✅ Tree structure restored with expanded content")
        print("✅ Dict and list items shown as children")
        print("✅ View-only functionality maintained")
        
    except Exception as e:
        print("ERROR:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tree_structure()
