"""
JSON support
"""

import os
import hashlib
import time
from utils import log
from database.base import load_file, write_file, from_json, to_json, object_changed
import globals as GLOBALS



def save_to_json(objdata: object, filename: str, obj_id_name: str, force=False):
    """Save an object to JSON file"""
    # Make sure we update Player's playtime if shutting down or logging out
    data = to_json(objdata)
    checksum = make_checksum(data)
    if force or object_changed(objdata, checksum):
        # Update checksum / last saved
        objdata._checksum = checksum
        objdata._last_saved = time.time()
        write_file(data, filename)
    else:
        log.debug('   - Skipping %s: %s - NOT CHANGED', obj_id_name, type(objdata))


def load_from_json(filename):
    """Load from object from disk, return object"""
    log.debug('load_from_json(%s)', filename)
    data = load_file(filename)
    loaded = from_json(data)
    log.debug(' * Loaded object: %s', type(loaded))
    # Avoid resaving right away
    loaded._last_saved = time.time()
    loaded._checksum = hashlib.md5(data.encode('utf-8')).hexdigest()
    loaded.post_init()
    return loaded


def make_checksum(inp: str):
    """Makes a checksum hash from an input string
    Used to deduplicate objects, avoid saving unchanged data"""
    return hashlib.md5(inp.encode('utf-8')).hexdigest()