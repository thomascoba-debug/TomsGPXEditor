# TomsGPXEditor - Comprehensive Documentation

## Table of Contents
1. [Overview](#overview)
2. [Functionality](#functionality)
3. [Technical Architecture](#technical-architecture)
4. [Component Cross-Reference](#component-cross-reference)
5. [Data Flow](#data-flow)
6. [Configuration](#configuration)
7. [Development Guidelines](#development-guidelines)

---

## Overview

TomsGPXEditor is a desktop application for viewing, editing, and managing GPX (GPS Exchange Format) files. The application provides a user-friendly interface for loading multiple GPX files, visualizing them on an interactive map, and performing various operations on the GPS data.

### Key Features
- **Multi-file GPX Management**: Load and manage multiple GPX files simultaneously
- **Interactive Map Visualization**: Display tracks, routes, and waypoints on an interactive map
- **File Operations**: Convert between tracks and routes, downsample data, edit waypoints
- **Persistent Settings**: Save and restore application state and file configurations
- **Internationalization**: Multi-language support
- **Drag & Drop**: Intuitive file loading via drag and drop

---

## Functionality

### Core User Workflows

#### 1. File Management
```
User Action: Load GPX File
├── Method 1: File Dialog → Browse → Select GPX file
├── Method 2: Drag & Drop GPX file onto application
├── Result: File added to file list with metadata
└── Features: Duplicate detection, file analysis, color assignment
```

#### 2. Map Visualization
```
User Action: View GPX on Map
├── Automatic rendering of all visible files
├── Interactive controls (zoom, pan)
├── Visibility toggles per file
└── Color-coded tracks and routes
```

#### 3. Data Conversion
```
User Action: Convert Track ↔ Route
├── Select file(s) for conversion
├── Choose conversion direction
├── Configure conversion options
└── Save converted file
```

#### 4. Data Downsampling
```
User Action: Downsample GPX Data
├── Select file with many points
├── Configure downsampling parameters
├── Preview reduction statistics
└── Save downsampled file
```

### Advanced Features

#### Settings Management
- **Dialog Settings**: Logging levels, file paths, display options
- **Rendering Settings**: Line widths, colors, map preferences
- **Marker Settings**: Custom markers and waypoint display
- **Recent Files**: Automatic tracking of recently used files

#### Error Handling
- **Graceful Degradation**: Application continues with fallbacks
- **File Validation**: GPX file format validation
- **Recovery Mechanisms**: Automatic backup and recovery

---

## Technical Architecture

### Architecture Overview

The application follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │   Main App  │  │   Dialogs   │  │     UI Widgets      │   │
│  │  (app.py)   │  │ (dialogs/)  │  │   (widgets/)       │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │ Controllers  │  │   Services   │  │    Event Bus        │   │
│  │ (controllers)│  │ (services/)  │  │ (event_bus.py)      │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │ Repositories │  │   Utils     │  │   Error Handling    │   │
│  │   (repos/)   │  │   (utils/)  │  │ (error_handler.py)  │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Application Core (`app.py`)
**Responsibility**: Main application entry point and UI orchestration
```python
class TomsGPXEditor(tk.Tk):
    - Initialize infrastructure components
    - Create and manage UI layout
    - Coordinate controllers
    - Handle application lifecycle
```

#### 2. Controllers Layer
**GPXFileManager** (`src/application/gpx_file_manager.py`)
```python
class GPXFileManager:
    - File loading and validation
    - UI entry creation and management
    - File reference tracking
    - Session management
```

**MapController** (`src/application/map_controller.py`)
```python
class MapController:
    - Map rendering coordination
    - Visibility management
    - Coordinate calculations
    - Map widget interaction
```

**DialogController** (`src/application/dialog_controller.py`)
```python
class DialogController:
    - Settings dialog management
    - Dialog lifecycle
    - User preference handling
```

#### 3. UI Components
**FileEntryBuilder** (`src/ui/widgets/file_entry_builder.py`)
```python
class FileEntryBuilder:
    - File entry widget creation
    - Checkbox event handling
    - Color picker integration
    - State management
```

#### 4. Infrastructure Layer
**AppProperties** (`src/infrastructure/repositories/properties_repository.py`)
```python
class AppProperties:
    - Configuration persistence
    - File reference management
    - Settings validation
    - JSON operations
```

### Design Patterns Used

#### 1. Repository Pattern
```python
# Centralized data access
class AppProperties:
    def get_file_settings_by_reference(self, ref_num)
    def save_file_settings_by_reference(self, ref_num, settings)
    def get_or_create_file_reference(self, file_path)
```

#### 2. Builder Pattern
```python
# UI component construction
class FileEntryBuilder:
    def create_file_entry(self, path, ref_num, analysis, settings, properties)
```

#### 3. Controller Pattern
```python
# Separation of UI and business logic
class MapController:
    def update_map(self, entries)
    def fit_to_gpx(self, entries)
```

#### 4. Observer Pattern
```python
# Event-driven updates
visible_var.trace('w', on_visible_change)
```

---

## Component Cross-Reference

### Data Structure Cross-Reference

#### Properties File Structure
```json
{
  "files": {
    "session": {
      "1": {
        "path": "/path/to/file.gpx",
        "settings": {
          "visible": true,
          "editable": false,
          "color": "#ff0000"
        }
      }
    }
  },
  "dialogs": {
    "settings": {
      "logging": {"level": "INFO", "file": "app.log"},
      "rendering": {"line_width": 3},
      "marker": {"enabled": true}
    }
  },
  "app": {
    "main_window": {"geometry": "800x600+100+100"},
    "recent_files_timestamps": {}
  }
}
```

#### Component Dependencies

| Component | Dependencies | Used By |
|-----------|--------------|----------|
| `AppProperties` | JSON, OS | All controllers, services |
| `GPXFileManager` | `AppProperties`, `FileEntryBuilder` | Main App |
| `MapController` | `AppProperties`, `GPXCache` | Main App |
| `FileEntryBuilder` | `AppProperties`, tkinter | `GPXFileManager` |
| `DialogController` | `AppProperties`, various dialogs | Main App |
| `GPXEditController` | gpxpy, tkinter | Main App |

#### Method Cross-Reference

**File Reference Management**
```python
# Creation
ref_num = properties.get_or_create_file_reference(file_path)

# Settings Access
settings = properties.get_file_settings_by_reference(ref_num)
properties.save_file_settings_by_reference(ref_num, settings)

# Path Resolution
path = properties.get_file_path_by_reference(ref_num)
```

**UI State Synchronization**
```python
# File Entry → Properties
entry._save_states()  # Saves visible/editable state

# Properties → Map Rendering
session_files = properties.get('files.session')
is_visible = session_files[ref_num]['settings']['visible']
```

#### Event Flow Cross-Reference

```python
# Checkbox Interaction Flow
visible_var.trace('w', on_visible_change)
    ↓
on_visible_change()
    ↓
entry._save_states()
    ↓
properties.save_file_settings_by_reference()
    ↓
map_controller.update_map()
```

---

## Data Flow

### File Loading Flow
```
1. User selects GPX file
   ↓
2. GPXFileManager.load_gpx_file()
   ↓
3. File validation and analysis
   ↓
4. properties.get_or_create_file_reference()
   ↓
5. FileEntryBuilder.create_file_entry()
   ↓
6. UI widget creation and event binding
   ↓
7. MapController.update_map()
   ↓
8. GPXCache.get_gpx() → Map rendering
```

### Settings Persistence Flow
```
1. User changes checkbox state
   ↓
2. trace() event triggers
   ↓
3. on_visible_change() handler
   ↓
4. entry._save_states()
   ↓
5. properties.save_file_settings_by_reference()
   ↓
6. properties.save() → JSON file
```

### Map Rendering Flow
```
1. MapController.update_map(entries)
   ↓
2. Filter visible entries
   ↓
3. For each entry:
   ├─ Check visibility in properties
   ├─ Get GPX data from GPXCache
   └─ Render on map widget
   ↓
4. Fit map to visible data
```

---

## Configuration

### Application Configuration

#### Main Configuration File: `properties.json`
```json
{
  "files": {
    "session": {
      "file_ref": {
        "path": "absolute/path/to/file.gpx",
        "settings": {
          "visible": boolean,
          "editable": boolean,
          "color": "#hexcolor"
        }
      }
    }
  },
  "dialogs": {
    "settings": {
      "logging": {
        "level": "DEBUG|INFO|WARNING|ERROR",
        "file": "logfilename.txt",
        "display_lines": integer
      },
      "rendering": {
        "line_width": integer,
        "color_scheme": "default|custom"
      },
      "marker": {
        "enabled": boolean,
        "step": integer
      }
    }
  },
  "app": {
    "main_window": {
      "geometry": "widthxheight+x+y"
    },
    "recent_files_timestamps": {
      "filepath": timestamp
    }
  }
}
```

#### Environment Configuration
- **Log Files**: `app.log` (configurable)
- **Temporary Files**: System temp directory
- **Cache**: In-memory GPX data cache
- **Backups**: Automatic properties file backups

### Runtime Configuration

#### Logging Configuration
```python
# Configured via properties.json
logging.basicConfig(
    level=properties.get('level'),
    filename=properties.get('file')
)
```

#### Map Configuration
```python
# TkinterMapView settings
map_widget.set_position(lat, lon)
map_widget.set_zoom(level)
```

---

## Development Guidelines

### Code Organization Principles

#### 1. Layer Separation
- **Presentation Layer**: UI components, dialogs, main app
- **Application Layer**: Controllers, services, business logic
- **Infrastructure Layer**: Repositories, utilities, error handling

#### 2. Dependency Direction
```
UI → Controllers → Infrastructure
↑           ↓              ↓
└──────────┴──────────────┘
```

#### 3. Naming Conventions
- **Classes**: PascalCase (e.g., `GPXFileManager`)
- **Methods**: snake_case (e.g., `load_gpx_file`)
- **Variables**: snake_case (e.g., `file_path`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_ZOOM`)

### Testing Strategy

#### Test Categories
1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Component interaction testing
3. **Regression Tests**: Preventing functionality loss
4. **Performance Tests**: Ensuring acceptable performance

#### Test Files Structure
```
tests/
├── test_regression.py      # Regression prevention
├── test_integration_updated.py  # Integration testing
├── test_performance.py     # Performance validation
└── test_*.py              # Additional test modules
```

#### Running Tests
```bash
# Regression tests
python -m tests.test_regression

# Integration tests  
python -m tests.test_integration_updated

# All tests
python -m pytest tests/ -v
```

### Extension Guidelines

#### Adding New Features
1. **Define Requirements**: Clear functionality specification
2. **Choose Layer**: Determine appropriate architectural layer
3. **Implement Component**: Follow existing patterns
4. **Add Tests**: Comprehensive test coverage
5. **Update Documentation**: Keep docs current

#### Adding New Controllers
```python
class NewController:
    def __init__(self, dependencies):
        # Initialize with dependencies
        
    def main_method(self):
        # Core functionality
        
    def cleanup(self):
        # Resource cleanup
```

#### Adding New UI Components
```python
class NewWidgetBuilder:
    def __init__(self, parent_frame, callbacks):
        # Initialize builder
        
    def create_widget(self, data, properties):
        # Create and configure widget
        return widget
```

### Error Handling Guidelines

#### Error Categories
1. **Expected Errors**: File not found, invalid format
2. **Unexpected Errors**: Network issues, system failures
3. **Critical Errors**: Data corruption, security issues

#### Error Handling Pattern
```python
try:
    # Operation that might fail
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Specific error: {e}")
    # Handle gracefully
    fallback_operation()
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    # Critical error handling
    emergency_cleanup()
```

---

## API Reference

### Core APIs

#### AppProperties API
```python
class AppProperties:
    def get_or_create_file_reference(file_path: str) -> int
    def get_file_settings_by_reference(ref_num: int) -> dict
    def save_file_settings_by_reference(ref_num: int, settings: dict)
    def get_file_path_by_reference(ref_num: int) -> str
    def remove_file_from_session(ref_num: int)
    def save() -> None
    def load() -> None
```

#### GPXFileManager API
```python
class GPXFileManager:
    def add_file_to_ui(path: str) -> object
    def remove_file_from_ui(entry: object) -> None
    def get_all_entries() -> list
    def get_visible_entries() -> list
    def get_editable_entries() -> list
    def load_gpx_file(path: str) -> dict
    def clear_all_entries() -> None
```

#### MapController API
```python
class MapController:
    def update_map(entries: list) -> None
    def update_visibility_only(entries: list) -> None
    def fit_to_gpx(entries: list) -> None
    def _is_entry_visible(entry: object) -> bool
    def _get_entry_coordinates(entry: object) -> list
```

#### FileEntryBuilder API
```python
class FileEntryBuilder:
    def __init__(parent_frame, row, callbacks)
    def create_file_entry(path, ref_num, analysis, settings, properties) -> object
```

### Utility APIs

#### GPXCache API
```python
class GPXCache:
    @classmethod
    def get_gpx(path: str) -> object
    @classmethod
    def clear_all() -> None
```

---

## Troubleshooting

### Common Issues

#### Application Won't Start
1. Check Python dependencies: `pip install -r requirements.txt`
2. Verify tkinter installation
3. Check properties.json format
4. Review log files for errors

#### GPX Files Not Loading
1. Verify file format validity
2. Check file permissions
3. Ensure file path is accessible
4. Review file analysis logs

#### Map Not Rendering
1. Check tkintermapview installation
2. Verify network connectivity for map tiles
3. Check coordinate data validity
4. Review rendering settings

#### Settings Not Persisting
1. Check properties.json permissions
2. Verify JSON format validity
3. Check disk space
4. Review save operation logs

### Debug Mode
```python
# Enable debug logging
properties.set('level', 'DEBUG')

# Check component state
print(f"Entries: {len(gpx_file_manager.get_all_entries())}")
print(f"Properties keys: {list(properties.data.keys())}")
```

---

## Version History

### Current Version Features
- ✅ Modern FileEntryBuilder architecture
- ✅ Consistent properties structure
- ✅ Comprehensive test coverage (20 tests)
- ✅ Error handling and recovery
- ✅ Multi-language support
- ✅ Drag & drop functionality
- ✅ Interactive map visualization

### Recent Improvements
- Eliminated redundant FileEntry system
- Removed complex DI container
- Standardized properties structure
- Added comprehensive regression tests
- Improved error handling
- Enhanced code documentation

---

*This documentation is automatically generated and maintained. Last updated: 2026-03-28*
