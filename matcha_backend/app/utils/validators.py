# app/utils/validators.py

import re


def validate_username(username: str) -> tuple[bool, str]:
    """
    Validate username format
    Returns: (is_valid, error_message)
    """
    if len(username) > 12:
        return False, "Username must be 12 characters or less"
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password format
    Returns: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, ""