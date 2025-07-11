FUNC = print

def log(what:str, level:int=0, func=FUNC):
    """
    Custom logging function - just for my purposes.
    
    0 - info
    1 - warning
    2 - error
    """
    prefix:str = ""

    match level:
        case 0:
            prefix = "INFO: "
        case 1:
            prefix = "WARNING: "
        case 2:
            prefix = "ERROR: "
        case _:
            raise ValueError("Invalid logging level")
        
    func(f"{prefix}{what}")

