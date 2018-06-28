"""
Database table definitions
"""

import fnmatch
import os
import time
import copy
import hashlib
import jsonpickle
from utils import log
from actor.player import Player
from actor.race import Race
from user.user import User
from actor.npc import NPC
from item.base_item import BaseItem
from game_object import InstanceRegistry, instances
from world.room import Room
from database.game_state import GameState
import globals as GLOBALS



def boot_db():
    """Attempt to load game data from storage"""

    # Be sure GameState is initialized before we load data
    load_game_state()
    last_max_gid = GLOBALS.game_state.max_gid
    load_tables()
    load_help()
    item = BaseItem(name='Magic Wand', description='A magic wand hums with a mysterious energy',
                    short_desc='magic wand')
    item.add_to_room(2)
    save_to_json(item)

    # Persist game_state if max_gid changed.
    if GLOBALS.game_state.max_gid > last_max_gid:
        save_game_state()


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
        except (KeyError, AttributeError):
            continue
        path = os.path.join(GLOBALS.DATA_DIR, table_entry['path'])
        log.info(' +-> %s, scanning path %s', table_entry['name'], path)
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
        log.info(' +-> %s', table_entry['name'])
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


def load_game_state():
    """Load or initialize game state"""
    global InstanceRegistry
    try:
        state_file = os.path.join(GLOBALS.DATA_DIR, GLOBALS.STATE_DIR,
                                  'state.json')
        GLOBALS.game_state = load_from_json(state_file)
        log.info('Game state, max_gid = %s, runtime = %s',
                  GLOBALS.game_state.max_gid, GLOBALS.game_state.runtime)
    except Exception as err:
        log.warning('Game state data not found, initializing... %s', err)
        GLOBALS.game_state = GameState()
    # Sync gid counters
    GLOBALS.game_state.max_gid = InstanceRegistry.gid = max(InstanceRegistry.gid,
                                                     GLOBALS.game_state.max_gid)
    log.debug('AFTER SYNC: GLOBALS.game_state.max_gid=%s, InstanceRegistry.gid=%s',
              GLOBALS.game_state.max_gid, InstanceRegistry.gid)


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


def get_save_path(save_object):
    """Return the pathname where we should save an object"""
    # FIXME: nested items should have parent dir passed in
        # work around for now, maybe we need a list of actual Players
    if hasattr(save_object, 'gid'):
        obj_id_name = str(save_object.gid)
        if isinstance(save_object, BaseItem):
            log.debug('Saving Item instance %s', obj_id_name)
            pname = GLOBALS.ITEM_DIR
        elif isinstance(save_object, Room):
            log.debug('Saving Room instance %s', obj_id_name)
            pname = GLOBALS.ROOM_DIR
        elif isinstance(save_object, Player):
            # A player is always an instance
            # Here we create a dir for the player and save the player within it
            obj_id_name = save_object.name.lower()
            log.debug('Saving Player instance %s', obj_id_name)
            pname = GLOBALS.PLAYER_DIR + '/' + obj_id_name
        else:
            log.error('save_to_json: Weird object encountered: %s', save_object)
            return
        pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.INSTANCE_DIR, pname)
    else:
        obj_id_name = str(save_object.vnum)
        if isinstance(save_object, BaseItem):
            log.debug('Saving Item template %s', obj_id_name)
            pname = GLOBALS.ITEM_DIR
        elif isinstance(save_object, Room):
            log.debug('Saving Room template %s', obj_id_name)
            pname = GLOBALS.ROOM_DIR
        elif isinstance(save_object, Race):
            log.debug('Saving Race instance %s', obj_id_name)
            pname = GLOBALS.RACE_DIR
        else:
            log.error('save_to_json: Weird object encountered: %s', save_object)
            return            
        pathname = os.path.join(GLOBALS.DATA_DIR, pname)
    filename = os.path.join(pathname, obj_id_name + '.json')
    log.debug('SAVE DATA pathname = %s, filename = %s', pathname, filename)
    return (pathname, filename, obj_id_name)


