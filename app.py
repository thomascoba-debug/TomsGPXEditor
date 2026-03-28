"""
Toms GPX Editor - Main Application (Refactored)

Diese Datei enthält nur noch:
- UI-Initialisierung
- Menü-Steuerung
- Event-Handler
- Delegation an Business-Controller
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import logging

# Import new architecture controllers
from src.infrastructure.repositories.properties_repository import AppProperties
from src.infrastructure.error_handler import safe_execute, GPXEditorException, validate_gpx_data
from src.infrastructure.di_container import configure_container, get_container
from src.infrastructure.container_config import configure_container as setup_container
from src.infrastructure.state_manager import get_state_manager, ApplicationState
from src.infrastructure.resource_manager import get_resource_manager
from src.infrastructure.shutdown_manager import initialize_graceful_shutdown, get_shutdown_manager, ShutdownPriority

# Internationalization
from src.i18n import initialize_language_manager, t

# Business Logic Controllers
from src.application.gpx_file_manager import GPXFileManager
from src.application.map_controller import MapController
from src.application.dialog_controller import DialogController
from src.application.services.recent_files_service import RecentFilesFromSessionManager
from src.application.services.gpx_service import GPXEditController

# UI Components
from src.ui.widgets.progress_dialog import ProgressManager
from src.ui.widgets.context_menu import AutoSaveManager, KeyboardShortcutManager

# Configure logger
logger = logging.getLogger(__name__)


def setup_logging(properties):
    """Setup global logging configuration based on dialog settings only"""
    # Get logging settings from dialog-specific path only
    logging_settings = properties.get("dialogs", {}).get("settings", {}).get("logging", {})
    log_level = logging_settings.get("level", "WARNING")
    log_file = logging_settings.get("file", "applog.txt")
    display_lines = logging_settings.get("display_lines", 100)
    
    # Convert string log level to logging constant
    numeric_level = getattr(logging, str(log_level).upper(), logging.WARNING)
    
    # Clear existing handlers to avoid duplicates
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(name)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Also output to console
        ],
        force=True  # Force reconfiguration
    )
    
    logger.info(f"Logging initialized - Level: {log_level}, File: {log_file}")
    logger.debug(f"Numeric logging level: {numeric_level}")
    logger.debug("Using dialog-specific logging settings")

def reconfigure_logging(properties):
    """Reconfigure logging when settings change"""
    setup_logging(properties)


class TomsGPXEditor(TkinterDnD.Tk):
    """Main Application Window - Refactored Architecture"""
    
    def __init__(self):
        super().__init__()
        
        # Add initialization flag
        self._initialized = False
        
        # Initialize infrastructure components first
        self._initialize_infrastructure()
        
        # Initialize core components from container
        self.properties = self.container.get('properties')
        self.recent_files_manager = self.container.get('recent_files_manager')
        
        # Initialize controllers
        self.gpx_file_manager = None
        self.map_controller = None
        self.dialog_controller = None
        self.gpx_service = GPXEditController(self)
        
        # Initialize language manager
        initialize_language_manager(self.container.get('properties'))
        
        # Set window title after language manager is initialized
        self.title(t("app.title"))
        
        # Initialize UI managers
        self.progress_manager = ProgressManager(self)
        self.auto_save_manager = AutoSaveManager(self.container.get('properties'), self._save_all)
        self.keyboard_manager = KeyboardShortcutManager(self)
        
        # Restore window geometry
        self._restore_window_geometry()
        
        # Build UI FIRST (needed for controllers)
        self._build_ui()
        
        # Initialize controllers AFTER UI is built
        self._initialize_controllers()
        
        # Build menu AFTER controllers are initialized
        try:
            if self.winfo_exists():
                self._build_menu()
        except Exception as e:
            logger.error(f"Failed to build menu: {e}")
            # Don't crash the app, continue without menu
        
        # Setup logging AFTER all imports to avoid conflicts
        setup_logging(self.properties)
        
        # Update conversion button states (will be called after session loading)
        # self._load_session_files()  # Moved to after UI is fully built
        
        # Timer is no longer needed - callback system handles updates
        
        # Mark as initialized
        self._initialized = True
        
        # Set application state to ready
        state_manager = get_state_manager()
        if state_manager.state != ApplicationState.READY:
            state_manager.state = ApplicationState.READY
            logger.info("Application initialized successfully")
        else:
            logger.debug("Application already in ready state")
        
        # Schedule session file loading after app is fully ready
        self.after(1000, self._safe_load_session_files)
        
        # Handle window close (only if window still exists)
        try:
            if self.winfo_exists():
                self.protocol("WM_DELETE_WINDOW", self._on_close)
        except Exception as e:
            logger.warning(f"Could not set window close protocol: {e}")
        
        # Setup drag and drop (only if window still exists)
        try:
            if self.winfo_exists():
                self.drop_target_register(DND_FILES)
                self.dnd_bind("<<Drop>>", self._on_drop)
        except Exception as e:
            logger.warning(f"Could not setup drag and drop: {e}")
    
    def _initialize_infrastructure(self):
        """Initialize infrastructure components"""
        try:
            # Initialize state manager
            state_manager = get_state_manager()
            if state_manager.state != ApplicationState.INITIALIZING:
                state_manager.state = ApplicationState.INITIALIZING
            
            # Initialize resource manager
            resource_manager = get_resource_manager()
            
            # Initialize dependency injection container
            self.container = setup_container(self)
            
            # Initialize graceful shutdown
            initialize_graceful_shutdown()
            
            # Register shutdown handlers
            shutdown_manager = get_shutdown_manager()
            shutdown_manager.register_handler(self._cleanup_on_shutdown, priority=ShutdownPriority.CRITICAL, name="cleanup_app")
            
            logger.info("Infrastructure components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize infrastructure: {e}", exc_info=True)
            # Fallback: try to continue without advanced infrastructure
            try:
                logger.warning("Attempting to continue with basic infrastructure...")
                self._fallback_initialization()
            except Exception as fallback_error:
                logger.error(f"Fallback initialization also failed: {fallback_error}")
                raise
    
    def _fallback_initialization(self):
        """Fallback initialization when advanced infrastructure fails"""
        logger.warning("Using fallback initialization - some advanced features may not work")
        
        # Basic state management
        try:
            state_manager = get_state_manager()
            state_manager.state = ApplicationState.READY
        except Exception as e:
            logger.error(f"State manager fallback failed: {e}")
        
        # Basic resource management
        try:
            resource_manager = get_resource_manager()
        except Exception as e:
            logger.error(f"Resource manager fallback failed: {e}")
        
        logger.info("Fallback initialization completed")
    
    def _build_ui(self):
        """Build the main UI layout"""
        root = ttk.Frame(self)
        root.pack(fill="both", expand=True)
        
        left = ttk.Frame(root)
        left.pack(side="left", fill="y", padx=5, pady=5)
        
        right = ttk.Frame(root)
        right.pack(side="right", fill="both", expand=True)
        
        # File list header
        ttk.Label(left, text=t("menu.file")).pack(anchor="w")
        
        self.file_list_container = ttk.Frame(left)
        self.file_list_container.pack(fill="y", expand=False)
        
        # Main grid for header and file entries
        self.main_grid = ttk.Frame(self.file_list_container)
        self.main_grid.pack(fill="both", expand=True)
        
        # Header row
        ttk.Label(self.main_grid, text=t("file_list.header.visible"), width=2).grid(row=0, column=0, padx=3)
        ttk.Label(self.main_grid, text=t("file_list.header.editable"), width=2).grid(row=0, column=1, padx=3)
        ttk.Label(self.main_grid, text=t("file_list.header.number"), width=4).grid(row=0, column=2, padx=3)
        ttk.Label(self.main_grid, text="", width=3).grid(row=0, column=3, padx=3)
        ttk.Label(self.main_grid, text=t("file_list.header.filename")).grid(row=0, column=4, sticky="w", padx=3)
        ttk.Label(self.main_grid, text=t("file_list.header.type")).grid(row=0, column=5, sticky="w", padx=3)
        
        # Separator
        separator = ttk.Separator(self.main_grid, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=6, sticky="ew", pady=2)
        
        # Initialize map widget first (needed for controllers)
        try:
            from tkintermapview import TkinterMapView
            # Create map widget with error handling
            self.map_widget = TkinterMapView(right)
            self.map_widget.pack(fill="both", expand=True)
            
            # Set basic position and zoom with error handling
            try:
                self.map_widget.set_position(51.0, 10.0)
                self.map_widget.set_zoom(5)
            except Exception as e:
                logger.warning(f"Could not set initial map position/zoom: {e}")
            
            logger.debug("Map widget initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize map widget: {e}")
            # Create a fallback widget
            self.map_widget = ttk.Label(right, text="Map widget failed to initialize\nPlease check tkintermapview installation", 
                                      foreground="red", justify="center")
            self.map_widget.pack(fill="both", expand=True)
            # Continue with fallback widget
        
        # Register UI components in container after they are created
        from src.infrastructure.container_config import ContainerConfig
        config = ContainerConfig(self.container)
        config.configure_ui_components_after_build(self)
        
        # Initialize controllers after map widget is created
        self._initialize_controllers()
        
        # Build control buttons
        self._build_control_buttons(left)
        
        # Load session files AFTER everything is built and stable
        # TEMPORARILY DISABLED to stabilize startup
        # try:
        #     if self.winfo_exists():
        #         self._load_session_files()
        #         self._update_conversion_buttons()
        # except Exception as e:
        #     logger.warning(f"Could not load session files: {e}")
        logger.info("Session file loading temporarily disabled for stability")
    
    def _initialize_controllers(self):
        """Initialize business logic controllers"""
        try:
            # Initialize controllers using factory methods to avoid circular dependencies
            self.gpx_file_manager = GPXFileManager.create_from_container(self.container)
            self.map_controller = MapController.create_from_container(self.container)
            self.dialog_controller = DialogController.create_from_container(self.container)
            
            logger.info("Business logic controllers initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize controllers: {e}", exc_info=True)
            raise
    
    def _build_control_buttons(self, parent):
        """Build control buttons for file management"""
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", pady=10)
        
        # Visibility controls
        visibility_frame = ttk.LabelFrame(btn_frame, text=t("menu.visibility"))
        visibility_frame.pack(side="top", padx=(0, 0), fill="x", pady=(0, 5))
        
        ttk.Button(visibility_frame, text=t("buttons.show_all"), command=self._select_all).pack(side="left", padx=2)
        ttk.Button(visibility_frame, text=t("buttons.hide_all"), command=self._deselect_all).pack(side="left", padx=2)
        ttk.Button(visibility_frame, text=t("buttons.update"), command=self._update_map).pack(side="left", padx=2)
        
        # Edit controls
        edit_frame = ttk.LabelFrame(btn_frame, text=t("menu.edit"))
        edit_frame.pack(side="top", fill="x")
        
        ttk.Button(edit_frame, text=t("buttons.select_all"), command=self._select_all_edit).pack(side="left", padx=2)
        ttk.Button(edit_frame, text=t("buttons.deselect_all"), command=self._deselect_all_edit).pack(side="left", padx=2)
        ttk.Button(edit_frame, text=t("buttons.delete"), command=self._delete_selected).pack(side="left", padx=2)
        
        # GPX Analysis section
        analysis_frame = ttk.LabelFrame(btn_frame, text="GPX Analysis")
        analysis_frame.pack(side="top", fill="x", pady=(10, 0))
        
        self.analyze_btn = ttk.Button(
            analysis_frame,
            text=t("buttons.analyze_gpx"),
            command=self._analyze_selected_gpx,
            state="disabled"  # Initially disabled
        )
        self.analyze_btn.pack(side="left", padx=2)
        
        # Text display for analysis results
        self.analysis_text = tk.Text(analysis_frame, height=8, width=50, wrap=tk.WORD)
        self.analysis_text.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Add scrollbar for text display
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=self.analysis_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.analysis_text.configure(yscrollcommand=scrollbar.set)
    
    def _update_conversion_buttons(self, update_map=True):
        """Update conversion button states based on editable files"""
        # Count editable files directly
        editable_count = 0
        for entry in self.gpx_file_manager.get_all_entries():
            if hasattr(entry, 'editable_var') and entry.editable_var.get():
                editable_count += 1
        
        # Debug logging
        logger.debug(f"_update_conversion_buttons: editable_count={editable_count}, total_entries={len(self.gpx_file_manager.get_all_entries())}")
        
        # Enable/disable conversion buttons
        if editable_count > 0:
            if hasattr(self, 'delete_btn'):
                self.delete_btn.config(state="normal")
            if hasattr(self, 'analyze_btn'):
                self.analyze_btn.config(state="normal")
        else:
            if hasattr(self, 'delete_btn'):
                self.delete_btn.config(state="disabled")
            if hasattr(self, 'analyze_btn'):
                self.analyze_btn.config(state="disabled")
        
        # Update track editor button (only enabled for exactly one editable file)
        if hasattr(self, 'dialog_controller'):
            self.dialog_controller.update_track_editor_button(self.gpx_file_manager.get_all_entries())
        
        # Update map when visibility changes (optional for performance)
        if update_map:
            self._update_map()
        
        logger.debug(f"Updated conversion buttons: {editable_count} editable files found")
    
    def _update_editable_buttons_only(self):
        """Update editable buttons without map update"""
        # Count editable files directly
        editable_count = 0
        for entry in self.gpx_file_manager.get_all_entries():
            if hasattr(entry, 'editable_var') and entry.editable_var.get():
                editable_count += 1
        
        # Debug logging
        logger.debug(f"_update_editable_buttons_only: editable_count={editable_count}, total_entries={len(self.gpx_file_manager.get_all_entries())}")
        
        # Enable/disable conversion buttons
        if editable_count > 0:
            if hasattr(self, 'delete_btn'):
                self.delete_btn.config(state="normal")
            if hasattr(self, 'analyze_btn'):
                self.analyze_btn.config(state="normal")
        else:
            if hasattr(self, 'delete_btn'):
                self.delete_btn.config(state="disabled")
            if hasattr(self, 'analyze_btn'):
                self.analyze_btn.config(state="disabled")
        
        # Update track editor button (only enabled for exactly one editable file)
        if hasattr(self, 'dialog_controller'):
            self.dialog_controller.update_track_editor_button(self.gpx_file_manager.get_all_entries())
        
        # NO MAP UPDATE for editable changes
        logger.debug(f"Updated editable buttons only: {editable_count} editable files found")
    
    # Timer method removed - callback system handles button updates more efficiently
    
    def _build_menu(self):
        menubar = tk.Menu(self)
        
        # File menu
        self._build_file_menu(menubar)
        
        # Edit menu (delegated to dialog controller)
        self.dialog_controller.create_edit_menu(menubar, self.gpx_file_manager.get_all_entries())
        
        # Settings menu (delegated to dialog controller)
        self.dialog_controller.create_settings_menu(menubar)
        
        self.config(menu=menubar)
        logger.debug("Menu bar created successfully")
    
    def _build_file_menu(self, menubar):
        """Build the File menu"""
        file_menu = tk.Menu(menubar, tearoff=0)
        
        file_menu.add_command(label="Open GPX", command=self._open_file_dialog)
        
        # Recent files submenu
        self.recent_files_menu = tk.Menu(file_menu, tearoff=0)
        self._update_recent_files_menu()
        file_menu.add_cascade(label="Recent Files", menu=self.recent_files_menu)
        
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)
        
        menubar.add_cascade(label="File", menu=file_menu)
    
    # Menu and UI event handlers
    def _open_file_dialog(self):
        """Open file dialog for GPX files"""
        files = filedialog.askopenfilenames(filetypes=[("GPX files", "*.gpx")])
        added_files = []
        
        for path in files:
            entry = self.gpx_file_manager.add_file_to_ui(path)
            if entry:
                added_files.append(path)
                logger.info(f"Added file via dialog: {path}")
            else:
                logger.warning(f"Failed to add file via dialog: {path}")
        
        # Update map after adding files
        self._update_map()
        
        # Update recent files menu if files were added
        if added_files:
            # Force reload recent files to ensure they appear in the list
            self.recent_files_manager.reload_recent_files()
            self._update_recent_files_menu()
            logger.info(f"Updated recent files for {len(added_files)} dialog files")
    
    def _on_drop(self, event):
        """Handle drag and drop files"""
        files = self.tk.splitlist(event.data)
        added_files = []
        
        for path in files:
            if path.endswith(".gpx"):
                entry = self.gpx_file_manager.add_file_to_ui(path)
                if entry:
                    added_files.append(path)
                    logger.info(f"Added file via drag and drop: {path}")
                else:
                    logger.warning(f"Failed to add file via drag and drop: {path}")
        
        # Update map after adding files
        self._update_map()
        
        # Update recent files menu if files were added
        if added_files:
            # Force reload recent files to ensure they appear in the list
            self.recent_files_manager.reload_recent_files()
            self._update_recent_files_menu()
            logger.info(f"Updated recent files for {len(added_files)} drag and drop files")
    
    def _select_all(self):
        """Select all files (make visible)"""
        for entry in self.gpx_file_manager.get_all_entries():
            entry.visible_var.set(True)
            entry._save_states()
        
        # Update buttons and fast visibility update
        self._update_conversion_buttons(update_map=False)
        self._update_visibility_only()
    
    def _deselect_all(self):
        """Deselect all files (make invisible)"""
        for entry in self.gpx_file_manager.get_all_entries():
            entry.visible_var.set(False)
            entry._save_states()
        
        # Update buttons and fast visibility update
        self._update_conversion_buttons(update_map=False)
        self._update_visibility_only()
    
    def _select_all_edit(self):
        """Select all files for editing"""
        for entry in self.gpx_file_manager.get_all_entries():
            entry.editable_var.set(True)
            entry._save_states()
        
        # Update button states without map update
        self._update_editable_buttons_only()
    
    def _deselect_all_edit(self):
        """Deselect all files from editing"""
        for entry in self.gpx_file_manager.get_all_entries():
            entry.editable_var.set(False)
            entry._save_states()
        
        # Update button states without map update
        self._update_editable_buttons_only()
    
    def _delete_selected(self):
        """Delete selected files"""
        remaining = []
        deleted_refs = []
        
        for entry in self.gpx_file_manager.get_all_entries():
            if entry.is_editable():
                deleted_refs.append(entry.ref_num)
                entry.destroy()
            else:
                remaining.append(entry)
        
        # Remove from properties
        for ref_num in deleted_refs:
            self.properties.remove_file_from_session(ref_num)
        
        # Update file manager
        self.gpx_file_manager.entries = remaining
        self._update_map()
        
        # Update button states
        self._update_conversion_buttons()
    
    def _analyze_selected_gpx(self):
        """Analyze selected GPX files and display results"""
        from src.application.services.gpx_service import analyze_gpx_file
        
        logger.debug("GPX analysis started")
        
        analysis_results = []
        selected_files = 0
        
        for entry in self.gpx_file_manager.get_all_entries():
            if hasattr(entry, 'editable_var') and entry.editable_var.get():
                selected_files += 1
                try:
                    logger.debug(f"Analyzing file: {entry.path}")
                    
                    # Use existing analysis function
                    analysis = analyze_gpx_file(entry.path)
                    
                    # Create result display
                    import os
                    result = f"📁 {os.path.basename(entry.path)}\n"
                    result += f"   File type: {analysis.get('file_type', 'unknown')}\n"
                    result += f"   Tracks: {analysis.get('track_count', 0)}\n"
                    result += f"   Routes: {analysis.get('route_count', 0)}\n"
                    result += f"   Waypoints: {analysis.get('waypoint_count', 0)}\n"
                    
                    if analysis.get('error'):
                        result += f"   ❌ Error: {analysis['error']}\n"
                    
                    result += "\n"
                    analysis_results.append(result)
                    
                except Exception as ex:
                    logger.error(f"Error analyzing {entry.path}: {str(ex)}", exc_info=True)
                    error_result = f"📁 {os.path.basename(entry.path)}\n   ❌ Error: {str(ex)}\n\n"
                    analysis_results.append(error_result)
        
        # Display results in text widget
        self._display_analysis_results(analysis_results, selected_files)
        
        logger.debug(f"GPX analysis completed: {selected_files} files analyzed")

    def _display_analysis_results(self, analysis_results, selected_files):
        """Display analysis results in the text widget"""
        import tkinter as tk
        
        # Clear previous results
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete(1.0, tk.END)
        
        if selected_files == 0:
            self.analysis_text.insert(tk.END, "⚠️ No files selected for analysis.\n\nPlease select files using the Edit checkboxes and click 'Analyze GPX'.")
        else:
            self.analysis_text.insert(tk.END, f"📊 GPX Analysis Results ({selected_files} file{'s' if selected_files != 1 else ''}):\n\n")
            
            if analysis_results:
                for result in analysis_results:
                    self.analysis_text.insert(tk.END, result)
            else:
                self.analysis_text.insert(tk.END, "No analysis results available.")
        
        # Make text read-only again
        self.analysis_text.config(state=tk.DISABLED)
    
    def _update_map(self):
        """Update the map using the map controller"""
        if self.map_controller:
            entries = self.gpx_file_manager.get_all_entries()
            self.map_controller.update_map(entries)
    
    def _update_visibility_only(self):
        """Fast visibility update without full map reload"""
        if self.map_controller:
            entries = self.gpx_file_manager.get_all_entries()
            self.map_controller.update_visibility_only(entries)
    
    def _update_recent_files_menu(self):
        """Update the recent files menu"""
        # Clear existing menu items
        self.recent_files_menu.delete(0, "end")
        
        recent_files = self.recent_files_manager.get_recent_files()
        
        if not recent_files:
            self.recent_files_menu.add_command(label="(No recent files)", state="disabled")
            return
        
        # Add recent files
        for file_path in recent_files:
            display_name = self.recent_files_manager.get_display_name(file_path)
            self.recent_files_menu.add_command(
                label=display_name,
                command=lambda p=file_path: self._open_recent_file(p)
            )
        
        # Add separator and clear option
        self.recent_files_menu.add_separator()
        self.recent_files_menu.add_command(
            label="Clear Recent Files",
            command=self._clear_recent_files
        )
    
    def _open_recent_file(self, file_path):
        """Open a recent file"""
        if os.path.exists(file_path):
            self.gpx_file_manager.add_file_to_ui(file_path)
            self._update_map()
        else:
            logger.warning(f"Recent file not found: {file_path}")
            self.recent_files_manager.remove_file(file_path)
            self._update_recent_files_menu()
            messagebox.showwarning("File Not Found", 
                                 f"The file no longer exists:\n{file_path}\n\n"
                                 "It has been removed from recent files.")
    
    def _clear_recent_files(self):
        """Clear all recent files"""
        if messagebox.askyesno("Clear Recent Files", 
                              "Are you sure you want to clear all recent files?"):
            self.recent_files_manager.clear_recent_files()
            self._update_recent_files_menu()
    
    def _load_session_files(self):
        """Load session files using the GPX file manager"""
        try:
            self.gpx_file_manager.load_session_files()
            self._update_map()
        except Exception as e:
            logger.error(f"Error loading session files: {e}")
            # Don't crash the app, just continue without session files
    
    def _safe_load_session_files(self):
        """Safely load session files after app is fully initialized"""
        try:
            if self.winfo_exists() and hasattr(self, 'gpx_file_manager'):
                logger.info("Loading session files safely...")
                self._load_session_files()
                self._update_conversion_buttons()
                logger.info("Session files loaded successfully")
            else:
                logger.warning("App not ready for session loading")
        except Exception as e:
            logger.error(f"Safe session loading failed: {e}")
            # Don't crash the app
    
    def _save_properties(self):
        """Save properties and update map"""
        self.properties.save()
        self._update_map()
    
    def _save_properties_only(self):
        """Save properties without updating map"""
        self.properties.save()
    
    def _save_properties_and_map(self):
        """Save properties and update map (for rendering changes)"""
        self.properties.save()
        self._update_map()
    
    def _save_properties_and_reconfigure_logging(self):
        """Save properties and reconfigure logging"""
        self.properties.save()
        # Note: The actual reconfigure_logging is called by the dialog
        # This method just saves properties without map update
    
    def _save_all(self):
        """Save all changes - used by AutoSaveManager"""
        try:
            self.properties.save()
            logger.debug("Auto-save completed successfully")
            return True
        except Exception as e:
            logger.error(f"Auto-save failed: {e}")
            return False
    
    # Window management
    def _restore_window_geometry(self):
        """Restore window geometry from properties"""
        geom = self.properties.get("app.main_window.geometry")
        def set_geom():
            if geom:
                try:
                    logger.debug(f"Setting window geometry: {geom}")
                    self.geometry(geom)
                except Exception as e:
                    logger.debug(f"Error setting geometry: {e}")
                    self.geometry("1200x800")
            else:
                logger.debug("No saved geometry found, using default.")
        self.after(0, set_geom)
    
    def _on_close(self):
        """Handle window close event with graceful shutdown"""
        try:
            # Set application state to shutting down
            state_manager = get_state_manager()
            state_manager.state = ApplicationState.SHUTTING_DOWN
            
            logger.info("Initiating graceful shutdown...")
            
            # Save window geometry
            geom = self.geometry()
            logger.debug(f"Saving window geometry: {geom}")
            self.properties.set("app.main_window.geometry", geom)
            
            # Use graceful shutdown system
            shutdown_manager = get_shutdown_manager()
            shutdown_manager.shutdown()
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}", exc_info=True)
            # Force close if graceful shutdown fails
            try:
                self.properties.save()
            except:
                pass
            self.destroy()
    
    def _cleanup_on_shutdown(self):
        """Cleanup handler for graceful shutdown"""
        try:
            logger.info("Application cleanup started")
            
            # Save properties
            if hasattr(self, 'properties'):
                self.properties.save_dialog_geometries()
                self.properties.save()
                logger.debug("Properties saved in cleanup")
            
            logger.info("Application cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during application cleanup: {e}", exc_info=True)
    
    def run(self):
        """Start the application main loop"""
        self.mainloop()


# Entry point
if __name__ == "__main__":
    app = TomsGPXEditor()
    app.run()
