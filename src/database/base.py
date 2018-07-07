"""
Basic File I/O operations
Used by the rest of the database module
"""

import copy
import jsonpickle
from utils import log


def write_file(data: str, filename: str):
    """Write string to disk, no other processing"""
    log.debug('   + Saving %s: %s', filename, type(data))
    with open(filename, "w") as file:
        file.write(data)


def load_file(filename: str):
    """Load a file from disk, no other processing, return string"""
    data = ''
    log.debug('Attempting to load file: %s', filename)
    with open(filename, "r") as file:
        for line in file:
            data += line
    return data


def to_json(target: object):
    """Create a Player() with select fields and serialize to JSON"""
    try:
        log.debug('skip_list imported for target: %s, SKIP_LIST: %s', target, target._skip_list)
        skip_list = target._skip_list
    except:
        log.debug('No skip_list found for target: %s', target)
        skip_list = []
    p = copy.copy(target)
    for i in skip_list:
        log.debug(' +-> skip_list: %s', i)
        try:
            delattr(p, i)
        except AttributeError:
            pass
    # format to make more legible
    jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
    jsonpickle.set_preferred_backend('simplejson')
    return jsonpickle.encode(p, keys=True)


def from_json(inp=str):
    """Deserialize JSON data and return object(s)"""
    try:
        #log.debug('Input = %s', inp)
        return jsonpickle.decode(inp, keys=True)
    except Exception as err:
        raise AttributeError('Could not deserialize JSON: {}'.format(err))


def object_changed(test_obj: object, checksum: str):
    """Compare the object._checksum, if present, against checksum arg
    Return false if not changed.
    If no checksum present or checksum changed return true"""
    if hasattr(test_obj, '_checksum'):
        if test_obj._checksum == checksum:
            return False
    return True