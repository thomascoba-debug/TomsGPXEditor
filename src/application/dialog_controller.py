"""
Dialog Controller - Zentrale Steuerung aller Dialoge

Dieser Controller kümmert sich um:
- Dialog-Erstellung und -Management
- Settings-Dialog Integration
- Menu-Handler für Dialoge
- Callback-Management
"""

import logging
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from src.infrastructure.repositories.properties_repository import AppProperties
from src.ui.dialogs.settings_logging_dialog import LoggingSettingsDialog
from src.ui.dialogs.settings_marker_dialog import MarkerSettingsDialog
from src.ui.dialogs.settings_rendering_dialog import RenderingSettingsDialog
from src.ui.dialogs.settings_properties_dialog import PropertiesEditorDialog
from src.ui.dialogs.settings_language_dialog import LanguageSettingsDialog
from src.ui.dialogs.track_to_route_dialog import TrackToRouteDialog
from src.ui.dialogs.route_to_track_dialog import RouteToTrackDialog
from src.ui.dialogs.track_downsampling_dialog import TrackDownsamplingDialog
from src.i18n import t

logger = logging.getLogger(__name__)


class DialogController:
    """Central control of all dialogs"""
    
    def __init__(self, parent, properties: AppProperties, save_callback: Callable):
        self.parent = parent
        self.properties = properties
        self.save_callback = save_callback
        
    def show_settings_dialog(self) -> None:
        """Open the settings dialog with language selection"""
        try:
            # Create a temporary dialog window for settings selection
            settings_window = tk.Toplevel(self.parent)
            settings_window.title(t("menu.settings"))
            settings_window.geometry("300x200")
            settings_window.resizable(False, False)
            
            # Center the window
            settings_window.transient(self.parent)
            settings_window.grab_set()
            
            frame = ttk.Frame(settings_window)
            frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Settings selection
            ttk.Label(frame, text=t("menu.settings_choose"), font=("TkDefaultFont", 12, "bold")).pack(pady=(0, 10))
            
            # Logging Settings
            logging_btn = ttk.Button(
                frame,
                text=t("menu.settings_items.logging"),
                command=lambda: (settings_window.destroy(), self.show_logging_dialog()),
                width=20
            )
            logging_btn.pack(pady=5)
            
            # Marker Settings
            marker_btn = ttk.Button(
                frame,
                text=t("menu.settings_items.marker"),
                command=lambda: (settings_window.destroy(), self.show_marker_dialog()),
                width=20
            )
            marker_btn.pack(pady=5)
            
            # Rendering Settings
            rendering_btn = ttk.Button(
                frame,
                text=t("menu.settings_items.rendering"),
                command=lambda: (settings_window.destroy(), self.show_rendering_dialog()),
                width=20
            )
            rendering_btn.pack(pady=5)
            
            # Properties Editor
            properties_btn = ttk.Button(
                frame,
                text=t("menu.settings_items.properties"),
                command=lambda: (settings_window.destroy(), self.show_properties_editor_dialog()),
                width=20
            )
            properties_btn.pack(pady=5)
            
            # Language Settings
            language_btn = ttk.Button(
                frame,
                text=t("menu.settings_items.language"),
                command=lambda: (settings_window.destroy(), self.show_language_dialog()),
                width=20
            )
            language_btn.pack(pady=5)
            
            # Separator
            ttk.Separator(frame, orient='horizontal').pack(fill="x", pady=10)
            
            # Close Button
            close_btn = ttk.Button(
                frame,
                text=t("buttons.close"),
                command=settings_window.destroy,
                width=20
            )
            close_btn.pack(pady=5)
            
            logger.debug("Settings selection dialog opened")
            
        except Exception as e:
            logger.error(f"Error opening settings dialog: {e}", exc_info=True)
    
    def show_language_dialog(self) -> None:
        """Öffne den Language-Settings Dialog"""
        try:
            dialog = LanguageSettingsDialog(
                self.parent,
                self.properties,
                self.parent._save_properties_only,  # No map update needed
                modal=True
            )
            logger.debug("Language settings dialog opened")
        except Exception as e:
            logger.error(f"Error opening language dialog: {e}", exc_info=True)
    
    def show_logging_dialog(self) -> None:
        """Öffne den Logging-Settings Dialog"""
        try:
            dialog = LoggingSettingsDialog(
                self.parent,
                self.properties,
                self.parent._save_properties_and_reconfigure_logging,  # No map update needed
                modal=True
            )
            logger.debug("Logging settings dialog opened")
        except Exception as e:
            logger.error(f"Error opening logging dialog: {e}", exc_info=True)
    
    def show_marker_dialog(self) -> None:
        """Öffne den Marker-Settings Dialog"""
        try:
            dialog = MarkerSettingsDialog(
                self.parent,
                self.properties,
                self.parent._save_properties_and_map,  # Map update needed for marker changes
                modal=True
            )
            logger.debug("Marker settings dialog opened")
        except Exception as e:
            logger.error(f"Error opening marker dialog: {e}", exc_info=True)
    
    def show_rendering_dialog(self) -> None:
        """Öffne den Rendering-Settings Dialog"""
        try:
            dialog = RenderingSettingsDialog(
                self.parent,
                self.properties,
                self.parent._save_properties_and_map,  # Map update needed for rendering changes
                modal=True
            )
            logger.debug("Rendering settings dialog opened")
        except Exception as e:
            logger.error(f"Error opening rendering dialog: {e}", exc_info=True)
    
    def show_properties_editor_dialog(self) -> None:
        """Öffne den Properties Editor Dialog"""
        try:
            dialog = PropertiesEditorDialog(
                self.parent,
                self.properties,
                self.parent._save_properties_only,  # No map update needed for properties editor
                modal=True
            )
            logger.debug("Properties editor dialog opened")
        except Exception as e:
            logger.error(f"Error opening properties editor dialog: {e}", exc_info=True)
    
    def show_track_to_route_dialog(self, entries) -> None:
        """Öffne den Track-to-Route Dialog"""
        try:
            dialog = TrackToRouteDialog(self.parent, entries, self.properties, modal=True)
            logger.debug("Track to route dialog opened")
        except Exception as e:
            logger.error(f"Error opening track to route dialog: {e}", exc_info=True)
    
    def show_route_to_track_dialog(self, entries) -> None:
        """Öffne den Route-to-Track Dialog"""
        try:
            dialog = RouteToTrackDialog(self.parent, entries, self.properties, modal=True)
            logger.debug("Route to track dialog opened")
        except Exception as e:
            logger.error(f"Error opening route to track dialog: {e}", exc_info=True)
    
    def show_track_downsampling_dialog(self, entries) -> None:
        """Öffne den Track-Downsampling Dialog"""
        try:
            dialog = TrackDownsamplingDialog(self.parent, entries, self.properties, modal=True)
            logger.debug("Track downsampling dialog opened")
        except Exception as e:
            logger.error(f"Error opening track downsampling dialog: {e}", exc_info=True)
    
    def _reconfigure_logging(self) -> None:
        """Rekonfiguriere das Logging-System"""
        try:
            from app import setup_logging
            setup_logging(self.properties)
            logger.info("Logging reconfigured successfully")
        except Exception as e:
            logger.error(f"Error reconfiguring logging: {e}", exc_info=True)
    
    def create_settings_menu(self, menubar) -> None:
        """Erstelle das Settings-Menü mit allen Dialog-Optionen"""
        
        try:
            settings_menu = tk.Menu(menubar, tearoff=0)
            
            # Logging
            logging_label = t("menu.settings_items.logging")
            settings_menu.add_command(
                label=logging_label,
                command=self.show_logging_dialog
            )
            
            # Marker
            marker_label = t("menu.settings_items.marker")
            settings_menu.add_command(
                label=marker_label,
                command=self.show_marker_dialog
            )
            
            # Rendering
            rendering_label = t("menu.settings_items.rendering")
            settings_menu.add_command(
                label=rendering_label,
                command=self.show_rendering_dialog
            )
            
            # Properties Editor
            properties_label = t("menu.settings_items.properties")
            settings_menu.add_command(
                label=properties_label,
                command=self.show_properties_editor_dialog
            )
            
            # Language (mit insert-Methode zum Testen)
            try:
                # Teste insert-Methode anstelle von add_command
                language_label = t("menu.settings_items.language")
                
                # Füge am Ende vor dem Separator ein
                insert_position = settings_menu.index("end") - 1  # Vor dem Separator
                settings_menu.insert_command(
                    insert_position,
                    label=language_label,
                    command=self.show_language_dialog
                )
                
            except Exception as e:
                import traceback
                traceback.print_exc()
            
            settings_menu.add_separator()
            
            # Restore Clean Snapshot
            restore_label = t("menu.settings_items.restore_snapshot")
            settings_menu.add_command(
                label=restore_label,
                command=self._restore_clean_snapshot
            )
            
            # Prüfe Menu-Einträge vor dem Hinzufügen
            
            settings_label = t("menu.settings")
            menubar.add_cascade(label=settings_label, menu=settings_menu)
            
            # Prüfe Menu-Einträge nach dem Hinzufügen
            
            logger.debug("Settings menu created successfully")
            
        except Exception as e:
            logger.error(f"Error creating settings menu: {e}")
            import traceback
            traceback.print_exc()
            logger.error(f"Error creating settings menu: {e}", exc_info=True)
    
    def create_edit_menu(self, menubar, entries) -> None:
        """Erstelle das Edit-Menü mit Konvertierungs-Optionen"""
        try:
            # Store reference to parent for getting current entries
            # Navigate up to get the main app instance
            parent = menubar
            while hasattr(parent, 'master') and parent.master:
                parent = parent.master
            self.parent_app = parent
            edit_menu = tk.Menu(menubar, tearoff=0)
            
            # Open Track Table Editor
            edit_menu.add_command(
                label=t("menu.edit_open_table_editor"),
                command=lambda: self._open_table_editor(self._get_current_entries())
            )
            # Store reference to menu and index for later updates
            self.track_editor_menu = edit_menu
            self.track_editor_index = 0  # First item in the menu
            
            edit_menu.add_separator()
            
            # Track to Route
            edit_menu.add_command(
                label=t("menu.edit_track_to_route"),
                command=lambda: self.show_track_to_route_dialog(self._get_current_entries())
            )
            self.track_to_route_index = 2  # After separator
            
            # Route to Track
            edit_menu.add_command(
                label=t("menu.edit_route_to_track"), 
                command=lambda: self.show_route_to_track_dialog(self._get_current_entries())
            )
            self.route_to_track_index = 3
            
            edit_menu.add_separator()
            
            # Track Downsampling
            edit_menu.add_command(
                label=t("menu.edit_track_downsampling"),
                command=lambda: self.show_track_downsampling_dialog(self._get_current_entries())
            )
            self.track_downsampling_index = 5  # After second separator
            
            menubar.add_cascade(label=t("menu.edit"), menu=edit_menu)
            logger.debug("Edit menu created successfully")
            
        except Exception as e:
            logger.error(f"Error creating edit menu: {e}", exc_info=True)
    
    def update_track_editor_button(self, entries) -> None:
        """Update all edit menu items based on editable files count"""
        try:
            editable_count = sum(1 for e in entries if e.is_editable())
            
            if hasattr(self, 'track_editor_menu') and self.track_editor_menu:
                # Track Editor: only enabled for exactly one editable file
                if editable_count == 1:
                    self.track_editor_menu.entryconfig(self.track_editor_index, state="normal")
                else:
                    self.track_editor_menu.entryconfig(self.track_editor_index, state="disabled")
                
                # Track to Route, Route to Track, Track Downsampling: enabled for at least one editable file
                state = "normal" if editable_count > 0 else "disabled"
                
                if hasattr(self, 'track_to_route_index'):
                    self.track_editor_menu.entryconfig(self.track_to_route_index, state=state)
                if hasattr(self, 'route_to_track_index'):
                    self.track_editor_menu.entryconfig(self.route_to_track_index, state=state)
                if hasattr(self, 'track_downsampling_index'):
                    self.track_editor_menu.entryconfig(self.track_downsampling_index, state=state)
                    
                logger.debug(f"Edit menu updated: {editable_count} editable files")
        except Exception as e:
            logger.error(f"Error updating edit menu: {e}")
    
    def _get_current_entries(self):
        """Get current entries from the app"""
        try:
            logger.debug(f"Getting current entries, parent_app: {getattr(self, 'parent_app', None)}")
            if hasattr(self, 'parent_app') and hasattr(self.parent_app, 'gpx_file_manager'):
                entries = self.parent_app.gpx_file_manager.get_all_entries()
                logger.debug(f"Found {len(entries)} entries")
                return entries
            logger.debug("No parent_app or gpx_file_manager found")
            return []
        except Exception as e:
            logger.error(f"Error getting current entries: {e}")
            return []
    
    def _open_table_editor(self, entries) -> None:
        """Öffne den Track Table Editor"""
        try:
            from src.ui.widgets.gpx_table_editor import GPXTableEditor
            from src.application.services.gpx_service import GPXEditController
            
            editable_entries = [e for e in entries if e.is_editable()]
            
            logger.debug(f"Track editor: found {len(editable_entries)} editable files")
            
            if len(editable_entries) == 0:
                import tkinter.messagebox as messagebox
                messagebox.showwarning(
                    "No editable file",
                    "Enable editable checkbox for exactly one file."
                )
                return
            elif len(editable_entries) > 1:
                import tkinter.messagebox as messagebox
                messagebox.showwarning(
                    "Multiple editable files",
                    f"Exactly one file must be editable for Track Table Editor.\nCurrently {len(editable_entries)} files are editable."
                )
                return
            
            selected = editable_entries[0]
            logger.debug(f"Track editor: selected file: {selected.get_path()}")
            
            gpx_service = GPXEditController(self.parent)
            
            try:
                logger.debug(f"Track editor: loading document...")
                document = gpx_service.load_document(selected.get_path())
                logger.debug(f"Track editor: document loaded successfully")
                
                logger.debug(f"Track editor: creating GPXTableEditor...")
                GPXTableEditor(
                    self.parent,
                    document,
                    self.save_callback,
                    lambda doc: gpx_service.save_document(doc),
                    self.properties
                )
                logger.debug(f"Track table editor opened for: {selected.get_path()}")
                
            except (ValueError, FileNotFoundError) as e:
                logger.error(f"Track editor: GPX file error: {e}")
                import tkinter.messagebox as messagebox
                messagebox.showerror("GPX File Error", f"Failed to load GPX file:\n{str(e)}")
            except Exception as e:
                logger.error(f"Track editor: Unexpected error: {e}", exc_info=True)
                import tkinter.messagebox as messagebox
                messagebox.showerror("Unexpected Error", f"An unexpected error occurred:\n{str(e)}")
        except Exception as e:
            logger.error(f"Track editor: Critical error: {e}", exc_info=True)
            import tkinter.messagebox as messagebox
            messagebox.showerror("Critical Error", f"A critical error occurred:\n{str(e)}")
                
        except Exception as e:
            logger.error(f"Error opening track table editor: {e}", exc_info=True)
    
    def _restore_clean_snapshot(self) -> None:
        """Stelle den Clean Snapshot wieder her"""
        try:
            import tkinter.messagebox as messagebox
            import os
            import subprocess
            import sys
            
            # Finde letzten Clean Snapshot
            snapshot_dir = None
            archive_dir = "archive"
            
            if os.path.exists(archive_dir):
                for item in os.listdir(archive_dir):
                    if item.startswith("clean_snapshot_") and os.path.isdir(os.path.join(archive_dir, item)):
                        snapshot_dir = os.path.join(archive_dir, item)
                        break
            
            if not snapshot_dir:
                messagebox.showwarning("No Snapshot", "No clean snapshot found in archive/ directory.")
                return
            
            # Bestätigung einholen
            result = messagebox.askyesno(
                "Restore Clean Snapshot",
                f"This will restore project to clean state from:\n{snapshot_dir}\n\n"
                "All current changes will be lost.\n\n"
                "Do you want to continue?"
            )
            
            if not result:
                return
            
            # Restore-Skript ausführen
            restore_script = os.path.join(snapshot_dir, "restore.py")
            if os.path.exists(restore_script):
                subprocess.Popen([sys.executable, restore_script], 
                               cwd=os.getcwd(),
                               creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
                
                messagebox.showinfo("Restore Started", "Clean snapshot restore started.\nThe application will restart automatically.")
                self.parent.quit()
            else:
                messagebox.showerror("Error", f"Restore script not found: {restore_script}")
                
        except Exception as e:
            logger.error(f"Error restoring clean snapshot: {e}", exc_info=True)
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Failed to start restore: {str(e)}")
