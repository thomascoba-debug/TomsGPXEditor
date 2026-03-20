import gpxpy
import logging
import os
from gpxpy.gpx import GPXXMLSyntaxException
from src.infrastructure.error_handler import safe_execute, GPXEditorException, validate_gpx_data


class GPXDocument:

    def __init__(self, gpx, path):

        self.gpx = gpx
        self.path = path

    def get_first_segment(self):

        for track in self.gpx.tracks:

            for segment in track.segments:

                return segment

        return None


class GPXEditController:

    def __init__(self, app):

        self.app = app

    @safe_execute("Failed to load GPX document", show_error=True)
    def load_document(self, path):
        """Load a GPX document from file with enhanced error handling"""
        logger = logging.getLogger(__name__)
        
        # Check if file exists and is not empty
        if not os.path.exists(path):
            raise FileNotFoundError(f"GPX file not found: {path}")
        
        if os.path.getsize(path) == 0:
            raise ValueError(f"GPX file is empty: {path}")
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                # Read first few bytes to check for content
                content = f.read(100)
                f.seek(0)
                
                # Check if file starts with XML declaration or GPX tag
                if not content.strip().startswith(('<?xml', '<gpx')):
                    raise ValueError(f"File does not appear to be a valid GPX file: {path}")
                
                gpx = gpxpy.parse(f)
                
                # Validate the parsed data
                errors, warnings = validate_gpx_data(gpx)
                
                if errors:
                    error_msg = f"GPX validation failed for {path}:\n" + "\n".join(errors)
                    raise GPXEditorException(error_msg)
                
                if warnings:
                    for warning in warnings:
                        logger.warning(f"GPX warning for {path}: {warning}")
                
                logger.debug(f"Successfully loaded GPX document: {path}")
                return GPXDocument(gpx, path)
            
        except GPXXMLSyntaxException as e:
            raise GPXEditorException(f"Invalid GPX XML in {path}: {str(e)}")
        except Exception as e:
            if isinstance(e, GPXEditorException):
                raise
            raise GPXEditorException(f"Error loading GPX file {path}: {str(e)}")
    
    def save_document(self, document):
        """Save the GPX document back to its file"""
        try:
            with open(document.path, "w", encoding="utf-8") as f:
                f.write(document.gpx.to_xml())
            return True, "File saved successfully"
        except Exception as e:
            return False, f"Error saving file: {str(e)}"


def analyze_gpx_file(path):
    """
    Analyze a GPX file to determine what type of data it contains.
    Returns a dictionary with file type information.
    """
    logger = logging.getLogger(__name__)
    
    # Check if file exists and is not empty
    if not os.path.exists(path):
        return {
            'has_tracks': False,
            'has_routes': False,
            'has_waypoints': False,
            'track_count': 0,
            'route_count': 0,
            'waypoint_count': 0,
            'file_type': 'error',
            'error': f'File not found: {path}'
        }
    
    if os.path.getsize(path) == 0:
        return {
            'has_tracks': False,
            'has_routes': False,
            'has_waypoints': False,
            'track_count': 0,
            'route_count': 0,
            'waypoint_count': 0,
            'file_type': 'error',
            'error': f'File is empty: {path}'
        }
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            # Quick content validation
            content = f.read(100)
            f.seek(0)
            
            if not content.strip().startswith(('<?xml', '<gpx')):
                return {
                    'has_tracks': False,
                    'has_routes': False,
                    'has_waypoints': False,
                    'track_count': 0,
                    'route_count': 0,
                    'waypoint_count': 0,
                    'file_type': 'error',
                    'error': f'File does not appear to be a valid GPX file: {path}'
                }
            
            gpx = gpxpy.parse(f)
        
        analysis = {
            'has_tracks': len(gpx.tracks) > 0,
            'has_routes': len(gpx.routes) > 0,
            'has_waypoints': len(gpx.waypoints) > 0,
            'track_count': len(gpx.tracks),
            'route_count': len(gpx.routes),
            'waypoint_count': len(gpx.waypoints),
            'file_type': 'unknown'
        }
        
        # Determine primary file type
        if analysis['has_tracks'] and not analysis['has_routes']:
            analysis['file_type'] = 'track'
        elif analysis['has_routes'] and not analysis['has_tracks']:
            analysis['file_type'] = 'route'
        elif analysis['has_tracks'] and analysis['has_routes']:
            analysis['file_type'] = 'mixed'
        elif analysis['has_waypoints']:
            analysis['file_type'] = 'waypoint'
        else:
            analysis['file_type'] = 'empty'
            
        logger.debug(f"Analyzed GPX file {path}: {analysis['file_type']}")
        return analysis
        
    except GPXXMLSyntaxException as e:
        logger.error(f"XML syntax error analyzing GPX file {path}: {str(e)}")
        return {
            'has_tracks': False,
            'has_routes': False,
            'has_waypoints': False,
            'track_count': 0,
            'route_count': 0,
            'waypoint_count': 0,
            'file_type': 'error',
            'error': f'XML syntax error: {str(e)}'
        }
    except UnicodeDecodeError as e:
        logger.error(f"Encoding error analyzing GPX file {path}: {str(e)}")
        return {
            'has_tracks': False,
            'has_routes': False,
            'has_waypoints': False,
            'track_count': 0,
            'route_count': 0,
            'waypoint_count': 0,
            'file_type': 'error',
            'error': f'Encoding error: {str(e)}'
        }
    except Exception as e:
        logger.error(f"Unexpected error analyzing GPX file {path}: {str(e)}")
        return {
            'has_tracks': False,
            'has_routes': False,
            'has_waypoints': False,
            'track_count': 0,
            'route_count': 0,
            'waypoint_count': 0,
            'file_type': 'error',
            'error': str(e)
        }
