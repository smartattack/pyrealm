"""
Utility functions for PyRealm
"""

import logging
import jsonpickle
import json
import copy
import hashlib


def init_log(filename = 'log/pyrealm.log', level = logging.DEBUG):
        """Called only once in main to give us consistent logging"""
        log = logging.getLogger('self.log')
        log.setLevel(level)
        fh = logging.FileHandler(filename)
        if level == logging.DEBUG:
            fh.setFormatter(logging.Formatter('%(asctime)s %(filename)s:%(lineno)s %(levelname)s: %(message)s'))
        else:
            fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        log.addHandler(fh)
        return log


# I will be global
log = init_log()


def to_json(target: object, skip_list = []):
    """Create a Player() with select fields
    and serialize to JSON"""

    p = copy.copy(target)
    assert isinstance(skip_list, list)
    for i in skip_list:
        log.debug('skip_list: {}'.format(i))
        try:
            delattr(p, i)
        except:
            pass
    # jsonpickle does the serialization we need, but
    # to pretty print it to disk, we have to loads/dumps again
    return json.dumps(json.loads(jsonpickle.encode(p)), indent=4, sort_keys=True)


def from_json(input = str):
    """Deserialize JSON data and return object(s)"""
    try:
        return jsonpickle.decode(input)
    except:
        raise AttributeError('Could not deserialize JSON')


def make_checksum(input: str):
    """Makes a checksum hash from an input string
    Used to deduplicate objects, avoid saving unchanged data"""
    return hashlib.md5(input.encode('utf-8')).hexdigest()


def object_changed(test_obj: object, checksum: str):
    """Compare the object._checksum, if present, against checksum arg
    Return false if not changed.
    If no checksum present or checksum changed return true"""
    if hasattr(test_obj, '_checksum'):
        if test_obj._checksum == checksum:
            log.debug('Testing object_changed: {}: {}'.format(type(object), False))
            return False
    log.debug('Testing object_changed: {}: {}'.format(type(object), True))
    return True

