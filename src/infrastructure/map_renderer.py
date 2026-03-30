import gpxpy
import logging
import os

logger = logging.getLogger(__name__)


class GPXCache:
    """Cache for GPX data to avoid repeated file parsing"""
    _cache = {}
    
    @classmethod
    def get_gpx(cls, path):
        """Get GPX data from cache or load from file"""
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            return None
            
        if path in cls._cache:
            cached_data, cached_time = cls._cache[path]
            if cached_time >= mtime:
                return cached_data
                
        # Load and parse GPX file
        try:
            with open(path, 'r', encoding='utf-8') as f:
                gpx = gpxpy.parse(f)
            cls._cache[path] = (gpx, mtime)
            return gpx
        except Exception as e:
            logger.error(f"Error parsing GPX file {path}: {e}")
            return None
    
    @classmethod
    def clear_all(cls):
        """Clear all cached data"""
        cls._cache.clear()


# Global reference to keep PIL marker images from being garbage collected
_pil_marker_references = []


def _set_default_marker_size(map_widget, marker, size):
    """Set the size of a default TkinterMapView marker"""
    try:
        # Try different methods to set marker size
        if hasattr(marker, 'marker_size'):
            marker.marker_size = size
        elif hasattr(marker, 'set_marker_size'):
            marker.set_marker_size(size)
        elif hasattr(map_widget, 'set_marker_size'):
            map_widget.set_marker_size(marker, size)
    except Exception as e:
        logger.debug(f"Could not set marker size: {e}")


def _add_marker_with_colors(map_widget, latitude, longitude, text=None, icon_path=None, icon_size=None, color_circle="#9B261E", color_outside="#C5542D", color_text="#652A22"):
    """Add a marker to the map with custom colors"""
    try:
        logger.debug(f"_add_marker_with_colors called at {latitude}, {longitude} with text: {text}")
        
        # Only show text if provided
        display_text = text if text else ""
        
        # Create TkinterMapView marker with custom colors
        try:
            marker = map_widget.set_marker(latitude, longitude, text=display_text,
                                         marker_color_circle=color_circle,
                                         marker_color_outside=color_outside,
                                         text_color=color_text)
            logger.debug(f"Custom color TkinterMapView marker created: {marker}")
            return marker
        except Exception as e:
            logger.debug(f"Error creating custom color marker: {e}")
            # Fallback to default marker
            try:
                marker = map_widget.set_marker(latitude, longitude, text=display_text)
                logger.debug(f"Fallback default TkinterMapView marker created: {marker}")
                return marker
            except Exception as fallback_error:
                logger.debug(f"Error creating fallback marker: {fallback_error}")
                return None
    except Exception as e:
        logger.debug(f"Error in _add_marker_with_colors: {e}")
        return None


def _add_marker(map_widget, latitude, longitude, text, icon_path, icon_size, color=None):
    """Add a single marker to the map using TkinterMapView's built-in system"""
    try:
        logger.debug(f"_add_marker called at {latitude}, {longitude} with text: {text}")
        
        # Check marker settings
        try:
            from src.infrastructure.repositories.properties_repository import AppProperties
            props = AppProperties()
            marker_step = props.get("marker_step", 20)
        except ImportError:
            # Fallback if import fails
            marker_step = 20
        
        logger.debug(f"Marker settings: marker_step={marker_step}")
        
        # Create default TkinterMapView marker with color options
        try:
            # Use custom color if provided, otherwise default colors
            if color is not None:
                marker_color_circle = color
                marker_color_outside = color
                text_color = '#FFFFFF'  # White text for contrast
            else:
                # Get marker color from properties
                marker_color_circle = props.get('marker_color_circle', '#9B261E')
                marker_color_outside = props.get('marker_color_outside', '#C5542D')
                text_color = props.get('marker_text_color', '#652A22')
            
            # Create marker with custom colors
            marker = map_widget.set_marker(latitude, longitude, text=text,
                                         marker_color_circle=marker_color_circle,
                                         marker_color_outside=marker_color_outside,
                                         text_color=text_color)
            logger.debug(f"Default TkinterMapView marker created with colors: {marker}")
            
            return marker
        except Exception as e:
            logger.debug(f"Error creating default marker with colors: {e}")
            # Fallback to basic marker
            try:
                marker = map_widget.set_marker(latitude, longitude, text=text)
                logger.debug(f"Basic default TkinterMapView marker created: {marker}")
                return marker
            except Exception as fallback_error:
                logger.debug(f"Error creating basic default marker: {fallback_error}")
                return None
            
    except Exception as e:
        logger.debug(f"Error in _add_marker: {e}")
        return None


