"""
Domain Entities

Core business objects representing GPX data structures.
"""

from .gpx_file import GPXFile
from .gpx_track import GPXTrack
from .gpx_route import GPXRoute

__all__ = ['GPXFile', 'GPXTrack', 'GPXRoute']
