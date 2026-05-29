"""Parser for listen command"""

def parse_listen(args):
    """
    Parse listen command arguments.
    Listen command takes no arguments.
    Returns True if valid.
    """
    # listen command has no arguments
    # Just check if there are too many
    if len(args) > 2:
        return False
    return True