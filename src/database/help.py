"""
Help file support
"""

import os
from utils import log
import globals as GLOBALS


def load_help():
    """Load help files"""
    pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.HELP_DIR)
    log.info('Loading help files...')
    filespec = '*'
    for root, dirs, files in os.walk(pathname):
        for filename in files:
            try:
                helpfile = os.path.join(pathname, filename)
                data = ''
                with open(helpfile, 'r') as file:
                    for line in file:
                        data += line
                GLOBALS.helps[filename] = data
                log.info(' +-> loaded "%s"', filename)
            except Exception as err:
                log.warning(' +-> ERROR loading "%s": %s', filename, err)