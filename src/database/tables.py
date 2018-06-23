"""
Database table definitions
"""

import fnmatch
import os
import time
import hashlib
import jsonpickle
from utils import log, object_changed, make_checksum
from actor.player import Player
from actor.race import Race
from user.user import User
from actor.npc import NPC
from world.room import *
from database.game_state import GameState
from item.base_item import BaseItem
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


def boot_db():
    """Attempt to load game data from storage"""
    load_tables()
    try:
        state_file = os.path.join(GLOBALS.DATA_DIR, GLOBALS.STATE_DIR, 'state.json')
        GLOBALS.game_state = load_from_json(state_file)
    except Exception as err:
        log.warning('Game state data not found, initializing... %s', err)
        GLOBALS.game_state = GameState()
    
    item = BaseItem(name='Magic Wand', description='A magic wand hums with a mysterious energy',
                    short_desc='magic wand')
    item.add_to_room(2)
    

    # log.debug("***** DIR_NORTH = %s", type(DIR_NORTH))
    """
    GLOBALS.rooms[1] = Room(vnum=1, name='Entrance', desc='A lit entryway', outside=True,
                            exits={DIR_NORTH: {'to_room':2}})

    GLOBALS.rooms[2] = Room(vnum=2, name='Courtyard', desc='An empty courtyard', outside=True,
                            exits={DIR_SOUTH: {'to_room':1}})

    GLOBALS.rooms[3] = Room(vnum=3, name='CircleZone', description='A test room with exits', outside=True,
    exits={0:{'to_room':1},1:{'to_room':1},2:{'to_room':1},3:{'to_room':1},4:{'to_room':1},5:{'to_room':1},6:{'to_room':1},7:{'to_room':1},8:{'to_room':1}})

    save_to_json(GLOBALS.rooms[1])
    save_to_json(GLOBALS.rooms[2])
    save_to_json(GLOBALS.rooms[3])
    """


def sync_db():
    """Save changed game data, called on shutdown or checkpoint"""
    save_tables()
    save_game_state()


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


def save_game_state():
    """Save global game state to disk, called on shutdown or checkpoint"""
    log.debug('FUNC save_game_state()')
    pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.STATE_DIR)
    filename = os.path.join(pathname, 'state.json')
    try:
        os.makedirs(pathname, 0o755, True)
    except OSError as err:
        log.critical('Failed to create directory: %s -> %s', pathname, err)
    data = to_json(GLOBALS.game_state)
    log.info('Saving game state')
    with open(filename, "w") as file:
        file.write(data)


def save_to_json(save_object: object, logout=False):
    """Generic object save to json"""
    log.debug('FUNC save_to_json(%s)', save_object)
    # work around for now, maybe we need a list of actual Players
    if isinstance(save_object, User):
        save_object = save_object.player
    if isinstance(save_object, Player):
        obj_id_name = save_object.name.lower()
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
    loaded.post_init()
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
        log.info(' +-> Loaded Player()')
    elif isinstance(loaded, NPC):
        log.info(' +-> Loaded NPC()')
    elif isinstance(loaded, Race):
        log.info(' +-> Loaded Race()')
    #elif isinstance(loaded, Item):
    #    log.info(' +-> Loaded object is a and Item()')
    #    pass
    else:
        log.error(' +-> Unrecognized object: %s', type(loaded))
        return


def to_json(target: object):
    """Create a Player() with select fields and serialize to JSON"""

    try:
        log.debug('SKIP LIST IMPORTED FOR TARGET: %s, SKIP_LIST: %s', target, target._skip_list)
        skip_list = target._skip_list
    except:
        log.debug('NO SKIP LIST FOR TARGET: %s', target)
        skip_list = []
    p = copy.copy(target)
    for i in skip_list:
        log.debug('skip_list: %s', i)
        try:
            delattr(p, i)
        except AttributeError:
            pass
    # format to make more legible
    jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
    jsonpickle.set_preferred_backend('simplejson')
    return jsonpickle.encode(p, keys=True)


def from_json(inp=str):
    """Deserialize JSON data and return object(s)"""
    try:
        log.error('Input = %s', inp)
        return jsonpickle.decode(inp, keys=True)
    except Exception as err:
        raise AttributeError('Could not deserialize JSON: {}'.format(err))
