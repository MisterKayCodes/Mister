def parse_teach(args):
    """Usage: kay teach <word> <intent>"""
    if len(args) < 4:
        return None, None
    return args[2], args[3]
