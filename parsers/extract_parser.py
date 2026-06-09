def parse_extract(args):
    """Usage: kay extract <file> <name> <dest>"""
    if len(args) < 5:
        return None, None, None
    return args[2], args[3], args[4]
