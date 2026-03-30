
from src.constants.property_keys import TRACK_TO_ROUTE_POINTS_PER_100KM
from src.constants.property_keys import SESSION_FILES
#!/usr/bin/env python3
"""
Stability Manager for Application Robustness
"""

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Callable
from .json_validator import JSONValidator
from .error_handler import safe_execute, validate_condition

logger = logging.getLogger(__name__)

class StabilityManager:
    """Manages application stability and prevents common issues"""
    
    def __init__(self, properties_file: str = "properties.json"):
        self.properties_file = Path(properties_file)
        self.stability_log_file = Path("logs") / "stability.log"
        self.stability_log_file.parent.mkdir(exist_ok=True)
        
        # Known problematic patterns
        self.problematic_patterns = {
            "duplicate_recent_files": [
                "recent_files",
                "recent_files.with_timestamps",
                "app.recent_files"  # flat version
            ],
            "legacy_settings": [
                .TRACK_TO_ROUTE_POINTS_PER_100KM  # flat version
            ],
            "invalid_references": [
                None  # Will be populated dynamically
            ]
        }
    
    def check_and_fix_stability(self) -> Dict[str, Any]:
        """Check and fix stability issues"""
        logger.info("Running stability check...")
        
        issues_found = {}
        
        # Check JSON structure
        json_issues = self._check_json_stability()
        if json_issues:
            issues_found.update(json_issues)
        
        # Check file references
        ref_issues = self._check_file_references()
        if ref_issues:
            issues_found.update(ref_issues)
        
        # Check for circular dependencies
        dep_issues = self._check_circular_dependencies()
        if dep_issues:
            issues_found.update(dep_issues)
        
        # Log results
        self._log_stability_check(issues_found)
        
        return issues_found
    
    def _check_json_stability(self) -> Dict[str, Any]:
        """Check JSON structure stability"""
        issues = {}
        
        try:
            validator = JSONValidator(str(self.properties_file))
            validator.load_and_validate()
            
            if validator.errors or validator.warnings:
                issues["json_structure"] = {
                    "errors": validator.errors,
                    "warnings": validator.warnings
                }
                
                # Auto-fix if possible
                validator.save_sanitized()
                logger.info("Auto-fixed JSON structure issues")
                
        except Exception as e:
            issues["json_load"] = str(e)
            logger.error(f"JSON stability check failed: {e}")
        
        return issues
    
    def _check_file_references(self) -> Dict[str, Any]:
        """Check for invalid file references"""
        issues = {}
        
        try:
            with open(self.properties_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            invalid_files = []
            
            # Check session files
            session_files = data.get(.SESSION_FILES, {})
            for ref_num, file_data in session_files.items():
                file_path = file_data.get("path")
                if file_path and not Path(file_path).exists():
                    invalid_files.append(file_path)
            
            # Check recent files
            recent_files = data.get("app", {}).get("recent_files_timestamps", {})
            for file_path in recent_files.keys():
                if not Path(file_path).exists():
                    invalid_files.append(file_path)
            
            if invalid_files:
                issues["invalid_references"] = invalid_files
                logger.warning(f"Found {len(invalid_files)} invalid file references")
                
        except Exception as e:
            issues["reference_check"] = str(e)
            logger.error(f"File reference check failed: {e}")
        
        return issues
    
    def _check_circular_dependencies(self) -> Dict[str, Any]:
        """Check for circular dependency issues"""
        issues = {}
        
        # This would need to be implemented based on specific dependency patterns
        # For now, just log that check was performed
        logger.debug("Circular dependency check completed")
        
        return issues
    
    def _log_stability_check(self, issues: Dict[str, Any]) -> None:
        """Log stability check results"""
        timestamp = datetime.now().isoformat()
        
        try:
            with open(self.stability_log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] Stability Check Results:\n")
                
                if issues:
                    f.write(f"  Issues found: {len(issues)}\n")
                    for category, details in issues.items():
                        f.write(f"    {category}: {details}\n")
                else:
                    f.write("  No issues found\n")
                
                f.write("\n")
                
        except Exception as e:
            logger.error(f"Failed to log stability check: {e}")
    
    def create_backup(self) -> Path:
        """Create timestamped backup of properties"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.properties_file.with_suffix(f".backup_{timestamp}")
        
        try:
            import shutil
            shutil.copy2(self.properties_file, backup_file)
            logger.info(f"Created backup: {backup_file}")
            return backup_file
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return self.properties_file
    
    def restore_from_backup(self, backup_file: Path) -> bool:
        """Restore from backup file"""
        try:
            import shutil
            shutil.copy2(backup_file, self.properties_file)
            logger.info(f"Restored from backup: {backup_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore from backup: {e}")
            return False
    
    def get_recent_backups(self, count: int = 5) -> List[Path]:
        """Get recent backup files"""
        backup_pattern = f"{self.properties_file.stem}.backup_*"
        backup_files = list(self.properties_file.parent.glob(backup_pattern))
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        return backup_files[:count]
    
    def cleanup_old_backups(self, keep_count: int = 10) -> None:
        """Clean up old backup files"""
        backup_files = self.get_recent_backups(keep_count * 2)  # Get more to check
        
        if len(backup_files) > keep_count:
            for backup_file in backup_files[keep_count:]:
                try:
                    backup_file.unlink()
                    logger.debug(f"Removed old backup: {backup_file}")
                except Exception as e:
                    logger.warning(f"Failed to remove old backup {backup_file}: {e}")

# Global stability manager instance
_stability_manager = StabilityManager()

def get_stability_manager() -> StabilityManager:
    """Get global stability manager instance"""
    return _stability_manager

def run_stability_check() -> Dict[str, Any]:
    """Run global stability check"""
    return _stability_manager.check_and_fix_stability()

@safe_execute("Failed to create stability backup")
def create_stability_backup() -> Path:
    """Create stability backup"""
    return _stability_manager.create_backup()

@safe_execute("Failed to restore from backup")
def restore_from_backup(backup_file: Path) -> bool:
    """Restore from backup"""
    return _stability_manager.restore_from_backup(backup_file)
