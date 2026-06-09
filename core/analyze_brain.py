import os
import ast

class AnalyzeBrain:
    @staticmethod
    def analyze_file(path, target_file):
        """Parse target_file for Classes/Functions, and scan path for dependencies"""
        if not os.path.exists(target_file):
            return {"error": f"File not found: {target_file}"}
            
        if not target_file.endswith('.py'):
            return {"error": "AnalyzeBrain currently only supports .py files."}
            
        results = {
            "classes": [],
            "functions": [],
            "dependents": []
        }
        
        # 1. Parse the target file
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source)
            
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    start = node.lineno
                    end = node.end_lineno
                    results['classes'].append({"name": node.name, "start": start, "end": end})
                elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    start = node.lineno
                    end = node.end_lineno
                    results['functions'].append({"name": node.name, "start": start, "end": end})
        except Exception as e:
            return {"error": f"Failed to parse target file: {e}"}
            
        # 2. Find dependents
        target_module_name = os.path.splitext(os.path.basename(target_file))[0]
        skip_folders = {'.git', 'node_modules', '__pycache__', 'venv', '.venv', 'env'}
        
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip_folders]
            
            for file in files:
                if file.endswith('.py') and os.path.join(root, file) != target_file:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Very naive check for speed, then AST for accuracy if match found
                        if target_module_name in content:
                            try:
                                t = ast.parse(content)
                                imports_target = False
                                for node in ast.walk(t):
                                    if isinstance(node, ast.Import):
                                        for alias in node.names:
                                            if alias.name.split('.')[0] == target_module_name:
                                                imports_target = True
                                    elif isinstance(node, ast.ImportFrom):
                                        if node.module and node.module.split('.')[0] == target_module_name:
                                            imports_target = True
                                if imports_target:
                                    results['dependents'].append(os.path.relpath(file_path, path))
                            except Exception:
                                pass
                    except Exception:
                        pass
                        
        return results
