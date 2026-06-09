import os
import ast
import sys
import re

class CheckBrain:
    @staticmethod
    def run_check(path):
        """Run project health check (syntax, dependencies, heavy files)"""
        
        skip_folders = {'.git', 'node_modules', '__pycache__', 'venv', '.venv', 'env', '.mypy_cache', '.pytest_cache', 'Lib', 'Scripts', 'share'}
        
        results = {
            'syntax_errors': [],
            'heavy_files': [],
            'missing_requirements': [],
            'unused_requirements': [],
            'files_scanned': 0
        }
        
        # 1. Parse requirements.txt
        req_file = os.path.join(path, 'requirements.txt')
        declared_reqs = set()
        if os.path.exists(req_file):
            with open(req_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # get the package name, split by ==, >=, etc.
                        pkg_name = re.split(r'[=<>~!]', line)[0].strip().lower()
                        declared_reqs.add(pkg_name)
        
        imported_packages = set()
        
        # 2. Scan files
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip_folders]
            
            for file in files:
                if not file.endswith('.py'):
                    continue
                
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, path)
                results['files_scanned'] += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        source = f.read()
                        
                    lines = source.split('\n')
                    
                    # Heavy file check (> 550 lines)
                    if len(lines) > 550:
                        results['heavy_files'].append((rel_path, len(lines)))
                        
                    # Syntax & Import check
                    try:
                        tree = ast.parse(source, filename=file_path)
                        
                        # Find imports
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imported_packages.add(alias.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module and node.level == 0:
                                    imported_packages.add(node.module.split('.')[0])
                                    
                    except SyntaxError as e:
                        results['syntax_errors'].append({
                            'file': rel_path,
                            'line': e.lineno,
                            'msg': e.msg,
                            'text': e.text.strip() if e.text else ""
                        })
                        
                except Exception:
                    pass
                    
        # 3. Analyze Dependencies
        if hasattr(sys, 'stdlib_module_names'):
            stdlib = sys.stdlib_module_names
        else:
            stdlib = set() # Fallback
            
        # Common local modules - naive check
        local_modules = set()
        for item in os.listdir(path):
            if os.path.isdir(os.path.join(path, item)):
                local_modules.add(item)
            elif item.endswith('.py'):
                local_modules.add(item[:-3])
                
        external_imports = set()
        for pkg in imported_packages:
            if pkg not in stdlib and pkg not in local_modules:
                external_imports.add(pkg.lower())
                
        # Known mismatches (import name vs pip package name)
        alias_map = {
            'yaml': 'pyyaml',
            'bs4': 'beautifulsoup4',
            'cv2': 'opencv-python',
            'dotenv': 'python-dotenv',
            'pil': 'pillow'
        }
        
        normalized_imports = set()
        for imp in external_imports:
            norm = alias_map.get(imp, imp)
            normalized_imports.add(norm.replace('_', '-'))
            
        declared_normalized = {req.replace('_', '-') for req in declared_reqs}
        
        results['missing_requirements'] = list(normalized_imports - declared_normalized)
        results['unused_requirements'] = list(declared_normalized - normalized_imports)
        
        return results
