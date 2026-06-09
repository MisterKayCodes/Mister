def parse_analyze(args):
    """Usage: kay analyze <file>"""
    if len(args) < 3:
        return None
    return args[2]
