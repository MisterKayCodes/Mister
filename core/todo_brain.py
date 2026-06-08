import os
import re

class TodoBrain:
    @staticmethod
    def scan_todos(path):
        """Scan project for TODO, FIXME, BUG"""
        
        target_tags = ["TODO", "FIXME", "BUG"]
        skip_folders = {'.git', 'node_modules', '__pycache__', 'venv', '.venv', 'env', '.mypy_cache', '.pytest_cache', 'Lib', 'Scripts', 'share'}
        extensions = {'.py', '.txt', '.md', '.json', '.yml', '.csv', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.cpp', '.c', '.h', '.hpp'}
        
        results = []
        files_scanned = 0
        todos_found = 0
        
        pattern = re.compile(r'(TODO|FIXME|BUG)\b', re.IGNORECASE)
        
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in skip_folders]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext not in extensions and file != "Dockerfile" and not ext == "":
                    continue
                
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, path)
                
                files_scanned += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    file_results = []
                    for i, line in enumerate(lines):
                        if pattern.search(line):
                            file_results.append((i + 1, line.strip()))
                            todos_found += 1
                            
                    if file_results:
                        results.append((rel_path, file_results))
                except Exception:
                    pass
                    
        return {
            'files_scanned': files_scanned,
            'todos_found': todos_found,
            'results': results
        }
