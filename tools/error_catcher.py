"""Error Catcher - Hands that save and load crash errors"""

import os

# Path to store the last error
MEMORY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "memory")
ERROR_FILE = os.path.join(MEMORY_DIR, "last_error.txt")

def save_error(error_text):
    """Save error text to memory"""
    # Make sure memory folder exists
    os.makedirs(MEMORY_DIR, exist_ok=True)
    
    # Save the error
    with open(ERROR_FILE, 'w', encoding='utf-8') as f:
        f.write(error_text)
    
    return True

def get_last_error():
    """Get the last saved error"""
    if not os.path.exists(ERROR_FILE):
        return None
    
    with open(ERROR_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def has_error():
    """Check if there's a saved error"""
    return os.path.exists(ERROR_FILE)

def clear_error():
    """Clear the saved error"""
    if os.path.exists(ERROR_FILE):
        os.remove(ERROR_FILE)