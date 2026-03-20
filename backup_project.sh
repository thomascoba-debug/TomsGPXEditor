#!/bin/bash
# Backup Script für TomsGPXEditor (Linux/Mac)
# Erstellt ein Backup aller wichtigen Projektdateien

echo "🗂️  TomsGPXEditor Backup Script"
echo "================================"

# Projektverzeichnis (dieses Verzeichnis)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="TomsGPXEditor"

# Datum für Backup-Name
DATE=$(date +"%Y-%m-%d")

# Backup-Verzeichnis auf gleicher Höhe wie Projekt
BACKUP_DIR="$(dirname "$PROJECT_DIR")/${PROJECT_NAME}_${DATE}"

# Prüfe ob Backup-Verzeichnis schon existiert
if [ -d "$BACKUP_DIR" ]; then
    echo "⚠️  Backup-Verzeichnis existiert bereits, füge Zeitstempel hinzu"
    TIME=$(date +"%H-%M-%S")
    BACKUP_DIR="$(dirname "$PROJECT_DIR")/${PROJECT_NAME}_${DATE}_${TIME}"
fi

echo "📂 Projektverzeichnis: $PROJECT_DIR"
echo "📛 Projektname: $PROJECT_NAME"
echo "📁 Zielverzeichnis: $BACKUP_DIR"
echo ""

# Erstelle Backup-Verzeichnis
mkdir -p "$BACKUP_DIR"
if [ $? -ne 0 ]; then
    echo "❌ Fehler: Konnte Backup-Verzeichnis nicht erstellen"
    exit 1
fi

echo "🔄 Starte Backup..."
echo ""

# Zähler
FILES_COUNT=0
DIRS_COUNT=0
SKIPPED_COUNT=0

# Funktion zum Prüfen ob Verzeichnis ausgeschlossen werden soll
should_skip_dir() {
    local dir_name="$1"
    case "$dir_name" in
        __pycache__|.git|.vscode|venv|env|node_modules|dist|build)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Funktion zum Prüfen ob Datei ausgeschlossen werden soll
should_skip_file() {
    local file_name="$1"
    case "$file_name" in
        *.pyc|*.log|app.log|properties.json|*.tmp|*.temp|*.exe)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Verzeichnisse kopieren
echo "📁 Kopiere Verzeichnisse..."
for dir in */; do
    dir_name="${dir%/}"
    if should_skip_dir "$dir_name"; then
        echo "⏭️  Überspringe Verzeichnis: $dir_name"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    else
        echo "✅ Kopiere Verzeichnis: $dir_name"
        cp -r "$dir_name" "$BACKUP_DIR/" 2>/dev/null
        if [ $? -eq 0 ]; then
            DIRS_COUNT=$((DIRS_COUNT + 1))
        fi
    fi
done

# Dateien kopieren
echo ""
echo "📄 Kopiere Dateien..."
for file in *.py *.md *.txt *.json *.yml *.yaml *.gitignore *.requirements.txt; do
    if [ -f "$file" ]; then
        if should_skip_file "$file"; then
            echo "⏭️  Überspringe Datei: $file"
            SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        else
            echo "✅ Kopiere Datei: $file"
            cp "$file" "$BACKUP_DIR/" 2>/dev/null
            if [ $? -eq 0 ]; then
                FILES_COUNT=$((FILES_COUNT + 1))
            fi
        fi
    fi
done

# Erstelle Info-Datei
echo ""
echo "📝 Erstelle Backup-Info..."
cat > "$BACKUP_DIR/backup_info.txt" << EOF
BACKUP INFORMATION
==================

Projekt: $PROJECT_NAME
Datum: $(date '+%Y-%m-%d %H:%M:%S')
Quellverzeichnis: $PROJECT_DIR
Zielverzeichnis: $BACKUP_DIR

STATISTIK:
---------
Dateien gesichert: $FILES_COUNT
Verzeichnisse erstellt: $DIRS_COUNT
Dateien übersprungen: $SKIPPED_COUNT

AUSSCHLÜSSE:
-----------
- __pycache__ Verzeichnisse
- .git Verzeichnisse
- .vscode Verzeichnisse
- venv/env Verzeichnisse
- *.pyc Dateien
- *.log Dateien
- properties.json (benutzer-spezifisch)
- dist/build Verzeichnisse
- .env Dateien
EOF

echo ""
echo "================================"
echo "✅ Backup erfolgreich abgeschlossen!"
echo "📁 Backup-Verzeichnis: $BACKUP_DIR"
echo "📊 $FILES_COUNT Dateien gesichert"
echo "📁 $DIRS_COUNT Verzeichnisse erstellt"
echo ""

# Öffne Backup-Verzeichnis im Dateimanager (optional)
if command -v xdg-open > /dev/null; then
    echo "🔍 Öffne Backup-Verzeichnis im Dateimanager..."
    xdg-open "$(dirname "$BACKUP_DIR")" 2>/dev/null &
elif command -v open > /dev/null; then
    echo "🔍 Öffne Backup-Verzeichnis im Finder..."
    open "$(dirname "$BACKUP_DIR")" 2>/dev/null &
fi

echo "Backup abgeschlossen! 🎉"
