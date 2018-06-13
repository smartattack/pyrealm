"""
Database table definitions
"""

import fnmatch
import os
import sys
from globals import globals


# This module should work as follows:
#
#  Read a list from GLOBALS that defines what table types to load
#  { name: str = filename   (could be glob like *.json, *.txt)
#    path: str = pathname   (relative to DATA_DIR)
#    type: str = <json|jsondir|text|textdir>
#    varname: variable name under GLOBALS in which to store the loaded data
#    update: [true/false] - do we watch for updates?  defaults true
#  }
# 
# Call boot_db which will parse this table on startup, load all tables,
# and register watchers for all the files/dirs that need to be scanned 
# for updates.
#
# Watchers will look in dirs/files and check mtime against stored last mtimes
# found at last load/boot cycle and reload any watched data newer than last rev.
#
# Reload/update will wipe the current list and reload data

def load_tables():
    """Load database tables"""
    for table_entry in GLOBALS.TABLES:
        path = os.path.join(GLOBALS.DATA_DIR, table_entry['path'])
        filespec = table_entry['filename']
        # parse filespec for either a fixed filename of txt/json
        # or *.json, *.txt, etc

            
