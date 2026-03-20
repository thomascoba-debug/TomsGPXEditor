# 🗂️ **TomsGPXEditor Backup Scripts**

## **📋 Beschreibung:**
Drei Backup-Scripts für verschiedene Betriebssysteme zum Sichern aller wichtigen Projektdateien.

## **🚀 Verwendung:**

### **Windows (.bat)**
```bash
# Doppelklick oder Kommandozeile
backup_project.bat
```

### **Linux/Mac (.sh)**
```bash
# Terminal
./backup_project.sh
```

### **Python (plattformunabhängig)**
```bash
# Python 3.6+
python backup_project.py
```

## **📁 Backup-Struktur:**

### **Beispiel-Backup-Verzeichnis:**
```
W:/
├── TomsGPXEditor/              # Projektverzeichnis
└── TomsGPXEditor_2026-03-19/    # Backup-Verzeichnis
    ├── src/
    │   ├── ui/
    │   ├── infrastructure/
    │   └── ...
    ├── app.py
    ├── main.py
    ├── requirements.txt
    ├── README.md
    └── backup_info.txt         # Backup-Informationen
```

## **✅ Features:**

### **🔍 Automatische Ausschlüsse:**
- `__pycache__/` - Python Cache
- `.git/` - Git Repository
- `.vscode/` - VS Code Einstellungen
- `venv/`, `env/` - Virtuelle Umgebungen
- `*.pyc` - Python Bytecode
- `*.log` - Log-Dateien
- `properties.json` - Benutzer-spezifische Einstellungen
- `dist/`, `build/` - Build-Verzeichnisse
- `*.exe` - Executables

### **📊 Backup-Statistik:**
- Anzahl gesicherter Dateien
- Anzahl erstellter Verzeichnisse
- Übersprungene Dateien
- Zeitstempel und Projektinformationen

### **🔄 Automatische Namensgebung:**
- Format: `Projektname_JJJJ-MM-TT`
- Bei Konflikten: `Projektname_JJJJ-MM-TT_HH-MM-SS`

## **🎯 Vorteile:**

### **📦 Komplett:**
- Alle wichtigen Quelldateien
- Konfigurationsdateien
- Dokumentation

### **🚀 Schnell:**
- Nur relevante Dateien
- Keine unnötigen Cache-Dateien
- Optimiert für Git-Projekte

### **🔄 Automatisch:**
- Datum im Namen
- Konflikterkennung
- Statistik-Erstellung

## **📝 Anpassung:**

### **Weitere Ausschlüsse hinzufügen:**
```python
# In backup_project.py
exclude_patterns = [
    '__pycache__',
    '.git',
    'mein_verzeichnis',  # Neuer Ausschluss
    '*.meine_datei',     # Neuer Ausschluss
]
```

### **Backup-Ziel ändern:**
```python
# In backup_project.py
backup_dir = Path("/pfad/zu/meinen/backups") / backup_name
```

## **🎉 FERTIG!**

**Die Backup-Scripts sind bereit für die Verwendung:**

- **🪟 Windows:** `backup_project.bat`
- **🐧 Linux:** `backup_project.sh`
- **🐍 Python:** `backup_project.py`

**Einfach ausführen und das Backup wird erstellt!** 🚀
