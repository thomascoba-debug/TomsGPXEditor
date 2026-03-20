@echo off
REM Backup Script für TomsGPXEditor (Windows Batch)
REM Erstellt ein Backup aller wichtigen Projektdateien

echo 🗂️  TomsGPXEditor Backup Script
echo ================================

REM Projektverzeichnis (dieses Verzeichnis)
set PROJECT_DIR=%~dp0
set PROJECT_NAME=TomsGPXEditor

REM Datum für Backup-Name
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YYYY=%dt:~0,4%"
set "MM=%dt:~4,2%"
set "DD=%dt:~6,2%"
set "DATE=%YYYY%-%MM%-%DD%"

REM Backup-Verzeichnis auf gleicher Höhe wie Projekt
set BACKUP_DIR=%PROJECT_DIR..\%PROJECT_NAME%_%DATE%

REM Prüfe ob Backup-Verzeichnis schon existiert
if exist "%BACKUP_DIR%" (
    echo ⚠️  Backup-Verzeichnis existiert bereits, füge Zeitstempel hinzu
    for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
        set "HH=%%a"
        set "MI=%%b"
        set "SS=%%c"
    )
    set "TIME=%HH%-%MI%-%SS%"
    set BACKUP_DIR=%PROJECT_DIR..\%PROJECT_NAME%_%DATE%_%TIME%
)

echo 📂 Projektverzeichnis: %PROJECT_DIR%
echo 📛 Projektname: %PROJECT_NAME%
echo 📁 Zielverzeichnis: %BACKUP_DIR%
echo.

REM Erstelle Backup-Verzeichnis
mkdir "%BACKUP_DIR%" 2>nul
if errorlevel 1 (
    echo ❌ Fehler: Konnte Backup-Verzeichnis nicht erstellen
    pause
    exit /b 1
)

echo 🔄 Starte Backup...
echo.

REM Zähler
set FILES_COUNT=0
set DIRS_COUNT=0
set SKIPPED_COUNT=0

REM Verzeichnisse kopieren (ohne ausgeschlossene)
echo 📁 Kopiere Verzeichnisse...
for /d %%d in (*) do (
    REM Überspringe ausgeschlossene Verzeichnisse
    echo.%%d | findstr /i "__pycache__" >nul
    if not errorlevel 1 (
        echo ⏭️  Überspringe Verzeichnis: %%d
        set /a SKIPPED_COUNT+=1
    ) else (
        echo.%%d | findstr /i ".git" >nul
        if not errorlevel 1 (
            echo ⏭️  Überspringe Verzeichnis: %%d
            set /a SKIPPED_COUNT+=1
        ) else (
            echo.%%d | findstr /i ".vscode" >nul
            if not errorlevel 1 (
                echo ⏭️  Überspringe Verzeichnis: %%d
                set /a SKIPPED_COUNT+=1
            ) else (
                echo.%%d | findstr /i "venv" >nul
                if not errorlevel 1 (
                    echo ⏭️  Überspringe Verzeichnis: %%d
                    set /a SKIPPED_COUNT+=1
                ) else (
                    echo ✅ Kopiere Verzeichnis: %%d
                    xcopy "%%d" "%BACKUP_DIR%\%%d" /E /I /Q /H >nul 2>&1
                    if not errorlevel 1 (
                        set /a DIRS_COUNT+=1
                    )
                )
            )
        )
    )
)

REM Dateien kopieren
echo.
echo 📄 Kopiere Dateien...
for %%f in (*.py *.md *.txt *.json *.yml *.yaml *.gitignore *.requirements.txt) do (
    echo ✅ Kopiere Datei: %%f
    copy "%%f" "%BACKUP_DIR%\" >nul 2>&1
    if not errorlevel 1 (
        set /a FILES_COUNT+=1
    )
)

REM Erstelle Info-Datei
echo.
echo 📝 Erstelle Backup-Info...
echo BACKUP INFORMATION > "%BACKUP_DIR%\backup_info.txt"
echo ================== >> "%BACKUP_DIR%\backup_info.txt"
echo. >> "%BACKUP_DIR%\backup_info.txt"
echo Projekt: %PROJECT_NAME% >> "%BACKUP_DIR%\backup_info.txt"
echo Datum: %DATE% %TIME% >> "%BACKUP_DIR%\backup_info.txt"
echo Quellverzeichnis: %PROJECT_DIR% >> "%BACKUP_DIR%\backup_info.txt"
echo Zielverzeichnis: %BACKUP_DIR% >> "%BACKUP_DIR%\backup_info.txt"
echo. >> "%BACKUP_DIR%\backup_info.txt"
echo STATISTIK: >> "%BACKUP_DIR%\backup_info.txt"
echo --------- >> "%BACKUP_DIR%\backup_info.txt"
echo Dateien gesichert: %FILES_COUNT% >> "%BACKUP_DIR%\backup_info.txt"
echo Verzeichnisse erstellt: %DIRS_COUNT% >> "%BACKUP_DIR%\backup_info.txt"
echo. >> "%BACKUP_DIR%\backup_info.txt"
echo AUSSCHLÜSSE: >> "%BACKUP_DIR%\backup_info.txt"
echo ----------- >> "%BACKUP_DIR%\backup_info.txt"
echo - __pycache__ Verzeichnisse >> "%BACKUP_DIR%\backup_info.txt"
echo - .git Verzeichnisse >> "%BACKUP_DIR%\backup_info.txt"
echo - .vscode Verzeichnisse >> "%BACKUP_DIR%\backup_info.txt"
echo - venv Verzeichnisse >> "%BACKUP_DIR%\backup_info.txt"
echo - *.pyc Dateien >> "%BACKUP_DIR%\backup_info.txt"
echo - *.log Dateien >> "%BACKUP_DIR%\backup_info.txt"
echo - properties.json (benutzer-spezifisch) >> "%BACKUP_DIR%\backup_info.txt"

echo.
echo ================================
echo ✅ Backup erfolgreich abgeschlossen!
echo 📁 Backup-Verzeichnis: %BACKUP_DIR%
echo 📊 %FILES_COUNT% Dateien gesichert
echo 📁 %DIRS_COUNT% Verzeichnisse erstellt
echo.
pause
