import gpxpy
from debug_decorator import log_all_methods


@log_all_methods
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

    def load_document(self, path):

        with open(path, "r", encoding="utf-8") as f:

            gpx = gpxpy.parse(f)

        return GPXDocument(gpx, path)


def analyze_gpx_file(path):
    """
    Analyze a GPX file to determine what type of data it contains.
    Returns a dictionary with file type information.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
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
            
        return analysis
    except Exception as e:
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