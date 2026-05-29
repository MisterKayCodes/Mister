import os
from pathlib import Path

class TreeBrain:
    """Brain - knows HOW to print a tree"""
    
    @staticmethod
    def count_total_items(path):
        """Count total files and folders (recursively) without printing"""
        from tools.file_walker import FileWalker
        
        total = 0
        files, folders = FileWalker.get_contents(path)
        total += len(files) + len(folders)
        
        for folder in folders:
            folder_path = os.path.join(path, folder)
            total += TreeBrain.count_total_items(folder_path)
        
        return total
    
    @staticmethod
    def build_tree(path, max_depth=None, current_depth=0, prefix="", is_last=True):
        """
        Returns a string of the folder tree
        
        Args:
            path: folder to scan
            max_depth: None = full tree, 0 = root only, 1 = root + 1 level, etc.
            current_depth: internal use only
            prefix: internal use only
            is_last: internal use only
        """
        
        result = ""
        folder_name = os.path.basename(path)
        
        # Print current folder
        if prefix == "":
            result += f"📁 {path}/\n"
            new_prefix = ""
        else:
            connector = "└── " if is_last else "├── "
            result += f"{prefix}{connector}📁 {folder_name}/\n"
            new_prefix = prefix + ("    " if is_last else "│   ")
        
        # If max_depth is 0, stop here (only print this folder, no contents)
        if max_depth == 0:
            return result
        
        from tools.file_walker import FileWalker
        files, folders = FileWalker.get_contents(path)
        
        all_items = files + folders
        total_items = len(all_items)
        
        for idx, item in enumerate(all_items):
            is_last_item = (idx == total_items - 1)
            item_path = os.path.join(path, item)
            
            if os.path.isdir(item_path):
                # Check if empty
                if FileWalker.is_empty_folder(item_path):
                    connector = "└── " if is_last_item else "├── "
                    result += f"{new_prefix}{connector}📁 {item}/\n"
                    result += f"{new_prefix}    └── (empty)\n"
                else:
                    # Recursively build subfolder tree
                    # If max_depth is not None, reduce depth by 1
                    new_depth = max_depth - 1 if max_depth is not None else None
                    result += TreeBrain._build_subtree(item_path, new_prefix, is_last_item, new_depth)
            else:
                # It's a file
                connector = "└── " if is_last_item else "├── "
                file_size = os.path.getsize(item_path)
                if file_size == 0:
                    result += f"{new_prefix}{connector}📄 {item} (empty)\n"
                else:
                    result += f"{new_prefix}{connector}📄 {item}\n"
        
        return result
    
    @staticmethod
    def _build_subtree(folder_path, prefix, is_last, max_depth=None):
        """Helper to build subtree with correct prefix and depth limit"""
        folder_name = os.path.basename(folder_path)
        connector = "└── " if is_last else "├── "
        
        result = f"{prefix}{connector}📁 {folder_name}/\n"
        
        # If max_depth is 0, stop here
        if max_depth == 0:
            return result
        
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        from tools.file_walker import FileWalker
        files, folders = FileWalker.get_contents(folder_path)
        
        all_items = files + folders
        total_items = len(all_items)
        
        for idx, item in enumerate(all_items):
            is_last_item = (idx == total_items - 1)
            item_path = os.path.join(folder_path, item)
            
            if os.path.isdir(item_path):
                if FileWalker.is_empty_folder(item_path):
                    item_connector = "└── " if is_last_item else "├── "
                    result += f"{new_prefix}{item_connector}📁 {item}/\n"
                    result += f"{new_prefix}    └── (empty)\n"
                else:
                    new_depth = max_depth - 1 if max_depth is not None else None
                    result += TreeBrain._build_subtree(item_path, new_prefix, is_last_item, new_depth)
            else:
                item_connector = "└── " if is_last_item else "├── "
                file_size = os.path.getsize(item_path)
                if file_size == 0:
                    result += f"{new_prefix}{item_connector}📄 {item} (empty)\n"
                else:
                    result += f"{new_prefix}{item_connector}📄 {item}\n"
        
        return result
    
    @staticmethod
    def scan_with_prompt(path):
        """Smart scan: shows root level, asks if >50 items, then continues"""
        
        # First, count total items (fast)
        total_items = TreeBrain.count_total_items(path)
        
        # Show root level only first
        print(f"\n📁 Scanning: {path}")
        print("-" * 50)
        root_tree = TreeBrain.build_tree(path, max_depth=0)
        print(root_tree)
        print("-" * 50)
        
        # If total items <= 50, show full tree automatically
        if total_items <= 50:
            print(f"📊 This folder has {total_items} items (≤50). Showing full tree...\n")
            full_tree = TreeBrain.build_tree(path, max_depth=None)
            print(full_tree)
            return full_tree
        
        # If >50, ask user
        print(f"📊 This folder has {total_items} items (more than 50).")
        
        while True:
            answer = input("❓ Show all files? (y/n): ").lower().strip()
            if answer == 'y':
                print("\n📂 Showing full tree...\n")
                full_tree = TreeBrain.build_tree(path, max_depth=None)
                print(full_tree)
                return full_tree
            elif answer == 'n':
                print("\n✅ Scan complete. Use 'kay scan' again to see more.")
                return root_tree
            else:
                print("Please type 'y' for yes or 'n' for no.")