def _render_markers(map_widget, gpx_data, properties):
    """Render markers for waypoints, track points, and route points"""
    if not properties.get('marker_enabled', True):
        return
        
    # Separate Einstellungen für jeden Punkt-Typ
    waypoints_enabled = properties.get('dialogs.settings.rendering.waypoints.enabled', True)
    trackpoints_enabled = properties.get('dialogs.settings.rendering.trackpoints.enabled', True)
    routepoints_enabled = properties.get('dialogs.settings.rendering.routepoints.enabled', True)
    
    # % Werte aus Properties
    waypoints_percent = properties.get('dialogs.settings.rendering.waypoints.percent', 100)
    trackpoints_percent = properties.get('dialogs.settings.rendering.trackpoints.percent', 50)
    routepoints_percent = properties.get('dialogs.settings.rendering.routepoints.percent', 50)
    
    # Text-Enabled Einstellungen
    waypoints_text_enabled = properties.get('dialogs.settings.rendering.waypoints.text_enabled', True)
    trackpoints_text_enabled = properties.get('dialogs.settings.rendering.trackpoints.text_enabled', True)
    routepoints_text_enabled = properties.get('dialogs.settings.rendering.routepoints.text_enabled', True)
    
    # Step aus % berechnen
    def percent_to_step(percent):
        if percent >= 100:
            return 1
        elif percent <= 1:
            return 100
        else:
            return max(1, int(100 / percent))
    
    waypoints_step = percent_to_step(waypoints_percent)
    trackpoints_step = percent_to_step(trackpoints_percent)
    routepoints_step = percent_to_step(routepoints_percent)
    
    # Separate Farben für jeden Punkt-Typ (3 Farben pro Typ)
    waypoints_color_circle = properties.get('dialogs.settings.rendering.waypoints.color_circle', "#9B261E")
    waypoints_color_outside = properties.get('dialogs.settings.rendering.waypoints.color_outside', "#C5542D")
    waypoints_color_text = properties.get('dialogs.settings.rendering.waypoints.color_text', "#652A22")
    
    trackpoints_color_circle = properties.get('dialogs.settings.rendering.trackpoints.color_circle', "#4169E1")
    trackpoints_color_outside = properties.get('dialogs.settings.rendering.trackpoints.color_outside', "#6495ED")
    trackpoints_color_text = properties.get('dialogs.settings.rendering.trackpoints.color_text', "#FFFFFF")
    
    routepoints_color_circle = properties.get('dialogs.settings.rendering.routepoints.color_circle', "#228B22")
    routepoints_color_outside = properties.get('dialogs.settings.rendering.routepoints.color_outside', "#32CD32")
    routepoints_color_text = properties.get('dialogs.settings.rendering.routepoints.color_text', "#FFFFFF")
    
    # Render waypoints
    if waypoints_enabled and gpx_data.waypoints:
        for i, waypoint in enumerate(gpx_data.waypoints):
            if i % waypoints_step == 0:  # Downsample waypoints
                waypoint_text = waypoint.name if waypoints_text_enabled else None
                _add_marker_with_colors(map_widget, waypoint.latitude, waypoint.longitude, 
                                       waypoint_text, "", 0,
                                       waypoints_color_circle, waypoints_color_outside, waypoints_color_text)
    
    # Render track points (downsampled)
    if trackpoints_enabled and gpx_data.tracks:
        for track in gpx_data.tracks:
            for segment in track.segments:
                for i, point in enumerate(segment.points):
                    if i % trackpoints_step == 0:  # Downsample
                        trackpoint_text = f"Track Point {i}" if trackpoints_text_enabled else None
                        _add_marker_with_colors(map_widget, point.latitude, point.longitude,
                                           trackpoint_text, "", 0,
                                           trackpoints_color_circle, trackpoints_color_outside, trackpoints_color_text)
    
    # Render route points (downsampled)
    if routepoints_enabled and gpx_data.routes:
        for route in gpx_data.routes:
            for i, point in enumerate(route.points):
                if i % routepoints_step == 0:  # Downsample
                    routepoint_text = f"Route Point {i}" if routepoints_text_enabled else None
                    _add_marker_with_colors(map_widget, point.latitude, point.longitude,
                                       routepoint_text, "", 0,
                                       routepoints_color_circle, routepoints_color_outside, routepoints_color_text)


