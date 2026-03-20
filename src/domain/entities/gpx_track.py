"""
GPX Track Entity

Represents a GPX track with its segments and points.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import gpxpy
from gpxpy.gpx import GPXTrackPoint


@dataclass
class GPXTrack:
    """GPX track entity"""
    
    # Track metadata
    name: Optional[str] = None
    description: Optional[str] = None
    
    # Track content
    segments: List['GPXTrackSegment'] = field(default_factory=list)
    
    # Analysis results
    point_count: int = field(init=False)
    distance_km: float = field(init=False)
    elevation_gain: float = field(init=False)
    elevation_loss: float = field(init=False)
    
    def __post_init__(self):
        """Initialize analysis results"""
        self._update_analysis()
    
    def _update_analysis(self):
        """Update track analysis"""
        self.point_count = sum(seg.point_count for seg in self.segments)
        self.distance_km = sum(seg.distance_km for seg in self.segments)
        self.elevation_gain = sum(seg.elevation_gain for seg in self.segments)
        self.elevation_loss = sum(seg.elevation_loss for seg in self.segments)
    
    @classmethod
    def from_gpxpy(cls, track: gpxpy.gpx.GPXTrack) -> 'GPXTrack':
        """Create GPXTrack from gpxpy data"""
        segments = [GPXTrackSegment.from_gpxpy(seg) for seg in track.segments]
        
        return cls(
            name=track.name,
            description=track.description,
            segments=segments
        )
    
    def to_gpxpy(self) -> gpxpy.gpx.GPXTrack:
        """Convert to gpxpy format"""
        track = gpxpy.gpx.GPXTrack()
        track.name = self.name
        track.description = self.description
        
        for segment in self.segments:
            track.segments.append(segment.to_gpxpy())
        
        return track


@dataclass
class GPXTrackSegment:
    """GPX track segment entity"""
    
    # Segment content
    points: List[GPXTrackPoint] = field(default_factory=list)
    
    # Analysis results
    point_count: int = field(init=False)
    distance_km: float = field(init=False)
    elevation_gain: float = field(init=False)
    elevation_loss: float = field(init=False)
    
    def __post_init__(self):
        """Initialize analysis results"""
        self._update_analysis()
    
    def _update_analysis(self):
        """Update segment analysis"""
        self.point_count = len(self.points)
        
        if len(self.points) < 2:
            self.distance_km = 0.0
            self.elevation_gain = 0.0
            self.elevation_loss = 0.0
            return
        
        # Calculate distance and elevation
        total_distance = 0.0
        total_gain = 0.0
        total_loss = 0.0
        
        for i in range(1, len(self.points)):
            prev_point = self.points[i-1]
            curr_point = self.points[i]
            
            # Distance
            distance = prev_point.distance_3d(curr_point)
            total_distance += distance
            
            # Elevation
            if prev_point.elevation and curr_point.elevation:
                elevation_diff = curr_point.elevation - prev_point.elevation
                if elevation_diff > 0:
                    total_gain += elevation_diff
                else:
                    total_loss += abs(elevation_diff)
        
        self.distance_km = total_distance / 1000.0  # Convert to km
        self.elevation_gain = total_gain
        self.elevation_loss = total_loss
    
    @classmethod
    def from_gpxpy(cls, segment: gpxpy.gpx.GPXTrackSegment) -> 'GPXTrackSegment':
        """Create GPXTrackSegment from gpxpy data"""
        return cls(points=list(segment.points))
    
    def to_gpxpy(self) -> gpxpy.gpx.GPXTrackSegment:
        """Convert to gpxpy format"""
        segment = gpxpy.gpx.GPXTrackSegment()
        segment.points = self.points
        return segment
