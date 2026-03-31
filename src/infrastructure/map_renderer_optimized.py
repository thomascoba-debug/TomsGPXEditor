"""
Optimized Map Renderer with Performance Improvements
"""

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
            cache_key = os.path.abspath(path)
            
            if cache_key in cls._cache:
                cached_data = cls._cache[cache_key]
                if cached_data['mtime'] == mtime:
                    logger.debug(f"Using cached GPX data for: {path}")
                    return cached_data['gpx']
            
            # Load from file
            with open(path, "r", encoding="utf-8") as f:
                gpx = gpxpy.parse(f)
            
            # Cache the data
            cls._cache[cache_key] = {
                'gpx': gpx,
                'mtime': mtime
            }
            logger.debug(f"Loaded and cached GPX data for: {path}")
            return gpx
            
        except Exception as e:
            logger.error(f"Failed to load GPX file {path}: {e}")
            return None
    
    @classmethod
    def clear_cache(cls):
        """Clear the GPX cache"""
        cls._cache.clear()
        logger.debug("GPX cache cleared")
    
    @classmethod
    def remove_from_cache(cls, path):
        """Remove specific file from cache"""
        cache_key = os.path.abspath(path)
        if cache_key in cls._cache:
            del cls._cache[cache_key]
            logger.debug(f"Removed {path} from GPX cache")


def render_tracks_on_map(map_widget, entries, properties):

    try:
        map_widget.delete_all_path()
    except Exception:
        pass

    downsample = properties.get("dialogs.settings.rendering.downsampling.step", 1)
    marker_enabled = properties.get("dialogs.settings.marker.enabled", True)
    marker_step = properties.get("dialogs.settings.marker.waypoints.percent", 20)  # Use waypoints percent as step
    marker_icon_path = properties.get("dialogs.settings.marker.icon_path", "")
    marker_icon_size = properties.get("dialogs.settings.marker.icon_size", [32, 32])

    for entry in entries:

        if not entry.is_visible():
            continue

        path = entry.get_path()

        # Use cached GPX data instead of parsing file every time
        gpx = GPXCache.get_gpx(path)
        if gpx is None:
            logger.error(f"Failed to load GPX file {path}, skipping")
            continue
        
        logger.debug(f"Rendering GPX file on map: {path}")

        color = entry.get_color()

        # Render tracks
        for track in gpx.tracks:

            for segment in track.segments:

                coords = []

                for i, p in enumerate(segment.points):

                    if i % downsample != 0:
                        continue

                    coords.append((p.latitude, p.longitude))

                if len(coords) > 1:

                    map_widget.set_path(
                        coords,
                        color=color,
                        width=3
                    )
        
        # Render routes (routes don't have segments like tracks)
        for route in gpx.routes:
            coords = []
            
            for i, point in enumerate(route.points):
                if i % downsample != 0:
                    continue
                coords.append((point.latitude, point.longitude))
            
            if len(coords) > 1:
                # Use a slightly different style for routes (thinner width)
                map_widget.set_path(
                    coords,
                    color=color,
                    width=2
                )
        
        # Render markers if enabled
        if marker_enabled:
            _render_markers_optimized(map_widget, gpx, marker_step, marker_icon_path, marker_icon_size)


def _render_markers_optimized(map_widget, gpx, marker_step, marker_icon_path, marker_icon_size):
    """Optimized marker rendering for better performance"""
    
    try:
        # Always render waypoints (usually few)
        for i, waypoint in enumerate(gpx.waypoints):
            if i % marker_step == 0:
                _add_marker_optimized(map_widget, waypoint.latitude, waypoint.longitude, 
                           waypoint.name or f"Waypoint {i+1}", marker_icon_path, marker_icon_size)
        
        # Only render track/route points if marker_step is reasonable (> 50)
        # This prevents performance issues with large GPX files
        if marker_step > 50:
            logger.debug(f"Rendering track/route markers (marker_step={marker_step})")
            
            # Render track points as markers
            track_point_count = 0
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        if track_point_count % marker_step == 0:
                            _add_marker_optimized(map_widget, point.latitude, point.longitude,
                                       f"Track Point {track_point_count+1}", marker_icon_path, marker_icon_size)
                        track_point_count += 1
            
            # Render route points as markers
            route_point_count = 0
            for route in gpx.routes:
                for point in route.points:
                    if route_point_count % marker_step == 0:
                        _add_marker_optimized(map_widget, point.latitude, point.longitude,
                                   f"Route Point {route_point_count+1}", marker_icon_path, marker_icon_size)
                    route_point_count += 1
        else:
            logger.debug(f"Skipping track/route point markers (marker_step={marker_step} too small for performance)")
                
    except Exception as e:
        logger.error(f"Error rendering markers: {e}")


def _add_marker_optimized(map_widget, latitude, longitude, text, icon_path, icon_size):
    """Optimized marker addition with better performance"""
    
    try:
        # Use default marker for better performance
        # Custom icons cause significant slowdown due to PIL processing
        marker = map_widget.set_marker(latitude, longitude, text=text)
        
        # Only try custom icon if explicitly requested and marker_step is high
        # This prevents performance issues with many markers
        if icon_path and icon_path.endswith('.png'):
            try:
                # Check if we should use custom icon (only for reasonable marker counts)
                from ..repositories.properties_repository import AppProperties
                props = AppProperties()
                marker_step = props.get("marker_step", 20)
                
                # Only use custom icons if marker_step is high enough
                if marker_step > 100:
                    _set_custom_marker_icon(marker, icon_path, icon_size)
                else:
                    logger.debug(f"Using default marker for better performance (marker_step={marker_step})")
                    
            except Exception as img_error:
                logger.debug(f"Could not set custom marker image: {img_error}")
                # Continue with default marker
        
        logger.debug(f"Added marker at {latitude}, {longitude}: {text}")
            
    except Exception as e:
        logger.error(f"Error adding marker at {latitude}, {longitude}: {e}")
        # Fallback: try without text
        try:
            map_widget.set_marker(latitude, longitude)
        except Exception as e2:
            logger.error(f"Error adding fallback marker: {e2}")


def _set_custom_marker_icon(marker, icon_path, icon_size):
    """Set custom marker icon with PIL processing"""
    try:
        # Check if marker object supports image setting
        if hasattr(marker, 'set_image'):
            marker.set_image(icon_path, icon_size)
        elif hasattr(marker, 'image'):
            # Try to set image directly
            from PIL import Image, ImageTk
            
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                img = img.resize(icon_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                marker.image = photo
                marker.configure(image=photo)
    except Exception as e:
        logger.debug(f"Could not set custom marker image: {e}")
        # Continue with default marker
