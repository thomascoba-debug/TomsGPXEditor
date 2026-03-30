"""
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
