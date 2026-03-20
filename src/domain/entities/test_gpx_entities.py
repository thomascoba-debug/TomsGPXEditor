"""
Tests for GPX Domain Entities

Unit tests for GPXFile, GPXTrack, and GPXRoute entities.
"""

import pytest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch
import gpxpy.gpx

from .gpx_file import GPXFile
from .gpx_track import GPXTrack, GPXTrackSegment
from .gpx_route import GPXRoute


class TestGPXFile:
    """Test GPXFile entity"""
    
    def test_gpx_file_creation(self):
        """Test basic GPXFile creation"""
        file = GPXFile(
            path="/test/file.gpx",
            tracks=[],
            routes=[]
        )
        
        assert file.path == "/test/file.gpx"
        assert file.name == "file.gpx"
        assert file.tracks == []
        assert file.routes == []
        assert file.is_visible is True
        assert file.is_editable is False
        assert file.color == "#80ffff"
    
    def test_gpx_file_analysis_empty(self):
        """Test analysis of empty GPX file"""
        file = GPXFile(
            path="/test/empty.gpx",
            tracks=[],
            routes=[]
        )
        
        assert file.track_count == 0
        assert file.route_count == 0
        assert file.total_points == 0
        assert file.file_type == "empty"
        assert not file.has_content()
    
    def test_gpx_file_analysis_tracks_only(self):
        """Test analysis of GPX file with tracks only"""
        track = Mock(spec=GPXTrack)
        track.point_count = 100
        
        file = GPXFile(
            path="/test/tracks.gpx",
            tracks=[track],
            routes=[]
        )
        
        assert file.track_count == 1
        assert file.route_count == 0
        assert file.total_points == 100
        assert file.file_type == "track"
        assert file.has_content()
    
    def test_gpx_file_analysis_routes_only(self):
        """Test analysis of GPX file with routes only"""
        route = Mock(spec=GPXRoute)
        route.point_count = 50
        
        file = GPXFile(
            path="/test/routes.gpx",
            tracks=[],
            routes=[route]
        )
        
        assert file.track_count == 0
        assert file.route_count == 1
        assert file.total_points == 50
        assert file.file_type == "route"
        assert file.has_content()
    
    def test_gpx_file_analysis_mixed(self):
        """Test analysis of GPX file with tracks and routes"""
        track = Mock(spec=GPXTrack)
        track.point_count = 100
        route = Mock(spec=GPXRoute)
        route.point_count = 50
        
        file = GPXFile(
            path="/test/mixed.gpx",
            tracks=[track],
            routes=[route]
        )
        
        assert file.track_count == 1
        assert file.route_count == 1
        assert file.total_points == 150
        assert file.file_type == "mixed"
        assert file.has_content()
    
    def test_display_name(self):
        """Test display name generation"""
        # Empty file
        empty_file = GPXFile(path="/test/empty.gpx", tracks=[], routes=[])
        assert empty_file.get_display_name() == "empty.gpx"
        
        # Track file
        track = Mock(spec=GPXTrack)
        track.point_count = 5
        track_file = GPXFile(path="/test/tracks.gpx", tracks=[track], routes=[])
        assert track_file.get_display_name() == "tracks.gpx (T:5)"
        
        # Route file
        route = Mock(spec=GPXRoute)
        route.point_count = 3
        route_file = GPXFile(path="/test/routes.gpx", tracks=[], routes=[route])
        assert route_file.get_display_name() == "routes.gpx (R:3)"
        
        # Mixed file
        mixed_file = GPXFile(path="/test/mixed.gpx", tracks=[track], routes=[route])
        assert mixed_file.get_display_name() == "mixed.gpx (T:5,R:3)"
    
    @patch('pathlib.Path.stat')
    def test_file_metadata(self, mock_stat):
        """Test file metadata extraction"""
        # Mock file stats
        mock_stat.return_value = Mock(
            st_size=1024,
            st_mtime=1640995200.0  # 2022-01-01 00:00:00
        )
        
        file = GPXFile(path="/test/file.gpx", tracks=[], routes=[])
        
        assert file.file_size == 1024
        assert isinstance(file.last_modified, datetime)
    
    def test_from_gpxpy(self):
        """Test creation from gpxpy data"""
        gpx_data = Mock(spec=gpxpy.gpx.GPX)
        gpx_track = Mock(spec=gpxpy.gpx.GPXTrack)
        gpx_route = Mock(spec=gpxpy.gpx.GPXRoute)
        gpx_data.tracks = [gpx_track]
        gpx_data.routes = [gpx_route]
        
        with patch('src.domain.entities.gpx_track.GPXTrack.from_gpxpy') as mock_track_from, \
             patch('src.domain.entities.gpx_route.GPXRoute.from_gpxpy') as mock_route_from:
            
            mock_track_from.return_value = Mock(spec=GPXTrack)
            mock_route_from.return_value = Mock(spec=GPXRoute)
            
            file = GPXFile.from_gpxpy(
                "/test/file.gpx",
                gpx_data,
                is_visible=False,
                is_editable=True,
                color="#ff0000"
            )
            
            assert file.path == "/test/file.gpx"
            assert file.is_visible is False
            assert file.is_editable is True
            assert file.color == "#ff0000"
            assert len(file.tracks) == 1
            assert len(file.routes) == 1


