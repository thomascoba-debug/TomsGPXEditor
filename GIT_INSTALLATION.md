# 🚀 **Git Installation für Windows**

## **🌐 Methode 1: Offizielle Website (Empfohlen)**

### **📥 Download:**
1. **Website aufrufen:** https://git-scm.com/download/win
2. **Version wählen:** 64-bit oder 32-bit (meistens 64-bit)
3. **Download starten:** Git-2.XX.X-64-bit.exe

### **⚙️ Installation:**
1. **Setup starten** - Doppelklick auf gedownloadete .exe Datei
2. **Komponenten auswählen:**
   - ✅ Git GUI Here (empfohlen)
   - ✅ Git Bash (empfohlen)
   - ✅ Git LFS (optional)
3. **Standard-Editor wählen:** 
   - **Vim** (Standard) oder **Notepad++** (falls installiert)
4. **PATH-Variable konfigurieren:**
   - ✅ **Use Git from the Windows Command Prompt** (WICHTIG!)
   - ✅ **Use Git and optional Unix tools from Windows Command Prompt**
5. **HTTPS-Transport:** 
   - ✅ **Use the OpenSSL library** (Standard)
6. **Line endings:**
   - ✅ **Checkout Windows-style, commit Unix-style line endings**
   - ✅ **Convert Windows line endings to Unix style**

### **🔄 Installation überprüfen:**
```bash
# Kommandozeile öffnen (cmd oder PowerShell)
git --version
# Sollte anzeigen: git version 2.XX.X.windows.X
```

---

## **🏪 Methode 2: Windows Package Manager (winget)**

### **📦 Installation über winget:**
```powershell
# PowerShell als Administrator öffnen
winget install Git.Git

# Oder mit Version:
winget install Git.Git --version latest
```

### **🔄 Überprüfen:**
```powershell
git --version
```

---

## **🐧 Methode 3: Chocolatey Package Manager**

### **📦 Chocolatey installieren (falls nicht vorhanden):**
```powershell
# PowerShell als Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### **📦 Git über Chocolatey:**
```powershell
choco install git
```

---

## **🧪 Methode 4: Scoop Package Manager**

### **📦 Scoop installieren (falls nicht vorhanden):**
```powershell
# PowerShell ausführen
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

### **📦 Git über Scoop:**
```powershell
scoop install git
```

---

## **🔧 Nach der Installation:**

### **📋 Git konfigurieren:**
```bash
# Benutzername setzen
git config --global user.name "Ihr Name"

# E-Mail setzen
git config --global user.email "ihre.email@example.com"

# Standard-Editor (optional)
git config --global core.editor "notepad"

# Line endings (wichtig für Windows)
git config --global core.autocrlf true
```

### **🔄 Installation testen:**
```bash
# Version prüfen
git --version

# Konfiguration anzeigen
git config --list

# Hilfe anzeigen
git help
```

---

## **🌐 Git GUI Tools (Optional):**

### **📱 Empfohlene GUIs:**
1. **GitHub Desktop** - https://desktop.github.com
2. **GitKraken** - https://www.gitkraken.com
3. **SourceTree** - https://www.sourcetreeapp.com
4. **TortoiseGit** - https://tortoisegit.org

### **📦 Installation:**
- **GitHub Desktop:** Einfachste Integration mit GitHub
- **GitKraken:** Moderne UI, viele Features
- **SourceTree:** Kostenlos, gute Visualisierung
- **TortoiseGit:** Windows Explorer Integration

---

## **🚨 Häufige Probleme & Lösungen:**

### **Problem: "git not recognized"**
```bash
# Lösung 1: PC neustarten
# Lösung 2: PATH manuell prüfen
echo %PATH%

# Lösung 3: Git neu installieren mit PATH-Option
```

### **Problem: SSL/TLS Fehler**
```bash
# Git SSL-Zertifikate aktualisieren
git config --global http.sslBackend schannel
```

### **Problem: Proxy-Einstellungen**
```bash
# Falls Proxy erforderlich
git config --global http.proxy http://proxy.company.com:8080
git config --global https.proxy https://proxy.company.com:8080
```

---

## **📋 Installation überprüfen:**

### **✅ Erfolgreiche Installation:**
```bash
# Diese Befehle sollten funktionieren:
git --version
git config --list
git help

# Ausgabe sollte sein:
git version 2.40.0.windows.1
user.name=Ihr Name
user.email=ihre.email@example.com
```

### **🔄 Test mit Projekt:**
```bash
# In Projektverzeichnis wechseln
cd W:/TomsGPXEditor

# Git initialisieren
git init
git add .
git commit -m "Test commit"
```

---

## **🎯 Empfehlung:**

### **🥇 Beste Methode für Anfänger:**
1. **Offizielle Website** - Stabilste Version
2. **GitHub Desktop** - Visuelle Bedienung
3. **VS Code Integration** - Direkt im Editor

### **🥇 Für Entwickler:**
1. **winget** - Moderne Windows Integration
2. **Git Bash** - Unix-Kommandos in Windows
3. **VS Code mit Git Extension** - Beste Integration

---

## **🚀 Nächste Schritte nach Installation:**

1. **Git konfigurieren** mit Name und E-Mail
2. **TomsGPXEditor Repository initialisieren**
3. **GIT_SETUP_GUIDE.md befolgen**
4. **Remote einrichten** (GitHub/GitLab)

---

**🎉 Nach der Installation sind Sie bereit für die Git-Arbeit!**
