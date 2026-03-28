#!/usr/bin/env python3
"""
Test script to verify full tree expansion and check for duplicate downsample entries
"""

import sys
sys.path.insert(0, '.')

def test_full_expansion():
    """Test full tree expansion and check duplicate downsample entries"""
    print("=== Testing Full Tree Expansion ===")
    
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
        
        # Test full expansion
        print("Testing full tree expansion...")
        tree = dialog.tree
        
        def count_all_nodes(parent=None):
            """Count all nodes in tree"""
            count = 0
            items = tree.get_children(parent) if parent else tree.get_children()
            for item in items:
                count += 1
                count += count_all_nodes(item)
            return count
        
        total_nodes = count_all_nodes()
        print(f"Total nodes in tree: {total_nodes}")
        
        # Check for downsample duplicates
        print("\nChecking for downsample entries...")
        downsample_entries = []
        
        def find_downsample_entries(parent=None, path=""):
            """Find all entries containing 'downsample'"""
            items = tree.get_children(parent) if parent else tree.get_children()
            for item in items:
                item_text = tree.item(item, "text")
                current_path = f"{path}/{item_text}" if path else item_text
                
                if 'downsample' in item_text.lower():
                    downsample_entries.append(current_path)
                    print(f"Found downsample entry: {current_path}")
                
                # Check children
                find_downsample_entries(item, current_path)
        
        find_downsample_entries()
        
        print(f"\nTotal downsample entries found: {len(downsample_entries)}")
        
        # Show specific downsample values
        print("\nDownsample-related properties in app.properties:")
        for key, value in sorted(app.properties.data.items()):
            if 'downsample' in key.lower():
                print(f"  {key}: {value}")
        
        # Check expansion status
        print("\nChecking expansion status...")
        def check_expansion(parent=None, indent=0):
            """Check if all nodes are expanded"""
            items = tree.get_children(parent) if parent else tree.get_children()
            expanded_count = 0
            total_count = len(items)
            
            for item in items:
                item_text = tree.item(item, "text")
                is_expanded = tree.item(item, "open")
                children = tree.get_children(item)
                
                indent_str = "  " * indent
                if children:
                    status = "EXPANDED" if is_expanded else "COLLAPSED"
                    print(f"{indent_str}- {item_text} ({len(children)} children) - {status}")
                    if is_expanded:
                        expanded_count += 1
                        check_expansion(item, indent + 1)
                else:
                    print(f"{indent_str}- {item_text} (leaf)")
                    expanded_count += 1
            
            return expanded_count, total_count
        
        expanded, total = check_expansion()
        print(f"\nExpansion status: {expanded}/{total} nodes expanded")
        
        # Close dialog
        dialog._close()
        print("\nSUCCESS: Full expansion test completed!")
        print(f"Total nodes: {total_nodes}")
        print(f"Downsample entries: {len(downsample_entries)}")
        print(f"Expansion rate: {expanded}/{total}")
        
    except Exception as e:
        print("ERROR:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_expansion()
