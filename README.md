
# 🧠 Mister - Your Personal Coding Assistant

**Mister** is a lightweight, terminal-based AI assistant that lives in your project folder. No API calls. No token costs. Just pure Python that helps you scan, read, search, understand, and navigate your codebase.

> *"Stop burning money on LLMs. Let Mister do the simple stuff."*

---

## ✨ Features

### Current Capabilities

| Command | What it does |
|---------|---------------|
| `kay scan [path]` | Shows folder tree with smart depth control |
| `kay read <file>` | Shows file contents with line numbers and ranges |
| `kay find <term>` | Searches for text across files with filters |
| `kay copy <file>` | Copy file to clipboard (inter-process safe) |
| `kay paste [file]` | Paste clipboard to file with backup/undo |
| `kay imports` | Analyze imports and find broken dependencies |
| `kay clean --backups` | Delete all .bak backup files in current folder and subfolders |
| `kay listen` | Shows the last crash error in a nice format |
| `kay_run python <file>` | Runs Python files and auto-captures crashes |
| `kay help` | Displays this help message |

### Smart Scanning Behavior

- **≤50 items** → Shows full folder tree automatically
- **>50 items** → Shows root level, then asks "Show all files? (y/n)"
- **Auto-skips** → `venv`, `.git`, `node_modules`, `__pycache__`, and more
- **Current folder** → Type `kay scan` without a path to scan where you are

### Smart Reading Behavior

