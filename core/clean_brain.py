"""Clean Brain - removes backup and temp files"""

import os
import glob


class CleanBrain:
    """Brain - finds and deletes unwanted files"""
    
    @staticmethod
    def find_backups(root_path, dry_run=False):
        """
        Find all .bak files recursively
        
        Returns: (files_found, list_of_paths)
        """
        backup_files = []
        
        # Walk through all directories
        for foldername, subfolders, filenames in os.walk(root_path):
            for filename in filenames:
                if filename.endswith('.bak'):
                    full_path = os.path.join(foldername, filename)
                    backup_files.append(full_path)
        
        return len(backup_files), backup_files
    
    @staticmethod
    def delete_backups(root_path, dry_run=False):
        """
        Delete all .bak files
        
        Returns: (deleted_count, message)
        """
        count, files = CleanBrain.find_backups(root_path)
        
        if count == 0:
            return 0, "No .bak files found"
        
        if dry_run:
            return count, f"Would delete {count} .bak files:\n" + "\n".join(files[:10]) + (f"\n... and {count-10} more" if count > 10 else "")
        
        # Actually delete
        deleted = 0
        failed = []
        for file_path in files:
            try:
                os.remove(file_path)
                deleted += 1
            except Exception as e:
                failed.append(f"{file_path}: {e}")
        
        message = f"✅ Deleted {deleted} .bak files"
        if failed:
            message += f"\n⚠️ Failed to delete {len(failed)} files"
        
        return deleted, message