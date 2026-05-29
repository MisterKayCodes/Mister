# walks directories
import os
from pathlib import Path

class FileWalker:
    """Hands - touches the file system"""
    
    SKIP_FOLDERS = {
         '.git', 'node_modules', '__pycache__', 
    '.venv', 'venv', 'env',  # <-- 'venv' added (no dot)
    '.mypy_cache', '.pytest_cache',
    'Lib', 'Scripts', 'share',  # <-- virtual environment junk
    'site-packages', 'dist-info', '__pycache__'
    }
    
    @staticmethod
    def is_empty_folder(path):
        """Check if folder has any visible items"""
        try:
            items = os.listdir(path)
            # Filter out skipped folders
            visible = [i for i in items if i not in FileWalker.SKIP_FOLDERS and not (i.startswith('.') and i not in ['.env', '.gitignore'])]
            return len(visible) == 0
        except:
            return True
    
    @staticmethod
    def get_contents(path):
        """Get all files and folders in a path"""
        try:
            items = os.listdir(path)
            
            files = []
            folders = []
            
            for item in items:
                full_path = os.path.join(path, item)
                
                # Skip logic
                if item in FileWalker.SKIP_FOLDERS:
                    continue
                
                # Hidden files: only show .env and .gitignore
                if item.startswith('.') and item not in ['.env', '.gitignore']:
                    continue
                
                if os.path.isdir(full_path):
                    folders.append(item)
                else:
                    files.append(item)
            
            # Sort for consistent output
            files.sort()
            folders.sort()
            
            return files, folders
            
        except PermissionError:
            return [], []