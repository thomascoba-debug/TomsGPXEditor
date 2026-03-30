"""
Dialog Manager - Core dialog management functionality
"""
import tkinter as tk
from tkinter import messagebox

class DialogManager:
    """Core dialog management functionality"""
    
    def __init__(self, parent):
        self.parent = parent
        
    def show_info_dialog(self, title, message):
        """Show information dialog"""
        messagebox.showinfo(title, message)
    
    def show_warning_dialog(self, title, message):
        """Show warning dialog"""
        messagebox.showwarning(title, message)
    
    def show_error_dialog(self, title, message):
        """Show error dialog"""
        messagebox.showerror(title, message)
    
    def ask_yes_no(self, title, message):
        """Ask yes/no question"""
        return messagebox.askyesno(title, message)
