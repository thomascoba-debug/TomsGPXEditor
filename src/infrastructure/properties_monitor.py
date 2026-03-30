#!/usr/bin/env python3
"""
Properties Monitor - Checks properties.json at startup and shutdown
Shows error messages when issues are found
"""

import json
import logging
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from src.infrastructure.properties_validator import PropertiesValidator

logger = logging.getLogger(__name__)

class PropertiesMonitor:
    """Monitors properties.json and shows error messages"""
    
    @staticmethod
    def check_and_show_errors(parent_window=None, context="startup"):
        """
        Check properties and show error message if issues found
        
        Args:
            parent_window: Parent window for messagebox (optional)
            context: "startup" or "shutdown" for logging
            
        Returns:
            bool: True if issues were found and fixed
        """
        try:
            # Load current properties
            with open("properties.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Validate and clean
            cleaned_data, was_changed = PropertiesValidator.validate_and_clean(data)
            
            if was_changed:
                # Create backup
                backup_name = f"properties.json.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                with open(backup_name, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Save cleaned version
                with open("properties.json", "w", encoding="utf-8") as f:
                    json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
                
                # Log the fix
                logger.warning(f"Properties auto-cleaned at {context}, backup: {backup_name}")
                
                # Show error message to user
                error_title = "Properties.json Issues Fixed"
                error_message = f"Duplicate entries were found and automatically fixed in properties.json\n\n"
                error_message += f"Backup saved as: {backup_name}\n\n"
                error_message += f"The following issues were resolved:\n"
                
                # Check what was fixed
                issues_found = []
                
                # Check for recent_files duplicates
                app_data = data.get('app', {})
                if 'recent_files' in app_data and 'recent_files_timestamps' in app_data:
                    issues_found.append("• Duplicate recent_files entries")
                
                # Check for conversion duplicates
                if 'conversion' in data and 'dialogs' in data and 'settings' in data.get('dialogs', {}) and 'conversion' in data.get('dialogs', {}).get('settings', {}):
                    issues_found.append("• Duplicate conversion settings")
                
                # Check for ROOT entries
                if 'ROOT' in data:
                    issues_found.append("• Invalid ROOT entries")
                
                if issues_found:
                    error_message += "\n".join(issues_found)
                else:
                    error_message += "• Unknown structural issues"
                
                error_message += f"\n\nThe application will continue with the cleaned properties."
                
                # Show messagebox (with or without parent)
                if parent_window:
                    messagebox.showwarning(error_title, error_message, parent=parent_window)
                else:
                    # Create temporary root for messagebox if no parent available
                    temp_root = tk.Tk()
                    temp_root.withdraw()  # Hide the main window
                    messagebox.showwarning(error_title, error_message)
                    temp_root.destroy()
                
                return True
            else:
                logger.debug(f"Properties check at {context}: No issues found")
                return False
                
        except FileNotFoundError:
            # No properties file exists - that's OK for first run
            logger.info(f"No properties.json found at {context} - will be created")
            return False
            
        except Exception as e:
            # Serious error - show critical message
            error_title = "Properties.json Error"
            error_message = f"Critical error checking properties.json:\n\n{str(e)}\n\n"
            error_message += "Please check the log file for details."
            
            logger.error(f"Properties check failed at {context}: {e}")
            
            if parent_window:
                messagebox.showerror(error_title, error_message, parent=parent_window)
            else:
                temp_root = tk.Tk()
                temp_root.withdraw()
                messagebox.showerror(error_title, error_message)
                temp_root.destroy()
            
            return True
    
    @staticmethod
    def startup_check(parent_window=None):
        """Check properties at application startup"""
        logger.info("Performing properties startup check...")
        return PropertiesMonitor.check_and_show_errors(parent_window, "startup")
    
    @staticmethod
    def shutdown_check(parent_window=None):
        """Check properties at application shutdown"""
        logger.info("Performing properties shutdown check...")
        return PropertiesMonitor.check_and_show_errors(parent_window, "shutdown")