class TestGPXTrack:
    """Test GPXTrack entity"""
    
    def test_track_creation(self):
        """Test basic GPXTrack creation"""
        track = GPXTrack(
            name="Test Track",
            description="Test Description",
            segments=[]
        )
        
        assert track.name == "Test Track"
        assert track.description == "Test Description"
        assert track.segments == []
    
    def test_track_analysis_empty(self):
        """Test analysis of empty track"""
        track = GPXTrack(segments=[])
        
        assert track.point_count == 0
        assert track.distance_km == 0.0
        assert track.elevation_gain == 0.0
        assert track.elevation_loss == 0.0
    
    def test_track_analysis_with_segments(self):
        """Test analysis with segments"""
        segment1 = Mock(spec=GPXTrackSegment)
        segment1.point_count = 50
        segment1.distance_km = 5.5
        segment1.elevation_gain = 100.0
        segment1.elevation_loss = 50.0
        
        segment2 = Mock(spec=GPXTrackSegment)
        segment2.point_count = 30
        segment2.distance_km = 3.2
        segment2.elevation_gain = 80.0
        segment2.elevation_loss = 20.0
        
        track = GPXTrack(segments=[segment1, segment2])
        
        assert track.point_count == 80
        assert track.distance_km == 8.7
        assert track.elevation_gain == 180.0
        assert track.elevation_loss == 70.0
    
    def test_from_gpxpy(self):
        """Test creation from gpxpy data"""
        gpx_track = Mock(spec=gpxpy.gpx.GPXTrack)
        gpx_track.name = "Test Track"
        gpx_track.description = "Test Description"
        gpx_segment = Mock(spec=gpxpy.gpx.GPXTrackSegment)
        gpx_track.segments = [gpx_segment]
        
        with patch('src.domain.entities.gpx_track.GPXTrackSegment.from_gpxpy') as mock_from:
            mock_from.return_value = Mock(spec=GPXTrackSegment)
            
            track = GPXTrack.from_gpxpy(gpx_track)
            
            assert track.name == "Test Track"
            assert track.description == "Test Description"
            assert len(track.segments) == 1


class TestGPXTrackSegment:
    """Test GPXTrackSegment entity"""
    
    def test_segment_creation_empty(self):
        """Test creation of empty segment"""
        segment = GPXTrackSegment(points=[])
        
        assert segment.points == []
        assert segment.point_count == 0
        assert segment.distance_km == 0.0
        assert segment.elevation_gain == 0.0
        assert segment.elevation_loss == 0.0
    
    def test_segment_creation_with_points(self):
        """Test creation with points"""
        point1 = Mock()
        point1.distance_3d.return_value = 1000.0
        point1.elevation = 100.0
        
        point2 = Mock()
        point2.distance_3d.return_value = 0.0
        point2.elevation = 150.0
        
        point3 = Mock()
        point3.distance_3d.return_value = 500.0
        point3.elevation = 120.0
        
        segment = GPXTrackSegment(points=[point1, point2, point3])
        
        assert segment.points == [point1, point2, point3]
        assert segment.point_count == 3
        assert segment.distance_km == 1.5  # (1000 + 500) / 1000
        assert segment.elevation_gain == 50.0  # max(150-100, 120-150) = 50
        assert segment.elevation_loss == 30.0  # abs(min(150-100, 120-150)) = 30


class TestGPXRoute:
    """Test GPXRoute entity"""
    
    def test_route_creation(self):
        """Test basic GPXRoute creation"""
        route = GPXRoute(
            name="Test Route",
            description="Test Description",
            waypoints=[]
        )
        
        assert route.name == "Test Route"
        assert route.description == "Test Description"
        assert route.waypoints == []
    
    def test_route_analysis_empty(self):
        """Test analysis of empty route"""
        route = GPXRoute(waypoints=[])
        
        assert route.point_count == 0
        assert route.distance_km == 0.0
        assert route.elevation_gain == 0.0
        assert route.elevation_loss == 0.0
    
    def test_route_analysis_with_waypoints(self):
        """Test analysis with waypoints"""
        waypoint1 = Mock()
        waypoint1.distance_3d.return_value = 800.0
        waypoint1.elevation = 80.0
        
        waypoint2 = Mock()
        waypoint2.distance_3d.return_value = 0.0
        waypoint2.elevation = 120.0
        
        waypoint3 = Mock()
        waypoint3.distance_3d.return_value = 600.0
        waypoint3.elevation = 100.0
        
        route = GPXRoute(waypoints=[waypoint1, waypoint2, waypoint3])
        
        assert route.point_count == 3
        assert route.distance_km == 1.4  # (800 + 600) / 1000
        assert route.elevation_gain == 40.0  # max(120-80, 100-120) = 40
        assert route.elevation_loss == 20.0  # abs(min(120-80, 100-120)) = 20
    
    def test_from_gpxpy(self):
        """Test creation from gpxpy data"""
        gpx_route = Mock(spec=gpxpy.gpx.GPXRoute)
        gpx_route.name = "Test Route"
        gpx_route.description = "Test Description"
        gpx_waypoint = Mock()
        gpx_route.waypoints = [gpx_waypoint]
        
        route = GPXRoute.from_gpxpy(gpx_route)
        
        assert route.name == "Test Route"
        assert route.description == "Test Description"
        assert route.waypoints == [gpx_waypoint]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
