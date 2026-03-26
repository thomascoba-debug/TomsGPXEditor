import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkintermapview import TkinterMapView
import logging

# Import from new architecture
from src.infrastructure.repositories.properties_repository import AppProperties
from src.infrastructure.error_handler import safe_execute, GPXEditorException, validate_gpx_data
from src.application.services.gpx_service import GPXEditController
from src.application.services.conversion_service import convert_gpx_file, save_converted_gpx
from src.application.services.recent_files_service import RecentFilesFromSessionManager
from src.application.services.command_service import CommandManager, PointMoveCommand, PointEditCommand
from src.ui.dialogs.settings_logging_dialog import LoggingSettingsDialog
from src.ui.dialogs.settings_marker_dialog import MarkerSettingsDialog
from src.ui.dialogs.settings_rendering_dialog import RenderingSettingsDialog
from src.ui.dialogs.settings_properties_dialog import PropertiesEditorDialog
from src.ui.dialogs.track_to_route_dialog import TrackToRouteDialog
from src.ui.dialogs.route_to_track_dialog import RouteToTrackDialog

# UI Widgets from new architecture
from src.ui.widgets.file_entry import FileEntry
from src.ui.widgets.gpx_table_editor import GPXTableEditor
from src.ui.widgets.progress_dialog import ProgressManager
from src.ui.widgets.file_search import FileSearchFrame, FileSearchEngine, AdvancedSearchDialog
from src.ui.widgets.context_menu import ContextMenuManager, AutoSaveManager, KeyboardShortcutManager, QuickActionsManager

# Infrastructure components
from src.infrastructure.map_renderer import render_tracks_on_map, GPXCache

# Core dependencies
import gpxpy
# from debug_decorator import log_all_methods

# Configure logger
logger = logging.getLogger(__name__)

def setup_logging(properties):
    """Setup global logging configuration based on properties"""
    log_level = properties.get("log_level") or "INFO"
    log_file = properties.get("log_file") or "app.log"
    
    # Ensure log_level is not None
    if log_level is None:
        log_level = "INFO"
    
    # Convert string log level to logging constant
    numeric_level = getattr(logging, str(log_level).upper(), logging.INFO)
    
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
    
    logger.debug(f"Logging initialized - Level: {log_level}, File: {log_file}")

def reconfigure_logging(properties):
    """Reconfigure logging when settings change"""
    setup_logging(properties)


# @log_all_methods


