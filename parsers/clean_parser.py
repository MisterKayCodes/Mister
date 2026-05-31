"""Parser for clean command"""

def parse_clean(args):
    """
    Parse clean command arguments
    Returns (dry_run, backups, temp)
    """
    dry_run = "--dry-run" in args
    backups = "--backups" in args
    temp = "--temp" in args
    
    return dry_run, backups, temp