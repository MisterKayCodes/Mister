"""Imports Brain - knows how to find and fix broken imports"""

import os
import re
import sys

class ImportsBrain:
    """Brain - analyzes imports in Python files"""
    
    # Skip these folders (same as scan)
    SKIP_FOLDERS = {
        '.git', 'node_modules', '__pycache__', 
        '.venv', 'venv', 'env', 
        '.mypy_cache', '.pytest_cache',
        'Lib', 'Scripts', 'share', 'dist-info'
    }
    
    @staticmethod
    def find_python_files(root_path):
        """Find all .py files in project, skipping unwanted folders"""
        python_files = []
        
        for root, dirs, files in os.walk(root_path):
            # Skip unwanted folders (modify dirs in place)
            dirs[:] = [d for d in dirs if d not in ImportsBrain.SKIP_FOLDERS]
            
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    python_files.append(full_path)
        
        return python_files
    
    @staticmethod
    def extract_imports_from_file(file_path):
        """Extract all import statements from a Python file"""
        imports = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return imports
        
        # Pattern for: import module, import module as alias
        import_pattern = r'^import\s+([\w\.]+)(?:\s+as\s+\w+)?'
        
        # Pattern for: from module import something
        from_pattern = r'^from\s+([\w\.]+)\s+import\s+(.+?)(?:\s+as\s+\w+)?$'
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Match regular import
            match = re.match(import_pattern, line)
            if match:
                module = match.group(1)
                if not module:  # Skip empty module names
                    continue
                imports.append({
                    'line': line,
                    'type': 'import',
                    'module': module,
                    'from_module': None,
                    'names': None
                })
                continue
            
            # Match from...import
            match = re.match(from_pattern, line)
            if match:
                from_module = match.group(1)
                names = match.group(2)
                if not from_module:  # Skip empty module names
                    continue
                imports.append({
                    'line': line,
                    'type': 'from_import',
                    'module': from_module,
                    'from_module': from_module,
                    'names': names
                })
        
        return imports
    
    @staticmethod
    def check_import_valid(import_item, project_root):
        """
        Check if an import is valid.
        Returns (is_valid, error_message, suggestion)
        """
        module = import_item.get('module', '')
        
        # Skip if module is empty
        if not module:
            return False, "Empty module name", None
        
        # Handle relative imports (start with .)
        if module.startswith('.'):
            return True, None, None
        
        # Built-in modules (always valid)
        builtins = {'sys', 'os', 're', 'json', 'csv', 'math', 'random', 
                    'datetime', 'time', 'pathlib', 'argparse', 'logging',
                    'subprocess', 'threading', 'multiprocessing', 'socket',
                    'collections', 'itertools', 'functools', 'typing',
                    'enum', 'types', 'weakref', 'copy', 'pprint', 'tempfile',
                    'shutil', 'glob', 'fnmatch', 'hashlib', 'string', 'struct',
                    'pickle', 'sqlite3', 'xml', 'html', 'urllib', 'http',
                    'zipfile', 'tarfile', 'gzip', 'bz2', 'lzma', 'cgi', 'syslog'}
        
        first_part = module.split('.')[0]
        if first_part in builtins:
            return True, None, None
        
        # Check if it's a local file (actual file must exist)
        module_path = module.replace('.', os.sep)
        
        # Check for file.py or folder/__init__.py
        possible_paths = [
            os.path.join(project_root, f"{module_path}.py"),
            os.path.join(project_root, module_path, "__init__.py"),
        ]
        
        file_exists = False
        for path in possible_paths:
            if os.path.exists(path):
                file_exists = True
                break
        
        if file_exists:
            return True, None, None
        
        # If it's a dotted path and file doesn't exist, it's broken
        if '.' in module:
            return False, f"Module '{module}' not found (file does not exist)", None
        
        # Check if it's an installed package
        try:
            if first_part:
                __import__(first_part)
                return True, None, None
        except ImportError:
            pass
        except ValueError:
            return False, f"Invalid module name: '{module}'", None
        
        return False, f"Module '{module}' not found", None
    
    @staticmethod
    def analyze_imports(path):
        """
        Scan all Python files and find broken imports.
        Returns list of issues.
        """
        issues = []
        valid_imports = []
        
        # Find all Python files
        python_files = ImportsBrain.find_python_files(path)
        
        for file_path in python_files:
            imports = ImportsBrain.extract_imports_from_file(file_path)
            rel_path = os.path.relpath(file_path, path)
            
            for imp in imports:
                is_valid, error, suggestion = ImportsBrain.check_import_valid(imp, path)
                
                import_info = {
                    'file': rel_path,
                    'line': imp['line'],
                    'type': imp['type'],
                    'module': imp['module'],
                    'is_valid': is_valid,
                    'error': error,
                    'suggestion': suggestion
                }
                
                if is_valid:
                    valid_imports.append(import_info)
                else:
                    issues.append(import_info)
        
        return {
            "files_scanned": len(python_files),
            "total_imports": len(valid_imports) + len(issues),
            "valid_imports": len(valid_imports),
            "broken_imports": len(issues),
            "issues": issues
        }