def render_tracks_on_map(map_widget, entries, properties):
    """Render GPX tracks and markers on the map"""
    
    # Schutz gegen mehrfache Aufrufe
    if hasattr(render_tracks_on_map, '_is_running') and render_tracks_on_map._is_running:
        return
    
    render_tracks_on_map._is_running = True
    
    try:
        # Lösche alle Pfade aggressiver
        try:
            map_widget.delete_all_path()
        except Exception:
            pass
        
        # Lösche alle Marker aggressiver  
        try:
            map_widget.delete_all_marker()
        except Exception:
            pass
        
        # Zusätzliche Säuberung des Canvas
        try:
            if hasattr(map_widget, 'canvas'):
                # Lösche alle Canvas-Objekte mit "marker" oder "position" im Tag
                map_widget.canvas.delete("marker")
                map_widget.canvas.delete("position")
                map_widget.canvas.delete("all")
        except Exception:
            pass

    except Exception:
        pass

    # Clear PIL marker references when markers are deleted
    global _pil_marker_references
    _pil_marker_references.clear()
    
    # Clear GPX cache to avoid stale data
    GPXCache.clear_all()
    
    # Render tracks and markers for each entry
    for entry in entries:
        # Direkte Sichtbarkeits-Prüfung statt entry.is_visible()
        is_visible = False
        try:
            # Hole Sichtbarkeit aus Properties - verwende die korrekte Struktur
            session_files = properties.get('files.session') or properties.data.get('files', {}).get('session', {})
            for ref_num, file_info in session_files.items():
                if file_info.get('path') == entry.get_path():
                    is_visible = file_info.get('settings', {}).get('visible', True)
                    break
        except:
            is_visible = True  # Fallback: sichtbar
        
        if is_visible:
            gpx_data = GPXCache.get_gpx(entry.get_path())
            if gpx_data:
                logger.info(f"Rendering GPX file: {os.path.basename(entry.get_path())} ({len(gpx_data.tracks)} tracks, {len(gpx_data.routes)} routes)")
                
                # Render tracks with line width
                rendering_settings = properties.get('dialogs.settings.rendering', {})
                track_line = rendering_settings.get('track_line', {})
                track_line_enabled = track_line.get('enabled', True)
                track_line_width = track_line.get('width', 5)
                
                # Get downsampling settings
                downsampling_settings = rendering_settings.get('downsampling', {})
                downsampling_enabled = downsampling_settings.get('enabled', True)
                max_points = downsampling_settings.get('max_points', 500)
                threshold = downsampling_settings.get('threshold', 1000)
                
                if track_line_enabled and gpx_data.tracks:
                    for track in gpx_data.tracks:
                        for segment in track.segments:
                            if len(segment.points) > 1:
                                coordinates = [(p.latitude, p.longitude) for p in segment.points]
                                
                                # Downsample large segments for performance if enabled
                                if downsampling_enabled and len(coordinates) > threshold:
                                    # Keep every nth point for large segments
                                    step = max(1, len(coordinates) // max_points)
                                    coordinates = coordinates[::step]
                                    logger.debug(f"Downsampled track segment from {len(segment.points)} to {len(coordinates)} points")
                                
                                if coordinates:
                                    map_widget.set_path(coordinates, 
                                                        color=entry.get_color(),
                                                        width=track_line_width)
                
                # Render routes with line width
                route_line_enabled = properties.get('route_line_enabled', True)
                route_line_width = properties.get('route_line_width', 2)
                
                if route_line_enabled and gpx_data.routes:
                    for route in gpx_data.routes:
                        if len(route.points) > 1:
                            coordinates = [(p.latitude, p.longitude) for p in route.points]
                            if coordinates:
                                map_widget.set_path(coordinates,
                                                    color=entry.get_color(),
                                                    width=route_line_width)
                
                # Render markers
                _render_markers(map_widget, gpx_data, properties)
    
    # Update the map
    try:
        map_widget.update()
    except Exception:
        pass
    
    finally:
        # Schutz aufheben
        render_tracks_on_map._is_running = False
