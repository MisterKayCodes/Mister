def parse_bundle(args):
    """Usage: kay bundle file1.py file2.py ...
    Returns list of file paths or None if no files given.
    """
    if len(args) < 3:
        return None
    return args[2:]  # everything after 'bundle'
