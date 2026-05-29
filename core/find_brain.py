import os
import re
from pathlib import Path

# ============================================
# TODO(Future Me): Implement parallel search with threading/multiprocessing
# Current: Single-threaded search (slow for 10,000+ files)
# Plan: Use concurrent.futures.ThreadPoolExecutor to search multiple folders at once
# Expected speedup: 3-4x on multi-core machines
# Note: Be careful with file handle limits and memory please
# ============================================

class FindBrain:
    """Brain - knows how to search for text in files"""
    
    # Default text file extensions to search
    DEFAULT_EXTENSIONS = {'.py', '.txt', '.md', '.json', '.yml', '.yaml', '.csv', '.ini', '.cfg', '.toml'}
    
    # Skip these folders (same as scan)
    SKIP_FOLDERS = {
        '.git', 'node_modules', '__pycache__', 
        '.venv', 'venv', 'env', 
        '.mypy_cache', '.pytest_cache',
        'Lib', 'Scripts', 'share', 'dist-info'
    }
    
    @staticmethod
    def should_skip_folder(folder_name):
        """Check if folder should be skipped"""
        return folder_name in FindBrain.SKIP_FOLDERS
    
    @staticmethod
    def should_search_file(file_path, extensions):
        """Check if file should be searched based on extension"""
        if extensions is None:
            extensions = FindBrain.DEFAULT_EXTENSIONS
        
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in extensions
    
    @staticmethod
    def search_file(file_path, search_term, ignore_case=False):
        """
        Search a single file for search_term.
        Returns list of (line_number, line_content)
        """
        matches = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except (UnicodeDecodeError, PermissionError, OSError):
            return matches  # Skip binary/unreadable files
        
        for i, line in enumerate(lines, start=1):
            if ignore_case:
                found = search_term.lower() in line.lower()
            else:
                found = search_term in line
            
            if found:
                matches.append((i, line.rstrip()))
        
        return matches
    
    @staticmethod
    def search_folder(root_path, search_term, extensions=None, ignore_case=False, context_lines=0, count_only=False):
        """
        Search entire folder recursively.
        Returns results dictionary.
        """
        results = {}
        total_matches = 0
        files_searched = 0
        
        for root, dirs, files in os.walk(root_path):
            # Filter out skipped folders (modify dirs in place to prevent walking into them)
            dirs[:] = [d for d in dirs if not FindBrain.should_skip_folder(d)]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check if we should search this file
                if not FindBrain.should_search_file(file_path, extensions):
                    continue
                
                files_searched += 1
                matches = FindBrain.search_file(file_path, search_term, ignore_case)
                
                if matches:
                    total_matches += len(matches)
                    if not count_only:  # Only store details if not count_only
                        results[file_path] = matches
        
        # Build output
        output = f"\n🔍 Searching for \"{search_term}\" in {root_path}\n"
        output += "=" * 50 + "\n"
        
        if count_only:
            output += f"📊 Found {total_matches} matches across {len(results)} files\n"
            output += f"📁 Searched {files_searched} files\n"
            return output
        
        if not results:
            output += "❌ No matches found\n"
            return output
        
        for file_path, matches in results.items():
            # Show relative path (make it shorter)
            rel_path = os.path.relpath(file_path, root_path)
            output += f"\n📄 {rel_path}\n"
            output += "-" * 30 + "\n"
            
            for line_num, line_content in matches:
                if context_lines > 0:
                    # TODO: Add context lines around match (future feature)
                    output += f"  {line_num:4d} | {line_content}\n"
                else:
                    output += f"  {line_num:4d} | {line_content}\n"
        
        output += f"\n✅ Found {total_matches} matches in {len(results)} files\n"
        output += f"📁 Searched {files_searched} files\n"
        
        return output
    
    @staticmethod
    def search_with_prompt(path, search_term, extensions=None, ignore_case=False, context_lines=0, count_only=False):
        """Main entry point for search"""
        
        if not os.path.exists(path):
            return f"❌ Error: Path does not exist - {path}"
        
        if not os.path.isdir(path):
            return f"❌ Error: Not a folder - {path}"
        
        return FindBrain.search_folder(path, search_term, extensions, ignore_case, context_lines, count_only)