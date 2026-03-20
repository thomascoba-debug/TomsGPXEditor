import logging
import tkinter.messagebox as messagebox
import traceback
from functools import wraps

logger = logging.getLogger(__name__)


class GPXEditorException(Exception):
    """Base exception for GPX Editor specific errors"""
    pass


def safe_execute(error_msg="Operation failed", show_error=True, reraise=False):
    """Decorator for safe execution with error handling"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except GPXEditorException as e:
                logger.error(f"{error_msg}: {e}")
                if show_error:
                    messagebox.showerror("GPX Editor Error", f"{error_msg}: {e}")
                if reraise:
                    raise
                return None
            except Exception as e:
                logger.error(f"{error_msg}: {e}")
                logger.debug(f"Traceback: {traceback.format_exc()}")
                if show_error:
                    messagebox.showerror("Error", f"{error_msg}: {e}")
                if reraise:
                    raise
                return None
        return wrapper
    return decorator


def handle_file_error(file_path, operation="access"):
    """Handle file-related errors with user-friendly messages"""
    try:
        return True
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        messagebox.showerror("File Error", f"File not found:\n{file_path}")
        return False
    except PermissionError:
        logger.error(f"Permission denied: {file_path}")
        messagebox.showerror("Permission Error", f"Permission denied:\n{file_path}")
        return False
    except Exception as e:
        logger.error(f"Error {operation} file {file_path}: {e}")
        messagebox.showerror("File Error", f"Error {operation} file:\n{file_path}\n{e}")
        return False


def validate_gpx_data(gpx_data):
    """Validate GPX data for common issues"""
    errors = []
    warnings = []
    
    if not gpx_data.tracks and not gpx_data.routes:
        errors.append("No tracks or routes found in GPX file")
    
    # Check tracks
    for i, track in enumerate(gpx_data.tracks):
        if not track.segments:
            warnings.append(f"Track {i+1} has no segments")
            continue
            
        for j, segment in enumerate(track.segments):
            if len(segment.points) < 2:
                warnings.append(f"Track {i+1}, Segment {j+1} has only {len(segment.points)} point(s)")
            
            # Check for invalid coordinates
            for k, point in enumerate(segment.points):
                if not (-90 <= point.latitude <= 90):
                    errors.append(f"Invalid latitude {point.latitude} at Track {i+1}, Segment {j+1}, Point {k+1}")
                if not (-180 <= point.longitude <= 180):
                    errors.append(f"Invalid longitude {point.longitude} at Track {i+1}, Segment {j+1}, Point {k+1}")
    
    # Check routes
    for i, route in enumerate(gpx_data.routes):
        if len(route.points) < 2:
            warnings.append(f"Route {i+1} has only {len(route.points)} point(s)")
        
        for j, point in enumerate(route.points):
            if not (-90 <= point.latitude <= 90):
                errors.append(f"Invalid latitude {point.latitude} at Route {i+1}, Point {j+1}")
            if not (-180 <= point.longitude <= 180):
                errors.append(f"Invalid longitude {point.longitude} at Route {i+1}, Point {j+1}")
    
    return errors, warnings