def save_to_json(save_object: object, logout=False):
    """Save an object to JSON file
    Automatically detects object type and does appropriate save for type.
    If object has containers, it should save the items as needed, also.
    Objects may be either templates or instances.  Templates save to
    separate directories than instances and lack an instance_id but have
    a template id (vnum).
    Room, NPC, Player instances save items in a nested folder under the
    parent instance (nested containers in inventory are flattened on save)
    """

    (pathname, filename, obj_id_name) = get_save_path(save_object)
    # Make sure we update Player's playtime if shutting down or logging out
    if logout and isinstance(save_object, Player):
        log.debug('   + Updating playtime for %s += %s', save_object.name, 
                  save_object.client.duration())
        # update playtime duration
        if hasattr(save_object, '_playtime'):
            save_object._playtime += save_object.client.duration()
        else:
            save_object._playtime = save_object.client.duration()
    try:
        os.makedirs(pathname, 0o755, True)
    except OSError as err:
        log.critical('Failed to create directory: %s -> %s', pathname, err)
    data = to_json(save_object)
    checksum = make_checksum(data)
    # TODO: if logout, duration was calculated and therefore object should
    # have changed. TEST ME!
    #if object_changed(save_object, checksum) or logout:
    if object_changed(save_object, checksum):
        save_object._checksum = checksum
        save_object._last_saved = time.time()
        #log.debug('OBJECT: -----> %s', save_object.__dict__)
        log.info('   + Saving %s: %s', obj_id_name, type(save_object))
        with open(filename, "w") as file:
            file.write(data)
    else:
        log.debug('   - Skipping %s: %s - NOT CHANGED', obj_id_name, type(save_object))


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
    template = True
    try:
        log.debug('from_json(%s)', filename)
        loaded = load_from_json(filename)
    except Exception as err:
        log.error('Could not load json data: %s', err)
        return
    if hasattr(loaded, 'gid'):
        template = False
        if loaded.gid in GLOBALS.all_instances:
            log.warning('GID collision: %s, assigning new gid', loaded.gid)
            InstanceRegistry.track(loaded)
            log.info('New GID: %s', loaded.gid)
        current_max_gid = max(GLOBALS.game_state.max_gid, InstanceRegistry.gid)
        if loaded.gid > current_max_gid:
            log.error('Loaded object %s(%s) > %s', loaded.gid, type(loaded),
            current_max_gid)
            GLOBALS.game_state.max_gid = InstanceRegistry.gid = loaded.gid
        GLOBALS.all_instances[loaded.gid] = loaded
    if isinstance(loaded, Room):
        if template:
            log.info(' +-> Loaded object is a Room template')
            GLOBALS.rooms[loaded.vnum] = loaded
        else:
            log.info(' +-> Loaded object is a Room instance')
            GLOBALS.all_locations[loaded.gid] = loaded
        log.debug('ROOM DATA: %s', loaded)
    elif isinstance(loaded, Player):
        if template:
            log.error(' +-> Loaded object is a Player template (ERROR!)')
        else:
            log.info(' +-> Loaded object is a Player instance')
            GLOBALS.all_actors[loaded.gid] = loaded
            GLOBALS.all_players[loaded.gid] = loaded
    elif isinstance(loaded, NPC):
        if template:
            log.info(' +-> Loaded object is a NPC template')
            GLOBALS.npcs[loaded.vnum] = loaded
        else:
            log.info(' +-> Loaded object is a NPC instance')
            GLOBALS.all_actors[loaded.gid] = loaded
            GLOBALS.all_npcs[loaded.gid] = loaded
    elif isinstance(loaded, Race):
        log.info(' +-> Loaded Race()')
        # FIXME: implement something here
    elif isinstance(loaded, BaseItem):
        if template:
            log.info(' +-> Loaded object is an Item template')
            GLOBALS.items[loaded.vnum] = loaded
        else:
            log.info(' +-> Loaded object is an Item instance')
            GLOBALS.all_items[loaded.gid] = loaded
    else:
        log.error(' +-> Unrecognized object: %s', type(loaded))
        return
    return loaded


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
        log.debug('Input = %s', inp)
        return jsonpickle.decode(inp, keys=True)
    except Exception as err:
        raise AttributeError('Could not deserialize JSON: {}'.format(err))


def make_checksum(inp: str):
    """Makes a checksum hash from an input string
    Used to deduplicate objects, avoid saving unchanged data"""
    return hashlib.md5(inp.encode('utf-8')).hexdigest()


def object_changed(test_obj: object, checksum: str):
    """Compare the object._checksum, if present, against checksum arg
    Return false if not changed.
    If no checksum present or checksum changed return true"""
    if hasattr(test_obj, '_checksum'):
        if test_obj._checksum == checksum:
            log.debug('Testing object_changed: %s == %s', type(object), False)
            return False
    log.debug('Testing object_changed: %s == %s', type(object), True)
    return True