"""Parser for read command"""

def parse_read(args):
    """Parse read command arguments"""
    if len(args) < 3:
        return None, None, None
    
    file_path = args[2]
    show_lines = "--lines" in args
    
    # Check for line range (e.g., "10-25")
    line_range = None
    for arg in args[3:]:
        if "-" in arg and not arg.startswith("--"):
            try:
                parts = arg.split("-")
                start = int(parts[0])
                end = int(parts[1])
                line_range = (start, end)
            except:
                return file_path, show_lines, "invalid_range"
    
    return file_path, show_lines, line_range