#!/usr/bin/env python3
"""
Dead Code Analysis and Cleanup

This script identifies and removes truly unused functions and classes.
It focuses on the 199 dead code issues found in the anomaly analysis.
"""

import os
import ast
import json

class DeadCodeCleaner:
    def __init__(self):
        self.source_dir = "W:/TomsGPXEditor/src"
        self.used_functions = set()
        self.used_classes = set()
        self.all_functions = {}
        self.all_classes = {}
        
    def analyze_usage(self):
        """Analyze which functions and classes are actually used"""
        print("Analyzing function and class usage...")
        
        # Walk through all Python files
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self._analyze_file_usage(file_path)
    
    def _analyze_file_usage(self, file_path):
        """Analyze usage in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Find all function calls
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        self.used_functions.add(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        self.used_functions.add(node.func.attr)
                
                # Find all class instantiations
                elif isinstance(node, ast.ClassDef):
                    pass  # Classes are defined here
                
                # Find all imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        self.used_classes.add(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        if alias.name:
                            self.used_classes.add(alias.name)
                            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    def collect_all_definitions(self):
        """Collect all function and class definitions"""
        print("Collecting all function and class definitions...")
        
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self._collect_definitions(file_path)
    
    def _collect_definitions(self, file_path):
        """Collect definitions from a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Skip special methods and test functions
                    if not node.name.startswith('_') and not node.name.startswith('test'):
                        self.all_functions[node.name] = file_path
                
                elif isinstance(node, ast.ClassDef):
                    self.all_classes[node.name] = file_path
                    
        except Exception as e:
            print(f"Error collecting definitions from {file_path}: {e}")
    
    def identify_unused_code(self):
        """Identify truly unused functions and classes"""
        print("Identifying unused code...")
        
        unused_functions = []
        unused_classes = []
        
        # Find unused functions
        for func_name, file_path in self.all_functions.items():
            if func_name not in self.used_functions:
                # Additional check: some functions might be called indirectly
                if not self._is_likely_used_indirectly(func_name, file_path):
                    unused_functions.append({
                        'name': func_name,
                        'file': file_path,
                        'type': 'function'
                    })
        
        # Find unused classes
        for class_name, file_path in self.all_classes.items():
            if class_name not in self.used_classes:
                # Skip certain classes that are likely used indirectly
                if not self._is_likely_used_indirectly(class_name, file_path):
                    unused_classes.append({
                        'name': class_name,
                        'file': file_path,
                        'type': 'class'
                    })
        
        return unused_functions, unused_classes
    
    def _is_likely_used_indirectly(self, name, file_path):
        """Check if a function/class is likely used indirectly"""
        # Skip common patterns that are likely used indirectly
        indirect_patterns = [
            'main', 'setup', 'init', 'create', 'get', 'set',
            'update', 'delete', 'add', 'remove', 'load', 'save'
        ]
        
        # Skip if name suggests it's a utility function
        if any(pattern in name.lower() for pattern in indirect_patterns):
            return True
        
        # Skip if it's in a file that's likely a utility module
        if 'utils' in file_path.lower() or 'helper' in file_path.lower():
            return True
        
        return False
    
    def generate_cleanup_report(self, unused_functions, unused_classes):
        """Generate a cleanup report"""
        report = {
            'metadata': {
                'total_unused_functions': len(unused_functions),
                'total_unused_classes': len(unused_classes),
                'analysis_date': '2026-03-29'
            },
            'unused_functions': unused_functions,
            'unused_classes': unused_classes,
            'recommendations': []
        }
        
        # Add recommendations
        if len(unused_functions) > 0:
            report['recommendations'].append({
                'type': 'functions',
                'count': len(unused_functions),
                'action': 'Review and remove truly unused functions'
            })
        
        if len(unused_classes) > 0:
            report['recommendations'].append({
                'type': 'classes',
                'count': len(unused_classes),
                'action': 'Review and remove truly unused classes'
            })
        
        # Save report
        with open('W:/TomsGPXEditor/DEAD_CODE_ANALYSIS.json', 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def create_safe_cleanup_script(self, unused_functions, unused_classes):
        """Create a safe cleanup script"""
        script_content = '''#!/usr/bin/env python3
"""
Safe Dead Code Cleanup Script

This script removes identified unused functions and classes.
REVIEW THE CHANGES BEFORE APPLYING!
"""

import os
import shutil

def backup_file(file_path):
    """Create backup of file before modification"""
    backup_path = file_path + '.dead_code_backup'
    shutil.copy2(file_path, backup_path)
    print(f"Backed up: {backup_path}")

def remove_unused_function(file_path, function_name):
    """Remove a specific function from a file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find and remove the function
    lines = content.split('\\n')
    in_function = False
    function_indent = 0
    start_line = -1
    end_line = -1
    
    for i, line in enumerate(lines):
        if f'def {function_name}(' in line:
            start_line = i
            in_function = True
            function_indent = len(line) - len(line.lstrip())
        elif in_function:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= function_indent:
                end_line = i - 1
                break
    
    if start_line >= 0:
        # Remove the function
        new_lines = lines[:start_line] + lines[end_line + 1:]
        with open(file_path, 'w') as f:
            f.write('\\n'.join(new_lines))
        print(f"Removed function {function_name} from {os.path.basename(file_path)}")
        return True
    
    return False

def remove_unused_class(file_path, class_name):
    """Remove a specific class from a file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find and remove the class
    lines = content.split('\\n')
    in_class = False
    class_indent = 0
    start_line = -1
    end_line = -1
    
    for i, line in enumerate(lines):
        if f'class {class_name}' in line:
            start_line = i
            in_class = True
            class_indent = len(line) - len(line.lstrip())
        elif in_class:
            current_indent = len(line) - len(line.lstrip())
            if line.strip() and current_indent <= class_indent:
                end_line = i - 1
                break
    
    if start_line >= 0:
        # Remove the class
        new_lines = lines[:start_line] + lines[end_line + 1:]
        with open(file_path, 'w') as f:
            f.write('\\n'.join(new_lines))
        print(f"Removed class {class_name} from {os.path.basename(file_path)}")
        return True
    
    return False

def main():
    """Main cleanup function"""
    print("Starting safe dead code cleanup...")
    
    # Unused functions to remove (REVIEW THESE!)
    unused_functions = ''' + str(unused_functions) + '''
    
    # Unused classes to remove (REVIEW THESE!)
    unused_classes = ''' + str(unused_classes) + '''
    
    print("WARNING: This will remove unused code. Review the lists above carefully!")
    print("Press Ctrl+C to cancel, or press Enter to continue...")
    input()
    
    # Remove unused functions
    for func in unused_functions:
        if os.path.exists(func['file']):
            backup_file(func['file'])
            remove_unused_function(func['file'], func['name'])
    
    # Remove unused classes
    for cls in unused_classes:
        if os.path.exists(cls['file']):
            backup_file(cls['file'])
            remove_unused_class(cls['file'], cls['name'])
    
    print("Dead code cleanup complete!")

if __name__ == "__main__":
    main()
'''
        
        with open('W:/TomsGPXEditor/cleanup_dead_code.py', 'w') as f:
            f.write(script_content)
        
        print("Created safe cleanup script: cleanup_dead_code.py")
    
    def analyze_and_report(self):
        """Complete analysis and reporting"""
        print("Starting dead code analysis...")
        
        # Step 1: Analyze usage
        self.analyze_usage()
        
        # Step 2: Collect all definitions
        self.collect_all_definitions()
        
        # Step 3: Identify unused code
        unused_functions, unused_classes = self.identify_unused_code()
        
        # Step 4: Generate report
        report = self.generate_cleanup_report(unused_functions, unused_classes)
        
        # Step 5: Create cleanup script
        self.create_safe_cleanup_script(unused_functions, unused_classes)
        
        print(f"Dead code analysis complete!")
        print(f"  - Total functions analyzed: {len(self.all_functions)}")
        print(f"  - Total classes analyzed: {len(self.all_classes)}")
        print(f"  - Unused functions found: {len(unused_functions)}")
        print(f"  - Unused classes found: {len(unused_classes)}")
        print(f"  - Report saved: DEAD_CODE_ANALYSIS.json")
        print(f"  - Cleanup script: cleanup_dead_code.py")

def main():
    """Main function"""
    cleaner = DeadCodeCleaner()
    cleaner.analyze_and_report()

if __name__ == "__main__":
    main()
