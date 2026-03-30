"""
Color Utilities

Gemeinsame Funktionen für Farbauswahl und Farbverwaltung.
"""

import tkinter as tk
import logging

# Check if colorchooser is available
try:
    from tkinter import colorchooser
    HAS_COLORCHOOSER = True
except ImportError:
    HAS_COLORCHOOSER = False
    print("Warning: tkinter.colorchooser not available, using fallback")

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
    if not HAS_COLORCHOOSER:
        # Fallback: Use simple color entry dialog
        return _fallback_color_picker(parent, initial_color)
    
    try:
        color = colorchooser.askcolor(
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
        # Fallback to simple dialog
        return _fallback_color_picker(parent, initial_color)


def _fallback_color_picker(parent, initial_color):
    """
    Fallback color picker using simple entry dialog.
    
    Args:
        parent: Parent-Widget für den Dialog
        initial_color: Anfangsfarbe
    
    Returns:
        str|None: Die gewählte Farbe oder None wenn abgebrochen
    """
    try:
        # Create simple dialog
        dialog = tk.Toplevel(parent) if parent else tk.Toplevel()
        dialog.title("Farbauswahl")
        dialog.geometry("300x150")
        
        # Make dialog modal
        if parent:
            dialog.transient(parent)
            dialog.grab_set()
        
        # Color entry
        tk.Label(dialog, text="Farbe (Hex, z.B. #FF0000):").pack(pady=10)
        color_var = tk.StringVar(value=initial_color or "#ffffff")
        entry = tk.Entry(dialog, textvariable=color_var, width=20)
        entry.pack(pady=5)
        
        result = [None]
        
        def ok():
            color = color_var.get().strip()
            if color.startswith('#') and len(color) == 7:
                try:
                    int(color[1:], 16)  # Validate hex
                    result[0] = color
                except ValueError:
                    pass
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="OK", command=ok).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Abbrechen", command=cancel).pack(side=tk.LEFT, padx=5)
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Focus and wait
        entry.focus()
        entry.select_range(0, tk.END)
        dialog.wait_window()
        
        return result[0]
    
    except Exception as e:
        logger.error(f"Error in fallback color picker: {e}")
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
            color_btn.config(bg=color)
            logger.debug(f"Updated button color: {color}")
    except Exception as e:
        logger.error(f"Error updating button color: {e}")


def validate_hex_color(color):
    """
    Validiere einen Hex-Farbcode.
    
    Args:
        color: Der zu validierende Farbcode
    
    Returns:
        bool: True wenn gültig, False wenn ungültig
    """
    if not color or not isinstance(color, str):
        return False
    
    if not color.startswith('#'):
        return False
    
    if len(color) != 7:
        return False
    
    try:
        int(color[1:], 16)
        return True
    except ValueError:
        return False
