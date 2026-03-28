@echo off
echo Restoring clean snapshot: clean_snapshot_20260327_143052
echo ========================================
cd /d "%~dp0\..\.."
python "archive/clean_snapshot_20260327_143052\restore.py"
pause
