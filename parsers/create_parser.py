"""Parser for create command"""

def parse_create(args):
    """Parse create command arguments"""
    
    # args format: ['bot.py', 'create', 'backend']
    clean_args = [a for a in args if not a.startswith('--')]
    target = clean_args[2] if len(clean_args) > 2 else None
    
    return target
