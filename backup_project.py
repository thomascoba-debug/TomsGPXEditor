#!/usr/bin/env python3
"""
Backup Script für TomsGPXEditor
Sichert alle wichtigen Projektdateien in ein Verzeichnis auf gleicher Höhe wie das Projektverzeichnis
"""

import os
import shutil
import datetime
import sys
from pathlib import Path

def get_project_root():
    """Ermittle das Projektverzeichnis (dieses Skript-Verzeichnis)"""
    return Path(__file__).parent

def get_backup_directory(project_root, project_name):
    """Erstelle Backup-Verzeichnis auf gleicher Höhe wie Projekt"""
    parent_dir = project_root.parent
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    backup_name = f"{project_name}_{today}"
    backup_dir = parent_dir / backup_name
    
    # Wenn Verzeichnis schon existiert, füge Zeitstempel hinzu
    if backup_dir.exists():
        time_str = datetime.datetime.now().strftime("%H-%M-%S")
        backup_name = f"{project_name}_{today}_{time_str}"
        backup_dir = parent_dir / backup_name
    
    return backup_dir

def should_backup_file(file_path, project_root):
    """Prüfe ob Datei gesichert werden soll"""
    # Dateien und Verzeichnisse die NICHT gesichert werden sollen
    exclude_patterns = [
        '__pycache__',
        '.git',
        '.vscode',
        '*.pyc',
        '*.log',
        'app.log',
        'properties.json',  # Benutzer-spezifische Einstellungen
        'venv',
        'env',
        '.env',
        'node_modules',
        '*.tmp',
        '*.temp',
        'dist',
        'build',
        '*.exe',
        '*.spec'  # PyInstaller spec files können ausgeschlossen werden
    ]
    
    relative_path = file_path.relative_to(project_root)
    path_str = str(relative_path).replace('\\', '/')
    
    # Prüfe Ausschlussmuster
    for pattern in exclude_patterns:
        if pattern in path_str or path_str.endswith(pattern.replace('*', '')):
            return False
    
    return True

def backup_project(project_root, backup_dir):
    """Sichere das gesamte Projekt"""
    print(f"🔄 Starte Backup von: {project_root}")
    print(f"📁 Zielverzeichnis: {backup_dir}")
    
    # Erstelle Backup-Verzeichnis
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Zähler für gesicherte Dateien
    files_backed_up = 0
    dirs_created = 0
    files_skipped = 0
    
    # Gehe durch alle Dateien und Verzeichnisse
    for root, dirs, files in os.walk(project_root):
        # Filtere Verzeichnisse
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        # Berechne relativen Pfad
        rel_root = Path(root).relative_to(project_root)
        backup_root = backup_dir / rel_root
        
        # Erstelle Verzeichnis im Backup
        if not backup_root.exists():
            backup_root.mkdir(parents=True, exist_ok=True)
            dirs_created += 1
        
        # Sichere Dateien
        for file in files:
            source_file = Path(root) / file
            target_file = backup_root / file
            
            if should_backup_file(source_file, project_root):
                try:
                    shutil.copy2(source_file, target_file)
                    files_backed_up += 1
                    print(f"✅ {source_file.relative_to(project_root)}")
                except Exception as e:
                    print(f"❌ Fehler bei {source_file}: {e}")
                    files_skipped += 1
            else:
                files_skipped += 1
    
    return files_backed_up, dirs_created, files_skipped

def create_backup_info(backup_dir, project_root, files_count, dirs_count, skipped_count):
    """Erstelle Backup-Info-Datei"""
    info_file = backup_dir / "backup_info.txt"
    
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write(f"BACKUP INFORMATION\n")
        f.write(f"==================\n\n")
        f.write(f"Projekt: {project_root.name}\n")
        f.write(f"Datum: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')\n")
        f.write(f"Quellverzeichnis: {project_root}\n")
        f.write(f"Zielverzeichnis: {backup_dir}\n\n")
        f.write(f"STATISTIK:\n")
        f.write(f"---------\n")
        f.write(f"Dateien gesichert: {files_count}\n")
        f.write(f"Verzeichnisse erstellt: {dirs_count}\n")
        f.write(f"Dateien übersprungen: {skipped_count}\n\n")
        f.write(f"AUSSCHLÜSSE:\n")
        f.write(f"-----------\n")
        f.write(f"- __pycache__ Verzeichnisse\n")
        f.write(f"- .git Verzeichnisse\n")
        f.write(f"- .vscode Verzeichnisse\n")
        f.write(f"- *.pyc Dateien\n")
        f.write(f"- *.log Dateien\n")
        f.write(f"- properties.json (benutzer-spezifisch)\n")
        f.write(f"- venv/env Verzeichnisse\n")
        f.write(f"- dist/build Verzeichnisse\n")
        f.write(f"- .env Dateien\n")

def main():
    """Hauptfunktion"""
    print("🗂️  TomsGPXEditor Backup Script")
    print("=" * 40)
    
    # Projektverzeichnis ermitteln
    project_root = get_project_root()
    project_name = project_root.name
    
    print(f"📂 Projektverzeichnis: {project_root}")
    print(f"📛 Projektname: {project_name}")
    
    # Backup-Verzeichnis ermitteln
    backup_dir = get_backup_directory(project_root, project_name)
    
    # Prüfe ob Projektverzeichnis existiert
    if not project_root.exists():
        print(f"❌ Fehler: Projektverzeichnis nicht gefunden: {project_root}")
        sys.exit(1)
    
    try:
        # Führe Backup durch
        files_count, dirs_count, skipped_count = backup_project(project_root, backup_dir)
        
        # Erstelle Info-Datei
        create_backup_info(backup_dir, project_root, files_count, dirs_count, skipped_count)
        
        print("\n" + "=" * 40)
        print(f"✅ Backup erfolgreich abgeschlossen!")
        print(f"📁 Backup-Verzeichnis: {backup_dir}")
        print(f"📊 {files_count} Dateien gesichert")
        print(f"📁 {dirs_count} Verzeichnisse erstellt")
        print(f"⏭️  {skipped_count} Dateien übersprungen")
        
    except Exception as e:
        print(f"❌ Fehler beim Backup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
