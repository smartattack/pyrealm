"""
Utility functions for PyRealm
"""

import logging

def init_log(filename = '../log/pyrealms.log'):

        log = logging.getLogger('self.log')
        log.setLevel(logging.DEBUG)
        fh = logging.FileHandler(filename)
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        log.addHandler(fh)
        return log
