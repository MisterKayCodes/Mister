# Mister Kay - Capabilities

## Current Commands

### scan
- **Usage:** `kay scan [path]`
- **What it does:** Shows folder tree
- **Smart behavior:** 
  - ≤50 items → full tree
  - >50 items → root only, asks "show all?"
- **Skips:** venv, .git, node_modules, __pycache__, etc.

### help
- **Usage:** `kay help`
- **What it does:** Shows this message

## Coming Soon
- `kay read <file>` - Show file contents
- `kay find "<text>"` - Search files
- `kay teach "<pattern>"` - Learn new patterns
- `kay remember` - Show what I've learned

## Known Limitations
- Only scans text files (no binary)
- Max depth: unlimited (but asks for large folders)