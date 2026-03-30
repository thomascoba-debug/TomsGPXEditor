#!/usr/bin/env python3
"""
Cross-Reference Database Generator for TomsGPXEditor

Generates a comprehensive cross-reference database of all components,
methods, classes, and their relationships in the codebase.
"""

import os
import json
import re
import ast
from pathlib import Path
from typing import Dict, List, Set, Any
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class ClassInfo:
    name: str
    file_path: str
    methods: List[str]
    properties: List[str]
    base_classes: List[str]
    imports: List[str]
    line_number: int
    docstring: str = ""

@dataclass
class FunctionInfo:
    name: str
    file_path: str
    parameters: List[str]
    return_type: str
    line_number: int
    docstring: str = ""
    decorators: List[str] = None
    
    def __post_init__(self):
        if self.decorators is None:
            self.decorators = []

@dataclass
class ImportInfo:
    module: str
    alias: str
    file_path: str
    line_number: int
    is_from_import: bool
    imported_items: List[str] = None
    
    def __post_init__(self):
        if self.imported_items is None:
            self.imported_items = []

@dataclass
class PropertyInfo:
    name: str
    file_path: str
    type_hint: str
    default_value: str
    line_number: int
    is_class_property: bool

@dataclass
class CallInfo:
    caller_function: str
    caller_file: str
    called_function: str
    called_file: str
    line_number: int

