"""
JSON support
"""

import os
import hashlib
import time
from utils import log
from database.base import load_file, write_file, from_json, to_json, object_changed


def load_json_index():
    """Loads JSON index into GLOBALS.all_instances"""
    filename = os.path.join(GLOBALS.DATA_DIR, GLOBALS.INSTANCE_INDEX_FILE)
    temp_index = from_json(load_file(filename))
    for entry in temp_index.values():
        log.debug("Loading entry: %s", entry)
        entry_file = os.path.join(GLOBALS.DATA_DIR, GLOBALS.INSTANCE_DIR,
                                  'gid_' + entry.gid + '.json')
        # Load the object, adds to all_instances
        # Do NOT attempt to assign a unique GID
        load_object(entry_file, check_collision=False)


def save_json_index(data):
    """Saves an index to a JSON file"""
    log.debug('Running save_index_to_json()')
    write_file(to_json(data), filename=GLOBALS.INSTANCE_INDEX_FILE)


def save_json_objects(logout: bool, force: bool):
    """Persist all live game objects to json files"""
    pname = os.path.join(GLOBALS.DATA_DIR)
    for gid, gobj in GLOBALS.all_instances.items():
        save_object(gobj, save_dir=pname, logout=logout,
                    force=force)


def save_to_json(objdata: object, filename: str, obj_id_name: str, force=False):
    """Save an object to JSON file"""
    # Make sure we update Player's playtime if shutting down or logging out
    data = to_json(objdata)
    checksum = make_checksum(data)
    if force or object_changed(objdata, checksum):
        # Update checksum / last saved
        objdata._checksum = checksum
        objdata._last_saved = time.time()
        write_file(data, filename)
    else:
        log.debug('   - Skipping %s: %s - NOT CHANGED', obj_id_name, type(objdata))


def load_from_json(filename):
    """Load from object from disk, return object"""
    log.debug('load_from_json(%s)', filename)
    data = load_file(filename)
    loaded = from_json(data)
    log.debug(' * Loaded object: %s', type(loaded))
    # Avoid resaving right away
    loaded._last_saved = time.time()
    loaded._checksum = hashlib.md5(data.encode('utf-8')).hexdigest()
    loaded.post_init()
    return loaded


def make_checksum(inp: str):
    """Makes a checksum hash from an input string
    Used to deduplicate objects, avoid saving unchanged data"""
    return hashlib.md5(inp.encode('utf-8')).hexdigest()