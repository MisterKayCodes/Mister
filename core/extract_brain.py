import os
import ast
import re

class ExtractBrain:
    @staticmethod
    def extract_node(source_file, target_name, dest_file):
        """Extract a class or function from source_file and save to dest_file"""
        if not os.path.exists(source_file):
            return False, f"Source file not found: {source_file}"
            
        _, ext = os.path.splitext(source_file)
        
        if ext == '.py':
            return ExtractBrain._extract_python(source_file, target_name, dest_file)
        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            return ExtractBrain._extract_js(source_file, target_name, dest_file)
        else:
            return False, f"ExtractBrain does not support {ext} files yet."
            
    @staticmethod
    def _extract_python(source_file, target_name, dest_file):
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            source = "".join(lines)
            tree = ast.parse(source)
            
            node_to_extract = None
            for node in tree.body:
                if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name == target_name:
                        node_to_extract = node
                        break
                        
            if not node_to_extract:
                return False, f"Could not find '{target_name}' in {source_file}."
                
            start = node_to_extract.lineno - 1
            end = node_to_extract.end_lineno
            
            extracted_code = "".join(lines[start:end])
            
            os.makedirs(os.path.dirname(os.path.abspath(dest_file)), exist_ok=True)
            with open(dest_file, 'w', encoding='utf-8') as f:
                f.write(extracted_code)
                
            return True, f"Successfully extracted '{target_name}' to {dest_file}."
            
        except Exception as e:
            return False, f"Python extraction failed: {e}"

    @staticmethod
    def _extract_js(source_file, target_name, dest_file):
        """Lightweight bracket-matching parser for JS/TS/JSX/TSX"""
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Regex to find standard JS declarations
            # Matches: const target_name =, let target_name =, var target_name =, function target_name, class target_name
            pattern = re.compile(rf'\b(?:const|let|var|function|class)\s+{target_name}\b')

            start_line = -1
            for i, line in enumerate(lines):
                if pattern.search(line):
                    start_line = i
                    break

            if start_line == -1:
                return False, f"Could not find '{target_name}' in {source_file}."

            # Now find the opening brace and match until it closes
            brace_count = 0
            found_first_brace = False
            end_line = -1

            for i in range(start_line, len(lines)):
                line = lines[i]
                for char in line:
                    if char == '{':
                        brace_count += 1
                        found_first_brace = True
                    elif char == '}':
                        brace_count -= 1
                        
                if found_first_brace and brace_count == 0:
                    end_line = i
                    break

            if not found_first_brace or end_line == -1:
                return False, f"Could not perfectly match brackets for '{target_name}'. Code might be malformed."

            extracted_code = "".join(lines[start_line:end_line + 1])
            
            os.makedirs(os.path.dirname(os.path.abspath(dest_file)), exist_ok=True)
            with open(dest_file, 'w', encoding='utf-8') as f:
                f.write(extracted_code)

            return True, f"Successfully extracted '{target_name}' (JS/TS) to {dest_file}."

        except Exception as e:
            return False, f"JS extraction failed: {e}"
