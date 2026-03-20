# 📚 **TomsGPXEditor - Projektübersicht**

## **🎯 Projektbeschreibung**
Ein spezialisierter GPX-Editor mit GUI, basierend auf tkinter und mehreren Erweiterungen. Die Hauptfunktionalität umfasst das Laden, Bearbeiten, Visualisieren und Verwalten von GPX-Dateien mit einer interaktiven Kartenansicht.

## **🏗️ Architektur**

### **📁 Verzeichnisstruktur**
```
TomsGPXEditor/
├── 📄 main.py                    # Einstiegspunkt
├── 📄 app.py                     # Hauptanwendung (48KB)
├── 📁 src/                       # Quellcode
│   ├── 🏗️ infrastructure/         # Infrastruktur
│   │   ├── map_renderer.py      # Karten-Rendering
│   │   ├── error_handler.py     # Fehlerbehandlung
│   │   └── repositories/      # Datenzugriff
│   ├── 🎨 ui/                    # Benutzeroberfläche
│   │   ├── dialogs/            # Dialoge
│   │   ├── widgets/            # UI-Komponenten
│   │   └── views/              # Ansichten
│   └── 🏢 application/            # Anwendungslogik
│       ├── services/           # Services
│       └── domain/             # Domänenlogik
├── 📁 libs/                      # Externe DLLs
├── 📁 assets/                    # Ressourcen
├── 📄 requirements.txt           # Abhängigkeiten
└── 📄 properties.json           # Einstellungen
```

### **🔧 Hauptkomponenten**

#### **📱 Hauptanwendung (app.py)**
- **TomsGPXEditor Klasse** - Zentrales Fenster
- **Datei-Management** - Laden, Speichern, Verwalten von GPX-Dateien
- **Menü-System** - File, Edit, Settings Menüs
- **UI-Steuerung** - Buttons, Dialoge, Status

#### **🗺 Karten-Rendering (map_renderer.py)**
- **TkinterMapView Integration** - Interaktive Kartenansicht
- **GPX-Visualisierung** - Tracks, Routen, Waypoints
- **Linien-Dicke** - Konfigurierbare Darstellung
- **Marker-Rendering** - Verschiedene Punkttypen

#### **⚙️ Settings-Dialoge**
- **Rendering Settings** - Linien-Dicke, Downsampling
- **Marker Settings** - Farben, Sichtbarkeit
- **Logging Settings** - Log-Level, Datei
- **Properties Editor** - Manuelle Konfiguration

#### **🔄 Konvertierungs-Dialoge**
- **Track to Route** - Tracks → Routen mit Downsampling
- **Route to Track** - Routen → Tracks
- **GPX-Selektion** - Checkboxen für Dateiauswahl
- **Dateiauswahl** - Speichern-Dialoge

## **🚀 Features**

### **✅ Implementierte Features**
1. **📁 Datei-Management**
   - Drag&Drop Unterstützung
   - Kürzliche Dateien
   - Session-Wiederherstellung
   - Datei-Analyse

2. **🗺 Karten-Visualisierung**
   - Interaktive Karte (TkinterMapView)
   - GPX-Track/Routen-Darstellung
   - Konfigurierbare Linien-Dicke
   - Marker für verschiedene Punkttypen

3. **⚙️ Einstellungen**
   - Rendering Settings (Linien-Dicke)
   - Marker Settings (Farben, Sichtbarkeit)
   - Logging Settings (Level, Datei)
   - Persistente Geometrie-Speicherung

4. **🔄 Konvertierung**
   - Track → Route Konvertierung
   - Route → Track Konvertierung
   - Downsampling (Punkte pro 100km)
   - Start/Endpunkt-Erhaltung

5. **🎛️ Dynamische UI**
   - Menü-Zustände basierend auf Edit-Dateien
   - Kein UI-Flackern
   - Automatische Updates

6. **💾 Backup-System**
   - Python, Batch, Shell Scripts
   - Automatische Namensgebung
   - Intelligente Ausschlüsse

## **🔧 Technologie-Stack**

### **🐍 Python**
- **Version:** 3.14
- **GUI:** tkinter
- **GPX:** gpxpy
- **Karte:** tkintermapview

### **📦 Hauptabhängigkeiten**
```
tkintermapview    # Interaktive Kartenansicht
gpxpy            # GPX-Dateiverarbeitung
tkinterdnd2      # Drag&Drop Unterstützung
pillow           # Bildverarbeitung
```

### **🏗️ Architektur-Pattern**
- **MVC Pattern** - Model-View-Controller Trennung
- **Repository Pattern** - Datenzugriffsabstraktion
- **Service Pattern** - Geschäftslogik-Kapselung
- **Observer Pattern** - UI-Updates bei Datenänderungen

## **📋 Aktuelle Projektgröße**
- **Hauptdatei:** app.py (48KB)
- **Gesamtquellcode:** ~50+ Python-Dateien
- **Abhängigkeiten:** 5 Hauptpakete
- **Testabdeckung:** Basis-Tests vorhanden

## **🎯 Nächste Schritte**

### **🔧 Optimierungen**
1. **Logging reduzieren** - Weniger Debug-Ausgaben
2. **Code-Dokumentation** - DocStrings ergänzen
3. **Unit-Tests** - Testabdeckung erhöhen
4. **Performance** - Large GPX-Dateien optimieren

### **🚀 Features**
1. **GPX-Editor** - Direkte Punkt-Bearbeitung
2. **Mehr Formate** - KML, TCX Export
3. **Offline-Karten** - Lokale Kartenunterstützung
4. **Batch-Verarbeitung** - Mehrere Dateien gleichzeitig

---

## **📞 Support & Entwicklung**

### **🔧 Entwicklungsumgebung**
```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Anwendung starten
python main.py

# Cleanup durchführen
python cleanup_project.py

# Backup erstellen
python backup_project.py
```

### **📝 Code-Qualität**
- **Logging:** Strukturiertes Logging mit Levels
- **Fehlerbehandlung:** Try/Catch mit aussagekräftigen Meldungen
- **UI-Feedback:** Statusmeldungen und Fortschrittsanzeigen
- **Persistenz:** Automatische Speicherung von Einstellungen

---

**📅 Stand:** 20.03.2026  
**👤 Entwickler:** AI Assistant & User  
**🎯 Status:** Stabil & Produktiv bereit
