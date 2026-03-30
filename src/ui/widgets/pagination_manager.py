
"""
Pagination Manager - Handles all pagination logic for GPX table editor
"""
import tkinter as tk
from tkinter import ttk

class PaginationManager:
    """Handles pagination logic for large datasets"""
    
    def __init__(self, page_size=1000):
        self.page_size = page_size
        self.current_page = 0
        self.total_points = 0
        self.all_points = []
        self.page_size_var = None
        self.page_info_label = None
        
    def setup_ui(self, parent_frame):
        """Setup pagination UI controls"""
        # Pagination controls frame
        pagination_frame = ttk.Frame(parent_frame)
        pagination_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        # Page info label
        self.page_info_label = ttk.Label(pagination_frame, text="Page 1 of 1 (0 points)")
        self.page_info_label.pack(side="left", padx=(0, 20))
        
        # Navigation buttons
        ttk.Button(pagination_frame, text="First", command=self.first_page, width=8).pack(side="left", padx=2)
        ttk.Button(pagination_frame, text="Previous", command=self.previous_page, width=10).pack(side="left", padx=2)
        ttk.Button(pagination_frame, text="Next", command=self.next_page, width=10).pack(side="left", padx=2)
        ttk.Button(pagination_frame, text="Last", command=self.last_page, width=8).pack(side="left", padx=2)
        
        # Page size selector
        ttk.Label(pagination_frame, text="Page size:").pack(side="left", padx=(20, 5))
        self.page_size_var = tk.StringVar(value=str(self.page_size))
        page_size_combo = ttk.Combobox(pagination_frame, textvariable=self.page_size_var,
                                     values=["100", "500", "1000", "2000", "5000"],
                                     width=8, state="readonly")
        page_size_combo.pack(side="left")
        page_size_combo.bind("<<ComboboxSelected>>", self.on_page_size_changed)
        
        return pagination_frame
    
    def set_data(self, all_points):
        """Set the complete dataset"""
        self.all_points = all_points
        self.total_points = len(all_points)
        self.current_page = 0
        self.update_page_info()
    
    def get_current_page_data(self):
        """Get data for current page"""
        start_idx = self.current_page * self.page_size
        end_idx = min(start_idx + self.page_size, self.total_points)
        
        if start_idx >= self.total_points:
            return []
        
        return self.all_points[start_idx:end_idx]
    
    def first_page(self):
        """Go to first page"""
        if self.current_page != 0:
            self.current_page = 0
            return True
        return False
    
    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            return True
        return False
    
    def next_page(self):
        """Go to next page"""
        total_pages = (self.total_points + self.page_size - 1) // self.page_size
        if self.current_page < total_pages - 1:
            self.current_page += 1
            return True
        return False
    
    def last_page(self):
        """Go to last page"""
        total_pages = (self.total_points + self.page_size - 1) // self.page_size
        if total_pages > 0:
            self.current_page = total_pages - 1
            return True
        return False
    
    def on_page_size_changed(self, event):
        """Handle page size change"""
        try:
            new_page_size = int(self.page_size_var.get())
            if new_page_size > 0:
                self.page_size = new_page_size
                self.current_page = 0  # Reset to first page
                return True
        except ValueError:
            pass
        return False
    
    def update_page_info(self):
        """Update page information label"""
        total_pages = max(1, (self.total_points + self.page_size - 1) // self.page_size)
        current_page_display = self.current_page + 1  # Convert to 1-based
        
        start_point = self.current_page * self.page_size + 1
        end_point = min((self.current_page + 1) * self.page_size, self.total_points)
        
        info_text = f"Page {current_page_display} of {total_pages} ({self.total_points} points: {start_point}-{end_point})"
        if self.page_info_label:
            self.page_info_label.config(text=info_text)
