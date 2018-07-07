"""
Database Index load/save
"""

import os
from utils import log
from database.json import from_json, to_json
from database.base import load_file, write_file
from database.object import load_object
import globals as GLOBALS

def load_indexes():
    """Load persisted instance indexes"""
    log.debug("Running load_indexes()")
    load_json_index()


def save_indexes():
    """Persist the instance indexes"""
    log.debug("Running save_indexes()")
    data = []
    for instance in GLOBALS.all_instances.values():
        log.debug('SAVE_INDEXES: ++ %s', instance)
        data.append({ 'gid':instance.gid, 'itype':type(instance), 'name':instance.name })
    # Save to JSON for now, maybe SQLite later
    save_json_index(data)


def load_json_index():
    """Loads JSON index into GLOBALS.all_instances"""
    log.debug('Running load_json_index()')
    filename = os.path.join(GLOBALS.DATA_DIR, GLOBALS.INSTANCE_INDEX_FILE)
    try:
        temp_index = from_json(load_file(filename))
    except Exception as err:
        log.error('Exception: %s', err)
    log.debug('Loaded temp_index == %s (%s)', temp_index, type(temp_index))
    for entry in temp_index:
        log.debug("Loading entry: %s", entry)
        entry_file = os.path.join(GLOBALS.DATA_DIR, GLOBALS.INSTANCE_DIR,
                                  'gid_' + str(entry['gid']) + '.json')
        try:
            gobj = load_object(entry_file, check_collision=False)
        except Exception as err:
            log.error('FAILED: %s', err)


def save_json_index(data):
    """Saves an index to a JSON file"""
    log.debug('Running save_index_to_json()')
    filename = os.path.join(GLOBALS.DATA_DIR, GLOBALS.INSTANCE_INDEX_FILE)
    write_file(to_json(data), filename=filename)
