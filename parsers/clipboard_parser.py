"""Parser for clipboard commands"""


def parse_copy(args):
    """
    Parse copy command arguments
    
    Args:
        args: sys.argv
        
    Returns:
        tuple: (file_path, error_msg)
    """
    if len(args) < 3:
        return None, "Please provide a file to copy"
    
    file_path = args[2]
    return file_path, None


def parse_paste(args):
    """
    Parse paste command arguments
    
    Args:
        args: sys.argv
        
    Returns:
        tuple: (file_path, preview, undo, error_msg)
    """
    file_path = None
    preview = False
    undo = False
    
    # Parse options and file path
    for i, arg in enumerate(args[2:]):
        if arg == "--preview":
            preview = True
        elif arg == "--undo":
            undo = True
        elif not arg.startswith("--"):
            # This is the file path
            file_path = arg
    
    return file_path, preview, undo, None
