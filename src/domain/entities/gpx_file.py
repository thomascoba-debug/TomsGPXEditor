"""
GPX File Entity

Represents a GPX file with its metadata and content.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import gpxpy
from .gpx_track import GPXTrack
from .gpx_route import GPXRoute


@dataclass
class GPXFile:
    """Core GPX file entity"""
    
    # File metadata
    path: str
    name: str = field(init=False)
    file_size: int = field(init=False)
    last_modified: datetime = field(init=False)
    
    # GPX content
    tracks: List['GPXTrack'] = field(default_factory=list)
    routes: List['GPXRoute'] = field(default_factory=list)
    
    # File settings
    is_visible: bool = True
    is_editable: bool = False
    color: str = "#80ffff"
    
    # Analysis results
    track_count: int = field(init=False)
    route_count: int = field(init=False)
    total_points: int = field(init=False)
    file_type: str = field(init=False)  # 'track', 'route', 'mixed', 'empty'
    
    def __post_init__(self):
        """Initialize derived fields"""
        self.name = Path(self.path).name
        self._update_metadata()
        self._update_analysis()
    
    def _update_metadata(self):
        """Update file metadata"""
        try:
            path_obj = Path(self.path)
            self.file_size = path_obj.stat().st_size
            self.last_modified = datetime.fromtimestamp(path_obj.stat().st_mtime)
        except (OSError, FileNotFoundError):
            self.file_size = 0
            self.last_modified = datetime.now()
    
    def _update_analysis(self):
        """Update analysis results"""
        self.track_count = len(self.tracks)
        self.route_count = len(self.routes)
        self.total_points = sum(track.point_count for track in self.tracks) + \
                          sum(route.point_count for route in self.routes)
        
        if self.track_count > 0 and self.route_count > 0:
            self.file_type = "mixed"
        elif self.track_count > 0:
            self.file_type = "track"
        elif self.route_count > 0:
            self.file_type = "route"
        else:
            self.file_type = "empty"
    
    @classmethod
    def from_gpxpy(cls, path: str, gpx_data: gpxpy.gpx.GPX, 
                   is_visible: bool = True, is_editable: bool = False, 
                   color: str = "#80ffff") -> 'GPXFile':
        """Create GPXFile from gpxpy data"""
        tracks = [GPXTrack.from_gpxpy(track) for track in gpx_data.tracks]
        routes = [GPXRoute.from_gpxpy(route) for route in gpx_data.routes]
        
        return cls(
            path=path,
            tracks=tracks,
            routes=routes,
            is_visible=is_visible,
            is_editable=is_editable,
            color=color
        )
    
    def to_gpxpy(self) -> gpxpy.gpx.GPX:
        """Convert to gpxpy format"""
        gpx = gpxpy.gpx.GPX()
        
        # Add tracks
        for track in self.tracks:
            gpx.tracks.append(track.to_gpxpy())
        
        # Add routes
        for route in self.routes:
            gpx.routes.append(route.to_gpxpy())
        
        return gpx
    
    def has_content(self) -> bool:
        """Check if file has any tracks or routes"""
        return len(self.tracks) > 0 or len(self.routes) > 0
    
    def get_display_name(self) -> str:
        """Get display name for UI"""
        if self.file_type == "mixed":
            return f"{self.name} (T:{self.track_count},R:{self.route_count})"
        elif self.file_type == "track":
            return f"{self.name} (T:{self.track_count})"
        elif self.file_type == "route":
            return f"{self.name} (R:{self.route_count})"
        else:
            return self.name