class CrossReferenceDatabase:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.classes: Dict[str, ClassInfo] = {}
        self.functions: Dict[str, FunctionInfo] = {}
        self.imports: Dict[str, List[ImportInfo]] = defaultdict(list)
        self.properties: Dict[str, PropertyInfo] = {}
        self.calls: List[CallInfo] = []
        self.file_structure: Dict[str, List[str]] = defaultdict(list)
        
    def analyze_codebase(self):
        """Analyze the entire codebase and build cross-reference database"""
        print("Analyzing codebase...")
        
        # Find all Python files
        python_files = list(self.root_path.rglob("*.py"))
        print(f"Found {len(python_files)} Python files")
        
        for file_path in python_files:
            if "__pycache__" in str(file_path):
                continue
                
            try:
                self._analyze_file(file_path)
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
        
        print(f"Analysis complete:")
        print(f"   Classes: {len(self.classes)}")
        print(f"   Functions: {len(self.functions)}")
        print(f"   Imports: {sum(len(imports) for imports in self.imports.values())}")
        print(f"   Properties: {len(self.properties)}")
        print(f"   Calls: {len(self.calls)}")
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Track file structure
            self.file_structure[str(file_path)] = []
            
            # Analyze imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    self._analyze_import(node, file_path)
                elif isinstance(node, ast.ImportFrom):
                    self._analyze_import_from(node, file_path)
            
            # Analyze classes and functions
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self._analyze_class(node, file_path, content)
                elif isinstance(node, ast.FunctionDef):
                    self._analyze_function(node, file_path, content)
            
            # Analyze function calls
            self._analyze_calls(tree, file_path)
            
        except Exception as e:
            print(f"⚠️  Could not analyze {file_path}: {e}")
    
    def _analyze_import(self, node: ast.Import, file_path: Path):
        """Analyze regular import statements"""
        for alias in node.names:
            import_info = ImportInfo(
                module=alias.name,
                alias=alias.asname or alias.name,
                file_path=str(file_path),
                line_number=node.lineno,
                is_from_import=False
            )
            self.imports[str(file_path)].append(import_info)
    
    def _analyze_import_from(self, node: ast.ImportFrom, file_path: Path):
        """Analyze from...import statements"""
        module = node.module or ""
        for alias in node.names:
            import_info = ImportInfo(
                module=module,
                alias=alias.asname or alias.name,
                file_path=str(file_path),
                line_number=node.lineno,
                is_from_import=True,
                imported_items=[alias.name for alias in node.names]
            )
            self.imports[str(file_path)].append(import_info)
    
    def _analyze_class(self, node: ast.ClassDef, file_path: Path, content: str):
        """Analyze class definitions"""
        methods = []
        properties = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        properties.append(target.id)
        
        # Get base classes
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_classes.append(f"{base.value.id}.{base.attr}")
        
        # Get docstring
        docstring = ast.get_docstring(node) or ""
        
        class_info = ClassInfo(
            name=node.name,
            file_path=str(file_path),
            methods=methods,
            properties=properties,
            base_classes=base_classes,
            imports=[],
            line_number=node.lineno,
            docstring=docstring
        )
        
        self.classes[node.name] = class_info
        self.file_structure[str(file_path)].append(f"CLASS: {node.name}")
    
    def _analyze_function(self, node: ast.FunctionDef, file_path: Path, content: str):
        """Analyze function definitions"""
        # Get parameters
        parameters = []
        for arg in node.args.args:
            parameters.append(arg.arg)
        
        # Get return type
        return_type = ""
        if node.returns:
            return_type = ast.unparse(node.returns) if hasattr(ast, 'unparse') else str(node.returns)
        
        # Get decorators
        decorators = []
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
            elif isinstance(decorator, ast.Attribute):
                decorators.append(f"{decorator.value.id}.{decorator.attr}")
        
        # Get docstring
        docstring = ast.get_docstring(node) or ""
        
        function_info = FunctionInfo(
            name=node.name,
            file_path=str(file_path),
            parameters=parameters,
            return_type=return_type,
            line_number=node.lineno,
            docstring=docstring,
            decorators=decorators
        )
        
        key = f"{node.name}_{file_path.stem}"
        self.functions[key] = function_info
        self.file_structure[str(file_path)].append(f"FUNCTION: {node.name}")
    
    def _analyze_calls(self, tree: ast.AST, file_path: Path):
        """Analyze function calls"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    # Method call: obj.method()
                    if isinstance(node.func.value, ast.Name):
                        caller = node.func.value.id
                        called = node.func.attr
                        self.calls.append(CallInfo(
                            caller_function=caller,
                            caller_file=str(file_path),
                            called_function=called,
                            called_file="unknown",  # Would need more complex analysis
                            line_number=node.lineno
                        ))
                elif isinstance(node.func, ast.Name):
                    # Function call: function()
                    called = node.func.id
                    self.calls.append(CallInfo(
                        caller_function="unknown",
                        caller_file=str(file_path),
                        called_function=called,
                        called_file="unknown",
                        line_number=node.lineno
                    ))
    
    def generate_cross_reference_report(self) -> Dict[str, Any]:
        """Generate comprehensive cross-reference report"""
        report = {
            "metadata": {
                "generated_at": "2026-03-28",
                "total_files": len(self.file_structure),
                "total_classes": len(self.classes),
                "total_functions": len(self.functions),
                "total_imports": sum(len(imports) for imports in self.imports.values()),
                "total_calls": len(self.calls)
            },
            "classes": {name: asdict(info) for name, info in self.classes.items()},
            "functions": {name: asdict(info) for name, info in self.functions.items()},
            "imports": {file_path: [asdict(imp) for imp in imports] 
                      for file_path, imports in self.imports.items()},
            "calls": [asdict(call) for call in self.calls],
            "file_structure": dict(self.file_structure),
            "relationships": self._convert_to_regular_dict(self._analyze_relationships())
        }
        
        return report
    
    def _convert_to_regular_dict(self, obj):
        """Convert defaultdict and other non-serializable objects to regular dict"""
        if isinstance(obj, defaultdict):
            return {k: self._convert_to_regular_dict(v) for k, v in obj.items()}
        elif isinstance(obj, dict):
            return {k: self._convert_to_regular_dict(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_regular_dict(item) for item in obj]
        else:
            return obj
    
    def _analyze_relationships(self) -> Dict[str, Any]:
        """Analyze relationships between components"""
        relationships = {
            "inheritance": {},
            "composition": {},
            "dependencies": {},
            "call_graph": defaultdict(list)
        }
        
        # Inheritance relationships
        for class_name, class_info in self.classes.items():
            for base_class in class_info.base_classes:
                if base_class in self.classes:
                    relationships["inheritance"][class_name] = base_class
        
        # Dependencies from imports - convert sets to lists
        for file_path, imports in self.imports.items():
            deps = set()
            for import_info in imports:
                deps.add(import_info.module)
            relationships["dependencies"][file_path] = list(deps)
        
        # Call graph
        for call in self.calls:
            relationships["call_graph"][call.called_function].append({
                "caller": call.caller_function,
                "file": call.caller_file,
                "line": call.line_number
            })
        
        return relationships
    
    def save_database(self, output_path: str):
        """Save cross-reference database to JSON file"""
        report = self.generate_cross_reference_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Cross-reference database saved to: {output_path}")
    
    def generate_html_report(self, output_path: str):
        """Generate HTML cross-reference report"""
        report = self.generate_cross_reference_report()
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>TomsGPXEditor - Cross-Reference Database</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; }}
        .class, .function {{ margin: 10px 0; padding: 10px; border-left: 3px solid #007acc; }}
        .method {{ margin: 5px 0; padding: 5px; background: #f9f9f9; }}
        .import {{ margin: 3px 0; font-family: monospace; }}
        .call {{ margin: 3px 0; font-family: monospace; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat {{ background: #e8f4f8; padding: 15px; border-radius: 5px; text-align: center; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Cross-Reference Database</h1>
        <p>Generated on: {report['metadata']['generated_at']}</p>
        
        <div class="stats">
            <div class="stat">
                <h3>{report['metadata']['total_files']}</h3>
                <p>Files</p>
            </div>
            <div class="stat">
                <h3>{report['metadata']['total_classes']}</h3>
                <p>Classes</p>
            </div>
            <div class="stat">
                <h3>{report['metadata']['total_functions']}</h3>
                <p>Functions</p>
            </div>
            <div class="stat">
                <h3>{report['metadata']['total_imports']}</h3>
                <p>Imports</p>
            </div>
            <div class="stat">
                <h3>{report['metadata']['total_calls']}</h3>
                <p>Calls</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>Classes</h2>
        {self._generate_classes_html(report['classes'])}
    </div>

    <div class="section">
        <h2>Functions</h2>
        {self._generate_functions_html(report['functions'])}
    </div>

    <div class="section">
        <h2>Relationships</h2>
        {self._generate_relationships_html(report['relationships'])}
    </div>

    <div class="section">
        <h2>File Structure</h2>
        {self._generate_file_structure_html(report['file_structure'])}
    </div>
</body>
</html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML report saved to: {output_path}")
    
    def _generate_classes_html(self, classes: Dict) -> str:
        """Generate HTML for classes section"""
        html = ""
        for class_name, class_info in classes.items():
            html += f"""
            <div class="class">
                <h3>{class_name}</h3>
                <p><strong>File:</strong> {class_info['file_path']}</p>
                <p><strong>Line:</strong> {class_info['line_number']}</p>
                {f"<p><strong>Doc:</strong> {class_info['docstring']}</p>" if class_info['docstring'] else ""}
                
                {f"<p><strong>Base Classes:</strong> {', '.join(class_info['base_classes'])}</p>" if class_info['base_classes'] else ""}
                
                <h4>Methods ({len(class_info['methods'])})</h4>
                <div>
                    {''.join(f'<div class="method">{method}()</div>' for method in class_info['methods'])}
                </div>
                
                {f"<h4>Properties ({len(class_info['properties'])})</h4>" if class_info['properties'] else ""}
                <div>
                    {''.join(f'<div class="method">{prop}</div>' for prop in class_info['properties'])}
                </div>
            </div>
            """
        return html
    
    def _generate_functions_html(self, functions: Dict) -> str:
        """Generate HTML for functions section"""
        html = ""
        for func_key, func_info in functions.items():
            html += f"""
            <div class="function">
                <h3>{func_info['name']}</h3>
                <p><strong>File:</strong> {func_info['file_path']}</p>
                <p><strong>Line:</strong> {func_info['line_number']}</p>
                <p><strong>Parameters:</strong> {', '.join(func_info['parameters'])}</p>
                {f"<p><strong>Return:</strong> {func_info['return_type']}</p>" if func_info['return_type'] else ""}
                {f"<p><strong>Decorators:</strong> {', '.join(func_info['decorators'])}</p>" if func_info['decorators'] else ""}
                {f"<p><strong>Doc:</strong> {func_info['docstring']}</p>" if func_info['docstring'] else ""}
            </div>
            """
        return html
    
    def _generate_relationships_html(self, relationships: Dict) -> str:
        """Generate HTML for relationships section"""
        html = ""
        
        if relationships['inheritance']:
            html += "<h3>🧬 Inheritance</h3><table><tr><th>Child</th><th>Parent</th></tr>"
            for child, parent in relationships['inheritance'].items():
                html += f"<tr><td>{child}</td><td>{parent}</td></tr>"
            html += "</table>"
        
        if relationships['call_graph']:
            html += "<h3>📞 Call Graph</h3>"
            for function, callers in relationships['call_graph'].items():
                html += f"<h4>{function}() called by:</h4>"
                for caller in callers:
                    html += f"<div class='call'>{caller['caller']}() at line {caller['line']} in {caller['file']}</div>"
        
        return html
    
    def _generate_file_structure_html(self, file_structure: Dict) -> str:
        """Generate HTML for file structure section"""
        html = ""
        for file_path, items in file_structure.items():
            html += f"""
            <div class="class">
                <h3>{file_path}</h3>
                <div>
                    {''.join(f'<div class="method">{item}</div>' for item in items)}
                </div>
            </div>
            """
        return html

def main():
    """Main function to generate cross-reference database"""
    root_path = "W:/TomsGPXEditor/src"
    
    print("Generating Cross-Reference Database for TomsGPXEditor...")
    
    # Create database
    db = CrossReferenceDatabase(root_path)
    db.analyze_codebase()
    
    # Save JSON database
    db.save_database("W:/TomsGPXEditor/CROSS_REFERENCE_DB.json")
    
    # Generate HTML report
    db.generate_html_report("W:/TomsGPXEditor/CROSS_REFERENCE_REPORT.html")
    
    print("Cross-reference database generation complete!")
    print("Files created:")
    print("   - CROSS_REFERENCE_DB.json (machine-readable)")
    print("   - CROSS_REFERENCE_REPORT.html (human-readable)")

if __name__ == "__main__":
    main()
