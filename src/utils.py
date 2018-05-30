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