class TomsGPXEditor(TkinterDnD.Tk):

    def __init__(self):

        super().__init__()

        self.title("Toms GPX Editor")

        self.properties = AppProperties()
        
        # Initialize recent files manager (based on session files)
        self.recent_files_manager = RecentFilesFromSessionManager(self.properties)
        
        # Initialize quick wins managers
        self.progress_manager = ProgressManager(self)
        # self.context_menu_manager = ContextMenuManager(self)  # Temporarily disabled for testing
        self.auto_save_manager = AutoSaveManager(self.properties, self._save_all)
        self.keyboard_manager = KeyboardShortcutManager(self)
        self.quick_actions_manager = None
        
        # Setup logging first
        setup_logging(self.properties)

        # --------------------------------------------------
        # Fenstergeometrie wiederherstellen
        # --------------------------------------------------

        self._restore_window_geometry()

        # --------------------------------------------------

        self.edit_controller = GPXEditController(self)

        self.entries = []

        self._build_menu()
        self._build_ui()

        # Update conversion button states
        self._update_conversion_buttons()

        # --------------------------------------------------
        # Fenster schließen abfangen
        # --------------------------------------------------

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # --------------------------------------------------
        # Lade Session-Dateien am Ende (nach UI-Aufbau)
        # --------------------------------------------------
        
        self._load_session_files()

    # ------------------------------------------------------------
    # MENU
    # ------------------------------------------------------------

    def _build_menu(self):

        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)

        file_menu.add_command(
            label="Open GPX",
            command=self._open_file_dialog
        )

        # Add recent files submenu
        self.recent_files_menu = tk.Menu(file_menu, tearoff=0)
        self._update_recent_files_menu()
        file_menu.add_cascade(label="Recent Files", menu=self.recent_files_menu)

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self._on_close
        )

        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)

        edit_menu.add_command(
            label="Open Track Table Editor",
            command=self._open_table_editor
        )
        
        edit_menu.add_separator()
        
        self.track_to_route_menu = edit_menu.add_command(
            label="Track to Route",
            command=self._show_track_to_route_dialog
        )
        
        self.route_to_track_menu = edit_menu.add_command(
            label="Route to Track", 
            command=self._show_route_to_track_dialog
        )

        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Store edit_menu reference for menu state updates
        self.edit_menu = edit_menu

        settings_menu = tk.Menu(menubar, tearoff=0)

        settings_menu.add_command(
            label="Logging",
            command=lambda: LoggingSettingsDialog(
                self,
                self.properties,
                lambda: (self._save_properties(), reconfigure_logging(self.properties))
            )
        )

        settings_menu.add_command(
            label="Marker",
            command=lambda: MarkerSettingsDialog(
                self,
                self.properties,
                self._save_properties
            )
        )

        settings_menu.add_command(
            label="Rendering",
            command=lambda: RenderingSettingsDialog(
                self,
                self.properties,
                self._save_properties
            )
        )

        settings_menu.add_command(
            label="Properties Editor",
            command=lambda: PropertiesEditorDialog(
                self,
                self.properties,
                self._save_properties
            )
        )

        menubar.add_cascade(label="Settings", menu=settings_menu)

        self.config(menu=menubar)

    # ------------------------------------------------------------
    # UI
    # ------------------------------------------------------------

    def _build_ui(self):

        root = ttk.Frame(self)
        root.pack(fill="both", expand=True)

        left = ttk.Frame(root)
        left.pack(side="left", fill="y", padx=5, pady=5)

        right = ttk.Frame(root)
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(left, text="GPX Files").pack(anchor="w")

        self.file_list_container = ttk.Frame(left)
        self.file_list_container.pack(fill="y", expand=False)
        
        # Create main grid for header and file entries
        self.main_grid = ttk.Frame(self.file_list_container)
        self.main_grid.pack(fill="both", expand=True)
        
        # Header row in main grid
        ttk.Label(self.main_grid, text="V", width=2).grid(row=0, column=0, padx=3)
        ttk.Label(self.main_grid, text="E", width=2).grid(row=0, column=1, padx=3)
        ttk.Label(self.main_grid, text="Nr", width=4).grid(row=0, column=2, padx=3)
        ttk.Label(self.main_grid, text="", width=3).grid(row=0, column=3, padx=3)
        ttk.Label(self.main_grid, text="Filename").grid(row=0, column=4, sticky="w", padx=3)
        ttk.Label(self.main_grid, text="Type").grid(row=0, column=5, sticky="w", padx=3)
        
        # Separator
        separator = ttk.Separator(self.main_grid, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=6, sticky="ew", pady=2)
        
        # Track current row for file entries
        self.current_row = 2

        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill="x", pady=10)

        # Visibility controls group (relates to first checkbox=visible)
        visibility_frame = ttk.LabelFrame(btn_frame, text="Visibility")
        visibility_frame.pack(side="top", padx=(0, 0), fill="x", pady=(0, 5))

        ttk.Button(
            visibility_frame,
            text="Show All",
            command=self._select_all
        ).pack(side="left", padx=2)

        ttk.Button(
            visibility_frame,
            text="Hide All",
            command=self._deselect_all
        ).pack(side="left", padx=2)

        ttk.Button(
            visibility_frame,
            text="Update Map",
            command=self.update_map
        ).pack(side="left", padx=2)

        # Edit controls group (relates to second checkbox=edit)
        edit_frame = ttk.LabelFrame(btn_frame, text="Edit")
        edit_frame.pack(side="top", fill="x")

        ttk.Button(
            edit_frame,
            text="Select All",
            command=self._select_all_edit
        ).pack(side="left", padx=2)

        ttk.Button(
            edit_frame,
            text="Deselect All",
            command=self._deselect_all_edit
        ).pack(side="left", padx=2)

        # Create conversion buttons with references
        self.route_to_track_btn = ttk.Button(
            edit_frame,
            text="Route to Track",
            command=self._route_to_track,
            state="disabled"  # Initially disabled
        )
        self.route_to_track_btn.pack(side="left", padx=2)

        self.track_to_route_btn = ttk.Button(
            edit_frame,
            text="Track to Route",
            command=self._track_to_route,
            state="disabled"  # Initially disabled
        )
        self.track_to_route_btn.pack(side="left", padx=2)

        self.delete_btn = ttk.Button(
            edit_frame,
            text="Delete",
            command=self._delete_selected,
            state="disabled"  # Initially disabled
        )
        self.delete_btn.pack(side="left", padx=2)

        # GPX Analysis section
        analysis_frame = ttk.LabelFrame(btn_frame, text="GPX Analysis")
        analysis_frame.pack(side="top", fill="x", pady=(10, 0))

        self.analyze_btn = ttk.Button(
            analysis_frame,
            text="Analyze GPX",
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
        
        # Make text read-only
        self.analysis_text.config(state=tk.DISABLED)

        self.map_widget = TkinterMapView(right)
        self.map_widget.pack(fill="both", expand=True)

        self.map_widget.set_position(51.0, 10.0)
        self.map_widget.set_zoom(5)

        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self._on_drop)

    # ------------------------------------------------------------
    # FILE HANDLING
    # ------------------------------------------------------------

    def _open_file_dialog(self):

        files = filedialog.askopenfilenames(
            filetypes=[("GPX files", "*.gpx")]
        )

        for path in files:
            self._add_file(path)

    def _on_drop(self, event):

        files = self.tk.splitlist(event.data)

        for path in files:
            if path.endswith(".gpx"):
                self._add_file(path)

    def _add_file(self, path):

        if not os.path.exists(path):
            return

        logger.info(f"=== ADDING FILE: {path} ===")

        # Add to recent files
        self.recent_files_manager.add_file(path)

        # Analyze GPX file
        file_analysis = self._analyze_gpx_file(path)
        
        # Get reference and settings
        ref_num = self.properties.get_or_create_file_reference(path)
        settings = self.properties.get_file_settings_by_reference(ref_num)
        
        logger.info(f"File {path}: ref_num={ref_num}, settings={settings}")
        
        # Create widgets directly in main grid
        visible_var = tk.BooleanVar()
        editable_var = tk.BooleanVar()
        
        # Load checkbox states
        if settings:
            logger.info(f"Loading settings for ref {ref_num}: visible={settings.get('visible')}, editable={settings.get('editable')}, color={settings.get('color')}")
            visible_var.set(settings.get('visible', True))
            editable_var.set(settings.get('editable', False))
        else:
            logger.warning(f"No settings found for ref {ref_num}, using defaults")
            visible_var.set(True)
            editable_var.set(False)
        
        logger.info(f"After loading: visible={visible_var.get()}, editable={editable_var.get()}")
        
        # Create checkbox change handlers
        def on_visible_change():
            logger.info(f"=== VISIBLE CHANGE for ref {ref_num} ===")
            logger.info(f"Visible changed to: {visible_var.get()}")
            save_states()
            self.update_map()
        
        def on_editable_change():
            logger.info(f"=== EDITABLE CHANGE for ref {ref_num} ===")
            logger.info(f"Editable changed to: {editable_var.get()}")
            save_states()
        
        # Create widgets directly in main_grid
        visible_cb = ttk.Checkbutton(
            self.main_grid,
            variable=visible_var,
            width=2,
            command=on_visible_change
        )
        visible_cb.grid(row=self.current_row, column=0, padx=3)
        
        editable_cb = ttk.Checkbutton(
            self.main_grid,
            variable=editable_var,
            width=2,
            command=on_editable_change
        )
        editable_cb.grid(row=self.current_row, column=1, padx=3)
        
        # Add debug to verify handlers are connected
        logger.info(f"Created handlers for ref {ref_num}: visible_cb connected={visible_cb.cget('command')}, editable_cb connected={editable_cb.cget('command')}")
        
        ref_label = ttk.Label(
            self.main_grid,
            text=f"[{ref_num}]",
            foreground="blue",
            font=("TkDefaultFont", 7),
            width=4
        )
        ref_label.grid(row=self.current_row, column=2, padx=3)
        
        color = settings.get('color', '#0000ff') if settings else '#0000ff'
        color_btn = tk.Button(
            self.main_grid,
            bg=color,
            width=3,
            command=lambda: self._choose_color_for_file(ref_num)
        )
        color_btn.grid(row=self.current_row, column=3, padx=3)
        
        filename_label = ttk.Label(
            self.main_grid,
            text=os.path.basename(path)
        )
        filename_label.grid(row=self.current_row, column=4, sticky="w", padx=3)
        
        # Add file type indicator
        file_type_text = file_analysis.get('file_type', 'unknown').upper()
        if file_analysis.get('file_type') == 'mixed':
            file_type_text = f"T+R ({file_analysis['track_count']},{file_analysis['route_count']})"
        elif file_analysis.get('file_type') == 'track':
            file_type_text = f"T ({file_analysis['track_count']})"
        elif file_analysis.get('file_type') == 'route':
            file_type_text = f"R ({file_analysis['route_count']})"
        
        filetype_label = ttk.Label(
            self.main_grid,
            text=file_type_text,
            foreground="gray",
            font=("TkDefaultFont", 8)
        )
        filetype_label.grid(row=self.current_row, column=5, sticky="w", padx=(5, 0))
        
        # Create simple entry object for tracking
        entry = type('SimpleEntry', (), {
            'path': path,
            'visible_var': visible_var,
            'editable_var': editable_var,
            'color_btn': color_btn,
            'ref_num': ref_num,
            'file_analysis': file_analysis,
            'properties': self.properties,
            'visible_cb': visible_cb,
            'editable_cb': editable_cb,
            'ref_label': ref_label,
            'filename_label': filename_label,
            'filetype_label': filetype_label,
            'is_visible': lambda self: visible_var.get(),
            'get_path': lambda self: path,
            'get_color': lambda self: color_btn['bg'],
            '_save_checkbox_states': lambda self: self._save_states(),
            'destroy': lambda self: self._destroy_widgets()
        })()
        
        # Add save_states method to entry
        def save_states():
            logger.info(f"=== SAVING STATES for ref {ref_num} ===")
            logger.info(f"Before save: visible={visible_var.get()}, editable={editable_var.get()}")
            
            settings = self.properties.get_file_settings_by_reference(ref_num)
            logger.info(f"Current settings in DB: {settings}")
            
            settings['visible'] = visible_var.get()
            settings['editable'] = editable_var.get()
            
            logger.info(f"Settings to save: {settings}")
            self.properties.save_file_settings_by_reference(ref_num, settings)
            
            # Verify save
            saved_settings = self.properties.get_file_settings_by_reference(ref_num)
            logger.info(f"Settings after save: {saved_settings}")
            
            # Update edit menu state after editable state changes
            self._update_edit_menu_state()
        
        def destroy_widgets():
            # Remove all widgets from grid
            visible_cb.grid_remove()
            editable_cb.grid_remove()
            ref_label.grid_remove()
            color_btn.grid_remove()
            filename_label.grid_remove()
            filetype_label.grid_remove()
        
        entry._save_states = save_states
        entry._destroy_widgets = destroy_widgets
        
        self.entries.append(entry)
        self.current_row += 1

        self._save_session_file(path)

        # Update recent files from session files
        self.recent_files_manager.sync_with_session_files()

        # Update conversion button states
        self._update_conversion_buttons()
        
        # Start timer to keep buttons updated
        self._start_button_update_timer()

        # Verzögertes Karten-Update für korrekte Initialisierung
        self.after(100, self._delayed_map_update)
    
    def _analyze_gpx_file(self, path):
        """Analyze GPX file and return file type information"""
        try:
            import gpxpy
            with open(path, 'r', encoding='utf-8') as f:
                gpx = gpxpy.parse(f)
            
            track_count = len(gpx.tracks)
            route_count = len(gpx.routes)
            waypoint_count = len(gpx.waypoints)
            
            if track_count > 0 and route_count > 0:
                file_type = 'mixed'
            elif track_count > 0:
                file_type = 'track'
            elif route_count > 0:
                file_type = 'route'
            else:
                file_type = 'waypoints'
            
            return {
                'file_type': file_type,
                'track_count': track_count,
                'route_count': route_count,
                'waypoint_count': waypoint_count
            }
        except Exception as e:
            return {
                'file_type': 'unknown',
                'track_count': 0,
                'route_count': 0,
                'waypoint_count': 0
            }
    
    def _choose_color_for_file(self, ref_num):
        """Simple color chooser for file"""
        from tkinter import colorchooser
        
        color = colorchooser.askcolor()[1]
        if color:
            # Update color in settings
            settings = self.properties.get_file_settings_by_reference(ref_num)
            settings['color'] = color
            self.properties.save_file_settings_by_reference(ref_num, settings)
            
            # Find and update color button
            for entry in self.entries:
                if hasattr(entry, 'ref_num') and entry.ref_num == ref_num:
                    entry.color_btn.configure(bg=color)
                    break
            
            self.update_map()

    # ------------------------------------------------------------

    def update_map(self):
        """Aktualisiere die Karte und zoome auf sichtbare GPX-Daten"""
        render_tracks_on_map(
            self.map_widget,
            self.entries,
            self.properties
        )
        
        # Nach dem Rendern auf GPX-Daten zoomen
        self._fit_map_to_gpx()

    def _delayed_map_update(self):
        """Verzögertes Karten-Update für korrekte Initialisierung"""
        try:
            # Normale Karte aktualisieren (inkl. Fit-to-GPX)
            self.update_map()
                
        except Exception as e:
            print(f"Fehler beim verzögerten Karten-Update: {e}")
            # Fallback: normales Update
            self.update_map()

    def _fit_map_to_gpx(self):
        """Zoomt die Karte auf alle sichtbaren GPX-Daten"""
        try:
            all_coords = []
            
            # Sammle alle Koordinaten von sichtbaren Einträgen
            for entry in self.entries:
                # Direkte Sichtbarkeits-Prüfung statt entry.is_visible()
                is_visible = False
                try:
                    # Hole Sichtbarkeit aus Properties direkt
                    session_files = self.properties.data.get('session_files', {})
                    for ref_num, file_info in session_files.items():
                        if file_info.get('path') == entry.get_path():
                            is_visible = file_info.get('settings', {}).get('visible', True)
                            break
                except:
                    is_visible = True  # Fallback: sichtbar
                
                if is_visible:
                    gpx_data = GPXCache.get_gpx(entry.get_path())
                    if gpx_data:
                        # Track-Punkte
                        for track in gpx_data.tracks:
                            for segment in track.segments:
                                for point in segment.points:
                                    all_coords.append((point.latitude, point.longitude))
                        
                        # Route-Punkte
                        for route in gpx_data.routes:
                            for point in route.points:
                                all_coords.append((point.latitude, point.longitude))
                        
                        # Waypoints
                        for waypoint in gpx_data.waypoints:
                            all_coords.append((waypoint.latitude, waypoint.longitude))
            
            if all_coords:
                # Berechne Grenzen
                lats = [coord[0] for coord in all_coords]
                lons = [coord[1] for coord in all_coords]
                
                min_lat, max_lat = min(lats), max(lats)
                min_lon, max_lon = min(lons), max(lons)
                
                # Zentriere Karte auf GPX-Daten
                center_lat = (min_lat + max_lat) / 2
                center_lon = (min_lon + max_lon) / 2
                
                # Setze Kartenposition und Zoom
                if hasattr(self.map_widget, 'set_position'):
                    self.map_widget.set_position(center_lat, center_lon)
            else:
                # Keine GPX-Daten sichtbar - zeige Standard-Karten-Position
                if hasattr(self.map_widget, 'set_position'):
                    # Standard-Position (Mitte Deutschland)
                    self.map_widget.set_position(50.0, 10.0)
                
                # Erzwinge Karten-Update für Standard-Position
                try:
                    self.map_widget.update()
                except:
                    pass
                
                # Erzwinge stärkeres Karten-Update
                try:
                    self.map_widget.update()
                    # Zusätzliche Updates für TkinterMapView
                    if hasattr(self.map_widget, 'canvas'):
                        self.map_widget.canvas.update()
                    if hasattr(self.map_widget, 'canvas'):
                        self.map_widget.canvas.update_idletasks()
                except:
                    pass
                
        except Exception as e:
            print(f"Fehler beim Fit-to-GPX: {e}")

    # ------------------------------------------------------------

    def _select_all(self):
        logger.info("=== SELECT ALL CALLED ===")
        logger.info(f"Number of entries: {len(self.entries)}")

        for e in self.entries:
            logger.info(f"Processing entry: visible before={e.visible_var.get()}")
            e.visible_var.set(True)
            logger.info(f"Processing entry: visible after={e.visible_var.get()}")
            if hasattr(e, '_save_states'):
                logger.info(f"Calling save_states for entry")
                e._save_states()
            else:
                logger.warning(f"Entry has no _save_states method")

        self.update_map()
        logger.info("=== SELECT ALL FINISHED ===")

    def _deselect_all(self):

        for e in self.entries:
            e.visible_var.set(False)
            if hasattr(e, '_save_states'):
                e._save_states()

        self.update_map()

    def _select_all_edit(self):
        """Select all edit checkboxes"""
        logger.info("=== SELECT ALL EDIT CALLED ===")
        for e in self.entries:
            logger.info(f"Setting editable=True for entry")
            e.editable_var.set(True)
            if hasattr(e, '_save_states'):
                logger.info(f"Calling save_states for editable change")
                e._save_states()
        logger.info("=== SELECT ALL EDIT FINISHED ===")

    def _deselect_all_edit(self):
        """Deselect all edit checkboxes"""
        logger.info("=== DESELECT ALL EDIT CALLED ===")
        for e in self.entries:
            logger.info(f"Setting editable=False for entry")
            e.editable_var.set(False)
            if hasattr(e, '_save_states'):
                logger.info(f"Calling save_states for deselect")
                e._save_states()
        logger.info("=== DESELECT ALL EDIT FINISHED ===")

    def _route_to_track(self):
        """Convert selected GPX routes to tracks"""
        logger.debug("Route to track conversion started")
        
        converted_count = 0
        error_count = 0
        
        for e in self.entries:
            if e.editable_var.get():
                try:
                    logger.debug(f"Converting file: {e.path}")
                    
                    success, message, gpx_data = convert_gpx_file(e.path, 'route_to_track')
                    
                    if success:
                        # Show save dialog for new file
                        original_name = os.path.splitext(os.path.basename(e.path))[0]
                        suggested_name = f"{original_name}_converted_tracks.gpx"
                        
                        save_path = filedialog.asksaveasfilename(
                            parent=self,
                            title="Save converted GPX file",
                            initialfile=suggested_name,
                            defaultextension=".gpx",
                            filetypes=[("GPX files", "*.gpx"), ("All files", "*.*")]
                        )
                        
                        if save_path:
                            # Save the converted file
                            success_save, message_save = save_converted_gpx(gpx_data, save_path)
                            
                            if success_save:
                                logger.info(f"Successfully converted routes to tracks and saved to: {save_path}")
                                
                                # Add the new file to the file list
                                self._add_file(save_path)
                                converted_count += 1
                            else:
                                logger.error(f"Failed to save converted file: {message_save}")
                                error_count += 1
                        else:
                            logger.debug("User cancelled save dialog")
                    else:
                        logger.error(f"Failed to convert {e.path}: {message}")
                        error_count += 1
                        
                except Exception as ex:
                    logger.error(f"Exception converting {e.path}: {str(ex)}")
                    error_count += 1
        
        logger.info(f"Route to track conversion completed: {converted_count} files converted, {error_count} errors")

    def _track_to_route(self):
        """Convert selected GPX tracks to routes"""
        logger.debug("Track to route conversion started")
        
        converted_count = 0
        error_count = 0
        no_tracks_files = []
        conversion_results = []
        
        for e in self.entries:
            if e.editable_var.get():
                try:
                    logger.debug(f"Converting file: {e.path}")
                    
                    success, message, gpx_data = convert_gpx_file(e.path, 'track_to_route')
                    
                    logger.debug(f"Conversion result for {e.path}: success={success}, message={message}")
                    conversion_results.append((os.path.basename(e.path), success, message))
                    
                    if success:
                        # Show save dialog for new file
                        original_name = os.path.splitext(os.path.basename(e.path))[0]
                        suggested_name = f"{original_name}_converted_routes.gpx"
                        
                        logger.debug(f"Opening save dialog with suggested name: {suggested_name}")
                        
                        save_path = filedialog.asksaveasfilename(
                            parent=self,
                            title="Save converted GPX file",
                            initialfile=suggested_name,
                            defaultextension=".gpx",
                            filetypes=[("GPX files", "*.gpx"), ("All files", "*.*")]
                        )
                        
                        logger.debug(f"Save dialog result: {save_path}")
                        
                        if save_path:
                            # Save the converted file
                            success_save, message_save = save_converted_gpx(gpx_data, save_path)
                            
                            if success_save:
                                logger.info(f"Successfully converted tracks to routes and saved to: {save_path}")
                                
                                # Add the new file to the file list
                                self._add_file(save_path)
                                converted_count += 1
                            else:
                                logger.error(f"Failed to save converted file: {message_save}")
                                error_count += 1
                        else:
                            logger.debug("User cancelled save dialog")
                    else:
                        # Check if the error is "No tracks found"
                        if "No tracks found" in message:
                            no_tracks_files.append(os.path.basename(e.path))
                        else:
                            logger.error(f"Failed to convert {e.path}: {message}")
                            error_count += 1
                        
                except Exception as ex:
                    logger.error(f"Exception converting {e.path}: {str(ex)}", exc_info=True)
                    conversion_results.append((os.path.basename(e.path), False, f"Exception: {str(ex)}"))
                    error_count += 1
        
        # Show result messagebox
        self._show_conversion_results(conversion_results, converted_count, error_count, no_tracks_files)
        
        logger.info(f"Track to route conversion completed: {converted_count} files converted, {error_count} errors")

    def _show_conversion_results(self, conversion_results, converted_count, error_count, no_tracks_files):
        """Show conversion results in a messagebox"""
        title = "Track to Route Conversion Results"
        
        if converted_count > 0:
            message = f"Successfully converted {converted_count} file(s) to routes.\n\n"
        else:
            message = "No files were converted.\n\n"
        
        # Add details about each file
        if conversion_results:
            message += "Details:\n"
            for filename, success, msg in conversion_results:
                if success:
                    message += f"✓ {filename}: Converted successfully\n"
                else:
                    message += f"✗ {filename}: {msg}\n"
        
        # Add specific message about files with no tracks
        if no_tracks_files:
            message += f"\nNote: The following files contain no tracks:\n"
            for filename in no_tracks_files:
                message += f"• {filename}\n"
            message += "\nThese files may only contain routes or waypoints."
        
        # Add error count if any
        if error_count > 0:
            message += f"\n{error_count} file(s) had conversion errors."
        
        # Choose appropriate icon based on results
        if converted_count > 0:
            icon = "info"
        elif no_tracks_files:
            icon = "warning"
        else:
            icon = "error"
        
        messagebox.showinfo(title, message, icon=icon)

    def _analyze_selected_gpx(self):
        """Analyze selected GPX files and display results"""
        logger.debug("GPX analysis started")
        
        analysis_results = []
        selected_files = 0
        
        for e in self.entries:
            if e.editable_var.get():
                selected_files += 1
                try:
                    logger.debug(f"Analyzing file: {e.path}")
                    
                    # Use existing analysis from file_entry
                    analysis = e.file_analysis
                    
                    # Also do detailed GPX parsing with error handling
                    try:
                        with open(e.path, 'r', encoding='utf-8') as f:
                            gpx_data = gpxpy.parse(f)
                    except Exception as parse_error:
                        logger.error(f"Error parsing GPX file {e.path}: {str(parse_error)}")
                        result = f"📁 {os.path.basename(e.path)}\n"
                        result += f"   ❌ Error: Failed to parse GPX file\n"
                        result += f"   Details: {str(parse_error)}\n"
                        analysis_results.append(result)
                        continue
                    
                    # Create detailed analysis
                    result = f"📁 {os.path.basename(e.path)}\n"
                    result += f"   File type: {analysis.get('file_type', 'unknown')}\n"
                    
                    # Use actual parsed data instead of cached analysis
                    has_tracks = len(gpx_data.tracks) > 0
                    has_routes = len(gpx_data.routes) > 0
                    
                    result += f"   Has tracks: {has_tracks} "
                    result += f"   Tracks: {len(gpx_data.tracks)}\n"
                    result += f"   Has routes: {has_routes} "
                    result += f"   Routes: {len(gpx_data.routes)}\n"
                    
                    # Calculate total points
                    total_track_points = 0
                    if gpx_data.tracks:
                        for track in gpx_data.tracks:
                            for segment in track.segments:
                                total_track_points += len(segment.points)
                    
                    total_route_points = 0
                    if gpx_data.routes:
                        for route in gpx_data.routes:
                            total_route_points += len(route.points)
                    
                    total_points = total_track_points + total_route_points + len(gpx_data.waypoints)
                    
                    # Add total points summary
                    result += f"   📊 Total Points: {total_points}\n"
                    result += f"      Track Points: {total_track_points}\n"
                    result += f"      Route Points: {total_route_points}\n"
                    result += f"      Waypoints: {len(gpx_data.waypoints)}\n"
                    
                    # Track details
                    if gpx_data.tracks:
                        result += f"   Track details:\n"
                        for i, track in enumerate(gpx_data.tracks):
                            track_points = sum(len(seg.points) for seg in track.segments)
                            result += f"     Track {i+1}: {len(track.segments)} segments, {track_points} points\n"
                            if track.name:
                                result += f"       Name: {track.name}\n"
                    
                    # Route details
                    if gpx_data.routes:
                        result += f"   Route details:\n"
                        for i, route in enumerate(gpx_data.routes):
                            result += f"     Route {i+1}: {len(route.points)} points\n"
                            if route.name:
                                result += f"       Name: {route.name}\n"
                    
                    result += "\n"
                    analysis_results.append(result)
                    
                except Exception as ex:
                    logger.error(f"Error analyzing {e.path}: {str(ex)}", exc_info=True)
                    error_result = f"📁 {os.path.basename(e.path)}\n   ❌ Error: {str(ex)}\n\n"
                    analysis_results.append(error_result)
        
        # Display results in text widget
        self._display_analysis_results(analysis_results, selected_files)
        
        logger.debug(f"GPX analysis completed: {selected_files} files analyzed")

    def _display_analysis_results(self, analysis_results, selected_files):
        """Display analysis results in the text widget"""
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

    def _delete_selected(self):
        remaining = []
        deleted_refs = []
        
        for e in self.entries:
            if e.editable_var.get():
                deleted_refs.append(e.ref_num)
                e.destroy()  # Use the new destroy method
            else:
                remaining.append(e)
        
        # Remove deleted files from session_files in properties
        for ref_num in deleted_refs:
            self.properties.remove_file_from_session(ref_num)
        
        self.entries = remaining
        self.update_map()

    # ------------------------------------------------------------

    def _open_table_editor(self):

        selected = None

        for e in self.entries:
            if e.is_editable():
                selected = e
                break

        if not selected:
            messagebox.showwarning(
                "No editable file",
                "Enable editable checkbox."
            )
            return

        try:
            document = self.edit_controller.load_document(
                selected.get_path()
            )
        except (ValueError, FileNotFoundError) as e:
            messagebox.showerror(
                "GPX File Error",
                f"Failed to load GPX file:\n{str(e)}"
            )
            return
        except Exception as e:
            messagebox.showerror(
                "Unexpected Error",
                f"An unexpected error occurred while loading the GPX file:\n{str(e)}"
            )
            return

        GPXTableEditor(
            self,
            document,
            self.update_map,
            lambda doc: self.edit_controller.save_document(doc)
        )

    # ------------------------------------------------------------

    def _load_session_files(self):
        session_files = self.properties.get("files.session") or self.properties.get("session_files") or {}
        
        # Sort reference numbers numerically
        sorted_refs = sorted(session_files.keys(), key=int)
        
        for ref_num in sorted_refs:
            file_data = session_files[ref_num]
            file_path = file_data.get("path")
            if file_path and os.path.exists(file_path):
                self._add_file(file_path)
        
        # Update map after loading all files to show visible tracks
        self.update_map()

    def _save_session_file(self, path):
        ref_num = self.properties.get_or_create_file_reference(path)

    # ------------------------------------------------------------

    def _save_properties(self):

        self.properties.save()
        self.update_map()

    # ------------------------------------------------------------
    # Fenstergeometrie
    # ------------------------------------------------------------

    def _restore_window_geometry(self):
        geom = self.properties.get("main_window_geometry")
        def set_geom():
            if geom:
                try:
                    logger.debug(f"Setze Fenstergeometrie: {geom}")
                    self.geometry(geom)
                except Exception as e:
                    logger.debug(f"Fehler beim Setzen der Geometrie: {e}")
                    self.geometry("1200x800")
            else:
                logger.debug("Keine gespeicherte Geometrie gefunden, nutze Default.")
        self.after(0, set_geom)

    def _update_edit_menu_state(self):
        """Update edit menu items based on editable files count"""
        editable_count = sum(1 for entry in self.entries if entry.editable_var.get())
        
        # Enable/disable menu items based on editable files
        new_state = "normal" if editable_count > 0 else "disabled"
        
        # Only update if state actually changed
        if not hasattr(self, '_last_menu_state') or self._last_menu_state != new_state:
            # Reduced logging - only log state changes
            logger.info(f"Edit menu state changed: {editable_count} editable files -> {new_state}")
            
            try:
                # Configure menu items by index in edit_menu
                # Open Track Table Editor is at index 0
                # Track to Route is at index 2 (after separator)
                # Route to Track is at index 3
                self.edit_menu.entryconfig(0, state=new_state)  # Open Track Table Editor
                self.edit_menu.entryconfig(2, state=new_state)  # Track to Route
                self.edit_menu.entryconfig(3, state=new_state)  # Route to Track
            except Exception as e:
                logger.error(f"Error updating menu state: {e}")
            
            # Store current state
            self._last_menu_state = new_state

    def _show_track_to_route_dialog(self):
        """Show Track to Route dialog"""
        logger.debug("_show_track_to_route_dialog called")
        dialog = TrackToRouteDialog(self, self.entries, self.properties)
        
    def _show_route_to_track_dialog(self):
        """Show Route to Track dialog"""
        logger.debug("_show_route_to_track_dialog called")
        dialog = RouteToTrackDialog(self, self.entries, self.properties)

    def _on_close(self):
        geom = self.geometry()
        logger.debug(f"Speichere Fenstergeometrie: {geom}")
        self.properties.set(
            "main_window_geometry",
            geom
        )
        
        # Cleanup: Remove non-existent files from session
        session_files = self.properties.get('session_files', {})
        files_to_remove = []
        
        for ref, data in session_files.items():
            path = data.get('path', '')
            if not os.path.exists(path):
                files_to_remove.append(ref)
                logger.debug(f"Entferne nicht existierende Datei: {path}")
        
        # Remove non-existent files
        for ref in files_to_remove:
            del session_files[ref]
        
        if files_to_remove:
            self.properties.set('session_files', session_files)
            logger.debug(f"{len(files_to_remove)} nicht existierende Dateien entfernt")
        
        self.properties.save()
        
        self.destroy()
    
    def _update_recent_files_menu(self):
        """Update the recent files menu"""
        # Clear existing menu items
        self.recent_files_menu.delete(0, "end")
        
        recent_files = self.recent_files_manager.get_recent_files()
        
        if not recent_files:
            self.recent_files_menu.add_command(
                label="(No recent files)",
                state="disabled"
            )
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
            self._add_file(file_path)
        else:
            # File doesn't exist, remove from recent files
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
    
    def _update_conversion_buttons(self):
        """Update conversion button states based on editable files"""
        # Count editable files directly
        editable_count = 0
        for entry in self.entries:
            if hasattr(entry, 'editable_var') and entry.editable_var.get():
                editable_count += 1
        
        # Debug logging
        logger.debug(f"_update_conversion_buttons: editable_count={editable_count}, total_entries={len(self.entries)}")
        
        # Enable/disable conversion buttons
        if editable_count > 0:
            self.route_to_track_btn.config(state="normal")
            self.track_to_route_btn.config(state="normal")
            self.delete_btn.config(state="normal")
            self.analyze_btn.config(state="normal")
        else:
            self.route_to_track_btn.config(state="disabled")
            self.track_to_route_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")
            self.analyze_btn.config(state="disabled")
        
        # Update edit menu state as well
        self._update_edit_menu_state()
        
        logger.debug(f"Updated conversion buttons: {editable_count} editable files found")
    
    def _start_button_update_timer(self):
        """Start timer to periodically update button states"""
        def update_buttons():
            self._update_conversion_buttons()
            # Schedule next update
            self.after(3000, update_buttons)  # Update every 3 seconds instead of 1
        
        # Start the timer
        self.after(1000, update_buttons)
    
    def _save_all(self):
        """Save all changes - used by AutoSaveManager"""
        try:
            # Save properties
            self.properties.save()
            logger.debug("Auto-save completed successfully")
            return True
        except Exception as e:
            logger.error(f"Auto-save failed: {e}")
            return False

    # ------------------------------------------------------------

    def run(self):

        self.mainloop()
