import logging
import gpxpy
from gpxpy.gpx import GPXTrack, GPXTrackSegment, GPXRoute, GPXRoutePoint

# Get logger for this module
logger = logging.getLogger(__name__)

def route_to_track(gpx_data):
    """
    Convert all routes in GPX data to tracks
    
    Args:
        gpx_data: GPX object from gpxpy.parse()
    
    Returns:
        GPX object with routes converted to tracks
    """
    logger.debug("Starting route to track conversion")
    
    if not gpx_data.routes:
        logger.warning("No routes found in GPX data")
        return gpx_data
    
    routes_converted = 0
    total_points_converted = 0
    
    # Convert each route to a track
    for route in gpx_data.routes[:]:  # Copy list to avoid modification issues
        logger.debug(f"Converting route: {route.name if route.name else 'Unnamed route'}")
        
        # Create new track
        new_track = GPXTrack()
        new_track.name = route.name if route.name else "Converted Route"
        new_track.description = route.description if route.description else "Converted from route"
        
        # Create new segment
        new_segment = GPXTrackSegment()
        
        # Convert route points to track points
        for route_point in route.points:
            track_point = gpxpy.gpx.GPXTrackPoint(
                latitude=route_point.latitude,
                longitude=route_point.longitude,
                elevation=route_point.elevation,
                time=route_point.time,
                name=route_point.name
            )
            new_segment.points.append(track_point)
            
            # Copy additional properties
            if hasattr(route_point, 'symbol') and route_point.symbol:
                track_point.symbol = route_point.symbol
            if hasattr(route_point, 'comment') and route_point.comment:
                track_point.comment = route_point.comment
            if hasattr(route_point, 'description') and route_point.description:
                track_point.description = route_point.description
            
            total_points_converted += 1
        
        new_track.segments.append(new_segment)
        gpx_data.tracks.append(new_track)
        
        # Remove original route
        gpx_data.routes.remove(route)
        routes_converted += 1
        
        logger.debug(f"Converted route with {len(route.points)} points to track segment")
    
    logger.info(f"Route to track conversion completed: {routes_converted} routes converted, {total_points_converted} points total")
    return gpx_data

def track_to_route(gpx_data):
    """
    Convert all tracks in GPX data to routes
    
    Args:
        gpx_data: GPX object from gpxpy.parse()
    
    Returns:
        GPX object with tracks converted to routes
    """
    logger.debug("Starting track to route conversion")
    
    if not gpx_data.tracks:
        logger.warning("No tracks found in GPX data")
        logger.debug(f"GPX data contains: {len(gpx_data.routes)} routes, {len(gpx_data.tracks)} tracks, {len(gpx_data.waypoints)} waypoints")
        return gpx_data
    
    tracks_converted = 0
    total_points_converted = 0
    
    # Convert each track to a route
    for track in gpx_data.tracks[:]:  # Copy list to avoid modification issues
        logger.debug(f"Converting track: {track.name if track.name else 'Unnamed track'}")
        logger.debug(f"Track has {len(track.segments)} segments")
        
        # Create new route
        new_route = GPXRoute()
        new_route.name = track.name if track.name else "Converted Track"
        new_route.description = track.description if track.description else "Converted from track"
        
        # Convert all track points from all segments to route points
        segment_count = 0
        for segment in track.segments:
            segment_count += 1
            logger.debug(f"Processing segment {segment_count} with {len(segment.points)} points")
            
            for track_point in segment.points:
                route_point = GPXRoutePoint()
                route_point.latitude = track_point.latitude
                route_point.longitude = track_point.longitude
                route_point.elevation = track_point.elevation
                route_point.time = track_point.time
                route_point.name = track_point.name
                
                # Copy additional properties
                if hasattr(track_point, 'symbol') and track_point.symbol:
                    route_point.symbol = track_point.symbol
                if hasattr(track_point, 'comment') and track_point.comment:
                    route_point.comment = track_point.comment
                if hasattr(track_point, 'description') and track_point.description:
                    route_point.description = track_point.description
                
                new_route.points.append(route_point)
                total_points_converted += 1
        
        gpx_data.routes.append(new_route)
        
        # Remove original track
        gpx_data.tracks.remove(track)
        tracks_converted += 1
        
        total_segment_points = sum(len(seg.points) for seg in track.segments)
        logger.debug(f"Converted track with {segment_count} segments and {total_segment_points} points to route")
    
    logger.info(f"Track to route conversion completed: {tracks_converted} tracks converted, {total_points_converted} points total")
    return gpx_data

def convert_gpx_file(file_path, conversion_type):
    """
    Convert a GPX file (route to track or track to route)
    
    Args:
        file_path: Path to the GPX file
        conversion_type: 'route_to_track' or 'track_to_route'
    
    Returns:
        tuple: (success, message, modified_gpx_data)
    """
    try:
        logger.debug(f"Loading GPX file: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            gpx_data = gpxpy.parse(f)
        
        original_routes = len(gpx_data.routes)
        original_tracks = len(gpx_data.tracks)
        original_points = sum(len(seg.points) for track in gpx_data.tracks for seg in track.segments) + \
                         sum(len(route.points) for route in gpx_data.routes)
        
        logger.debug(f"Original GPX data: {original_routes} routes, {original_tracks} tracks, {original_points} points")
        
        # Debug: Show track details before conversion
        if conversion_type == 'track_to_route' and gpx_data.tracks:
            logger.debug(f"Track details before conversion:")
            for i, track in enumerate(gpx_data.tracks):
                track_points = sum(len(seg.points) for seg in track.segments)
                logger.debug(f"  Track {i+1}: {len(track.segments)} segments, {track_points} points, name='{track.name}'")
                for j, segment in enumerate(track.segments):
                    logger.debug(f"    Segment {j+1}: {len(segment.points)} points")
        
        if conversion_type == 'route_to_track':
            gpx_data = route_to_track(gpx_data)
        elif conversion_type == 'track_to_route':
            gpx_data = track_to_route(gpx_data)
        else:
            error_msg = f"Unknown conversion type: {conversion_type}"
            logger.error(error_msg)
            return False, error_msg, None
        
        # Verify conversion worked
        new_routes = len(gpx_data.routes)
        new_tracks = len(gpx_data.tracks)
        new_points = sum(len(seg.points) for track in gpx_data.tracks for seg in track.segments) + \
                    sum(len(route.points) for route in gpx_data.routes)
        
        success_msg = f"Conversion successful: {original_routes}→{new_routes} routes, {original_tracks}→{new_tracks} tracks, {original_points}→{new_points} points"
        logger.info(success_msg)
        
        return True, success_msg, gpx_data
        
    except Exception as e:
        error_msg = f"Error converting GPX file {file_path}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg, None

def save_converted_gpx(gpx_data, file_path):
    """
    Save converted GPX data to file
    
    Args:
        gpx_data: GPX object
        file_path: Path to save the file
    
    Returns:
        tuple: (success, message)
    """
    try:
        logger.debug(f"Saving converted GPX to: {file_path}")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(gpx_data.to_xml())
        
        success_msg = f"Successfully saved converted GPX to: {file_path}"
        logger.info(success_msg)
        return True, success_msg
        
    except Exception as e:
        error_msg = f"Error saving GPX file {file_path}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg
