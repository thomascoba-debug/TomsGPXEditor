@echo off
echo Restoring clean snapshot: clean_snapshot_20260327_131930
echo ========================================
cd /d "%~dp0\..\.."
python "archive/clean_snapshot_20260327_131930\restore.py"
pause
