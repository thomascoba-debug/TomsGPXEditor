"""
Main Window View Implementation

Concrete implementation of MainWindowView using tkinter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Optional, Callable, Dict, Any
import logging

from .main_window_view import MainWindowView
from ...domain.entities import GPXFile
from ..widgets.progress_dialog import ProgressManager

logger = logging.getLogger(__name__)


class MainWindowViewImpl(MainWindowView):
    """Concrete implementation of MainWindowView using tkinter"""
    
    def __init__(self):
        self.root: Optional[tk.Tk] = None
        self.presenter: Optional[Any] = None
        self.file_entries: List[Any] = []
        self.map_widget: Optional[Any] = None
        self.status_var: Optional[tk.StringVar] = None
        self.progress_manager: Optional[ProgressManager] = None
        
        # Menu callbacks
        self.menu_callbacks: Dict[str, Callable] = {}
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the main UI components"""
        self.root = tk.Tk()
        self.root.title("Tom's GPX Editor")
        self.root.geometry("1200x800")
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        
        # Setup main layout
        self._setup_menu()
        self._setup_main_layout()
        self._setup_status_bar()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_menu(self):
        """Setup menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="Open GPX...", command=self._on_open_file)
        file_menu.add_command(label="Save All", command=self._on_save_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        edit_menu.add_command(label="Convert Route to Track", command=self._on_convert_route_to_track)
        edit_menu.add_command(label="Convert Track to Route", command=self._on_convert_track_to_route)
        edit_menu.add_separator()
        edit_menu.add_command(label="Delete Selected", command=self._on_delete_selected)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        
        view_menu.add_command(label="Zoom In", command=self._on_zoom_in)
        view_menu.add_command(label="Zoom Out", command=self._on_zoom_out)
        view_menu.add_command(label="Refresh Map", command=self._on_refresh_map)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        tools_menu.add_command(label="Analyze GPX", command=self._on_analyze_gpx)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        settings_menu.add_command(label="Logging", command=self._on_settings_logging)
        settings_menu.add_command(label="Marker", command=self._on_settings_marker)
        settings_menu.add_command(label="Properties", command=self._on_settings_properties)
        settings_menu.add_command(label="Rendering", command=self._on_settings_rendering)
    
    def _setup_main_layout(self):
        """Setup main layout with file list and map"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel - File list
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=False, padx=(0, 5))
        
        ttk.Label(left_frame, text="GPX Files", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # File list with scrollbar
        file_frame = ttk.Frame(left_frame)
        file_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(file_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.file_listbox = tk.Listbox(file_frame, yscrollcommand=scrollbar.set)
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Right panel - Map
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        
        ttk.Label(right_frame, text="Map View", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Map placeholder (would integrate with actual map widget)
        self.map_frame = ttk.Frame(right_frame, relief="sunken", borderwidth=2)
        self.map_frame.pack(fill="both", expand=True)
        
        # Map placeholder label
        map_label = ttk.Label(self.map_frame, text="Map will be integrated here", 
                              font=("Arial", 14), foreground="gray")
        map_label.pack(expand=True)
        
        # Button frame
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill="x", pady=10)
        
        self.route_to_track_btn = ttk.Button(button_frame, text="Route to Track", 
                                         command=self._on_convert_route_to_track,
                                         state="disabled")
        self.route_to_track_btn.pack(side="left", padx=2)
        
        self.track_to_route_btn = ttk.Button(button_frame, text="Track to Route",
                                         command=self._on_convert_track_to_route,
                                         state="disabled")
        self.track_to_route_btn.pack(side="left", padx=2)
        
        self.delete_btn = ttk.Button(button_frame, text="Delete",
                                  command=self._on_delete_selected,
                                  state="disabled")
        self.delete_btn.pack(side="left", padx=2)
        
        self.analyze_btn = ttk.Button(button_frame, text="Analyze GPX",
                                    command=self._on_analyze_gpx,
                                    state="disabled")
        self.analyze_btn.pack(side="left", padx=2)
    
    def _setup_status_bar(self):
        """Setup status bar"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side="bottom", fill="x", padx=5, pady=2)
        
        ttk.Label(status_frame, textvariable=self.status_var).pack(side="left")
    
    # Menu action handlers
    def _on_open_file(self):
        """Handle open file menu action"""
        if self.presenter:
            file_path = self.show_file_dialog("Open GPX File", [
                ("GPX files", "*.gpx"),
                ("All files", "*.*")
            ])
            if file_path:
                self.presenter.load_gpx_file(file_path)
    
    def _on_save_all(self):
        """Handle save all menu action"""
        if self.presenter:
            # Implementation would depend on presenter
            pass
    
    def _on_convert_route_to_track(self):
        """Handle convert route to track"""
        if self.presenter:
            self.presenter.convert_route_to_track()
    
    def _on_convert_track_to_route(self):
        """Handle convert track to route"""
        if self.presenter:
            self.presenter.convert_track_to_route()
    
    def _on_delete_selected(self):
        """Handle delete selected"""
        if self.presenter:
            self.presenter.delete_files()
    
    def _on_analyze_gpx(self):
        """Handle analyze GPX"""
        if self.presenter:
            self.presenter.analyze_gpx_files()
    
    def _on_zoom_in(self):
        """Handle zoom in"""
        if self.map_widget:
            # Would integrate with actual map widget
            pass
    
    def _on_zoom_out(self):
        """Handle zoom out"""
        if self.map_widget:
            # Would integrate with actual map widget
            pass
    
    def _on_refresh_map(self):
        """Handle refresh map"""
        if self.presenter:
            self.refresh_map()
    
    def _on_settings_logging(self):
        """Handle logging settings"""
        if self.presenter:
            self.presenter.show_settings_dialog("logging")
    
    def _on_settings_marker(self):
        """Handle marker settings"""
        if self.presenter:
            self.presenter.show_settings_dialog("marker")
    
    def _on_settings_properties(self):
        """Handle properties settings"""
        if self.presenter:
            self.presenter.show_settings_dialog("properties")
    
    def _on_settings_rendering(self):
        """Handle rendering settings"""
        if self.presenter:
            self.presenter.show_settings_dialog("rendering")
    
    def _on_closing(self):
        """Handle window closing"""
        if self.presenter:
            # Would ask presenter about saving
            pass
        
        if self.root:
            self.root.destroy()
    
    # View interface implementation
    def set_presenter(self, presenter):
        """Set the presenter for this view"""
        self.presenter = presenter
    
    def update_file_list(self, files: List[GPXFile]):
        """Update the file list display"""
        if not self.file_listbox:
            return
            
        # Clear current list
        self.file_listbox.delete(0, tk.END)
        
        # Add files with colors
        for file in files:
            display_text = f"{file.get_display_name()}"
            self.file_listbox.insert(tk.END, display_text)
            
            # Set color (simplified - would use actual file color)
            if file.is_visible:
                self.file_listbox.itemconfig(tk.END, fg="black")
            else:
                self.file_listbox.itemconfig(tk.END, fg="gray")
    
    def update_conversion_buttons(self, enabled: bool):
        """Enable/disable conversion buttons based on editable files"""
        state = "normal" if enabled else "disabled"
        
        if hasattr(self, 'route_to_track_btn'):
            self.route_to_track_btn.config(state=state)
        if hasattr(self, 'track_to_route_btn'):
            self.track_to_route_btn.config(state=state)
        if hasattr(self, 'delete_btn'):
            self.delete_btn.config(state=state)
        if hasattr(self, 'analyze_btn'):
            self.analyze_btn.config(state=state)
    
    def update_status(self, message: str):
        """Update the status bar message"""
        if self.status_var:
            self.status_var.set(message)
    
    def get_selected_files(self) -> List[str]:
        """Get list of selected file paths"""
        if not self.file_listbox:
            return []
            
        selected_indices = self.file_listbox.curselection()
        selected_files = []
        
        for index in selected_indices:
            # Would need to map index back to file path
            # Simplified implementation
            selected_files.append(f"file_{index}")
        
        return selected_files
    
    def show_error(self, title: str, message: str):
        """Show error dialog"""
        messagebox.showerror(title, message)
    
    def show_info(self, title: str, message: str):
        """Show info dialog"""
        messagebox.showinfo(title, message)
    
    def show_file_dialog(self, title: str, file_types: List[tuple]) -> Optional[str]:
        """Show file open dialog"""
        return filedialog.askopenfilename(
            title=title,
            filetypes=file_types,
            parent=self.root
        )
    
    def show_save_dialog(self, title: str, default_name: str, file_types: List[tuple]) -> Optional[str]:
        """Show file save dialog"""
        return filedialog.asksaveasfilename(
            title=title,
            defaultextension=default_name,
            filetypes=file_types,
            parent=self.root
        )
    
    def confirm_delete(self, file_count: int) -> bool:
        """Show delete confirmation dialog"""
        return messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {file_count} file(s)?",
            parent=self.root
        )
    
    def show_progress(self, message: str, maximum: int) -> 'ProgressManager':
        """Show progress dialog"""
        if not self.progress_manager:
            self.progress_manager = ProgressManager(self.root)
        
        self.progress_manager.start_progress(message, maximum)
        return self.progress_manager
    
    def hide_progress(self):
        """Hide progress dialog"""
        if self.progress_manager:
            self.progress_manager.hide_progress()
    
    def refresh_map(self):
        """Refresh the map display"""
        # Would trigger map refresh
        logger.info("Map refresh requested")
    
    def add_file_to_map(self, gpx_file: GPXFile):
        """Add file to map display"""
        # Would integrate with actual map widget
        logger.info(f"Adding file to map: {gpx_file.path}")
    
    def remove_file_from_map(self, file_path: str):
        """Remove file from map display"""
        # Would integrate with actual map widget
        logger.info(f"Removing file from map: {file_path}")
    
    def update_file_on_map(self, gpx_file: GPXFile):
        """Update file on map display"""
        # Would integrate with actual map widget
        logger.info(f"Updating file on map: {gpx_file.path}")
    
    def set_menu_callbacks(self, callbacks: dict):
        """Set menu action callbacks"""
        self.menu_callbacks = callbacks
    
    def update_recent_files_menu(self, recent_files: List[str]):
        """Update recent files menu"""
        # Would update file menu with recent files
        logger.info(f"Recent files updated: {recent_files}")
    
    def show_settings_dialog(self, dialog_type: str):
        """Show settings dialog"""
        # Would delegate to presenter
        logger.info(f"Settings dialog requested: {dialog_type}")
    
    def show(self):
        """Show the main window"""
        if self.root:
            self.root.deiconify()
            self.root.lift()
    
    def hide(self):
        """Hide the main window"""
        if self.root:
            self.root.withdraw()
    
    def destroy(self):
        """Destroy the main window"""
        if self.root:
            self.root.destroy()
    
    def get_geometry(self) -> str:
        """Get window geometry for persistence"""
        if self.root:
            return self.root.geometry()
        return ""
    
    def set_geometry(self, geometry: str):
        """Set window geometry from persistence"""
        if self.root:
            self.root.geometry(geometry)
