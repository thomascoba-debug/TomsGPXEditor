# 🛡️ Stabilitäts-Guide für TomsGPXEditor

## 📋 Übersicht

Diese Guide beschreibt die Maßnahmen zur Erhöhung der Stabilität und Wartungsfreundlichkeit des GPX Editors.

## 🎯 Hauptprobleme behoben

### 1. **JSON-Stabilität**
- **Problem:** Ständige Dubletten und inkonsistente Struktur
- **Lösung:** Automatische Validierung und Aufräumung
- **Implementierung:** `src/infrastructure/json_validator.py`

### 2. **Recent Files Zuverlässigkeit**
- **Problem:** Dateien erscheinen nicht nach Drag & Drop
- **Lösung:** Sicheres Laden mit Reload-Mechanismus
- **Implementierung:** `src/application/services/recent_files_service.py`

### 3. **App-Start-Stabilität**
- **Problem:** Abstürze bei der Initialisierung
- **Lösung:** Robuste Fehlerbehandlung und sichere Reihenfolge
- **Implementierung:** `src/infrastructure/error_handler.py`

### 4. **Session-Management**
- **Problem:** Alte Session-Dateien werden nach Clear wieder geladen
- **Lösung:** Komplette Aufräumung inklusive Session
- **Implementierung:** `app.py` - `_clear_recent_files()`

## 🏗️ Architektur-Verbesserungen

### Zentrale Konfiguration
```python
# src/config/app_config.py
AppConfig.MAX_RECENT_FILES = 10
AppConfig.RECENT_FILES_KEY = "app.recent_files_timestamps"
AppConfig.PROPERTIES_FILE = "properties.json"
```

### Stabilitäts-Manager
```python
# src/infrastructure/stability_manager.py
stability_manager = StabilityManager()
issues = stability_manager.check_and_fix_stability()
```

### Error-Handler
```python
# src/infrastructure/error_handler.py
@safe_execute("Operation failed")
def risky_operation():
    return do_something()
```

## 🚀 Verwendung

### Stabiler Start
```bash
# Stabiler Start mit allen Features
python start_stable.py

# Normaler Start
python main.py
```

### JSON-Validierung
```python
# Manuelles Prüfen
python src/infrastructure/json_validator.py properties.json

# Automatische Validierung (im Code integriert)
```

### Wartung
```python
# Wartung laufen lassen
from src.infrastructure.stability_manager import get_stability_manager

manager = get_stability_manager()
manager.run_maintenance()
```

## 📊 Monitoring

### Log-Dateien
- `logs/app.log` - Hauptanwendungs-Log
- `logs/errors.log` - Fehler-Log mit Details
- `logs/stability.log` - Stabilitäts-Checks

### Backups
- `backups/` - Automatische Backups mit Zeitstempel
- `properties.json.backup_*` - Manuelle Backups

## 🔧 Konfiguration

### Entwicklung-Modus
```bash
# Entwicklung mit erweitertem Logging
export TGPX_DEV=true
python start_stable.py
```

### Log-Level anpassen
```python
# In app_config.py
class AppConfig:
    @classmethod
    def get_log_level(cls) -> str:
        if cls.is_development_mode():
            return "DEBUG"
        return "INFO"
```

## 🛠️ Fehlerbehebung

### Häufige Probleme

#### 1. JSON-Fehler
```bash
# JSON reparieren
python src/infrastructure/json_validator.py properties.json

# Backup wiederherstellen
python -c "from src.infrastructure.stability_manager import restore_from_backup; restore_from_backup(Path('backups/latest_backup'))"
```

#### 2. Recent Files Probleme
```bash
# Recent Files zurücksetzen
python -c "from app import TomsGPXEditor; app = TomsGPXEditor(); app._clear_recent_files()"
```

#### 3. Session-Probleme
```bash
# Session aufräumen
python -c "from src.infrastructure.stability_manager import get_stability_manager; get_stability_manager().cleanup_invalid_references()"
```

## 📈 Performance-Optimierung

### Automatische Aufräumung
- Invalid file references werden entfernt
- Alte Backups werden automatisch gelöscht
- JSON-Struktur wird validiert und korrigiert

### Memory-Management
- Fehler werden zentral gesammelt
- Stack-Traces werden begrenzt
- Ressourcen werden sauber freigegeben

## 🔍 Debugging

### Erweitertes Logging
```python
# Debug-Modus aktivieren
import logging
logging.getLogger().setLevel(logging.DEBUG)

# Oder über Umgebungsvariable
export TGPX_DEV=true
```

### Stabilitäts-Checks
```python
# Manuelles Prüfen
from src.infrastructure.stability_manager import run_stability_check
issues = run_stability_check()
print(f"Gefundene Probleme: {len(issues)}")
```

## 🎯 Best Practices

### 1. **Immer mit Stabilitäts-Features starten**
```bash
python start_stable.py  # statt python main.py
```

### 2. **Regelmäßige Wartung**
- JSON-Struktur prüfen
- Backups erstellen
- Logs überwachen

### 3. **Fehler dokumentieren**
- Screenshots bei Fehlern machen
- Log-Dateien sichern
- Schritte reproduzieren

### 4. **Vorsicht bei Änderungen**
- Immer Backup erstellen
- Änderungen schrittweise testen
- Stabilitäts-Checks laufen lassen

## 🚨 Notfall-Plan

### Wenn die App nicht startet
1. **Backup wiederherstellen:**
   ```bash
   cp backups/latest_backup.json properties.json
   ```

2. **Stabilen Start verwenden:**
   ```bash
   python start_stable.py
   ```

3. **Logs prüfen:**
   ```bash
   tail -f logs/errors.log
   ```

### Wenn JSON beschädigt ist
1. **Validierung laufen lassen:**
   ```bash
   python src/infrastructure/json_validator.py properties.json
   ```

2. **Manuell reparieren:**
   - Dubletten entfernen
   - Struktur korrigieren
   - Speichern

## 📞 Support

### Fehler melden
- Logs in `logs/errors.log` sichern
- Beschreibung des Problems
- Schritte zur Reproduktion
- System-Informationen

### Automatische Fehlerbehebung
Die meisten Probleme werden automatisch erkannt und behoben:
- JSON-Strukturfehler
- Invalid file references
- Memory leaks
- Circular dependencies

---

**Mit diesen Maßnahmen ist die GPX Editor App deutlich stabiler und wartungsfreundlicher!** 🛡️
