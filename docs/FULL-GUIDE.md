
# Mister Kay - Complete User Guide

## 📋 All Commands

### scan
- **Usage:** `kay scan [path]`
- **What it does:** Shows folder tree
- **Smart behavior:** ≤50 items → full tree, >50 items → asks "show all?"
- **Skips:** venv, .git, node_modules, __pycache__, etc.

### read
- **Usage:** `kay read <file>`
- **Options:** `--lines` (line numbers), `10-25` (line range)
- **Smart behavior:** Auto-detects missing files, folders, binary files

### find
- **Usage:** `kay find <term>`
- **Options:** `--ext .py`, `--ignore-case`, `--count`
- **Default extensions:** .py, .txt, .md, .json, .yml, .csv

### copy
- **Usage:** `kay copy <file>`
- **What it does:** Copies file content to clipboard
- **Smart behavior:** Uses tkinter + temp file fallback, remembers last copied file

### paste
- **Usage:** `kay paste [file]`
- **Options:** `--preview` (show first 20 lines), `--undo` (restore from backup)
- **Smart behavior:** Creates `.bak` backup before overwriting

### imports
- **Usage:** `kay imports`
- **What it does:** Analyzes Python imports, finds broken dependencies
- **Shows:** Files scanned, total imports, valid/broken count

### clean
- **Usage:** `kay clean --backups`
- **Options:** `--dry-run` (preview what would be deleted)
- **What it does:** Deletes all `.bak` files recursively

### listen
- **Usage:** `kay listen`
- **What it does:** Shows last crash error in nice format

### kay_run
- **Usage:** `kay_run python main.py`
- **What it does:** Runs file, auto-captures crashes for `kay listen`

## 🧪 Examples

```bash
# Scan
kay scan
kay scan C:\Project

# Read
kay read bot.py
kay read bot.py --lines
kay read bot.py 10-25

# Find
kay find import
kay find import --ext .py
kay find import --count

# Copy/Paste
kay copy bot.py
kay paste newfile.py
kay paste --preview
kay paste --undo

# Imports
kay imports

# Clean
kay clean --backups --dry-run
kay clean --backups

# Crash capture
kay_run python main.py
kay listen
```

## 📁 Full Project Structure

```
Mister/
├── bot.py
├── kay.bat
├── kay_run.bat
├── parsers/
│   ├── scan_parser.py
│   ├── read_parser.py
│   ├── find_parser.py
│   ├── clipboard_parser.py
│   ├── listen_parser.py
│   ├── imports_parser.py
│   └── clean_parser.py
├── core/
│   ├── tree_brain.py
│   ├── reader_brain.py
│   ├── find_brain.py
│   ├── clipboard_brain.py
│   ├── listen_brain.py
│   ├── imports_brain.py
│   └── clean_brain.py
├── tools/
│   ├── file_walker.py
│   ├── error_catcher.py
│   └── clipboard_helper.py
├── memory/
│   ├── last_error.txt
│   └── clipboard_history.json
└── docs/
    └── FULL_GUIDE.md
```

## 🔧 Skipped Folders (Auto-Ignored)

`.git`, `node_modules`, `__pycache__`, `venv`, `.venv`, `env`, `.mypy_cache`, `.pytest_cache`, `Lib`, `Scripts`, `share`

## 📝 Roadmap

- [x] scan, read, find, copy, paste, imports, clean, listen
- [ ] `--fix` for imports
- [ ] `--context` for find
- [ ] `teach` command
- [ ] Parallel search

## ❓ FAQ

**Why not use an LLM?** Cost. Mister is free.

**Does Mister use AI?** Not yet. Phase 2 will add local LLMs.

**How to update Mister?** `git pull`

**Where are backups saved?** Same folder as original file with `.bak` extension.
```

---

