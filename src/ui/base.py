import tkinter as tk
import logging

# Configure logger
logger = logging.getLogger(__name__)

class PersistentDialog(tk.Toplevel):

    def __init__(self, parent, properties, dialog_name=None, modal=False):

        super().__init__(parent)
        self.properties = properties

        # Dialog-Name explizit setzen, falls übergeben, sonst Klassenname
        self.dialog_name = dialog_name if dialog_name else self.__class__.__name__

        # Make modal if requested
        if modal:
            self.transient(parent)  # Keep dialog on top of parent
            self.grab_set()  # Make dialog modal

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Geometrie nach Initialisierung setzen (für einfache Dialoge)
        self._restore_geometry()

    def _restore_geometry(self):
        geo = self.properties.get_dialog_geometry(self.dialog_name)
        logger.debug(f"_restore_geometry: dialog_name={self.dialog_name}, geo={geo}")
        logger.debug(f"_restore_geometry: alle dialog_geometry-Keys: {list(self.properties.data.get('dialog_geometry', {}).keys())}")
        def set_geom():
            logger.debug(f"{self.dialog_name}: setze geometry: {geo}")
            if geo:
                try:
                    self.geometry(geo)
                    self.update_idletasks()
                    actual = self.geometry()
                    logger.debug(f"{self.dialog_name}: tatsächliche geometry nach Setzen: {actual}")
                    if actual != geo:
                        logger.debug(f"{self.dialog_name}: Warnung: geometry wurde nicht exakt übernommen!")
                except Exception as e:
                    logger.debug(f"{self.dialog_name}: Fehler beim Setzen der geometry: {e}")
        self.after(0, set_geom)

    def _on_close(self):

        self._save_geometry()

        self.destroy()

    def _save_geometry(self):

        try:
            geo = self.geometry()
            logger.debug(f"{self.dialog_name}: speichere geometry: {geo}")
            logger.debug(f"{self.dialog_name}: rufe set_dialog_geometry auf")
            self.properties.set_dialog_geometry(
                self.dialog_name,
                geo
            )
            logger.debug(f"{self.dialog_name}: set_dialog_geometry abgeschlossen")
        except Exception as e:
            logger.debug(f"{self.dialog_name}: Fehler beim Speichern der geometry: {e}")
            import traceback
            traceback.print_exc()
