"""
Utility functions for PyRealm
"""

import logging
import copy
import hashlib
import json
import jsonpickle


def init_log(filename='log/pyrealm.log', level=logging.DEBUG):
    """Called only once in main to give us consistent logging"""
    log = logging.getLogger('self.log')
    log.setLevel(level)
    file = logging.FileHandler(filename)
    if level == logging.DEBUG:
        file.setFormatter(logging.Formatter(
            '%(asctime)s %(filename)s:%(lineno)s %(levelname)s: %(message)s'))
    else:
        file.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'))
    log.addHandler(file)
    return log


# I will be global
log = init_log()


def to_json(target: object, skip_list=None):
    """Create a Player() with select fields
    and serialize to JSON"""

    if skip_list is None:
        skip_list = []
    p = copy.copy(target)
    for i in skip_list:
        log.debug('skip_list: %s', i)
        try:
            delattr(p, i)
        except AttributeError:
            pass
    # jsonpickle does the serialization we need, but
    # to pretty print it to disk, we have to loads/dumps again
    jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
    jsonpickle.set_preferred_backend('simplejson')
    return jsonpickle.encode(p, keys=True)
#    return json.dumps(json.loads(jsonpickle.encode(p), ),
#                      indent=4, sort_keys=True)



def from_json(inp=str):
    """Deserialize JSON data and return object(s)"""
    try:
        return jsonpickle.decode(inp, keys=True)
    except:
        raise AttributeError('Could not deserialize JSON')


def make_checksum(inp: str):
    """Makes a checksum hash from an input string
    Used to deduplicate objects, avoid saving unchanged data"""
    return hashlib.md5(inp.encode('utf-8')).hexdigest()


def object_changed(test_obj: object, checksum: str):
    """Compare the object._checksum, if present, against checksum arg
    Return false if not changed.
    If no checksum present or checksum changed return true"""
    if hasattr(test_obj, '_checksum'):
        if test_obj._checksum == checksum:
            log.debug('Testing object_changed: %s == %s', type(object), False)
            return False
    log.debug('Testing object_changed: %s == %s', type(object), True)
    return True


def stat_color(current: int, maximum: int):
    """Provide color code based on stat % of max"""
    # Get ratio, avoid divide by zero
    stat_ratio = float(current / (maximum + .0001))
    if stat_ratio < 0.25:
        return '^R'
    elif stat_ratio < 0.5:
        return '^Y'
    else:
        return '^G'


def calc_xp(level):
    """Return XP for a given level"""
    log.debug('FUNC calc_xp()')
    # Some coefficients: 150 -2 200,   100 -2 200
    a, b, c = 10, -2, 200
    return int((a * level) ** 2 + b * level + c)


def xp_to_level(current_level, current_xp):
    """Find XP needed to reach the next level"""
    log.debug('FUNC xp_to_level()')
    return calc_xp(current_level+1) - current_xp