- **Whole file** → `kay read bot.py` shows everything
- **With line numbers** → `kay read bot.py --lines` adds numbers
- **Specific lines** → `kay read bot.py 10-25` shows only lines 10 to 25
- **Auto-detects** → Missing files, folders, binary files (won't crash)

### Smart Search Behavior

- **Basic search** → `kay find import` searches all text files
- **Filter by type** → `kay find import --ext .py` only Python files
- **Case insensitive** → `kay find IMPORT --ignore-case`
- **Count only** → `kay find import --count` shows just the numbers
- **Auto-skips** → venv, .git, node_modules (same as scan)
- **Default extensions** → .py, .txt, .md, .json, .yml, .csv, and more

### Smart Clipboard Behavior

- **Copy files** → `kay copy bot.py` copies to clipboard (works in separate terminals)
- **Paste files** → `kay paste newfile.py` pastes clipboard to file
- **Auto-remember** → Remembers last copied file for easy paste
- **Backup safe** → Always creates `.bak` backup before overwriting
- **Preview first** → `kay paste --preview` shows first 20 lines
- **Easy undo** → `kay paste --undo` restores from backup
- **Cross-platform** → Uses tkinter (built-in Python) with temp file fallback

### Smart Clean Behavior

- **Delete backups** → `kay clean --backups` removes all `.bak` files recursively
- **Dry run** → `kay clean --backups --dry-run` previews what would be deleted
- **Recursive** → Finds backups in current folder AND all subfolders
- **Safe** → Asks nothing, just deletes (use dry-run first)

### Smart Crash Capture Behavior

- **Auto-capture** → `kay_run python main.py` saves crashes automatically
- **Formatted output** → Shows error with emojis and clear formatting
- **Traceback display** → Shows last 10 lines of the crash
- **Easy recall** → `kay listen` shows the last crash anytime

---

## 🚀 Quick Start

### Installation

1. **Clone or download Mister** to `C:\Kaycris\Mister`

2. **Add to PATH** (run PowerShell as Administrator):
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Kaycris\Mister", [EnvironmentVariableTarget]::Machine)
   ```

3. **Restart your terminal**

### Usage

```bash
# Scan any folder
kay scan C:\MyProject

# Scan current folder
cd C:\MyProject
kay scan

# Read any file
kay read bot.py
kay read bot.py --lines
kay read bot.py 10-25

# Search for text
kay find import
kay find import --ext .py
kay find import --ignore-case
kay find import --count

# Copy files to clipboard
kay copy bot.py
kay copy src/index.jsx

# Paste from clipboard
kay paste newfile.py          # Paste to new file
kay paste                     # Paste to last copied file
kay paste --preview           # Show first 20 lines
kay paste --undo              # Restore from backup

# Check for broken imports
kay imports

# Clean up backup files
kay clean --backups           # Delete all .bak files
kay clean --backups --dry-run # Preview what would be deleted

# Capture and view crashes
kay_run python main.py
kay listen

# Show help
kay help
```

---

## 📁 Project Structure

```
Mister/
├── bot.py                 # 🦴 Skeleton + Mouth (CLI entry point)
├── kay.bat                # 🖐️ Terminal launcher
├── kay_run.bat            # 🖐️ Crash capture wrapper
├── parsers/               # 👂 Ears (translates user input)
│   ├── __init__.py        # Parser package init
│   ├── scan_parser.py     # Scan command parser
│   ├── read_parser.py     # Read command parser
│   ├── find_parser.py     # Find command parser
│   ├── clipboard_parser.py # Copy/paste command parser
│   ├── listen_parser.py   # Listen command parser
│   ├── imports_parser.py  # Imports command parser
│   └── clean_parser.py    # Clean command parser
├── core/                  # 🧠 Brain (pure logic)
│   ├── tree_brain.py      # Scanning logic
│   ├── reader_brain.py    # Reading logic
│   ├── find_brain.py      # Search logic
│   ├── clipboard_brain.py # Copy/paste logic + memory
│   ├── listen_brain.py    # Crash capture logic
│   ├── imports_brain.py   # Import analysis logic
│   └── clean_brain.py     # Clean backup logic
├── tools/                 # 🖐️ Hands (file system access)
│   ├── file_walker.py     # File walking utilities
│   ├── error_catcher.py   # Save/load crash errors
│   └── clipboard_helper.py # Clipboard operations (tkinter)
├── memory/                # 💾 Memory (persistent storage)
│   ├── last_error.txt     # Last crash error
│   └── clipboard_history.json # Clipboard memory
├── docs/
│   └── capabilities.md    # 📋 Full command reference
└── README.md              # This file
```

### Biological Architecture (Updated)

| Component | Role | Location |
|-----------|------|----------|
| 👂 Ears | Translates user input into clean objects | `parsers/` |
| 🧠 Brain | Pure logic, no I/O | `core/` |
| 🖐️ Hands | File system actions | `tools/` |
| 👄 Mouth | CLI parsing and output | `bot.py` |
| 🦴 Skeleton | App entry & wiring | `bot.py` |
| 💾 Memory | Persistent storage | `memory/` |

---

## 🧪 Examples

### Small folder (≤50 items) - Auto full scan

```bash
$ kay scan C:\Kaycris\Mister_FC

📁 Scanning: C:\Kaycris\Mister_FC
--------------------------------------------------
📁 C:\Kaycris\Mister_FC/
├── 📄 convert.py
├── 📄 extract_players.py
├── 📁 Converted_PNGs/
│   ├── 📄 IMG_5009.png
│   └── 📄 IMG_5010.png
└── 📁 photos/
    ├── 📄 IMG_5009.jpeg
    └── 📄 IMG_5010.jpeg
```

### Large folder (>50 items) - Asks before full scan

```bash
$ kay scan C:\LargeProject

📁 Scanning: C:\LargeProject
--------------------------------------------------
📁 C:\LargeProject/
├── 📄 README.md
├── 📁 src/
├── 📁 tests/
└── 📁 assets/
--------------------------------------------------
📊 This folder has 156 items (more than 50).
❓ Show all files? (y/n): y

[shows full tree]
```

### Reading files

```bash
# Show entire file
$ kay read bot.py

📄 bot.py
==================================================
#!/usr/bin/env python3
"""
Mister Kay - Your personal coding assistant
...

# Show with line numbers
$ kay read bot.py --lines

📄 bot.py
==================================================
   1 | #!/usr/bin/env python3
   2 | """
   3 | Mister Kay - Your personal coding assistant
...

# Show specific lines only
$ kay read bot.py 10-25

📄 bot.py
📌 Lines 10 to 25 (total 87 lines in file)
==================================================
def print_help():
    """Show available commands"""
    print("""
📋 Mister Kay - Available Commands:
...
```

### Searching files

```bash
# Basic search
$ kay find import

🔍 Searching for "import" in C:\Kaycris\Mister
==================================================

📄 bot.py
------------------------------
    3 | import sys
    4 | import os

📄 core/find_brain.py
------------------------------
    1 | import os
    2 | import re

✅ Found 4 matches in 2 files
📁 Searched 8 files

# Search only Python files
$ kay find "TreeBrain" --ext .py

🔍 Searching for "TreeBrain" in C:\Kaycris\Mister
==================================================

📄 bot.py
------------------------------
   25 | from core.tree_brain import TreeBrain
   26 | TreeBrain.scan_with_prompt(path)

📄 core/tree_brain.py
------------------------------
    3 | class TreeBrain:

✅ Found 3 matches in 2 files

# Count only (fast)
$ kay find import --count

🔍 Searching for "import" in C:\Kaycris\Mister
==================================================
📊 Found 12 matches across 6 files
📁 Searched 8 files
```

### Copying and pasting files

```bash
# Copy a file to clipboard
$ kay copy bot.py

📋 Copied 246 lines (7.9 KB) from bot.py
✅ Ready to paste (Ctrl+V)

# Paste to a new file
$ kay paste newfile.py

✅ Pasted 246 lines to newfile.py

# Paste to last copied file (auto-remembers)
$ kay copy src/index.jsx
$ kay paste          # Pastes back to index.jsx

✅ Pasted 127 lines to src/index.jsx
💾 Backup saved: src/index.jsx.bak

# Preview clipboard before pasting
$ kay paste --preview

🔍 Preview (246 lines total):
#!/usr/bin/env python3
"""
Mister Kay - Your personal coding assistant
...
... and 243 more lines

# Undo a paste (restore from backup)
$ kay paste --undo

✅ Restored src/index.jsx from backup
```

### Cleaning up backup files

```bash
# Preview what would be deleted
$ kay clean --backups --dry-run

🧹 DRY RUN - Found 7 .bak files
========================================
Would delete 7 .bak files:
C:\Kaycris\Mister\test1.bak
C:\Kaycris\Mister\test2.bak
C:\Kaycris\Mister\subfolder\test3.bak
C:\Kaycris\Mister\subfolder\deep\deeper\test4.bak

💡 Run 'kay clean --backups' to delete them

# Actually delete all .bak files
$ kay clean --backups

🧹 ✅ Deleted 7 .bak files
```

### Capturing and viewing crashes

```bash
# Run your Python file with kay_run (auto-captures crashes)
$ kay_run python main.py

[Mister] Crash detected! Saving error...
[Mister] Error saved. Type 'kay listen' to see details.

Traceback (most recent call last):
  File "main.py", line 16, in <module>
    from loguru import logger
ModuleNotFoundError: No module named 'loguru'

# View the formatted crash
$ kay listen

🔍 Last Crash Report
==================================================
❌ Error: ModuleNotFoundError: No module named 'loguru'

📋 Full traceback (last 10 lines):
------------------------------
   File "main.py", line 16, in <module>
     from loguru import logger
ModuleNotFoundError: No module named 'loguru'
==================================================
💡 Tip: Type 'kay teach' to teach me about this error.
```

---

## 🔧 Skipped Folders (Auto-Ignored)

Mister automatically skips these to keep output clean:

- `.git`
- `node_modules`
- `__pycache__`
- `venv`, `.venv`, `env`
- `.mypy_cache`, `.pytest_cache`
- `Lib`, `Scripts`, `share` (virtual environment junk)

---

## 📝 Roadmap

- [x] `kay scan` - Smart folder tree
- [x] 50-item threshold with prompt
- [x] Current folder detection
- [x] Global `kay` command (PATH)
- [x] `kay read <file>` - Show file contents with line numbers and ranges
- [x] `kay find <term>` - Search across files with filters
- [x] `kay copy <file>` - Copy file to clipboard
- [x] `kay paste [file]` - Paste from clipboard with backup/undo
- [x] `kay imports` - Find broken imports in Python files
- [x] `kay clean --backups` - Delete all .bak backup files
- [x] `kay listen` - Capture and view crash errors
- [x] `kay_run` - Auto-capture crashes from any Python file
- [ ] `kay paste --fix` - Auto-fix import issues
- [ ] `kay listen --fix` - Auto-suggest fixes for errors
- [ ] `kay teach` - Teach Mister about new errors
- [ ] `kay find --context` - Show surrounding lines
- [ ] Parallel search (faster for large projects)

---

## ❓ FAQ

### Why not just use an LLM?

LLMs cost money per token. Mister costs $0. It handles the repetitive tasks (scanning, finding, reading) that don't need AI.

### Why "Mister"?

Short for **Mister Alert** - the biological architecture this project is built on. Every file has a purpose: Brain, Hands, Mouth, Memory.

### Does Mister use AI?

**Not yet.** Phase 1 is pure Python. Phase 2 will integrate local LLMs (Ollama, GPT4All) for teaching and learning.

### Can I teach Mister new things?

**Soon!** The `teach` command is in development. You'll be able to show Mister patterns once, and it will remember them forever.

### Is the find command slow?

For small/medium projects (<500 files), it's instant. For large projects (10,000+ files), it may take a few seconds. Parallel search is planned for future releases.

### How does kay listen work?

Run `kay_run python your_file.py` - if it crashes, Mister saves the error. Then `kay listen` shows it formatted nicely. Works from any folder.

### What does kay clean --backups do?

Deletes all `.bak` files in current folder and all subfolders. These are backup files created by `kay paste`. Use `--dry-run` first to preview.

---

## 🧠 Built On

- **Python 3.11+** - Pure Python, no external dependencies
- **Mister Alert Architecture** - Biological code organization
- **Your Feedback** - Built for developers, by a developer

---

## 📄 License

MIT - Do whatever you want with it.

---

## 🙏 Credits

Inspired by the **Mister Alert** biological architecture (Brain, Mouth, Hands, Memory). Built because LLM tokens are crazy expensive.

---

**Made with 🧠 by Kay** | [Report Issue](https://github.com/misterkaycodes/mister/issues)
```

---
