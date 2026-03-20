#!/usr/bin/env python3
"""
Test script for GPXTableEditor functionality
"""

import tkinter as tk
from tkinter import messagebox
import gpxpy
from edit_controller import GPXEditController, GPXDocument
from gpx_table_editor import GPXTableEditor

def create_test_gpx():
    """Create a simple test GPX file"""
    gpx = gpxpy.gpx.GPX()
    
    # Create first track
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    
    # Create segment
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    
    # Add some test points
    points = [
        (47.0, 8.0, 450.0),
        (47.001, 8.001, 455.0),
        (47.002, 8.002, 460.0),
        (47.003, 8.003, 465.0),
    ]
    
    for lat, lon, ele in points:
        gpx_point = gpxpy.gpx.GPXTrackPoint(latitude=lat, longitude=lon, elevation=ele)
        gpx_segment.points.append(gpx_point)
    
    return gpx

def test_table_editor():
    """Test the GPXTableEditor"""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    # Create test data
    gpx = create_test_gpx()
    document = GPXDocument(gpx, "test.gpx")
    
    # Create editor
    editor = GPXTableEditor(
        parent=root,
        document=document,
        update_callback=lambda: print("Map update callback called"),
        save_callback=lambda: print("Save callback called")
    )
    
    # Show the editor
    editor.deiconify()
    root.mainloop()

if __name__ == "__main__":
    test_table_editor()
