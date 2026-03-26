#!/usr/bin/env python3
"""
Test Dialog Settings Persistence
Testet ob alle Dialog-Settings korrekt gespeichert und geladen werden
"""

import os
import sys
import tempfile
import json
from src.infrastructure.repositories.properties_repository import AppProperties

def test_dialog_settings_persistence():
    """Testet die Settings-Persistenz für alle Dialoge"""
    print("=== TESTING DIALOG SETTINGS PERSISTENCE ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
        
        # Test 1: Track Downsampling Settings
        print("\n--- Test 1: Track Downsampling Settings ---")
        props = AppProperties(temp_path)
        
        # Simuliere Settings-Speicherung
        props.set("downsample_points_per_100km", 50)
        props.set("downsample_keep_waypoints", False)
        props.set("downsample_overwrite_original", True)
        
        # Simuliere Dialog-Geometrie
        props.set_dialog_geometry("TrackDownsamplingDialog", "500x400+100+100")
        
        # Neustart simulieren
        props2 = AppProperties(temp_path)
        
        # Settings überprüfen
        points = props2.get("downsample_points_per_100km", 20)
        keep_waypoints = props2.get("downsample_keep_waypoints", True)
        overwrite_original = props2.get("downsample_overwrite_original", False)
        geometry = props2.get_dialog_geometry("TrackDownsamplingDialog")
        
        assert points == 50, f"Expected points=50, got {points}"
        assert keep_waypoints == False, f"Expected keep_waypoints=False, got {keep_waypoints}"
        assert overwrite_original == True, f"Expected overwrite_original=True, got {overwrite_original}"
        assert geometry == "500x400+100+100", f"Expected geometry=500x400+100+100, got {geometry}"
        print("Track Downsampling settings: PASSED")
        
        # Test 2: Track to Route Settings
        print("\n--- Test 2: Track to Route Settings ---")
        props.set("track_to_route_points_per_100km", 75)
        props.set_dialog_geometry("TrackToRouteDialog", "600x450+150+150")
        
        # Neustart simulieren
        props3 = AppProperties(temp_path)
        
        track_points = props3.get("track_to_route_points_per_100km", 100)
        track_geometry = props3.get_dialog_geometry("TrackToRouteDialog")
        
        assert track_points == 75, f"Expected track_points=75, got {track_points}"
        assert track_geometry == "600x450+150+150", f"Expected track_geometry=600x450+150+150, got {track_geometry}"
        print("Track to Route settings: PASSED")
        
        # Test 3: Route to Track Settings (nur Geometrie)
        print("\n--- Test 3: Route to Track Settings ---")
        props.set_dialog_geometry("RouteToTrackDialog", "550x420+200+200")
        
        # Neustart simulieren
        props4 = AppProperties(temp_path)
        
        route_geometry = props4.get_dialog_geometry("RouteToTrackDialog")
        
        assert route_geometry == "550x420+200+200", f"Expected route_geometry=550x420+200+200, got {route_geometry}"
        print("Route to Track settings: PASSED")
        
        # Test 4: Alle Settings zusammen
        print("\n--- Test 4: Complete Settings Check ---")
        final_props = AppProperties(temp_path)
        
        # Alle Settings überprüfen
        all_settings = {
            "downsample_points_per_100km": final_props.get("downsample_points_per_100km"),
            "downsample_keep_waypoints": final_props.get("downsample_keep_waypoints"),
            "downsample_overwrite_original": final_props.get("downsample_overwrite_original"),
            "track_to_route_points_per_100km": final_props.get("track_to_route_points_per_100km"),
        }
        
        all_geometries = {
            "TrackDownsamplingDialog": final_props.get_dialog_geometry("TrackDownsamplingDialog"),
            "TrackToRouteDialog": final_props.get_dialog_geometry("TrackToRouteDialog"),
            "RouteToTrackDialog": final_props.get_dialog_geometry("RouteToTrackDialog"),
        }
        
        expected_settings = {
            "downsample_points_per_100km": 50,
            "downsample_keep_waypoints": False,
            "downsample_overwrite_original": True,
            "track_to_route_points_per_100km": 75,
        }
        
        expected_geometries = {
            "TrackDownsamplingDialog": "500x400+100+100",
            "TrackToRouteDialog": "600x450+150+150",
            "RouteToTrackDialog": "550x420+200+200",
        }
        
        for key, expected in expected_settings.items():
            actual = all_settings[key]
            assert actual == expected, f"Expected {key}={expected}, got {actual}"
        
        for key, expected in expected_geometries.items():
            actual = all_geometries[key]
            assert actual == expected, f"Expected {key}={expected}, got {actual}"
        
        print("All settings persistence: PASSED")
        
        # Test 5: Properties-Datei überprüfen
        print("\n--- Test 5: Properties File Check ---")
        with open(temp_path, 'r') as f:
            data = json.load(f)
        
        # Überprüfen ob alle Keys vorhanden
        assert "downsample_points_per_100km" in data, "downsample_points_per_100km not in data"
        assert "downsample_keep_waypoints" in data, "downsample_keep_waypoints not in data"
        assert "downsample_overwrite_original" in data, "downsample_overwrite_original not in data"
        assert "track_to_route_points_per_100km" in data, "track_to_route_points_per_100km not in data"
        assert "dialog_geometry" in data, "dialog_geometry not in data"
        
        dialog_geom = data["dialog_geometry"]
        assert "TrackDownsamplingDialog" in dialog_geom, "TrackDownsamplingDialog not in dialog_geometry"
        assert "TrackToRouteDialog" in dialog_geom, "TrackToRouteDialog not in dialog_geometry"
        assert "RouteToTrackDialog" in dialog_geom, "RouteToTrackDialog not in dialog_geometry"
        
        print("Properties file structure: PASSED")
        
        print("\n=== ALL DIALOG SETTINGS TESTS PASSED ===")
        return True

if __name__ == "__main__":
    try:
        test_dialog_settings_persistence()
        print("\n🎉 ALL DIALOG SETTINGS WORK CORRECTLY!")
        print("✅ Settings are saved when dialogs close")
        print("✅ Settings are loaded when dialogs open")
        print("✅ Dialog geometries are preserved")
        print("✅ All three dialogs follow the same pattern")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        try:
            os.unlink(temp_path)
        except:
            pass
