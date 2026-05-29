"""Parser for scan command"""

def parse_scan(args):
    """Parse scan command arguments"""
    path = args[2] if len(args) > 2 else None
    return path