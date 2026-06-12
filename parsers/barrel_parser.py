"""Parser for barrel command"""

def parse_barrel(args):
    """Parse barrel command arguments"""
    if len(args) < 3:
        return None
    return args[2]
