# Track and Route Support Implementation

## Summary
Added support for distinguishing between tracks and routes in GPX files to the TomsGPXEditor interface.

## Changes Made

### 1. GPX Analysis Function (edit_controller.py)
- Added `analyze_gpx_file(path)` function that:
  - Parses GPX files to detect presence of tracks, routes, and waypoints
  - Returns analysis dictionary with file type information
  - Categorizes files as: 'track', 'route', 'mixed', 'waypoint', 'empty', or 'error'

### 2. Enhanced FileEntry (file_entry.py)
- Added file type analysis during initialization
- Added visual indicators showing file type:
  - **T (count)**: Track-only files
  - **R (count)**: Route-only files  
  - **T+R (tcount,rcount)**: Mixed files with both tracks and routes
- Added `get_file_analysis()` method for accessing analysis data

### 3. Enhanced Map Renderer (map_renderer.py)
- Added route rendering support alongside existing track rendering
- Routes are rendered with thinner lines (width=2) vs tracks (width=3)
- Both tracks and routes respect the downsample setting
- Routes are rendered directly (no segments like tracks)

## File Type Display Format

The interface now shows file type indicators next to each GPX file:

- **T (3)**: Contains 3 tracks
- **R (2)**: Contains 2 routes
- **T+R (1,2)**: Contains 1 track and 2 routes
- **WAYPOINT**: Contains waypoints only
- **EMPTY**: No GPS data found
- **ERROR**: File could not be parsed

## Technical Details

### GPX Structure Differences
- **Tracks**: Collection of track segments, each containing points
- **Routes**: Collection of route points (no segments)
- **Waypoints**: Individual point locations

### Rendering Differences
- Tracks: Width 3, full path rendering
- Routes: Width 2, direct point-to-point rendering

## Test Files Created
- `test_mixed.gpx`: Contains both track and route
- `test_track_only.gpx`: Contains track only
- `test_route_only.gpx`: Contains route only

## Usage
1. Load GPX files via dialog or drag & drop
2. File type indicators appear automatically
3. Both tracks and routes render on the map
4. Existing functionality (visibility, color, editing) preserved

## Backward Compatibility
- All existing functionality preserved
- No breaking changes to existing GPX files
- Graceful fallback for files that cannot be analyzed
