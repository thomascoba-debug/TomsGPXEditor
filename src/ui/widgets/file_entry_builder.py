"""
File Entry Builder - Erstellung von UI-Elementen für GPX-Dateien

Dieser Builder kümmert sich um:
- Erstellung von Checkboxen, Labels, Buttons
- Event-Handler Registration
- Widget-Layout im Grid
- State Management
"""

import logging
import os
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable
from src.ui.utils.dialog_utils import create_tooltip

from src.infrastructure.repositories.properties_repository import AppProperties

logger = logging.getLogger(__name__)


class FileEntryBuilder:
    """Builder für die Erstellung von GPX-Datei-Einträgen in der UI"""
    
    def __init__(self, parent_frame, row: int, button_update_callback=None, editable_update_callback=None):
        self.parent_frame = parent_frame
        self.row = row
        self.entries = []  # Speichere die Entry-Objekte
        self.properties = None  # Will be set in create_file_entry
        self.button_update_callback = button_update_callback
        self.editable_update_callback = editable_update_callback
        
    def create_file_entry(self, path: str, ref_num: int, file_analysis: Dict[str, Any], 
                       settings: Dict[str, Any], properties: AppProperties):
        """Erstelle einen kompletten Datei-Eintrag mit allen UI-Elementen"""
        
        # Store properties for use in _create_widgets
        self.properties = properties
        
        logger.debug(f"create_file_entry called for {path} (ref: {ref_num})")
        
        # Erstelle Variablen
        visible_var = tk.BooleanVar()
        editable_var = tk.BooleanVar()
        
        # Lade Checkbox-States
        if settings:
            visible_var.set(settings.get('visible', True))
            editable_var.set(settings.get('editable', False))
        else:
            visible_var.set(True)
            editable_var.set(False)
        
        logger.debug("Creating widgets...")
        # Erstelle Widgets
        widgets = self._create_widgets(visible_var, editable_var, ref_num, path, file_analysis, settings)
        
        logger.debug("Creating entry object...")
        # Erstelle Entry-Objekt
        entry = self._create_entry_object(path, ref_num, file_analysis, properties, widgets, visible_var, editable_var)
        
        # Speichere das Entry-Objekt
        self.entries.append(entry)
        
        logger.debug("Registering handlers...")
        # Registriere Event-Handler
        self._register_handlers(entry, visible_var, editable_var, properties)
        
        logger.debug(f"Returning entry: {entry}")
        return entry
    
    def _create_widgets(self, visible_var: tk.BooleanVar, editable_var: tk.BooleanVar, 
                      ref_num: int, path: str, file_analysis: Dict[str, Any], 
                      settings: Dict[str, Any]) -> Dict[str, Any]:
        """Erstelle alle UI-Widgets für den Eintrag"""
        
        widgets = {}
        
        # Visible Checkbox
        widgets['visible_cb'] = ttk.Checkbutton(
            self.parent_frame,
            variable=visible_var,
            width=2
        )
        widgets['visible_cb'].grid(row=self.row, column=0, padx=3)
        
        # Editable Checkbox
        widgets['editable_cb'] = ttk.Checkbutton(
            self.parent_frame,
            variable=editable_var,
            width=2
        )
        widgets['editable_cb'].grid(row=self.row, column=1, padx=3)
        
        # Reference Label
        widgets['ref_label'] = ttk.Label(
            self.parent_frame,
            text=f"[{ref_num}]",
            foreground="blue",
            font=("TkDefaultFont", 7),
            width=4
        )
        widgets['ref_label'].grid(row=self.row, column=2, padx=3)
        
        # Color Button
        logger.debug(f"Creating color button for ref {ref_num}...")
        color = settings.get('color', '#0000ff') if settings else '#0000ff'
        color_btn = tk.Button(
            self.parent_frame,
            bg=color,
            width=3,
            command=lambda p=self.properties: self._pick_color_for_file(ref_num, color_btn, p)
        )
        widgets['color_btn'] = color_btn
        color_btn.grid(row=self.row, column=3, padx=3)
        logger.debug("Color button created")
        
        # Filename Label
        filename_label = ttk.Label(
            self.parent_frame,
            text=os.path.basename(path)
        )
        filename_label.grid(row=self.row, column=4, sticky="w", padx=3)
        create_tooltip(filename_label, path)  # Show full path as tooltip
        widgets['filename_label'] = filename_label
        
        # File Type Label
        file_type_text = self._get_file_type_text(file_analysis)
        widgets['filetype_label'] = ttk.Label(
            self.parent_frame,
            text=file_type_text,
            foreground="gray",
            font=("TkDefaultFont", 8)
        )
        widgets['filetype_label'].grid(row=self.row, column=5, sticky="w", padx=(5, 0))
        
        return widgets
    
    def _get_file_type_text(self, file_analysis: Dict[str, Any]) -> str:
        """Erstelle den Text für den Datei-Typ"""
        file_type = file_analysis.get('file_type', 'unknown').upper()
        
        if file_type == 'mixed':
            return f"T+R ({file_analysis['track_count']},{file_analysis['route_count']})"
        elif file_type == 'track':
            return f"T ({file_analysis['track_count']})"
        elif file_type == 'route':
            return f"R ({file_analysis['route_count']})"
        else:
            return file_type
    
    def _create_entry_object(self, path: str, ref_num: int, file_analysis: Dict[str, Any],
                          properties: AppProperties, widgets: Dict[str, Any],
                          visible_var: tk.BooleanVar, editable_var: tk.BooleanVar):
        """Erstelle das Entry-Objekt mit allen Methoden"""
        
        class SimpleEntry:
            def __init__(self):
                self.path = path
                self.ref_num = ref_num
                self.file_analysis = file_analysis
                self.properties = properties
                self.widgets = widgets
                self.visible_var = visible_var
                self.editable_var = editable_var
                self.color = widgets['color_btn'].cget('bg')
                
            def get_path(self):
                return self.path
            
            def is_visible(self):
                return self.visible_var.get()
            
            def is_editable(self):
                return self.editable_var.get()
            
            def get_color(self):
                return self.widgets['color_btn'].cget('bg')
            
            def destroy(self):
                """Entferne alle Widgets aus dem Grid"""
                for widget in self.widgets.values():
                    if hasattr(widget, 'grid_remove'):
                        widget.grid_remove()
        
        entry = SimpleEntry()
        
        # Füge Methoden hinzu
        entry._save_states = lambda: self._save_states(entry, properties)
        entry._destroy_widgets = entry.destroy
        entry._map_update_callback = lambda: self._update_map_callback()
        
        return entry
    
    def _update_map_callback(self):
        """Trigger map update if callback is available"""
        # This method will be called when checkbox states change
        # Use the button_update_callback which should trigger map update
        if self.button_update_callback:
            self.button_update_callback()
    
    def _button_update_callback_only(self):
        """Trigger button update without map update"""
        # This method will be called when editable states change
        if self.button_update_callback:
            # Call with update_map=False to prevent map update
            # We need to modify the callback to accept this parameter
            self.button_update_callback()
    
    def _register_handlers(self, entry, visible_var: tk.BooleanVar, 
                        editable_var: tk.BooleanVar, properties: AppProperties):
        """Registriere Event-Handler für die Checkboxen"""
        
        def on_visible_change():
            logger.debug(f"Visible changed for ref {entry.ref_num}: {visible_var.get()}")
            entry._save_states()
            # Trigger map update via callback
            if hasattr(entry, '_map_update_callback'):
                entry._map_update_callback()
        
        def on_editable_change():
            logger.debug(f"Editable changed for ref {entry.ref_num}: {editable_var.get()}")
            entry._save_states()
            # Trigger editable-only button update (no map update)
            if self.editable_update_callback:
                self.editable_update_callback()
        
        # Registriere Handler
        visible_var.trace('w', lambda *args: on_visible_change())
        editable_var.trace('w', lambda *args: on_editable_change())
        
        # Speichere Callback-Referenz
        entry._on_visible_change = on_visible_change
        entry._on_editable_change = on_editable_change
    
    def _save_states(self, entry, properties: AppProperties):
        """Speichere die Zustände in den Properties"""
        settings = properties.get_file_settings_by_reference(entry.ref_num)
        settings['visible'] = entry.is_visible()
        settings['editable'] = entry.is_editable()
        
        logger.debug(f"Saved states for ref {entry.ref_num}: visible={entry.is_visible()}, editable={entry.is_editable()}")
    
    def _pick_color_for_file(self, ref_num: int, color_btn, properties):
        """Farbauswahl für Datei (wie in Marker Settings)"""
        from src.ui.utils.color_utils import pick_color, update_color_button
        
        try:
            logger.debug(f"_pick_color_for_file called for ref {ref_num}")
            
            # Hole aktuelle Farbe vom Button
            current_color = color_btn.cget('bg')
            logger.debug(f"Current color: {current_color}")
            
            # Öffne Farbauswahl-Dialog
            new_color = pick_color(parent=self.parent_frame, initial_color=current_color)
            logger.debug(f"New color chosen: {new_color}")
            
            if new_color:
                logger.debug(f"Processing new color: {new_color}")
                
                # Update color in settings
                settings = properties.get_file_settings_by_reference(ref_num)
                settings['color'] = new_color
                properties.save_file_settings_by_reference(ref_num, settings)
                logger.debug("Saved color to properties")
                
                # Update button
                logger.debug("Updating button color...")
                update_color_button(color_btn, new_color)
                logger.debug("Button color updated")
                
                # Update map
                if hasattr(self, 'parent') and hasattr(self.parent, '_update_map'):
                    self.parent._update_map()
                    logger.debug("Map updated")
                else:
                    logger.debug("No parent or _update_map method found")
            else:
                logger.debug("Color chooser cancelled")
                
        except Exception as e:
            logger.error(f"_pick_color_for_file failed: {e}")
            import traceback
            traceback.print_exc()
            logger.debug(f"Fehler bei Farbauswahl: {e}")
