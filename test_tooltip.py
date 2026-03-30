import tkinter as tk
from tkinter import ttk
from src.ui.utils.dialog_utils import create_tooltip

def test_tooltip():
    root = tk.Tk()
    root.title("Tooltip Test")
    
    # Create a button with tooltip
    button = ttk.Button(root, text="Hover over me!")
    button.pack(padx=20, pady=20)
    
    # Add tooltip
    create_tooltip(button, "This is a test tooltip!")
    
    # Create a label with tooltip
    label = ttk.Label(root, text="Label with tooltip")
    label.pack(padx=20, pady=10)
    
    create_tooltip(label, "This is a label tooltip!")
    
    root.mainloop()

if __name__ == "__main__":
    test_tooltip()
