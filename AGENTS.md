# AGENTS.md – Leitfaden für AI Coding Agents

## Überblick
Dieses Projekt ist ein spezialisierter GPX-Editor mit GUI, der auf `tkinter` und mehreren Erweiterungen basiert. Die Hauptfunktionalität umfasst das Laden, Bearbeiten, Visualisieren und Verwalten von GPX-Dateien mit einer interaktiven Kartenansicht. Die Architektur ist modular, mit klar getrennten Komponenten für UI, Dateiverwaltung, GPX-Parsing, Rendering und Einstellungen.

## Architektur & Hauptkomponenten
- **main.py**: Einstiegspunkt, startet die App über `TomsGPXEditor` aus `app.py`.
- **app.py**: Zentrale Klasse `TomsGPXEditor`, steuert das Hauptfenster, Menü, Datei-Handling, Map-Rendering und bindet alle Subsysteme zusammen.
- **edit_controller.py**: Kapselt das Laden und Parsen von GPX-Dateien (über `gpxpy`), stellt `GPXDocument` bereit.
- **file_entry.py**: UI-Komponente für einzelne GPX-Dateien, verwaltet Sichtbarkeit, Editierbarkeit und Farbauswahl pro Datei.
- **map_renderer.py**: Zeichnet GPX-Tracks auf die Karte (`TkinterMapView`), unterstützt Downsampling und Farbanpassung.
- **gpx_table_editor.py**: Editor für Trackpunkte in Tabellenform.
- **settings_*.py**: Dialoge für verschiedene Einstellungen (Logging, Marker, Rendering, Properties).
- **properties.py**: Persistente Speicherung und Verwaltung von App-Einstellungen und zuletzt geöffneten Dateien.
- **assets/**: Enthält Marker-Icons und andere Ressourcen.
- **libs/**: Externe DLLs für Drag&Drop-Unterstützung.

## Datenflüsse & Interaktionen
- GPX-Dateien werden per Dialog oder Drag&Drop geladen (`_add_file` in `app.py`).
- Jede Datei wird als `FileEntry`-Widget dargestellt und kann individuell ein-/ausgeblendet, editiert oder farblich angepasst werden.
- Änderungen an Dateien oder Einstellungen triggern ein Neurendern der Karte (`update_map`).
- Einstellungen werden persistent in `properties.json` gespeichert und beim Start geladen.
- Die Map-Ansicht basiert auf `TkinterMapView`, Marker und Tracks werden dynamisch gerendert.

## Build- und Entwicklungs-Workflows
- **Build als Exe:**
  - `pyexe.bat` ruft PyInstaller mit `TGPXE.spec` auf, um eine Windows-Executable zu bauen.
  - Assets und DLLs werden explizit in der `.spec`-Datei eingebunden.
- **Abhängigkeiten:**
  - Siehe `requirements.txt` (u.a. `tkintermapview`, `tkinterdnd2`, `gpxpy`, `pillow`).
- **Debugging:**
  - Logging-Level und Logdatei sind über die Properties konfigurierbar.
- **Eigene Einstellungen:**
  - Dialog-Geometrien und weitere UI-States werden in `properties.json` gespeichert.

## Projektspezifische Konventionen
- **Dateipfade:** Windows-Pfade, häufig absolute Pfadangaben in Properties.
- **UI-Logik:** Fast alle UI-Elemente sind als eigene Klassen gekapselt, Änderungen an Properties führen meist zu sofortigem Speichern und UI-Update.
- **GPX-Farben:** Pro Datei individuell, persistent gespeichert.
- **Keine klassischen Unit-Tests** im Workspace gefunden.

## Beispiele & Hinweise
- **Datei laden:**
  ```python
  app._add_file('C:/Pfad/zur/Datei.gpx')
  ```
- **Eigene Properties speichern:**
  ```python
  app.properties.set('key', value)
  app.properties.save()
  ```
- **Build ausführen:**
  ```bat
  pyexe.bat
  ```
- **Map aktualisieren:**
  ```python
  app.update_map()
  ```

## Wichtige Dateien/Verzeichnisse
- `app.py`, `main.py`, `edit_controller.py`, `file_entry.py`, `map_renderer.py`, `gpx_table_editor.py`, `settings_*.py`, `properties.py`, `requirements.txt`, `TGPXE.spec`, `pyexe.bat`, `assets/`, `libs/`

## Integration & Erweiterung
- Neue Einstellungen sollten über `properties.py` verwaltet werden.
- Neue Dateitypen oder Map-Features erfordern Anpassungen in `app.py` und ggf. `map_renderer.py`.
- Externe Bibliotheken müssen in `requirements.txt` und ggf. in der `.spec`-Datei ergänzt werden.

---
Weitere Details zu Architektur und Workflows sind direkt in den jeweiligen Modulen dokumentiert. Für tiefere Analysen empfiehlt sich ein Blick in `app.py` und die zugehörigen Settings-Dialoge.
