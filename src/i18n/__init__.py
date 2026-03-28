"""
Internationalization (i18n) Package

This package provides:
- Multi-language support
- Translation management
- Language switching
- Text localization
"""

from .language_manager import (
    LanguageManager,
    get_language_manager,
    initialize_language_manager,
    t
)

__all__ = [
    'LanguageManager',
    'get_language_manager', 
    'initialize_language_manager',
    't'
]
