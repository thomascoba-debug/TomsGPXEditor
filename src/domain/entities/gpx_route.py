"""
GPX Route Entity

Represents a GPX route with its waypoints.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import gpxpy
from gpxpy.gpx import GPXWaypoint


@dataclass
class GPXRoute:
    """GPX route entity"""
    
    # Route metadata
    name: Optional[str] = None
    description: Optional[str] = None
    
    # Route content
    waypoints: List[GPXWaypoint] = field(default_factory=list)
    
    # Analysis results
    point_count: int = field(init=False)
    distance_km: float = field(init=False)
    elevation_gain: float = field(init=False)
    elevation_loss: float = field(init=False)
    
    def __post_init__(self):
        """Initialize analysis results"""
        self._update_analysis()
    
    def _update_analysis(self):
        """Update route analysis"""
        self.point_count = len(self.waypoints)
        
        if len(self.waypoints) < 2:
            self.distance_km = 0.0
            self.elevation_gain = 0.0
            self.elevation_loss = 0.0
            return
        
        # Calculate distance and elevation
        total_distance = 0.0
        total_gain = 0.0
        total_loss = 0.0
        
        for i in range(1, len(self.waypoints)):
            prev_point = self.waypoints[i-1]
            curr_point = self.waypoints[i]
            
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
    def from_gpxpy(cls, route: gpxpy.gpx.GPXRoute) -> 'GPXRoute':
        """Create GPXRoute from gpxpy data"""
        return cls(
            name=route.name,
            description=route.description,
            waypoints=list(route.waypoints)
        )
    
    def to_gpxpy(self) -> gpxpy.gpx.GPXRoute:
        """Convert to gpxpy format"""
        route = gpxpy.gpx.GPXRoute()
        route.name = self.name
        route.description = self.description
        route.waypoints = self.waypoints
        return route
