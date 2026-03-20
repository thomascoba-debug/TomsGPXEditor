#!/usr/bin/env python3
"""
Cleanup Script für TomsGPXEditor
Entfernt unnötige Dateien und Verzeichnisse
"""

import os
import shutil
import glob
from pathlib import Path

def cleanup_project():
    """Räume das Projektverzeichnis auf"""
    
    project_root = Path(__file__).parent
    print(f"🧹 Cleanup für: {project_root}")
    
    # Zu löschende Dateien/Verzeichnisse
    cleanup_items = [
        # Alte Dateien
        "**/*_old*",
        
        # Build-Verzeichnisse
        "build/",
        "dist/",
        
        # Python Cache
        "**/__pycache__/",
        "**/*.pyc",
        
        # Log-Dateien (außer aktuelle)
        "applog.txt",
        "tests/*.log",
        
        # Temporäre Dateien
        "*.tmp",
        "*.temp",
        
        # IDE-Dateien
        ".idea/",
        
        # Test-Dateien
        "test_track.gpx",
        "test_with_waypoints.gpx",
        "karte.html",
    ]
    
    # Zähler
    removed_files = 0
    removed_dirs = 0
    
    for pattern in cleanup_items:
        # Finde alle Treffer
        matches = list(project_root.glob(pattern))
        
        for item in matches:
            try:
                if item.is_file():
                    item.unlink()
                    removed_files += 1
                    print(f"🗑️  Datei gelöscht: {item.relative_to(project_root)}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    removed_dirs += 1
                    print(f"📁 Verzeichnis gelöscht: {item.relative_to(project_root)}")
            except Exception as e:
                print(f"❌ Fehler beim Löschen von {item}: {e}")
    
    print(f"\n✅ Cleanup abgeschlossen:")
    print(f"   🗑️  {removed_files} Dateien gelöscht")
    print(f"   📁 {removed_dirs} Verzeichnisse gelöscht")

if __name__ == "__main__":
    cleanup_project()
