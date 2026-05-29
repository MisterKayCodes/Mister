"""Parser for find command"""

def parse_find(args):
    """Parse find command arguments"""
    if len(args) < 3:
        return None, None, None, None, None
    
    search_term = args[2]
    
    # Parse options
    extensions = None
    ignore_case = False
    context_lines = 0
    count_only = False
    
    i = 3
    while i < len(args):
        arg = args[i]
        
        if arg == "--ext" and i + 1 < len(args):
            ext = args[i + 1]
            if not ext.startswith('.'):
                ext = '.' + ext
            if extensions is None:
                extensions = {ext}
            else:
                extensions.add(ext)
            i += 2
        
        elif arg == "--ignore-case":
            ignore_case = True
            i += 1
        
        elif arg == "--context" and i + 1 < len(args):
            try:
                context_lines = int(args[i + 1])
            except:
                return search_term, None, None, None, "invalid_context"
            i += 2
        
        elif arg == "--count":
            count_only = True
            i += 1
        
        else:
            i += 1
    
    return search_term, extensions, ignore_case, context_lines, count_only