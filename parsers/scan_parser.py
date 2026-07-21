"""Parser for scan command"""

def parse_scan(args):
    """Parse scan command arguments"""
    show_line_count = '--line-count' in args
    folders_only = '--folders-only' in args
    
    depth = None
    if '--depth' in args:
        try:
            depth_idx = args.index('--depth')
            depth = int(args[depth_idx + 1])
        except (ValueError, IndexError):
            pass # Invalid depth, ignore or handle elsewhere

    # Remove flags and their values to find the path
    clean_args = []
    skip_next = False
    for a in args:
        if skip_next:
            skip_next = False
            continue
        if a == '--depth':
            skip_next = True
            continue
        if not a.startswith('--'):
            clean_args.append(a)
            
    path = clean_args[2] if len(clean_args) > 2 else None
    
    return path, show_line_count, folders_only, depth