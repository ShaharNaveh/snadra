import os

def is_root() -> bool:
    """
    Check if the running user have root privileges.

    Returns
    -------
    bool
        True if the effective user id is 0 (root)
    """
    return os.geteuid() == 0
