"""
Color Utilities

Gemeinsame Funktionen für Farbauswahl und Farbverwaltung.
"""

import tkinter as tk
import logging

logger = logging.getLogger(__name__)


def pick_color(parent=None, initial_color=None):
    """
    Öffne einen Farbauswahl-Dialog und gib die gewählte Farbe zurück.
    
    Args:
        parent: Parent-Widget für den Dialog (optional)
        initial_color: Anfangsfarbe für den Dialog (optional)
    
    Returns:
        str|None: Die gewählte Farbe als Hex-String oder None wenn abgebrochen
    """
    try:
        color = tk.colorchooser.askcolor(
            parent=parent,
            initialcolor=initial_color or "#ffffff"
        )[1]
        
        if color:
            logger.debug(f"Color chosen: {color}")
        else:
            logger.debug("Color chooser cancelled")
            
        return color
    except Exception as e:
        logger.error(f"Error in color chooser: {e}")
        return None


def update_color_button(color_btn, color):
    """
    Aktualisiere die Hintergrundfarbe eines Buttons.
    
    Args:
        color_btn: Der Button-Widget
        color: Die neue Farbe als Hex-String
    """
    try:
        if color_btn and color:
            color_btn.configure(bg=color)
            logger.debug(f"Updated button color to: {color}")
    except Exception as e:
        logger.error(f"Error updating button color: {e}")


def validate_color(color):
    """
    Prüfe, ob ein String eine gültige Hex-Farbe ist.
    
    Args:
        color: Zu prüfender Farbwert
    
    Returns:
        bool: True wenn gültig, False wenn ungültig
    """
    if not color or not isinstance(color, str):
        return False
    
    # Prüfe auf Hex-Format (#RRGGBB oder #RGB)
    if color.startswith('#'):
        # Entferne # und prüfe Länge
        hex_part = color[1:]
        return len(hex_part) in (3, 6) and all(c in '0123456789abcdefABCDEF' for c in hex_part)
    
    return False
