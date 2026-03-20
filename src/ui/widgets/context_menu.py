"""
Context menu functionality for GPX Editor
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import logging
from typing import Callable, Optional, List

logger = logging.getLogger(__name__)


class ContextMenuManager:
    """Manages context menus for various components"""
    
    def __init__(self, parent):
        self.parent = parent
        self.context_menu = None
    
    def create_file_context_menu(self, event, file_entry, callbacks: dict):
        """Create context menu for file entry"""
        # Destroy existing menu
        if self.context_menu:
            self.context_menu.destroy()
        
        # Create new menu
        self.context_menu = tk.Menu(self.parent, tearoff=0)
        
        # Add menu items
        if callbacks.get('open_table_editor'):
            self.context_menu.add_command(
                label="Open in Table Editor",
                command=lambda: callbacks['open_table_editor'](file_entry)
            )
        
        if callbacks.get('toggle_visibility'):
            label = "Hide" if file_entry.is_visible() else "Show"
            self.context_menu.add_command(
                label=label,
                command=lambda: callbacks['toggle_visibility'](file_entry)
            )
        
        if callbacks.get('toggle_editable'):
            label = "Make Editable" if not file_entry.editable_var.get() else "Make Non-Editable"
            self.context_menu.add_command(
                label=label,
                command=lambda: callbacks['toggle_editable'](file_entry)
            )
        
        self.context_menu.add_separator()
        
        if callbacks.get('change_color'):
            self.context_menu.add_command(
                label="Change Color",
                command=lambda: callbacks['change_color'](file_entry)
            )
        
        if callbacks.get('duplicate_file'):
            self.context_menu.add_command(
                label="Duplicate",
                command=lambda: callbacks['duplicate_file'](file_entry)
            )
        
        self.context_menu.add_separator()
        
        if callbacks.get('show_file_info'):
            self.context_menu.add_command(
                label="File Info",
                command=lambda: callbacks['show_file_info'](file_entry)
            )
        
        if callbacks.get('open_file_location'):
            self.context_menu.add_command(
                label="Open File Location",
                command=lambda: callbacks['open_file_location'](file_entry)
            )
        
        self.context_menu.add_separator()
        
        if callbacks.get('remove_file'):
            self.context_menu.add_command(
                label="Remove",
                command=lambda: callbacks['remove_file'](file_entry)
            )
        
        # Show menu
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def create_main_context_menu(self, event, callbacks: dict):
        """Create context menu for main application"""
        # Destroy existing menu
        if self.context_menu:
            self.context_menu.destroy()
        
        # Create new menu
        self.context_menu = tk.Menu(self.parent, tearoff=0)
        
        # Add menu items
        if callbacks.get('paste_files'):
            self.context_menu.add_command(
                label="Paste Files",
                command=callbacks['paste_files']
            )
        
        if callbacks.get('refresh_all'):
            self.context_menu.add_command(
                label="Refresh All",
                command=callbacks['refresh_all']
            )
        
        if callbacks.get('show_advanced_search'):
            self.context_menu.add_command(
                label="Advanced Search",
                command=callbacks['show_advanced_search']
            )
        
        self.context_menu.add_separator()
        
        if callbacks.get('select_all'):
            self.context_menu.add_command(
                label="Select All",
                command=callbacks['select_all']
            )
        
        if callbacks.get('deselect_all'):
            self.context_menu.add_command(
                label="Deselect All",
                command=callbacks['deselect_all']
            )
        
        # Show menu
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()


class AutoSaveManager:
    """Manages automatic saving functionality"""
    
    def __init__(self, properties, save_callback: Callable):
        self.properties = properties
        self.save_callback = save_callback
        self.auto_save_enabled = properties.get("auto_save_enabled", False)
        self.auto_save_interval = properties.get("auto_save_interval", 300)  # 5 minutes default
        self.auto_save_timer = None
        
        logger.debug(f"Auto-save initialized: enabled={self.auto_save_enabled}, interval={self.auto_save_interval}s")
    
    def start_auto_save(self):
        """Start auto-save timer"""
        if self.auto_save_enabled and not self.auto_save_timer:
            self._schedule_auto_save()
            logger.debug("Auto-save timer started")
    
    def stop_auto_save(self):
        """Stop auto-save timer"""
        if self.auto_save_timer:
            self.after_cancel(self.auto_save_timer)
            self.auto_save_timer = None
            logger.debug("Auto-save timer stopped")
    
    def _schedule_auto_save(self):
        """Schedule next auto-save"""
        if self.auto_save_enabled:
            self.auto_save_timer = self.after(self.auto_save_interval * 1000, self._perform_auto_save)
    
    def _perform_auto_save(self):
        """Perform auto-save"""
        try:
            logger.debug("Performing auto-save")
            success = self.save_callback()
            
            if success:
                logger.info("Auto-save completed successfully")
            else:
                logger.warning("Auto-save failed")
            
            # Schedule next auto-save
            self._schedule_auto_save()
            
        except Exception as e:
            logger.error(f"Auto-save error: {e}")
            # Continue with next auto-save even if this one failed
            self._schedule_auto_save()
    
    def set_auto_save_enabled(self, enabled: bool):
        """Enable/disable auto-save"""
        self.auto_save_enabled = enabled
        self.properties.set("auto_save_enabled", enabled)
        self.properties.save()
        
        if enabled:
            self.start_auto_save()
        else:
            self.stop_auto_save()
        
        logger.debug(f"Auto-save {'enabled' if enabled else 'disabled'}")
    
    def set_auto_save_interval(self, interval_seconds: int):
        """Set auto-save interval"""
        if interval_seconds < 60:  # Minimum 1 minute
            interval_seconds = 60
        
        self.auto_save_interval = interval_seconds
        self.properties.set("auto_save_interval", interval_seconds)
        self.properties.save()
        
        # Restart timer with new interval
        if self.auto_save_enabled:
            self.stop_auto_save()
            self.start_auto_save()
        
        logger.debug(f"Auto-save interval set to {interval_seconds} seconds")
    
    def get_auto_save_status(self) -> dict:
        """Get current auto-save status"""
        return {
            'enabled': self.auto_save_enabled,
            'interval': self.auto_save_interval,
            'active': self.auto_save_timer is not None
        }


class KeyboardShortcutManager:
    """Manages keyboard shortcuts"""
    
    def __init__(self, parent):
        self.parent = parent
        self.shortcuts = {}
    
    def register_shortcut(self, key_sequence: str, callback: Callable, description: str = ""):
        """Register a keyboard shortcut"""
        self.parent.bind(key_sequence, callback)
        self.shortcuts[key_sequence] = {
            'callback': callback,
            'description': description
        }
        logger.debug(f"Registered shortcut: {key_sequence} - {description}")
    
    def unregister_shortcut(self, key_sequence: str):
        """Unregister a keyboard shortcut"""
        self.parent.unbind(key_sequence)
        if key_sequence in self.shortcuts:
            del self.shortcuts[key_sequence]
            logger.debug(f"Unregistered shortcut: {key_sequence}")
    
    def get_shortcuts_list(self) -> List[tuple]:
        """Get list of all shortcuts"""
        return [
            (key, info['description']) 
            for key, info in self.shortcuts.items()
            if info['description']
        ]
    
    def setup_default_shortcuts(self, app):
        """Setup default keyboard shortcuts"""
        # File operations
        self.register_shortcut('<Control-o>', lambda e: app._open_file_dialog(), "Open File")
        self.register_shortcut('<Control-s>', lambda e: app._save_all(), "Save All")
        self.register_shortcut('<Control-q>', lambda e: app._on_close(), "Quit")
        
        # Edit operations
        self.register_shortcut('<Control-a>', lambda e: app._select_all_files(), "Select All")
        self.register_shortcut('<Control-d>', lambda e: app._deselect_all_files(), "Deselect All")
        self.register_shortcut('<Delete>', lambda e: app._delete_selected(), "Delete Selected")
        
        # View operations
        self.register_shortcut('<Control-f>', lambda e: app._show_search(), "Search")
        self.register_shortcut('<Control-r>', lambda e: app._refresh_all(), "Refresh")
        self.register_shortcut('<F5>', lambda e: app._refresh_all(), "Refresh")
        
        # Map operations
        self.register_shortcut('<Control-plus>', lambda e: app._zoom_in(), "Zoom In")
        self.register_shortcut('<Control-minus>', lambda e: app._zoom_out(), "Zoom Out")
        self.register_shortcut('<Control-0>', lambda e: app._zoom_fit(), "Zoom to Fit")
        
        logger.debug("Default shortcuts registered")


class QuickActionsManager:
    """Manages quick action buttons and features"""
    
    def __init__(self, parent_frame, app):
        self.parent = parent_frame
        self.app = app
        self.quick_actions_frame = None
    
    def create_quick_actions_bar(self):
        """Create quick actions toolbar"""
        if self.quick_actions_frame:
            self.quick_actions_frame.destroy()
        
        self.quick_actions_frame = ttk.Frame(self.parent)
        self.quick_actions_frame.pack(fill="x", padx=5, pady=2)
        
        # Quick action buttons
        ttk.Button(
            self.quick_actions_frame,
            text="🔍 Search",
            command=self.app._show_search,
            width=10
        ).pack(side="left", padx=2)
        
        ttk.Button(
            self.quick_actions_frame,
            text="📁 Open",
            command=self.app._open_file_dialog,
            width=10
        ).pack(side="left", padx=2)
        
        ttk.Button(
            self.quick_actions_frame,
            text="💾 Save",
            command=self.app._save_all,
            width=10
        ).pack(side="left", padx=2)
        
        ttk.Button(
            self.quick_actions_frame,
            text="🗑️ Delete",
            command=self.app._delete_selected,
            width=10
        ).pack(side="left", padx=2)
        
        ttk.Button(
            self.quick_actions_frame,
            text="🔄 Refresh",
            command=self.app._refresh_all,
            width=10
        ).pack(side="left", padx=2)
        
        # Separator
        ttk.Separator(self.quick_actions_frame, orient="vertical").pack(side="left", padx=10, fill="y")
        
        # View controls
        ttk.Button(
            self.quick_actions_frame,
            text="👁️ Show All",
            command=self.app._select_all,
            width=10
        ).pack(side="left", padx=2)
        
        ttk.Button(
            self.quick_actions_frame,
            text="🙈 Hide All",
            command=self.app._deselect_all,
            width=10
        ).pack(side="left", padx=2)
        
        ttk.Button(
            self.quick_actions_frame,
            text="🎨 Random Colors",
            command=self.app._randomize_colors,
            width=12
        ).pack(side="left", padx=2)
    
    def update_quick_actions(self):
        """Update quick actions based on current state"""
        if not self.quick_actions_frame:
            return
        
        # Update button states based on selection
        has_selection = any(entry.editable_var.get() for entry in self.app.entries)
        
        # Find and update delete button
        for widget in self.quick_actions_frame.winfo_children():
            if isinstance(widget, ttk.Button) and "Delete" in widget.cget("text"):
                widget.config(state="normal" if has_selection else "disabled")
                break
