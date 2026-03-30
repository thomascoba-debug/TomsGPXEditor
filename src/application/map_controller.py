"""
Map Controller - Zentrale Steuerung der Kartenansicht

Dieser Controller kümmert sich um:
- Karten-Aktualisierung
- Zentrierung auf GPX-Daten
- Sichtbarkeits-Management
- Koordinaten-Berechnung
"""

import logging
from typing import List, Optional, Tuple
from tkintermapview import TkinterMapView

from src.infrastructure.repositories.properties_repository import AppProperties
from src.infrastructure.map_renderer import GPXCache, render_tracks_on_map

logger = logging.getLogger(__name__)


class MapController:
    """Zentrale Steuerung der Kartenansicht"""
    
    def __init__(self, map_widget: TkinterMapView, properties: AppProperties):
        self.map_widget = map_widget
        self.properties = properties
        
    def update_map(self, entries) -> None:
        """Aktualisiere die Karte mit allen Einträgen"""
        try:
            logger.debug(f"Updating map with {len(entries)} entries")
            
            # Check if map widget is still valid
            if not self.map_widget or not self.map_widget.winfo_exists():
                logger.warning("Map widget no longer exists, skipping update")
                return
            
            # Filter out entries with destroyed widgets
            valid_entries = []
            for entry in entries:
                try:
                    # Test if the widget still exists
                    if hasattr(entry, 'widgets') and entry.widgets:
                        for widget_name, widget in entry.widgets.items():
                            if hasattr(widget, 'winfo_exists') and not widget.winfo_exists():
                                logger.debug(f"Widget {widget_name} destroyed, skipping entry")
                                break
                        else:
                            # All widgets exist
                            valid_entries.append(entry)
                    else:
                        # Entry without widgets or widgets check method
                        valid_entries.append(entry)
                except Exception as e:
                    logger.debug(f"Error checking entry widgets: {e}")
                    # Skip this entry
                    continue
            
            if not valid_entries:
                logger.debug("No valid entries to render")
                return
            
            # Rendere Tracks und Marker
            render_tracks_on_map(
                self.map_widget,
                valid_entries,
                self.properties
            )
            
            # Zentriere auf GPX-Daten
            self.fit_to_gpx(valid_entries)
            
            logger.debug("Map update completed successfully")
            
        except Exception as e:
            logger.error(f"Error updating map: {e}", exc_info=True)
            # Don't re-raise, just log and continue
    
    def update_visibility_only(self, entries) -> None:
        """Schnelle Sichtbarkeits-Update ohne kompletten Neuaufbau"""
        try:
            logger.debug(f"Fast visibility update with {len(entries)} entries")
            
            # Nur Sichtbarkeit aktualisieren, ohne kompletten Neuaufbau
            render_tracks_on_map(
                self.map_widget,
                entries,
                self.properties
            )
            
            # Keine Neuzentrierung für bessere Performance
            logger.debug("Fast visibility update completed successfully")
            
        except Exception as e:
            logger.error(f"Error updating visibility: {e}", exc_info=True)
    
    def fit_to_gpx(self, entries) -> None:
        """Zentriere die Karte auf alle sichtbaren GPX-Daten"""
        try:
            all_coords = []
            
            # Sammle alle Koordinaten von sichtbaren Einträgen
            for entry in entries:
                if self._is_entry_visible(entry):
                    coords = self._get_entry_coordinates(entry)
                    all_coords.extend(coords)
            
            if all_coords:
                # Berechne Grenzen und zentriere
                self._center_on_coordinates(all_coords)
            else:
                # Keine sichtbaren Daten - Standard-Position
                self._set_default_position()
                
        except Exception as e:
            logger.error(f"Error fitting map to GPX: {e}", exc_info=True)
            self._set_default_position()
    
    def _is_entry_visible(self, entry) -> bool:
        """Prüfe ob ein Eintrag sichtbar ist"""
        try:
            # Prüfe neuen Pfad zuerst
            session_files_new = self.properties.data.get('files', {}).get('session', {})
            for ref_num, file_info in session_files_new.items():
                if file_info.get('path') == entry.get_path():
                    return file_info.get('settings', {}).get('visible', True)
            
            # Fallback zu altem Pfad
            session_files_old = self.properties.data.get('session_files', {})
            for ref_num, file_info in session_files_old.items():
                if file_info.get('path') == entry.get_path():
                    return file_info.get('settings', {}).get('visible', True)
            
            return True  # Default: sichtbar
            
        except (KeyError, TypeError, AttributeError) as e:
            logger.warning(f"Error checking visibility for {entry.get_path()}: {e}")
            return True
    
    def _get_entry_coordinates(self, entry) -> List[Tuple[float, float]]:
        """Hole alle Koordinaten eines Eintrags"""
        coords = []
        
        try:
            gpx_data = GPXCache.get_gpx(entry.get_path())
            if not gpx_data:
                return coords
            
            # Track-Punkte
            for track in gpx_data.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        coords.append((point.latitude, point.longitude))
            
            # Route-Punkte
            for route in gpx_data.routes:
                for point in route.points:
                    coords.append((point.latitude, point.longitude))
            
            # Waypoints
            for waypoint in gpx_data.waypoints:
                coords.append((waypoint.latitude, waypoint.longitude))
                
        except Exception as e:
            logger.error(f"Error getting coordinates for {entry.get_path()}: {e}")
        
        return coords
    
    def _center_on_coordinates(self, coords: List[Tuple[float, float]]) -> None:
        """Zentriere die Karte auf die gegebenen Koordinaten"""
        if not coords:
            return
        
        try:
            # Berechne Grenzen
            lats = [coord[0] for coord in coords]
            lons = [coord[1] for coord in coords]
            
            min_lat, max_lat = min(lats), max(lats)
            min_lon, max_lon = min(lons), max(lons)
            
            # Zentriere Karte
            center_lat = (min_lat + max_lat) / 2
            center_lon = (min_lon + max_lon) / 2
            
            # Setze Kartenposition
            if hasattr(self.map_widget, 'set_position'):
                self.map_widget.set_position(center_lat, center_lon)
                logger.debug(f"Map centered on: {center_lat}, {center_lon}")
            
            # Erzwinge Karten-Update
            self._force_map_update()
            
        except Exception as e:
            logger.error(f"Error centering map: {e}")
    
    def _set_default_position(self) -> None:
        """Setze die Karte auf die Standard-Position"""
        try:
            # Standard-Position (Mitte Deutschland)
            if hasattr(self.map_widget, 'set_position'):
                self.map_widget.set_position(50.0, 10.0)
                logger.debug("Map set to default position: 50.0, 10.0")
            
            # Erzwinge Karten-Update
            self._force_map_update()
            
        except Exception as e:
            logger.error(f"Error setting default position: {e}")
    
    def _force_map_update(self) -> None:
        """Erzwinge ein Karten-Update"""
        try:
            self.map_widget.update()
            
            # Zusätzliche Updates für TkinterMapView
            if hasattr(self.map_widget, 'canvas'):
                self.map_widget.canvas.update()
                self.map_widget.canvas.update_idletasks()
                
        except Exception as e:
            logger.warning(f"Could not force map update: {e}")
    
    def set_zoom_level(self, zoom: int) -> None:
        """Setze den Zoom-Level der Karte"""
        try:
            if hasattr(self.map_widget, 'set_zoom'):
                self.map_widget.set_zoom(zoom)
                logger.debug(f"Map zoom set to: {zoom}")
        except Exception as e:
            logger.error(f"Error setting zoom: {e}")
    
    def get_current_position(self) -> Optional[Tuple[float, float]]:
        """Hole die aktuelle Karten-Position"""
        try:
            if hasattr(self.map_widget, 'get_position'):
                return self.map_widget.get_position()
        except Exception as e:
            logger.error(f"Error getting map position: {e}")
        return None
    
    def get_current_zoom(self) -> Optional[int]:
        """Hole den aktuellen Zoom-Level"""
        try:
            if hasattr(self.map_widget, 'get_zoom'):
                return self.map_widget.get_zoom()
        except Exception as e:
            logger.error(f"Error getting map zoom: {e}")
        return None
