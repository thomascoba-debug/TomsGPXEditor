"""
Search and filter functionality for GPX files
"""

import tkinter as tk
from tkinter import ttk
import os
import re
import logging
from typing import List, Callable, Optional

logger = logging.getLogger(__name__)


class FileSearchFrame(ttk.Frame):
    """Search and filter frame for GPX files"""
    
    def __init__(self, parent, on_search_callback: Optional[Callable] = None):
        super().__init__(parent)
        
        self.on_search_callback = on_search_callback
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All Files")
        
        self._create_ui()
        self._setup_bindings()
    
    def _create_ui(self):
        """Create the search UI"""
        # Search frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        # Search entry
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=(0, 5))
        
        self.search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.search_var,
            width=30
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        # Clear search button
        self.clear_button = ttk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search,
            width=8
        )
        self.clear_button.pack(side="left", padx=(0, 10))
        
        # Filter dropdown
        ttk.Label(search_frame, text="Filter:").pack(side="left", padx=(0, 5))
        
        self.filter_combo = ttk.Combobox(
            search_frame,
            textvariable=self.filter_var,
            values=["All Files", "Visible Only", "Hidden Only", "Editable Only"],
            width=15,
            state="readonly"
        )
        self.filter_combo.pack(side="left")
        
        # Results label
        self.results_label = ttk.Label(self, text="")
        self.results_label.pack(fill="x", padx=5, pady=(0, 5))
    
    def _setup_bindings(self):
        """Setup event bindings"""
        # Search on Enter key
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        # Search on typing (with delay)
        self.search_var.trace('w', self._on_search_change)
        
        # Filter change
        self.filter_var.trace('w', lambda *args: self.perform_search())
    
    def _on_search_change(self, *args):
        """Handle search text change with delay"""
        # Cancel previous timer if exists
        if hasattr(self, '_search_timer'):
            self.after_cancel(self._search_timer)
        
        # Set new timer for delayed search
        self._search_timer = self.after(300, self.perform_search)  # 300ms delay
    
    def perform_search(self):
        """Perform the search and filter"""
        search_term = self.search_var.get().strip()
        filter_type = self.filter_var.get()
        
        if self.on_search_callback:
            results = self.on_search_callback(search_term, filter_type)
            self._update_results_label(len(results), search_term, filter_type)
    
    def clear_search(self):
        """Clear search and reset"""
        self.search_var.set("")
        self.filter_var.set("All Files")
        self.perform_search()
    
    def _update_results_label(self, count: int, search_term: str, filter_type: str):
        """Update the results label"""
        if search_term or filter_type != "All Files":
            self.results_label.config(text=f"Found {count} file(s)")
        else:
            self.results_label.config(text="")
    
    def get_search_term(self) -> str:
        """Get current search term"""
        return self.search_var.get().strip()
    
    def get_filter_type(self) -> str:
        """Get current filter type"""
        return self.filter_var.get()


class FileSearchEngine:
    """Engine for searching and filtering GPX files"""
    
    @staticmethod
    def search_files(file_entries: List, search_term: str, filter_type: str) -> List:
        """Search and filter file entries"""
        results = []
        
        for entry in file_entries:
            # Skip None entries
            if entry is None:
                continue
            
            # Apply filter first
            if not FileSearchEngine._matches_filter(entry, filter_type):
                continue
            
            # Apply search if term provided
            if search_term and not FileSearchEngine._matches_search(entry, search_term):
                continue
            
            results.append(entry)
        
        return results
    
    @staticmethod
    def _matches_filter(entry, filter_type: str) -> bool:
        """Check if entry matches filter type"""
        if filter_type == "All Files":
            return True
        elif filter_type == "Visible Only":
            return entry.is_visible()
        elif filter_type == "Hidden Only":
            return not entry.is_visible()
        elif filter_type == "Editable Only":
            return entry.editable_var.get()
        
        return True
    
    @staticmethod
    def _matches_search(entry, search_term: str) -> bool:
        """Check if entry matches search term"""
        search_term = search_term.lower()
        
        # Search in filename
        filename = os.path.basename(entry.path).lower()
        if search_term in filename:
            return True
        
        # Search in directory path
        directory = os.path.dirname(entry.path).lower()
        if search_term in directory:
            return True
        
        # Search in reference number
        if hasattr(entry, 'file_ref'):
            if search_term in str(entry.file_ref):
                return True
        
        # Search in file content (basic)
        try:
            # Quick content search for GPX files
            if entry.path.endswith('.gpx'):
                with open(entry.path, 'r', encoding='utf-8') as f:
                    content = f.read(1000).lower()  # Read first 1000 chars
                    if search_term in content:
                        return True
        except Exception:
            pass  # Ignore file read errors
        
        return False
    
    @staticmethod
    def highlight_search_term(text: str, search_term: str) -> str:
        """Highlight search term in text (for display purposes)"""
        if not search_term:
            return text
        
        # Simple highlighting with asterisks
        pattern = re.compile(re.escape(search_term), re.IGNORECASE)
        return pattern.sub(lambda m: f"*{m.group()}*", text)


