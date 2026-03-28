"""
Language Settings Dialog - Language selection and management

This dialog provides:
- Language selection
- Preview of available languages
- Settings integration
"""

import tkinter as tk
from tkinter import ttk
from src.ui.base import PersistentDialog
from src.i18n.language_manager import get_language_manager, t
import logging

logger = logging.getLogger(__name__)


class LanguageSettingsDialog(PersistentDialog):
    """Dialog for language settings"""
    
    def __init__(self, parent, properties, save_callback, modal=False):
        super().__init__(parent, properties, "LanguageSettingsDialog", modal=modal)
        
        self.save_callback = save_callback
        self.language_manager = get_language_manager()
        
        self.title(self.language_manager.t("menu.settings_items.language"))
        
        # Get current language
        self.current_language = tk.StringVar(value=self.language_manager.get_language())
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the dialog UI"""
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Language selection
        selection_frame = ttk.LabelFrame(frame, text=self.language_manager.t("menu.settings_items.language"))
        selection_frame.pack(fill="x", pady=(0, 10))
        
        # Current language label
        current_label = ttk.Label(selection_frame, text=f"{self.language_manager.t('menu.settings_items.language')}:")
        current_label.pack(anchor="w", padx=5, pady=5)
        
        # Language combobox
        self.language_combo = ttk.Combobox(
            selection_frame,
            textvariable=self.current_language,
            state="readonly",
            width=20
        )
        self.language_combo.pack(padx=5, pady=5)
        
        # Populate with available languages
        self._populate_languages()
        
        # Language info
        info_frame = ttk.LabelFrame(frame, text=self.language_manager.t("app.info"))
        info_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Current language info
        current_info = ttk.Label(
            info_frame,
            text=f"{self.language_manager.t('messages.language_changed', language=self.current_language.get())}",
            font=("TkDefaultFont", 10, "italic")
        )
        current_info.pack(anchor="w", padx=5, pady=5)
        
        # Available languages info
        languages = self.language_manager.get_available_languages()
        if languages:
            lang_text = self.language_manager.t("menu.settings_items.language") + ":\n"
            for code, name in languages.items():
                current = " ✓" if code == self.current_language.get() else "   "
                lang_text += f"{current} {code} - {name}\n"
            
            lang_label = ttk.Label(info_frame, text=lang_text, justify="left")
            lang_label.pack(anchor="w", padx=5, pady=5)
        
        # Note about restart
        note_label = ttk.Label(
            info_frame,
            text=self.language_manager.t("messages.language_restart_note", default="Note: Language changes will take effect after application restart."),
            font=("TkDefaultFont", 9, "italic"),
            foreground="gray"
        )
        note_label.pack(anchor="w", padx=5, pady=(10, 0))
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text=self.language_manager.t("buttons.ok"), command=self._ok).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=self.language_manager.t("buttons.cancel"), command=self._cancel).pack(side="left", padx=5)
        
        # Bind language change
        self.current_language.trace('w', self._on_language_change)
    
    def _populate_languages(self):
        """Populate the language combobox with available languages"""
        try:
            languages = self.language_manager.get_available_languages()
            language_codes = list(languages.keys())
            language_names = [languages[code] for code in language_codes]
            
            self.language_combo['values'] = language_names
            
            # Set current selection
            current_lang = self.language_manager.get_language()
            if current_lang in languages:
                current_index = language_codes.index(current_lang)
                self.language_combo.current(current_index)
                
        except Exception as e:
            logger.error(f"Error populating languages: {e}", exc_info=True)
    
    def _on_language_change(self, *args):
        """Handle language selection change"""
        try:
            # Find language code from selected name
            languages = self.language_manager.get_available_languages()
            selected_name = self.current_language.get()
            
            for code, name in languages.items():
                if name == selected_name:
                    # Update language manager
                    self.language_manager.set_language(code)
                    break
                    
        except Exception as e:
            logger.error(f"Error changing language: {e}", exc_info=True)
    
    def _ok(self):
        """Save settings and close dialog"""
        try:
            self.save_callback()
            self._on_close()
        except Exception as e:
            logger.error(f"Error saving language settings: {e}", exc_info=True)
    
    def _cancel(self):
        """Close dialog without saving"""
        self._on_close()
