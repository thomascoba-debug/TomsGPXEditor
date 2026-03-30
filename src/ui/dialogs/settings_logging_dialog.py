from src.constants.property_keys import DIALOGS_SETTINGS_LOGGING
from src.i18n import t
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from src.ui.base import PersistentDialog
from src.ui.utils.dialog_utils import create_tooltip
import os

class LoggingSettingsDialog(PersistentDialog):
    def __init__(self, parent, properties, save_callback, modal=False):
        super().__init__(parent, properties, modal=modal)
        
        self.save_callback = save_callback
        self.title(t("dialogs.logging.title"))

        # Get logging settings from structured path
        logging_settings = properties.get(DIALOGS_SETTINGS_LOGGING, {})
        
        level = tk.StringVar(value=logging_settings.get("level") or "INFO")
        logfile = tk.StringVar(value=logging_settings.get("file") or "app.log")
        log_lines = tk.IntVar(value=logging_settings.get("display_lines") or 10)

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure frame to allow expansion
        frame.grid_columnconfigure(1, weight=1)  # Make entry column expandable

        ttk.Label(frame, text=t("dialogs.logging.level")).grid(row=0, column=0)
        
        level_box = ttk.Combobox(
            frame,
            textvariable=level,
            values=["DEBUG", "INFO", "WARNING", "ERROR"]
        )
        level_box.grid(row=0, column=1)
        create_tooltip(level_box, t("tooltips.settings_logging"))
        
        ttk.Label(frame, text=t("dialogs.logging.file")).grid(row=1, column=0)
        
        entry = ttk.Entry(frame, textvariable=logfile)
        entry.grid(row=1, column=1, sticky="ew")  # Make entry expand
        create_tooltip(entry, t("tooltips.settings_logging"))

        def browse():
            path = filedialog.asksaveasfilename(
                parent=self,  # Explicitly set parent
                title=t("dialogs.logging.select_file")
            )
            if path:
                logfile.set(path)
                # Save immediately when file is selected
                logging_settings = properties.get(DIALOGS_SETTINGS_LOGGING, {})
                logging_settings["file"] = path
                properties.set(DIALOGS_SETTINGS_LOGGING, logging_settings)
                properties.save()
                save_callback()
                # Update log display
                update_log_display()
                # Dialog stays open for further changes
            # Don't close dialog regardless of user choice

        ttk.Button(frame, text=t("buttons.browse"), command=browse).grid(row=1, column=2)

        ttk.Label(frame, text=t("dialogs.logging.display_lines")).grid(row=2, column=0)
        
        lines_entry = ttk.Entry(frame, textvariable=log_lines, width=10)
        lines_entry.grid(row=2, column=1, sticky="w")
        
        # Add live update when lines count changes
        def on_lines_change(*args):
            try:
                # Validate that we have a valid integer
                num = log_lines.get()
                if num > 0:  # Only update if we have a positive number
                    update_log_display()
            except (tk.TclError, ValueError):
                # Ignore invalid values (empty, non-numeric, etc.)
                pass
        
        log_lines.trace('w', on_lines_change)

        # Add log file display section
        ttk.Label(frame, text="Last Log Lines:").grid(row=3, column=0, columnspan=3, sticky="w", pady=(10, 5))
        
        # Create a frame for the text area with resize capability
        text_frame = ttk.Frame(frame)
        text_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        text_frame.grid_columnconfigure(0, weight=1)  # Text area fills full width
        text_frame.grid_rowconfigure(0, weight=1)  # Allow vertical expansion
        
        log_display = scrolledtext.ScrolledText(
            text_frame,
            height=8,
            wrap=tk.WORD,  # Remove fixed width to allow full width
            state=tk.DISABLED
        )
        log_display.grid(row=0, column=0, sticky="nsew")  # Fill entire frame
        
        # Add resize handle
        def start_resize(event):
            """Start resizing the text area"""
            self.resize_start_y = event.y
            self.resize_start_height = log_display.winfo_height()
            self.bind("<B1-Motion>", on_resize)
            self.bind("<ButtonRelease-1>", stop_resize)
            
        def on_resize(event):
            """Handle resize motion"""
            try:
                new_height = self.resize_start_height + (event.y - self.resize_start_y)
                # Minimum and maximum height constraints
                new_height = max(100, min(400, new_height))
                log_display.config(height=new_height // 20)  # Convert pixels to lines (approx)
            except:
                pass
                
        def stop_resize(event):
            """Stop resizing"""
            self.unbind("<B1-Motion>")
            self.unbind("<ButtonRelease-1>")
        
        # Create resize handle at the bottom of text area
        resize_handle = tk.Frame(text_frame, height=5, bg="gray", cursor="sb_v_double_arrow")
        resize_handle.grid(row=1, column=0, sticky="ew")
        resize_handle.bind("<Button-1>", start_resize)

        def update_log_display():
            """Update the log display with specified number of lines"""
            log_file_path = logfile.get()
            try:
                num_lines = log_lines.get()
                if num_lines <= 0:
                    num_lines = 10  # Default fallback
            except (tk.TclError, ValueError):
                num_lines = 10  # Default fallback
            
            try:
                if os.path.exists(log_file_path):
                    with open(log_file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        last_lines = lines[-num_lines:] if len(lines) > num_lines else lines
                    
                    log_display.config(state=tk.NORMAL)
                    log_display.delete(1.0, tk.END)
                    for line in last_lines:
                        log_display.insert(tk.END, line)
                    log_display.config(state=tk.DISABLED)
                else:
                    log_display.config(state=tk.NORMAL)
                    log_display.delete(1.0, tk.END)
                    log_display.insert(tk.END, f"Log file not found: {log_file_path}")
                    log_display.config(state=tk.DISABLED)
            except Exception as e:
                log_display.config(state=tk.NORMAL)
                log_display.delete(1.0, tk.END)
                log_display.insert(tk.END, f"Error reading log file: {e}")
                log_display.config(state=tk.DISABLED)

        def clear_log_file():
            """Clear log file but keep specified number of lines"""
            log_file_path = logfile.get()
            try:
                num_lines = log_lines.get()
                if num_lines <= 0:
                    num_lines = 10  # Default fallback
            except (tk.TclError, ValueError):
                num_lines = 10  # Default fallback
            
            try:
                if os.path.exists(log_file_path):
                    with open(log_file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # Keep specified number of lines
                    lines_to_keep = lines[-num_lines:] if len(lines) > num_lines else lines
                    
                    with open(log_file_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines_to_keep)
                    
                    update_log_display()
                else:
                    log_display.config(state=tk.NORMAL)
                    log_display.delete(1.0, tk.END)
                    log_display.insert(tk.END, f"Log file not found: {log_file_path}")
                    log_display.config(state=tk.DISABLED)
            except Exception as e:
                log_display.config(state=tk.NORMAL)
                log_display.delete(1.0, tk.END)
                log_display.insert(tk.END, f"Error clearing log file: {e}")
                log_display.config(state=tk.DISABLED)

        # Add clear button
        ttk.Button(frame, text="Clear Log (Keep Specified Lines)", command=clear_log_file).grid(row=5, column=0, columnspan=3, pady=(0, 10))

        # Initial update of log display
        update_log_display()

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=6, columnspan=3, pady=10)

        def ok():
            """Save settings and close dialog"""
            # Get current logging settings
            logging_settings = properties.get(DIALOGS_SETTINGS_LOGGING, {})
            
            # Update settings
            logging_settings["level"] = level.get()
            logging_settings["file"] = logfile.get()
            logging_settings["display_lines"] = log_lines.get()
            
            # Save structured settings
            properties.set(DIALOGS_SETTINGS_LOGGING, logging_settings)
            
            # Use save_callback which handles save and reconfigure_logging
            save_callback()
            self._on_close()

        def cancel():
            """Close dialog without saving"""
            self._on_close()

        ttk.Button(btn_frame, text="OK", command=ok).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Cancel", command=cancel).pack(side="left", padx=2)

