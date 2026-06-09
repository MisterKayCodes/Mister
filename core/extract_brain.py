import os
import ast

class ExtractBrain:
    @staticmethod
    def extract_node(source_file, target_name, dest_file):
        """Extract a class or function from source_file and save to dest_file"""
        if not os.path.exists(source_file):
            return False, f"Source file not found: {source_file}"
            
        if not source_file.endswith('.py'):
            return False, "ExtractBrain currently only supports .py files."
            
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
            
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(os.path.abspath(dest_file)), exist_ok=True)
            
            # Write to destination
            with open(dest_file, 'w', encoding='utf-8') as f:
                f.write(extracted_code)
                
            return True, f"Successfully extracted '{target_name}' to {dest_file}."
            
        except Exception as e:
            return False, f"Extraction failed: {e}"
