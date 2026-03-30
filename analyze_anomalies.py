#!/usr/bin/env python3
"""
Cross-Reference Anomaly Analyzer for TomsGPXEditor

Analyzes the cross-reference database for anomalies, code smells,
and unusual patterns that might indicate architectural issues.
"""

import json
import os
from collections import defaultdict, Counter
from pathlib import Path

class CrossReferenceAnomalyAnalyzer:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db = self._load_database()
        
    def _load_database(self):
        """Load cross-reference database"""
        with open(self.db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_all_anomalies(self):
        """Perform comprehensive anomaly analysis"""
        print("Starting Cross-Reference Anomaly Analysis...")
        print(f"Database: {self.db['metadata']['total_classes']} classes, {self.db['metadata']['total_functions']} functions")
        
        anomalies = {
            "architectural_issues": self.analyze_architectural_issues(),
            "code_smells": self.analyze_code_smells(),
            "dependency_anomalies": self.analyze_dependencies(),
            "naming_anomalies": self.analyze_naming(),
            "size_anomalies": self.analyze_size_anomalies(),
            "import_anomalies": self.analyze_imports(),
            "dead_code": self.analyze_dead_code(),
            "complexity_anomalies": self.analyze_complexity_anomalies()
        }
        
        self._generate_anomaly_report(anomalies)
        return anomalies
    
    def analyze_architectural_issues(self):
        """Analyze architectural issues and violations"""
        issues = []
        
        # 1. Classes with too many responsibilities (God Objects)
        for class_name, class_info in self.db['classes'].items():
            method_count = len(class_info['methods'])
            if method_count > 20:
                issues.append({
                    "type": "god_object",
                    "severity": "high",
                    "component": class_name,
                    "file": class_info['file_path'],
                    "description": f"Class has {method_count} methods (too many responsibilities)",
                    "suggestion": "Consider splitting into smaller, focused classes"
                })
        
        # 2. Classes with no methods (likely data classes)
        for class_name, class_info in self.db['classes'].items():
            if len(class_info['methods']) == 0:
                issues.append({
                    "type": "empty_class",
                    "severity": "medium",
                    "component": class_name,
                    "file": class_info['file_path'],
                    "description": "Class has no methods",
                    "suggestion": "Consider using @dataclass or removing if unused"
                })
        
        # 3. Inheritance anomalies
        inheritance = self.db['relationships']['inheritance']
        for child, parent in inheritance.items():
            # Check for inheritance depth
            depth = self._calculate_inheritance_depth(child)
            if depth > 3:
                issues.append({
                    "type": "deep_inheritance",
                    "severity": "medium",
                    "component": child,
                    "description": f"Inheritance depth of {depth} levels",
                    "suggestion": "Consider composition over inheritance"
                })
        
        # 4. Circular dependencies
        circular_deps = self._find_circular_dependencies()
        for dep in circular_deps:
            issues.append({
                "type": "circular_dependency",
                "severity": "high",
                "component": " -> ".join(dep),
                "description": f"Circular dependency detected: {' -> '.join(dep)}",
                "suggestion": "Refactor to break circular dependency"
            })
        
        return issues
    
    def analyze_code_smells(self):
        """Analyze code smells and anti-patterns"""
        smells = []
        
        # 1. Long parameter lists
        for func_key, func_info in self.db['functions'].items():
            param_count = len(func_info['parameters'])
            if param_count > 7:
                smells.append({
                    "type": "long_parameter_list",
                    "severity": "medium",
                    "component": func_info['name'],
                    "file": func_info['file_path'],
                    "description": f"Function has {param_count} parameters",
                    "suggestion": "Consider using parameter objects or configuration classes"
                })
        
        # 2. Functions with no parameters (might be candidates for methods)
        for func_key, func_info in self.db['functions'].items():
            if len(func_info['parameters']) == 0 and not func_info['name'].startswith('_'):
                smells.append({
                    "type": "parameterless_function",
                    "severity": "low",
                    "component": func_info['name'],
                    "file": func_info['file_path'],
                    "description": "Function has no parameters",
                    "suggestion": "Consider if this should be a method or utility function"
                })
        
        # 3. Duplicate method names across classes
        method_names = defaultdict(list)
        for class_name, class_info in self.db['classes'].items():
            for method in class_info['methods']:
                method_names[method].append(class_name)
        
        for method_name, classes in method_names.items():
            if len(classes) > 3:
                smells.append({
                    "type": "duplicate_method_names",
                    "severity": "low",
                    "component": method_name,
                    "description": f"Method '{method_name}' exists in {len(classes)} classes: {', '.join(classes)}",
                    "suggestion": "Consider if these methods should be in a common base class"
                })
        
        return smells
    
    def analyze_dependencies(self):
        """Analyze dependency issues"""
        issues = []
        
        # 1. Files with too many dependencies
        dependencies = self.db['relationships']['dependencies']
        for file_path, deps in dependencies.items():
            if len(deps) > 15:
                issues.append({
                    "type": "high_coupling",
                    "severity": "medium",
                    "component": file_path,
                    "description": f"File has {len(deps)} dependencies",
                    "suggestion": "Consider reducing dependencies or splitting the file"
                })
        
        # 2. Files with no dependencies (isolated)
        for file_path, deps in dependencies.items():
            if len(deps) == 0:
                issues.append({
                    "type": "isolated_file",
                    "severity": "low",
                    "component": file_path,
                    "description": "File has no dependencies",
                    "suggestion": "Check if this file is actually used"
                })
        
        # 3. Suspicious import patterns
        for file_path, imports in self.db['imports'].items():
            import_modules = [imp['module'] for imp in imports]
            
            # Multiple imports from same module
            module_counts = Counter(import_modules)
            for module, count in module_counts.items():
                if count > 5:
                    issues.append({
                        "type": "excessive_imports_from_module",
                        "severity": "low",
                        "component": file_path,
                        "description": f"Imported {count} items from module '{module}'",
                        "suggestion": "Consider importing the module and using module.prefix"
                    })
        
        return issues
    
    def analyze_naming(self):
        """Analyze naming convention anomalies"""
        issues = []
        
        # 1. Class naming violations
        for class_name, class_info in self.db['classes'].items():
            if not class_name[0].isupper():
                issues.append({
                    "type": "class_naming_violation",
                    "severity": "medium",
                    "component": class_name,
                    "file": class_info['file_path'],
                    "description": f"Class name '{class_name}' doesn't start with uppercase",
                    "suggestion": "Use PascalCase for class names"
                })
        
        # 2. Function naming violations
        for func_key, func_info in self.db['functions'].items():
            func_name = func_info['name']
            if func_name and not func_name.startswith('_') and not func_name.islower():
                issues.append({
                    "type": "function_naming_violation",
                    "severity": "medium",
                    "component": func_name,
                    "file": func_info['file_path'],
                    "description": f"Function name '{func_name}' should be snake_case",
                    "suggestion": "Use snake_case for function names"
                })
        
        # 3. Suspicious names
        suspicious_names = ['temp', 'tmp', 'test', 'data', 'info', 'stuff']
        for func_key, func_info in self.db['functions'].items():
            func_name = func_info['name'].lower()
            for suspicious in suspicious_names:
                if suspicious in func_name and len(func_name) < 10:
                    issues.append({
                        "type": "suspicious_name",
                        "severity": "low",
                        "component": func_name,
                        "file": func_info['file_path'],
                        "description": f"Function name '{func_name}' contains generic term '{suspicious}'",
                        "suggestion": "Use more descriptive names"
                    })
        
        return issues
    
    def analyze_size_anomalies(self):
        """Analyze size-related anomalies"""
        issues = []
        
        # 1. Very large files
        file_sizes = defaultdict(int)
        for class_info in self.db['classes'].values():
            file_sizes[class_info['file_path']] += len(class_info['methods'])
        for func_info in self.db['functions'].values():
            file_sizes[func_info['file_path']] += 1
        
        for file_path, size in file_sizes.items():
            if size > 50:
                issues.append({
                    "type": "large_file",
                    "severity": "medium",
                    "component": file_path,
                    "description": f"File contains {size} functions/classes",
                    "suggestion": "Consider splitting into smaller modules"
                })
        
        # 2. Very small files
        for file_path, size in file_sizes.items():
            if size < 3:
                issues.append({
                    "type": "tiny_file",
                    "severity": "low",
                    "component": file_path,
                    "description": f"File contains only {size} functions/classes",
                    "suggestion": "Consider merging with related files"
                })
        
        return issues
    
    def analyze_imports(self):
        """Analyze import anomalies"""
        issues = []
        
        # 1. Unused imports (approximate - would need more sophisticated analysis)
        for file_path, imports in self.db['imports'].items():
            # Check for imports that might be unused
            for import_info in imports:
                if import_info['is_from_import'] and len(import_info['imported_items']) == 1:
                    item = import_info['imported_items'][0]
                    if item.startswith('_') and not item.startswith('__'):
                        issues.append({
                            "type": "private_import",
                            "severity": "low",
                            "component": file_path,
                            "description": f"Importing private item '{item}' from '{import_info['module']}'",
                            "suggestion": "Avoid importing private items"
                        })
        
        # 2. Relative imports
        for file_path, imports in self.db['imports'].items():
            for import_info in imports:
                if import_info['module'].startswith('.'):
                    issues.append({
                        "type": "relative_import",
                        "severity": "low",
                        "component": file_path,
                        "description": f"Using relative import: '{import_info['module']}'",
                        "suggestion": "Use absolute imports when possible"
                    })
        
        return issues
    
    def analyze_dead_code(self):
        """Analyze potential dead code"""
        issues = []
        
        # 1. Functions that might be unused (no calls found)
        all_function_calls = set()
        for call in self.db['calls']:
            all_function_calls.add(call['called_function'])
        
        for func_key, func_info in self.db['functions'].items():
            func_name = func_info['name']
            if func_name not in all_function_calls and not func_name.startswith('_'):
                issues.append({
                    "type": "potentially_unused_function",
                    "severity": "medium",
                    "component": func_name,
                    "file": func_info['file_path'],
                    "description": f"Function '{func_name}' has no recorded calls",
                    "suggestion": "Verify if this function is actually used"
                })
        
        # 2. Classes that might be unused
        all_class_references = set()
        for call in self.db['calls']:
            # This is approximate - would need more sophisticated analysis
            all_class_references.add(call['called_function'])
        
        for class_name, class_info in self.db['classes'].items():
            if class_name not in all_class_references:
                issues.append({
                    "type": "potentially_unused_class",
                    "severity": "medium",
                    "component": class_name,
                    "file": class_info['file_path'],
                    "description": f"Class '{class_name}' might not be referenced",
                    "suggestion": "Verify if this class is actually used"
                })
        
        return issues
    
    def analyze_complexity_anomalies(self):
        """Analyze complexity-related anomalies"""
        issues = []
        
        # 1. Classes with too many methods (complexity indicator)
        for class_name, class_info in self.db['classes'].items():
            method_count = len(class_info['methods'])
            if method_count > 15:
                issues.append({
                    "type": "high_class_complexity",
                    "severity": "medium",
                    "component": class_name,
                    "file": class_info['file_path'],
                    "description": f"Class has {method_count} methods (high complexity)",
                    "suggestion": "Consider splitting into smaller classes"
                })
        
        # 2. Deep inheritance chains
        inheritance = self.db['relationships']['inheritance']
        for child, parent in inheritance.items():
            depth = self._calculate_inheritance_depth(child)
            if depth > 2:
                issues.append({
                    "type": "deep_inheritance_chain",
                    "severity": "medium",
                    "component": child,
                    "description": f"Inheritance chain depth: {depth}",
                    "suggestion": "Consider flattening inheritance hierarchy"
                })
        
        return issues
    
    def _calculate_inheritance_depth(self, class_name, visited=None):
        """Calculate inheritance depth for a class"""
        if visited is None:
            visited = set()
        
        if class_name in visited:
            return 0  # Circular inheritance
        
        visited.add(class_name)
        
        inheritance = self.db['relationships']['inheritance']
        if class_name in inheritance:
            parent = inheritance[class_name]
            return 1 + self._calculate_inheritance_depth(parent, visited.copy())
        
        return 0
    
    def _find_circular_dependencies(self):
        """Find circular dependencies in imports"""
        dependencies = self.db['relationships']['dependencies']
        circular_deps = []
        
        for file_path, deps in dependencies.items():
            for dep in deps:
                if dep in dependencies:
                    # Check if dependency depends back on us
                    if file_path in dependencies[dep]:
                        circular_deps.append([file_path, dep, file_path])
        
        return circular_deps
    
    def _generate_anomaly_report(self, anomalies):
        """Generate comprehensive anomaly report"""
        total_issues = sum(len(issues) for issues in anomalies.values())
        
        print(f"\nANOMALY ANALYSIS COMPLETE")
        print(f"   Total Issues Found: {total_issues}")
        
        for category, issues in anomalies.items():
            if issues:
                print(f"\n{category.upper().replace('_', ' ')}: {len(issues)} issues")
                
                # Count by severity
                severity_counts = Counter(issue['severity'] for issue in issues)
                for severity, count in severity_counts.items():
                    print(f"   {severity.capitalize()}: {count}")
        
        # Generate detailed report
        report = {
            "metadata": {
                "generated_at": "2026-03-28",
                "total_issues": total_issues,
                "categories": {cat: len(issues) for cat, issues in anomalies.items()}
            },
            "anomalies": anomalies,
            "summary": self._generate_summary(anomalies)
        }
        
        # Save report
        with open("W:/TomsGPXEditor/ANOMALY_ANALYSIS_REPORT.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Generate HTML report
        self._generate_html_report(report)
        
        print(f"\nReports saved:")
        print(f"   - ANOMALY_ANALYSIS_REPORT.json (machine-readable)")
        print(f"   - ANOMALY_ANALYSIS_REPORT.html (human-readable)")
        
        return report
    
    def _generate_summary(self, anomalies):
        """Generate summary statistics"""
        summary = {
            "total_issues": sum(len(issues) for issues in anomalies.values()),
            "high_severity": sum(1 for issues in anomalies.values() for issue in issues if issue['severity'] == 'high'),
            "medium_severity": sum(1 for issues in anomalies.values() for issue in issues if issue['severity'] == 'medium'),
            "low_severity": sum(1 for issues in anomalies.values() for issue in issues if issue['severity'] == 'low'),
            "most_common_issues": {},
            "files_with_most_issues": {}
        }
        
        # Most common issue types
        all_issues = []
        for issues in anomalies.values():
            all_issues.extend(issues)
        
        issue_types = Counter(issue['type'] for issue in all_issues)
        summary["most_common_issues"] = dict(issue_types.most_common(5))
        
        # Files with most issues - handle missing file key
        file_issues = Counter()
        for issue in all_issues:
            if 'file' in issue:
                file_issues[issue['file']] += 1
            elif 'file_path' in issue:
                file_issues[issue['file_path']] += 1
        
        summary["files_with_most_issues"] = dict(file_issues.most_common(5))
        
        return summary
    
    def _generate_html_report(self, report):
        """Generate HTML anomaly report"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>TomsGPXEditor - Anomaly Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat {{ background: #e8f4f8; padding: 15px; border-radius: 5px; text-align: center; }}
        .section {{ margin: 20px 0; }}
        .issue {{ margin: 10px 0; padding: 10px; border-left: 3px solid #ff6b6b; }}
        .issue.high {{ border-left-color: #ff6b6b; }}
        .issue.medium {{ border-left-color: #ffa500; }}
        .issue.low {{ border-left-color: #90ee90; }}
        .severity {{ font-weight: bold; padding: 2px 8px; border-radius: 3px; }}
        .severity.high {{ background: #ff6b6b; color: white; }}
        .severity.medium {{ background: #ffa500; color: white; }}
        .severity.low {{ background: #90ee90; color: black; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Cross-Reference Anomaly Analysis</h1>
        <p>Generated on: {report['metadata']['generated_at']}</p>
        
        <div class="summary">
            <div class="stat">
                <h3>{report['summary']['total_issues']}</h3>
                <p>Total Issues</p>
            </div>
            <div class="stat">
                <h3>{report['summary']['high_severity']}</h3>
                <p>High Severity</p>
            </div>
            <div class="stat">
                <h3>{report['summary']['medium_severity']}</h3>
                <p>Medium Severity</p>
            </div>
            <div class="stat">
                <h3>{report['summary']['low_severity']}</h3>
                <p>Low Severity</p>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>Most Common Issues</h2>
        <table>
            <tr><th>Issue Type</th><th>Count</th></tr>
            {''.join(f"<tr><td>{issue_type}</td><td>{count}</td></tr>" 
                    for issue_type, count in report['summary']['most_common_issues'].items())}
        </table>
    </div>

    <div class="section">
        <h2>Files With Most Issues</h2>
        <table>
            <tr><th>File</th><th>Issue Count</th></tr>
            {''.join(f"<tr><td>{file_path}</td><td>{count}</td></tr>" 
                    for file_path, count in report['summary']['files_with_most_issues'].items())}
        </table>
    </div>

    {self._generate_issues_html(report['anomalies'])}
</body>
</html>
        """
        
        with open("W:/TomsGPXEditor/ANOMALY_ANALYSIS_REPORT.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_issues_html(self, anomalies):
        """Generate HTML for issues"""
        html = ""
        for category, issues in anomalies.items():
            if issues:
                html += f"""
                <div class="section">
                    <h2>{category.replace('_', ' ').title()}</h2>
                """
                for issue in issues:
                    file_path = issue.get('file', issue.get('file_path', 'Unknown'))
                    html += f"""
                    <div class="issue {issue['severity']}">
                        <span class="severity {issue['severity']}">{issue['severity'].upper()}</span>
                        <h3>{issue['component']}</h3>
                        <p><strong>File:</strong> {file_path}</p>
                        <p><strong>Description:</strong> {issue['description']}</p>
                        <p><strong>Suggestion:</strong> {issue['suggestion']}</p>
                    </div>
                    """
                html += "</div>"
        return html

def main():
    """Main function to analyze cross-reference anomalies"""
    print("Starting Cross-Reference Anomaly Analysis...")
    
    analyzer = CrossReferenceAnomalyAnalyzer("W:/TomsGPXEditor/CROSS_REFERENCE_DB.json")
    anomalies = analyzer.analyze_all_anomalies()
    
    print("\nAnomaly Analysis Complete!")

if __name__ == "__main__":
    main()
