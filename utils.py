import re

def find_matches(pattern, text):
    """
    Returns all matches of a regex pattern.
    """
    return re.findall(pattern, text)