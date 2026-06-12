import os
import re

class BarrelBrain:
    @staticmethod
    def generate_barrel(folder_path):
        if not os.path.exists(folder_path):
            return False, f"❌ Directory not found: {folder_path}"
            
        if not os.path.isdir(folder_path):
            return False, f"❌ Path is not a directory: {folder_path}"
            
        index_path = os.path.join(folder_path, 'index.js')
        
        valid_extensions = ['.js', '.jsx', '.ts', '.tsx']
        export_statements = []
        
        # We also generate a comment header
        header = [
            "/**",
            " * Auto-generated Barrel Index",
            " * Created by Mister Kay",
            " */",
            ""
        ]
        
        files_found = 0
        for filename in sorted(os.listdir(folder_path)):
            if filename == 'index.js' or filename == 'index.ts' or filename == 'index.jsx' or filename == 'index.tsx':
                continue
                
            name, ext = os.path.splitext(filename)
            if ext in valid_extensions:
                file_path = os.path.join(folder_path, filename)
                
                # Check if it has any exports (export const, export function, export default)
                has_exports = False
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'export ' in content:
                            has_exports = True
                except Exception:
                    pass
                    
                if has_exports:
                    files_found += 1
                    export_statements.append(f"export * from './{name}';")
                    
        if files_found == 0:
            return False, f"❌ No exportable JS/TS files found in {folder_path}"
            
        final_content = '\n'.join(header + export_statements) + '\n'
        
        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            return True, f"✅ Successfully generated barrel file with {files_found} exports at: {index_path}"
        except Exception as e:
            return False, f"❌ Failed to write barrel file: {e}"
