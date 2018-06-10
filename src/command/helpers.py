"""
Command helper utility functions
"""

import globals as GLOBALS
from utils import log

def find_actor(name: str):
    """Return an actor object with given name or None"""
    if name is None:
        return None
    log.debug('{} -> {}'.format(name, type(name)))
    name = name.capitalize()
    for a in GLOBALS.actors:
        if a.get_name() == name:
            return a
    return None


