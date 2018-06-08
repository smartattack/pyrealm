"""
Utility functions for PyRealm
"""

import logging
import jsonpickle
import json

def init_log(filename = '../log/pyrealms.log', level = logging.DEBUG):
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


def to_json(skip_list = None):
    """Create a Player() with select fields
    and serialize to JSON"""

    p = copy.copy(self)
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