class AdvancedSearchDialog(tk.Toplevel):
    """Advanced search dialog with more options"""
    
    def __init__(self, parent, file_entries: List):
        super().__init__(parent)
        
        self.title("Advanced Search")
        self.geometry("500x400")
        self.transient(parent)
        self.grab_set()
        
        self.file_entries = file_entries
        self.results = []
        
        self._create_ui()
        self._center_on_parent(parent)
    
    def _center_on_parent(self, parent):
        """Center dialog on parent window"""
        parent.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        dialog_width = 500
        dialog_height = 400
        
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    def _create_ui(self):
        """Create the advanced search UI"""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Search options
        options_frame = ttk.LabelFrame(main_frame, text="Search Options", padding="10")
        options_frame.pack(fill="x", pady=(0, 10))
        
        # Search term
        ttk.Label(options_frame, text="Search term:").grid(row=0, column=0, sticky="w", pady=2)
        self.search_entry = ttk.Entry(options_frame, width=40)
        self.search_entry.grid(row=0, column=1, sticky="ew", pady=2)
        
        # Search options
        self.search_filename = tk.BooleanVar(value=True)
        self.search_path = tk.BooleanVar(value=True)
        self.search_content = tk.BooleanVar(value=False)
        self.case_sensitive = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="Filename", variable=self.search_filename).grid(row=1, column=0, sticky="w", pady=2)
        ttk.Checkbutton(options_frame, text="Path", variable=self.search_path).grid(row=1, column=1, sticky="w", pady=2)
        ttk.Checkbutton(options_frame, text="Content", variable=self.search_content).grid(row=2, column=0, sticky="w", pady=2)
        ttk.Checkbutton(options_frame, text="Case sensitive", variable=self.case_sensitive).grid(row=2, column=1, sticky="w", pady=2)
        
        options_frame.grid_columnconfigure(1, weight=1)
        
        # Filter options
        filter_frame = ttk.LabelFrame(main_frame, text="Filter Options", padding="10")
        filter_frame.pack(fill="x", pady=(0, 10))
        
        self.filter_visible = tk.StringVar(value="All")
        ttk.Label(filter_frame, text="Visibility:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Radiobutton(filter_frame, text="All", variable=self.filter_visible, value="All").grid(row=0, column=1, sticky="w", pady=2)
        ttk.Radiobutton(filter_frame, text="Visible", variable=self.filter_visible, value="Visible").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Radiobutton(filter_frame, text="Hidden", variable=self.filter_visible, value="Hidden").grid(row=1, column=1, sticky="w", pady=2)
        
        # Results
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(fill="both", expand=True)
        
        # Results list
        self.results_tree = ttk.Treeview(results_frame, columns=("path", "ref"), show="tree headings")
        self.results_tree.heading("#0", text="Filename")
        self.results_tree.heading("path", text="Path")
        self.results_tree.heading("ref", text="Ref")
        
        self.results_tree.column("#0", width=150)
        self.results_tree.column("path", width=300)
        self.results_tree.column("ref", width=50)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="Search", command=self.perform_search).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_search).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Close", command=self.destroy).pack(side="right", padx=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.pack(fill="x", pady=(5, 0))
    
    def perform_search(self):
        """Perform advanced search"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.status_label.config(text="Please enter a search term")
            return
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        self.results = []
        
        for entry in self.file_entries:
            if self._matches_advanced_search(entry, search_term):
                filename = os.path.basename(entry.path)
                path = entry.path
                ref = getattr(entry, 'file_ref', 'N/A')
                
                self.results_tree.insert("", "end", text=filename, values=(path, ref))
                self.results.append(entry)
        
        self.status_label.config(text=f"Found {len(self.results)} file(s)")
    
    def _matches_advanced_search(self, entry, search_term: str) -> bool:
        """Check if entry matches advanced search criteria"""
        if not self._matches_visibility_filter(entry):
            return False
        
        if not search_term:
            return True
        
        # Prepare search term
        if not self.case_sensitive.get():
            search_term = search_term.lower()
        
        # Search in filename
        if self.search_filename.get():
            filename = os.path.basename(entry.path)
            if not self.case_sensitive.get():
                filename = filename.lower()
            if search_term in filename:
                return True
        
        # Search in path
        if self.search_path.get():
            path = entry.path
            if not self.case_sensitive.get():
                path = path.lower()
            if search_term in path:
                return True
        
        # Search in content
        if self.search_content.get():
            try:
                with open(entry.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not self.case_sensitive.get():
                        content = content.lower()
                    if search_term in content:
                        return True
            except Exception:
                pass
        
        return False
    
    def _matches_visibility_filter(self, entry) -> bool:
        """Check if entry matches visibility filter"""
        filter_type = self.filter_visible.get()
        
        if filter_type == "All":
            return True
        elif filter_type == "Visible":
            return entry.is_visible()
        elif filter_type == "Hidden":
            return not entry.is_visible()
        
        return True
    
    def clear_search(self):
        """Clear search and results"""
        self.search_entry.delete(0, tk.END)
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        self.results = []
        self.status_label.config(text="")
    
    def get_results(self) -> List:
        """Get search results"""
        return self.results
