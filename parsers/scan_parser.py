"""Parser for scan command"""

def parse_scan(args):
    """Parse scan command arguments"""
    show_line_count = '--line-count' in args
    
    # Remove flags to find the path
    clean_args = [a for a in args if not a.startswith('--')]
    path = clean_args[2] if len(clean_args) > 2 else None
    
    return path, show_line_count