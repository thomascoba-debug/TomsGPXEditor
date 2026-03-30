"""
Dialog Utilities - Implements the "Mantra": Always configurable language settings and always tooltips
"""

import tkinter as tk
from tkinter import ttk
from src.i18n.language_manager import get_language_manager, t


def _destroy_tooltip(widget):
    """Helper function to destroy tooltip"""
    if hasattr(widget, '_tooltip'):
        try:
            widget._tooltip.destroy()
        except:
            pass
        del widget._tooltip


def create_tooltip(widget, text):
    """Create a tooltip for a widget - Mantra: Always tooltips"""
    def on_enter(event):
        # Destroy existing tooltip if any
        if hasattr(widget, '_tooltip'):
            widget._tooltip.destroy()
        
        # Create new tooltip
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        
        label = tk.Label(tooltip, text=text, background="lightyellow", 
                         relief="solid", borderwidth=1, font=("TkDefaultFont", 9))
        label.pack()
        
        # Store reference
        widget._tooltip = tooltip
        
        # Auto-destroy after 3 seconds
        tooltip.after(3000, lambda: _destroy_tooltip(widget))
    
    def on_leave(event):
        _destroy_tooltip(widget)
    
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


class LocalizedDialog:
    """Base class for dialogs with language support - Mantra: Always configurable language settings"""
    
    def __init__(self, parent, properties, dialog_key, modal=False):
        self.parent = parent
        self.properties = properties
        self.dialog_key = dialog_key
        self.language_manager = get_language_manager()
        
    def t(self, key, **kwargs):
        """Translation helper"""
        return self.language_manager.t(key, **kwargs)
    
    def create_localized_label(self, parent, text_key, tooltip_key=None, **grid_kwargs):
        """Create a label with translation and optional tooltip"""
        label = ttk.Label(parent, text=self.t(text_key))
        if tooltip_key:
            create_tooltip(label, self.t(tooltip_key))
        if grid_kwargs:
            label.grid(**grid_kwargs)
        return label
    
    def create_localized_button(self, parent, text_key, command, tooltip_key=None, **pack_kwargs):
        """Create a button with translation and optional tooltip"""
        button = ttk.Button(parent, text=self.t(text_key), command=command)
        if tooltip_key:
            create_tooltip(button, self.t(tooltip_key))
        if pack_kwargs:
            button.pack(**pack_kwargs)
        return button
    
    def create_localized_checkbutton(self, parent, text_key, variable, tooltip_key=None, **grid_kwargs):
        """Create a checkbutton with translation and optional tooltip"""
        checkbutton = ttk.Checkbutton(parent, text=self.t(text_key), variable=variable)
        if tooltip_key:
            create_tooltip(checkbutton, self.t(tooltip_key))
        if grid_kwargs:
            checkbutton.grid(**grid_kwargs)
        return checkbutton
    
    def create_localized_labelframe(self, parent, text_key, tooltip_key=None, **grid_kwargs):
        """Create a labelframe with translation and optional tooltip"""
        labelframe = ttk.LabelFrame(parent, text=self.t(text_key))
        if tooltip_key:
            create_tooltip(labelframe, self.t(tooltip_key))
        if grid_kwargs:
            labelframe.grid(**grid_kwargs)
        return labelframe


def apply_mantra_to_dialog(dialog_class):
    """
    Decorator to apply the mantra to any dialog class:
    - Always configurable language settings
    - Always tooltips
    """
    original_init = dialog_class.__init__
    
    def new_init(self, parent, properties, save_callback=None, modal=False, *args, **kwargs):
        # Initialize language manager
        self.language_manager = get_language_manager()
        
        # Call original init
        original_init(self, parent, properties, save_callback, modal, *args, **kwargs)
        
        # Add tooltip to dialog title area
        if hasattr(self, 'title') and hasattr(self, 't'):
            try:
                title_tooltip_key = f"tooltips.{self.__class__.__name__.lower().replace('dialog', '')}"
                if hasattr(self, '_create_tooltip') and hasattr(self, 'winfo_children'):
                    # Try to add tooltip to title area if possible
                    pass
            except:
                pass
    
    dialog_class.__init__ = new_init
    dialog_class.create_tooltip = staticmethod(create_tooltip)
    dialog_class.t = lambda self, key, **kwargs: self.language_manager.t(key, **kwargs)
    
    return dialog_class
