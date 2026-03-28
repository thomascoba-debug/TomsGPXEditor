"""
Properties Editor Dialog - View Only
Shows all application properties in a read-only format
"""

import tkinter as tk
from tkinter import ttk
import logging

from src.ui.base import PersistentDialog

logger = logging.getLogger(__name__)


class PropertiesEditorDialog(PersistentDialog):
    """View-only dialog for displaying application properties"""

    def __init__(self, parent, properties, save_callback, modal=False):
        logger.debug(f"__init__ START: parent={type(parent).__name__}, properties keys={list(properties.data.keys())}")
        super().__init__(parent, properties, "PropertiesEditorDialog", modal=modal)
        
        self.save_callback = save_callback
        self.title("Properties Viewer")
        logger.debug(f"Dialog title gesetzt")
        
        # Store original data for reference (not used in view-only)
        self.original_data = dict(properties.data)
        
        # Create main frame
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add title
        title_label = ttk.Label(frame, text="Application Properties", font=("TkDefaultFont", 12, "bold"))
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Create treeview container that can expand
        tree_container = ttk.Frame(frame)
        tree_container.pack(fill="both", expand=True)
        
        # Create treeview for properties display
        columns = ("value",)
        self.tree = ttk.Treeview(tree_container, columns=columns, show="tree headings", height=20)
        
        # Configure columns
        self.tree.heading("#0", text="Property Key")
        self.tree.heading("value", text="Value")
        
        self.tree.column("#0", width=200)
        self.tree.column("value", width=400)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar in their container
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate treeview with properties
        self._populate_treeview()
        
        # Buttons - Only Close button for view-only dialog (below treeview)
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", side="bottom", pady=(10, 0))
        btn_frame.columnconfigure(0, weight=1)
        
        ttk.Button(btn_frame, text="Close", command=self._close).grid(row=0, column=0, padx=5)
        
        logger.debug(f"Properties Viewer Dialog completed")
    
    def _populate_treeview(self):
        """Populate treeview with all properties in expanded tree structure"""
        logger.debug(f"_populate_treeview START")
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add all properties with tree structure
        count = 0
        for key, value in sorted(self.properties.data.items()):
            if isinstance(value, dict):
                # Add dict as parent node
                parent_item = self.tree.insert("", "end", text=key, values=(f"{{dict}} {len(value)} items",))
                count += 1
                
                # Add dict items as children
                for dict_key, dict_value in sorted(value.items()):
                    if isinstance(dict_value, dict):
                        child_item = self.tree.insert(parent_item, "end", text=dict_key, values=(f"{{dict}} {len(dict_value)} items",))
                        self._add_dict_children(child_item, dict_value)
                        count += 1
                    elif isinstance(dict_value, list):
                        child_item = self.tree.insert(parent_item, "end", text=dict_key, values=(f"[list] {len(dict_value)} items",))
                        self._add_list_children(child_item, dict_value)
                        count += 1
                    else:
                        display_value = str(dict_value)[:100] + "..." if len(str(dict_value)) > 100 else str(dict_value)
                        self.tree.insert(parent_item, "end", text=dict_key, values=(display_value,))
                        count += 1
                
                # Expand dict node
                self.tree.item(parent_item, open=True)
                
            elif isinstance(value, list):
                # Add list as parent node
                parent_item = self.tree.insert("", "end", text=key, values=(f"[list] {len(value)} items",))
                count += 1
                
                # Add list items as children
                self._add_list_children(parent_item, value)
                count += len(value)
                
                # Expand list node
                self.tree.item(parent_item, open=True)
                
            else:
                # Add simple value
                display_value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                self.tree.insert("", "end", text=key, values=(display_value,))
                count += 1
        
        logger.debug(f"Populated {count} properties in treeview")
        
        # Expand all tree nodes
        self._expand_all_nodes()
    
    def _expand_all_nodes(self):
        """Expand all tree nodes recursively"""
        def expand_children(parent):
            for child in self.tree.get_children(parent):
                self.tree.item(child, open=True)
                expand_children(child)
        
        # Expand all root items
        for root_item in self.tree.get_children():
            self.tree.item(root_item, open=True)
            expand_children(root_item)
    
    def _add_dict_children(self, parent_item, dict_data):
        """Add dict children to treeview"""
        for key, value in sorted(dict_data.items()):
            if isinstance(value, dict):
                child_item = self.tree.insert(parent_item, "end", text=key, values=(f"{{dict}} {len(value)} items",))
                self._add_dict_children(child_item, value)
            elif isinstance(value, list):
                child_item = self.tree.insert(parent_item, "end", text=key, values=(f"[list] {len(value)} items",))
                self._add_list_children(child_item, value)
            else:
                display_value = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                self.tree.insert(parent_item, "end", text=key, values=(display_value,))
    
    def _add_list_children(self, parent_item, list_data):
        """Add list children to treeview"""
        for i, item in enumerate(list_data):
            if isinstance(item, dict):
                child_item = self.tree.insert(parent_item, "end", text=f"[{i}]", values=(f"{{dict}} {len(item)} items",))
                self._add_dict_children(child_item, item)
            elif isinstance(item, list):
                child_item = self.tree.insert(parent_item, "end", text=f"[{i}]", values=(f"[list] {len(item)} items",))
                self._add_list_children(child_item, item)
            else:
                display_value = str(item)[:100] + "..." if len(str(item)) > 100 else str(item)
                self.tree.insert(parent_item, "end", text=f"[{i}]", values=(display_value,))
    
    def _close(self):
        """Close the dialog"""
        logger.debug(f"_close START")
        
        # Save geometry before closing
        self._save_geometry()
        
        self.destroy()
        logger.debug(f"Properties Viewer Dialog closed")
