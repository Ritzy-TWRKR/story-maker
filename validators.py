# filepath: validators.py
import html

def sanitize_string(v: str) -> str:
    if not isinstance(v, str):
        raise ValueError('Must be a string')
    sanitized = html.escape(v.strip())
    if not sanitized:
        raise ValueError('Field cannot be empty')
    return sanitized