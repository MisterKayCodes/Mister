import os
import pyperclip

class BundleBrain:
    @staticmethod
    def bundle_files(file_paths):
        """Bundle multiple files into a single clipboard-ready string"""
        
        sections = []
        missing = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                missing.append(file_path)
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                rel_path = os.path.relpath(file_path)
                section = f"# {rel_path}\n{content}"
                sections.append(section)
            except Exception as e:
                missing.append(f"{file_path} ({e})")
                
        if not sections:
            return False, "❌ No files could be read.", missing
            
        divider = "\n\n------------------\n\n"
        bundle = divider.join(sections)
        
        try:
            pyperclip.copy(bundle)
        except Exception:
            # Fallback: write to temp file for clipboard
            try:
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(bundle)
                root.update()
                root.after(500, root.destroy)
                root.mainloop()
            except Exception as e:
                return False, f"❌ Could not copy to clipboard: {e}", missing
                
        return True, bundle, missing
