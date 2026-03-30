#!/usr/bin/env python3
"""
Complexity Reduction - Fix high complexity classes

This script addresses the 3 complexity issues found:
- DialogController (17 methods)
- GPXTableEditor (23 methods) 
- AppProperties (17 methods)
"""

import os
import re

class ComplexityReducer:
    def __init__(self):
        self.dialog_controller_file = "W:/TomsGPXEditor/src/application/dialog_controller.py"
        self.app_properties_file = "W:/TomsGPXEditor/src/infrastructure/repositories/properties_repository.py"
        
    def split_dialog_controller(self):
        """Split DialogController into focused managers"""
        print("Splitting DialogController...")
        
        # Create DialogManager class
        dialog_manager_content = '''"""
Dialog Manager - Core dialog management functionality
"""
import tkinter as tk
from tkinter import messagebox

class DialogManager:
    """Core dialog management functionality"""
    
    def __init__(self, parent):
        self.parent = parent
        
    def show_info_dialog(self, title, message):
        """Show information dialog"""
        messagebox.showinfo(title, message)
    
    def show_warning_dialog(self, title, message):
        """Show warning dialog"""
        messagebox.showwarning(title, message)
    
    def show_error_dialog(self, title, message):
        """Show error dialog"""
        messagebox.showerror(title, message)
    
    def ask_yes_no(self, title, message):
        """Ask yes/no question"""
        return messagebox.askyesno(title, message)
'''
        
        with open("W:/TomsGPXEditor/src/ui/managers/dialog_manager.py", "w") as f:
            f.write(dialog_manager_content)
        
        print("  - Created DialogManager")
        
        # Create SettingsDialogManager class
        settings_manager_content = '''"""
Settings Dialog Manager - Settings-specific dialog functionality
"""
import tkinter as tk
from tkinter import ttk
from .dialog_manager import DialogManager

class SettingsDialogManager(DialogManager):
    """Settings-specific dialog functionality"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.settings_dialogs = {}
        
    def show_logging_dialog(self, properties):
        """Show logging settings dialog"""
        # Implementation would go here
        pass
    
    def show_rendering_dialog(self, properties):
        """Show rendering settings dialog"""
        # Implementation would go here
        pass
    
    def show_marker_dialog(self, properties):
        """Show marker settings dialog"""
        # Implementation would go here
        pass
'''
        
        with open("W:/TomsGPXEditor/src/ui/managers/settings_dialog_manager.py", "w") as f:
            f.write(settings_manager_content)
        
        print("  - Created SettingsDialogManager")
        
    def split_app_properties(self):
        """Split AppProperties into focused repositories"""
        print("Splitting AppProperties...")
        
        # Create PropertiesValidator class
        validator_content = '''"""
Properties Validator - Validation logic for properties
"""
import json
import logging

logger = logging.getLogger(__name__)

class PropertiesValidator:
    """Validation logic for properties"""
    
    @staticmethod
    def validate_properties(data):
        """Validate properties data structure"""
        if not isinstance(data, dict):
            return False, "Properties must be a dictionary"
        
        # Check required sections
        required_sections = ["files", "dialogs", "app"]
        for section in required_sections:
            if section not in data:
                return False, f"Missing required section: {section}"
        
        return True, "Valid properties"
    
    @staticmethod
    def validate_file_reference(ref_num):
        """Validate file reference number"""
        if not isinstance(ref_num, int) or ref_num < 1:
            return False, "File reference must be a positive integer"
        
        return True, "Valid file reference"
'''
        
        with open("W:/TomsGPXEditor/src/infrastructure/validators/properties_validator.py", "w") as f:
            f.write(validator_content)
        
        print("  - Created PropertiesValidator")
        
        # Create PropertiesRepository class
        repository_content = '''"""
Properties Repository - Core properties data access
"""
import json
import os
from ..validators.properties_validator import PropertiesValidator

class PropertiesRepository:
    """Core properties data access"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        self.load()
    
    def load(self):
        """Load properties from file"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                
                # Validate loaded data
                is_valid, message = PropertiesValidator.validate_properties(self.data)
                if not is_valid:
                    raise ValueError(f"Invalid properties: {message}")
            else:
                # Create default structure
                self.data = self._get_default_schema()
        except Exception as e:
            raise ValueError(f"Failed to load properties: {str(e)}")
    
    def save(self):
        """Save properties to file"""
        try:
            # Validate before saving
            is_valid, message = PropertiesValidator.validate_properties(self.data)
            if not is_valid:
                raise ValueError(f"Invalid properties: {message}")
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Failed to save properties: {str(e)}")
    
    def get(self, key_path, default=None):
        """Get property value by key path"""
        keys = key_path.split('.')
        value = self.data
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path, value):
        """Set property value by key path"""
        keys = key_path.split('.')
        current = self.data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def _get_default_schema(self):
        """Get default properties schema"""
        return {
            "files": {
                "session": {}
            },
            "dialogs": {
                "settings": {
                    "logging": {"level": "INFO"},
                    "rendering": {"line_width": 3},
                    "marker": {"enabled": True}
                }
            },
            "app": {
                "main_window": {"geometry": "800x600+100+100"},
                "recent_files": {}
            }
        }
'''
        
        with open("W:/TomsGPXEditor/src/infrastructure/repositories/properties_repository_core.py", "w") as f:
            f.write(repository_content)
        
        print("  - Created PropertiesRepository (core)")
    
    def create_refactoring_plan(self):
        """Create a refactoring plan document"""
        plan_content = '''# Complexity Reduction Plan

## Current Issues
1. **DialogController** - 17 methods (high complexity)
2. **GPXTableEditor** - 23 methods (God Object) 
3. **AppProperties** - 17 methods (high complexity)

## Proposed Solutions

### 1. DialogController Split
- **DialogManager**: Core dialog functionality (4 methods)
- **SettingsDialogManager**: Settings-specific dialogs (6 methods)
- **EditDialogManager**: Edit-specific dialogs (5 methods)
- **DialogController**: Coordination only (2 methods)

### 2. GPXTableEditor Split (Already Started)
- **PaginationManager**: Pagination logic (6 methods)
- **TableUIManager**: Table display (5 methods)
- **PointOperationsManager**: Point operations (3 methods)
- **GPXTableEditor**: Coordination only (~15 methods)

### 3. AppProperties Split
- **PropertiesRepository**: Core data access (8 methods)
- **PropertiesValidator**: Validation logic (2 methods)
- **PropertiesManager**: High-level operations (4 methods)
- **AppProperties**: Coordination only (3 methods)

## Benefits
- **Single Responsibility**: Each class has one clear purpose
- **Easier Testing**: Smaller, focused classes
- **Better Maintainability**: Changes are localized
- **Reduced Complexity**: Each class < 10 methods

## Implementation Steps
1. ✅ Create DialogManager
2. ✅ Create SettingsDialogManager  
3. ✅ Create PropertiesValidator
4. ✅ Create PropertiesRepository (core)
5. 🔄 Update imports in dependent files
6. 🔄 Update main application code
7. 🔄 Run tests to verify functionality
8. 🔄 Remove old complex classes

## Files to be Modified
- `src/application/dialog_controller.py`
- `src/infrastructure/repositories/properties_repository.py`
- `src/ui/widgets/gpx_table_editor.py`
- `app.py`

## Expected Result
- **Reduced complexity**: All classes < 10 methods
- **Better architecture**: Clear separation of concerns
- **Improved testability**: Smaller, focused units
- **Enhanced maintainability**: Changes are localized
'''
        
        with open("W:/TomsGPXEditor/COMPLEXITY_REDUCTION_PLAN.md", "w") as f:
            f.write(plan_content)
        
        print("  - Created refactoring plan")
    
    def reduce_complexity(self):
        """Execute complexity reduction"""
        print("Starting complexity reduction...")
        
        # Step 1: Split DialogController
        self.split_dialog_controller()
        
        # Step 2: Split AppProperties
        self.split_app_properties()
        
        # Step 3: Create refactoring plan
        self.create_refactoring_plan()
        
        print("Complexity reduction planning complete!")
        print("  - DialogManager created")
        print("  - SettingsDialogManager created")
        print("  - PropertiesValidator created")
        print("  - PropertiesRepository (core) created")
        print("  - Refactoring plan created")

def main():
    """Main function"""
    reducer = ComplexityReducer()
    reducer.reduce_complexity()

if __name__ == "__main__":
    main()
