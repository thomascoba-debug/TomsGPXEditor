# 🚀 **Git Repository Setup für TomsGPXEditor**

## **📋 Voraussetzungen:**
- **Git installiert** - Muss auf Ihrem System verfügbar sein
- **Projekt sauber** - Mit `cleanup_project.py` aufgeräumt

## **🔧 Schritt-für-Schritt Anleitung:**

### **1. Git initialisieren**
```bash
# In das Projektverzeichnis wechseln
cd W:/TomsGPXEditor

# Git Repository initialisieren
git init
```

### **2. .gitignore hinzufügen**
```bash
# .gitignore zum Staging-Bereich hinzufügen
git add .gitignore

# Mit Commit-Nachricht speichern
git commit -m "Add comprehensive .gitignore for Python project"
```

### **3. Alle Quelldateien hinzufügen**
```bash
# Alle Python-Dateien, Konfigurationen, Dokumentation
git add src/
git add *.py
git add *.md
git add requirements.txt
git add TGPXE.spec
git add libs/
git add assets/

# Commit erstellen
git commit -m "Initial commit: TomsGPXEditor with all core features"
```

### **4. Projektstruktur prüfen**
```bash
# Status anzeigen
git status

# Sollte zeigen:
# On branch master
# nothing to commit, working tree clean
```

## **🌐 Remote Repository einrichten (Optional):**

### **GitHub Repository erstellen:**
1. **GitHub aufrufen** - https://github.com
2. **New Repository** - "TomsGPXEditor"
3. **Public/Private** - Nach Wahl
4. **README initialisieren** - Haken setzen

### **Remote hinzufügen:**
```bash
# Remote URL ersetzen mit Ihrer GitHub-URL
git remote add origin https://github.com/IHR_USERNAME/TomsGPXEditor.git

# Zum Remote pushen
git push -u origin master
```

## **📁 Empfohlene .gitignore (bereits erstellt):**
```gitignore
# Python Cache & Build
__pycache__/
*.pyc
build/
dist/

# IDE & OS
.idea/
.vscode/
.DS_Store

# Projekt-spezifisch
*.log
*_old*
PROJECT_NAMEDATE/
```

## **🔄 Tägliche Arbeit mit Git:**

### **Änderungen committen:**
```bash
# Status prüfen
git status

# Geänderte Dateien hinzufügen
git add .

# Commit mit aussagekräftiger Nachricht
git commit -m "Implement feature: Linien-Dicke im Rendering Dialog"
```

### **Änderungen pushen:**
```bash
# Zum Remote Repository pushen
git push
```

## **🏷️ Branching & Tags (Empfehlungen):**

### **Feature-Branches:**
```bash
# Neuen Feature-Branch erstellen
git checkout -b feature/linien-dicke

# Arbeit durchführen...
# Zurück zu master mergen
git checkout master
git merge feature/linien-dicke
```

### **Version-Tags:**
```bash
# Version taggen
git tag -a v1.0.0 -m "Release version 1.0.0"

# Tags pushen
git push --tags
```

## **🚨 Häufige Probleme & Lösungen:**

### **Problem: Git nicht gefunden**
```bash
# Git installieren (Windows):
# Download: https://git-scm.com/download/win
# Oder über Package Manager: winget install Git
```

### **Problem: Dateien werden ignoriert**
```bash
# .gitignore prüfen
git check-ignore *.pyc

# Cache leeren
git rm -r --cached .
git add .
git commit -m "Update .gitignore and clear cache"
```

### **Problem: Large Files**
```bash
# Git LFS für große Dateien
git lfs track "*.gpx"
git add .gitattributes
git commit -m "Track GPX files with Git LFS"
```

## **📊 Repository-Struktur nach Setup:**
```
TomsGPXEditor/
├── .git/                    # Git Repository
├── .gitignore               # Ausschlussregeln
├── src/                     # Quellcode
├── *.py                     # Hauptdateien
├── *.md                     # Dokumentation
├── requirements.txt          # Abhängigkeiten
└── libs/                    # Externe Bibliotheken
```

---

## **🎯 Nächste Schritte:**

1. **Git installieren** (falls nicht vorhanden)
2. **Repository initialisieren** mit `git init`
3. **.gitignore hinzufügen** und committen
4. **Quelldateien committen**
5. **Remote einrichten** (GitHub/GitLab/etc.)
6. **Arbeits-Workflow etablieren**

---

**🚀 Ihr TomsGPXEditor ist dann ein vollwertiges Git Repository!**
