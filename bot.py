#!/usr/bin/env python3
"""
Mister Kay - Your personal coding assistant
Usage: python bot.py <command> [arguments]
"""

import sys
import os

# Add the current directory to path so we can import core
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_help():
    """Show available commands"""
    print("""
📋 Mister Kay - Available Commands:

  scan [path]     Show folder tree of [path]
                  If no path given, scans current folder
                  Example: python bot.py scan C:/myproject
                  Example: python bot.py scan

  help            Show this message

More commands coming: teach, find, read, remember
""")

def command_scan(path):
    """Handle the 'scan' command"""
    
    if not path:
        path = os.getcwd()
        print(f"📁 No path specified. Scanning current folder: {path}")
    
    if not os.path.exists(path):
        print(f"❌ Error: Path does not exist: {path}")
        return
    
    if not os.path.isdir(path):
        print(f"❌ Error: Path is not a folder: {path}")
        return
    
    from core.tree_brain import TreeBrain
    # Use the new smart scan with prompt
    TreeBrain.scan_with_prompt(path)

def main():
    """The Mouth - parses what you say"""
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        print_help()
    
    elif command == "scan":
        path = sys.argv[2] if len(sys.argv) > 2 else None
        command_scan(path)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Type 'python bot.py help' for available commands")

if __name__ == "__main__":
    main()