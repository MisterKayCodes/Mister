# Mister Kay - Capabilities

## Current Commands

### scan
- **Usage:** `kay scan [path]`
- **What it does:** Shows folder tree
- **Smart behavior:** 
  - ≤50 items → full tree
  - >50 items → root only, asks "show all?"
- **Skips:** venv, .git, node_modules, __pycache__, etc.

### read
- **Usage:** `kay read <file>`
- **What it does:** Shows file contents in the terminal
- **Options:**
  - `kay read bot.py` → Shows entire file
  - `kay read bot.py --lines` → Shows file with line numbers
  - `kay read bot.py 10-25` → Shows only lines 10 to 25
  - `kay read bot.py 10-25 --lines` → Shows lines 10-25 with numbers
- **Smart behavior:**
  - Auto-detects if file exists
  - Won't crash on binary files (images, videos)
  - Shows "file not found" if missing
  - Shows "that's a folder" if you try to read a folder
  - Shows line range info when using specific lines
- **Skips:** Binary files (can't read them)

### find
- **Usage:** `kay find <search_term>`
- **What it does:** Searches for text across all files in current folder
- **Options:**
  - `kay find import` → Basic search (default extensions)
  - `kay find import --ext .py` → Only search Python files
  - `kay find import --ext .py --ext .js` → Search multiple extensions
  - `kay find import --ignore-case` → Case insensitive search
  - `kay find import --count` → Show only match count (no line details)
  - `kay find import --context 2` → Show 2 lines before/after match (coming soon)
- **Smart behavior:**
  - Auto-skips venv, .git, node_modules, etc.
  - Shows file path, line number, and matching line
  - Won't crash on binary/unreadable files
  - Shows search summary (total matches, files searched)
- **Default extensions:** .py, .txt, .md, .json, .yml, .yaml, .csv, .ini, .cfg, .toml
- **Skips:** Same folders as scan + binary files

### help
- **Usage:** `kay help`
- **What it does:** Shows this message

## Coming Soon
- `kay find --context` - Show surrounding lines
- `kay teach "<pattern>"` - Learn new patterns
- `kay remember` - Show what I've learned
- `kay run <file>` - Execute Python files
- Parallel search (faster for large projects)

## Known Limitations
- Only reads text files (no binary/image files)
- Max depth for scan: unlimited (but asks for large folders)
- Line numbers start at 1 (not 0)
- File encoding assumes UTF-8
- Find command is single-threaded (may be slow on 10,000+ files)
- Context lines feature not yet implemented