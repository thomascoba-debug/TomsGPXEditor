@echo off
echo Restoring clean snapshot: clean_snapshot_20260327_132210
echo ========================================
cd /d "%~dp0\..\.."
python "archive/clean_snapshot_20260327_132210\restore.py"
pause
