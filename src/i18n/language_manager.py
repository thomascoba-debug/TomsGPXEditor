"""
Internationalization (i18n) Manager for multi-language support

This module provides:
- Language switching
- Translation loading
- Text localization
- Settings integration
"""

import json
import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class LanguageManager:
    """Central language management and translation system"""
    
    def __init__(self, properties_manager):
        self.properties = properties_manager
        self.current_language = "de"  # Default: German
        self.translations: Dict[str, Dict[str, str]] = {}
        self.fallback_translations: Dict[str, str] = {}
        
        # Load default language
        self._load_language(self.current_language)
    
    def _load_language(self, language_code: str) -> None:
        """Lade Übersetzungen für eine Sprache"""
        try:
            translation_file = os.path.join(
                "src", "i18n", "translations", f"{language_code}.json"
            )
            
            if os.path.exists(translation_file):
                with open(translation_file, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
                logger.info(f"Loaded translations for language: {language_code}")
            else:
                logger.warning(f"Translation file not found: {translation_file}")
                self.translations = {}
                
        except Exception as e:
            logger.error(f"Error loading language {language_code}: {e}", exc_info=True)
            self.translations = {}
        
        # Load fallback translations (English)
        if language_code != "en":
            self._load_fallback()
    
    def _load_fallback(self) -> None:
        """Lade Fallback-Übersetzungen (Englisch)"""
        try:
            fallback_file = os.path.join(
                "src", "i18n", "translations", "en.json"
            )
            
            if os.path.exists(fallback_file):
                with open(fallback_file, 'r', encoding='utf-8') as f:
                    self.fallback_translations = json.load(f)
                logger.debug("Loaded fallback translations (English)")
            else:
                logger.warning("Fallback translation file not found")
                self.fallback_translations = {}
                
        except Exception as e:
            logger.error(f"Error loading fallback translations: {e}", exc_info=True)
            self.fallback_translations = {}
    
    def set_language(self, language_code: str) -> None:
        """Setze die aktuelle Sprache"""
        if language_code == self.current_language:
            return
        
        self.current_language = language_code
        self._load_language(language_code)
        
        # Speichere in Properties
        self.properties.set("dialogs.settings.language", language_code)
        self.properties.save()
        
        logger.info(f"Language changed to: {language_code}")
    
    def get_language(self) -> str:
        """Gib die aktuelle Sprache zurück"""
        return self.current_language
    
    def t(self, key: str, **kwargs) -> str:
        """Übersetze einen Text-Schlüssel"""
        # Unterstütze verschachtelte Schlüssel (z.B. "app.title")
        text = self._get_nested_translation(key)
        
        if text is None:
            # Fallback zu Englisch
            text = self._get_nested_translation(key, self.fallback_translations)
            if text is None:
                # Letzter Fallback: Schlüssel selbst
                text = key
                logger.warning(f"Translation missing for key: {key}")
        
        # String-Formatierung mit kwargs
        try:
            if kwargs:
                return text.format(**kwargs)
            return text
        except (KeyError, ValueError) as e:
            logger.error(f"Error formatting translation for key '{key}': {e}")
            return text
    
    def _get_nested_translation(self, key: str, translations_dict=None) -> str:
        """Hole Übersetzung für verschachtelte Schlüssel"""
        if translations_dict is None:
            translations_dict = self.translations
        
        keys = key.split('.')
        current = translations_dict
        
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return None
    
    def get_available_languages(self) -> Dict[str, str]:
        """Gib verfügbare Sprachen zurück"""
        languages = {}
        translations_dir = os.path.join("src", "i18n", "translations")
        
        if os.path.exists(translations_dir):
            for file in os.listdir(translations_dir):
                if file.endswith('.json'):
                    lang_code = file[:-5]  # Entferne .json
                    try:
                        with open(os.path.join(translations_dir, file), 'r', encoding='utf-8') as f:
                            lang_data = json.load(f)
                            languages[lang_code] = lang_data.get('language_name', lang_code.title())
                    except Exception as e:
                        logger.error(f"Error loading language info for {lang_code}: {e}")
        
        return languages
    
    def initialize_from_settings(self) -> None:
        """Initialisiere Sprache aus den Settings"""
        saved_language = self.properties.get("dialogs.settings.language", "de")
        if saved_language != self.current_language:
            self.set_language(saved_language)


# Global instance für einfachen Zugriff
_language_manager: Optional[LanguageManager] = None


def get_language_manager() -> Optional[LanguageManager]:
    """Gib den globalen Language Manager zurück"""
    return _language_manager


def initialize_language_manager(properties_manager) -> LanguageManager:
    """Initialisiere den globalen Language Manager"""
    global _language_manager
    _language_manager = LanguageManager(properties_manager)
    _language_manager.initialize_from_settings()
    return _language_manager


def t(key: str, **kwargs) -> str:
    """Global translation function"""
    if _language_manager:
        return _language_manager.t(key, **kwargs)
    return key  # Fallback wenn nicht initialisiert
