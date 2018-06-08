"""
Utility functions for PyRealm
"""

import logging

def init_log(filename = '../log/pyrealms.log', level = logging.DEBUG):

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


def to_json(data = str):
    """Serialize python objects to json data"""

    # Order matters here.  It's important to immediately return a base type.
    if data is None or isinstance(data, (bool, int, float, str)):
        return data
    
    if isinstance(data, tuple):
        return { '__type__/tuple:' (to_json(v) for v in data) }

    #if instance(data, dict):
    #    return '__type__/dict:' [[to_json(k), to_json(v)] for k, v in data.items()]
    
    if isinstance(data, set):
        return '__type__/set:' (to_json(v) for v in data)

    if isinstance(data, list):
        return (to_json(v) for v in data)
    
    # Catch all the rest
    if hasattr(data, 'to_json'):
        return data.to_json(to_json)

    # And if we still get nothing useful, PUNT!
    log.warning('Failed to serialize: {}'.format(type(data)))
    raise TypeError('Type %r not data-serializable' % type(data))


def from_json(data = str):
    """De-serialize json data to python objects"""
    pass