"""
Database table definitions
"""

import fnmatch
import os
import time
import hashlib
#from world.room import Room
from utils import log, to_json, from_json, object_changed, make_checksum
from actor.player import Player
from actor.race import Race
from user.user import User
from actor.npc import NPC
from world.room import *
import globals as GLOBALS



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
    log.info('Loading DB tables:')
    for table_entry in GLOBALS.TABLES:
        try:
            if not table_entry['on_boot'] == True:
                continue
        except:
            continue
        log.info(' * %s', table_entry['name'])
        path = os.path.join(GLOBALS.DATA_DIR, table_entry['path'])
        filespec = table_entry['filename']
        # parse filespec for either a fixed filename of txt/json
        # or *.json, *.txt, etc
        for root, dirs, files in os.walk(path):
            for filename in fnmatch.filter(files, filespec):
                load_object(os.path.join(path, filename))


def save_tables():
    """Save database table data"""
    log.info('Saving DB tables:')
    for table_entry in GLOBALS.TABLES:
        log.info(' * %s', table_entry['name'])
        path = os.path.join(GLOBALS.DATA_DIR, table_entry['path'])
        filespec = table_entry['filename']
        name = table_entry['name']
        try:
            for item in getattr(GLOBALS, name).values():
                save_to_json(item, logout=True)
        except Exception as err:
            log.error('Could not save GLOBALS.%s : %s', name, err)


def save_to_json(save_object: object, logout=False):
    """Generic object save to json"""
    log.debug('FUNC save_to_json(%s)', save_object)
    # work around for now, maybe we need a list of actual Players
    if isinstance(save_object, User):
        save_object = save_object.player
    if isinstance(save_object, Player):
        obj_id_name = 'Player: {}'.format(save_object.name)
        pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.PLAYER_DIR)
        filename = os.path.join(pathname, obj_id_name.lower() + '.json')
        if logout:
            log.debug('+ Updating playtime for %s += %s', save_object.name, 
                      save_object.client.duration())
            # update playtime duration
            if hasattr(save_object, '_playtime'):
                save_object._playtime += save_object.client.duration()
            else:
                save_object._playtime = save_object.client.duration()
    elif isinstance(save_object, Room):
        obj_id_name = str(save_object.vnum)
        pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.ROOM_DIR)
        filename = os.path.join(pathname, obj_id_name + '.json')
    elif isinstance(save_object, Race):
        obj_id_name = save_object.name
        pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.RACE_DIR)
        filename = os.path.join(pathname, obj_id_name + '.json')
    else:
        log.error('save_to_json: Weird object encountered: %s', save_object)
        return
    try:
        os.makedirs(pathname, 0o755, True)
    except OSError as err:
        log.critical('Failed to create directory: %s -> %s', pathname, err)
    data = to_json(save_object)
    checksum = make_checksum(data)
    if object_changed(save_object, checksum) or logout:
        save_object._checksum = checksum
        save_object._last_saved = time.time()
        log.debug('OBJECT: -----> %s', save_object.__dict__)
        log.info('Saving %s: %s', type(save_object), obj_id_name)
        with open(filename, "w") as file:
            file.write(data)


def load_from_json(filename):
    """Load from object from disk, return object"""
    log.debug('load_from_json(%s)', filename)
    data = ''
    log.info('Attempting to load file: %s', filename)
    with open(filename, "r") as file:
        for line in file:
            data += line
    loaded = from_json(data)
    log.debug(' * Loaded object: %s', type(loaded))
    # Avoid resaving right away
    loaded._last_saved = time.time()
    loaded._checksum = hashlib.md5(data.encode('utf-8')).hexdigest()
    return loaded


def load_object(filename: str):
    """Load an object and add to game data structures"""
    log.debug('FUNC load_object(%s)', filename)
    loaded = None
    try:
        log.debug('from_json(%s)', filename)
        loaded = load_from_json(filename)
    except Exception as err:
        log.error('Could not load json data: %s', err)
        return
    if isinstance(loaded, Room):
        log.info(' +-> Loaded object is a Room()')
        log.debug('ROOM DATA: %s', loaded)
        GLOBALS.rooms[loaded.vnum] = loaded
    elif isinstance(loaded, Player):
        log.info(' +-> Loaded object is a Player()')
    elif isinstance(loaded, NPC):
        log.info(' +-> Loaded object is an NPC()')
    elif isinstance(loaded, Race):
        log.info(' +-> Loaded object is a Race()')
    #elif isinstance(loaded, Item):
    #    log.info(' +-> Loaded object is a and Item()')
    #    pass
    else:
        log.error(' +-> Unrecognized object: %s', type(loaded))
        return

def boot_db():
    """Attempt to load game data from storage"""
    load_tables()
    # log.debug("***** DIR_NORTH = %s", type(DIR_NORTH))

    # GLOBALS.rooms[1] = Room(vnum=1, name='Entrance', desc='A lit entryway', outside=True,
    #                         exits={DIR_NORTH: {'to_room':2}})

    # GLOBALS.rooms[2] = Room(vnum=2, name='Courtyard', desc='An empty courtyard', outside=True,
    #                         exits={DIR_SOUTH: {'to_room':1}})

    # save_to_json(GLOBALS.rooms[1], skip_list=[])
    # save_to_json(GLOBALS.rooms[2], skip_list=[])


def sync_db():
    """Save changed game data, called on shutdown or checkpoint"""
    save_tables()