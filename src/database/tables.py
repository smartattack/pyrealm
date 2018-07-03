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
from item.base_item import BaseItem
from game_object import InstanceRegistry, instances
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
    #save_object(item)

    # Persist game_state if max_gid changed.
    if GLOBALS.game_state.max_gid > last_max_gid:
        save_game_state()
    
    save_instance_indexes()



def sync_db(force=False):
    """Save changed game data, called on shutdown or checkpoint"""
    save_tables(force=force)
    save_game_state()


def save_instance_indexes():
    """Persist the instance indexes"""
    print("Running save_instance_indexes()")
    for index in [index for index in GLOBALS.__dir__() if index.startswith('all_')]:
        save_index(getattr(GLOBALS, index))


def save_index(index):
    """Attempt to serialize one instance index"""
    data = []
    for instance in index.values():
        data.append({ 'gid':instance.gid, 'itype':type(instance), 'name':instance.name })
    data = to_json(data)
    print("index({}) == \n{}\n\n".format(index, data))
    return data
    

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


def save_tables(force=False):
    """Save database table data"""
    log.info('Saving DB tables:')
    for table_entry in GLOBALS.TABLES:
        log.info(' +-> %s', table_entry['name'])
        path = os.path.join(GLOBALS.DATA_DIR, table_entry['path'])
        filespec = table_entry['filename']
        name = table_entry['name']
        for player in GLOBALS.all_players:
            save_object(player)
        for inst in GLOBALS.all_items:
            save_object(item)
        for room in GLOBALS.rooms:
            save_object(room)


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


def objtype(input: object):
    """Return the class name of the input object"""
    retval = input.__class__.__name__
    log.debug('OBJTYPE of %s is: %s', input, retval)
    return retval


def get_save_path(objdata, save_dir=None):
    """Return the pathname where we should save an object"""
    # FIXME: nested items should have parent dir passed in
        # work around for now, maybe we need a list of actual Players
    type = objtype(objdata)
    if hasattr(objdata, 'gid'):
        obj_id_name = str(objdata.gid)
        if type == 'BaseItem':
            log.debug('Saving Item instance %s', obj_id_name)
            pname = GLOBALS.ITEM_DIR
        elif type == 'Room':
            log.debug('Saving Room instance %s', obj_id_name)
            pname = GLOBALS.ROOM_DIR
        elif type == 'Room':
            # A player is always an instance
            # Here we create a dir for the player and save the player within it
            obj_id_name = objdata.name.lower()
            log.debug('Saving Player instance %s', obj_id_name)
            pname = GLOBALS.PLAYER_DIR + '/' + obj_id_name
        else:
            log.error('get_save_path(): Weird object encountered: %s', objdata)
            return
        if save_dir:
            pathname = save_dir
        else:
            pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.INSTANCE_DIR, pname)
    else:
        obj_id_name = str(objdata.vnum)
        if type == 'BaseItem':
            log.debug('Saving Item template %s', obj_id_name)
            pname = GLOBALS.ITEM_DIR
        elif type == 'Room':
            log.debug('Saving Room template %s', obj_id_name)
            pname = GLOBALS.ROOM_DIR
        else:
            log.error('get_save_path(): Weird object encountered: %s', objdata)
            return            
        if save_dir:
            pathname = save_dir
        else:
            pathname = os.path.join(GLOBALS.DATA_DIR, pname)
    filename = os.path.join(pathname, obj_id_name + '.json')
    log.debug('SAVE DATA pathname = %s, filename = %s', pathname, filename)
    return (pathname, filename, obj_id_name)


def save_object(objdata, logout=False, save_dir=None, force=False):
    """Save object to disk:
    Automatically detects object type and does appropriate save for type.
    If object has containers, it should save nested objects, also.
    Objects may be either templates or instances.  Templates save to
    separate directories than instances and lack an instance_id but have
    a template id (vnum).
    Room, NPC, Player instances save items in a nested folder under the
    parent instance (nested containers in inventory are flattened on save)
    """
    # Do not save instances in items dir if owned by a room or location
    try:
        if not save_dir:
            if objdata.carried_by or objdata.worn_by or objdata.location:
                log.debug('save_object: Skipping %s: this object is owned', objdata.name)
                return
    except:
        pass
    (pathname, filename, obj_id_name) = get_save_path(objdata, save_dir)
    try:
        os.makedirs(pathname, 0o755, True)
    except OSError as err:
        log.error('Failed to create directory: %s -> %s', pathname, err)
    # Update playtime on logout
    if logout and objtype(objdata) == 'Player':
        log.debug('   + Updating playtime for %s += %s', objdata.name, 
                  objdata.client.duration())
        # update playtime duration
        if hasattr(objdata, '_playtime'):
            objdata._playtime += objdata.client.duration()
        else:
            objdata._playtime = objdata.client.duration()
    log.debug('Calling save_to_json(%s, %s, %s)', objdata.name, filename, obj_id_name)
    save_to_json(objdata, filename, obj_id_name, force=True)
    # Handle nested objects that need saving
    try:
        child_dir = os.path.join(pathname, GLOBALS.ITEM_DIR)
        # Clean child dir first, ensures we don't save dropped items
        try:
            os.remove(child_dir)
        except OSError as err:
            log.error('Failed to remove child dir: %s', child_dir)
        for item in objdata.inventory:
            log.debug(' +-> Saving inventory item %s', item.name)
            save_object(item, save_dir=child_dir, force=True)
    except:
        pass
    try:
        try:
            os.remove(child_dir)
        except OSError as err:
            log.error('Failed to remove child dir: %s', child_dir)
        child_dir = os.path.join(pathname, GLOBALS.EQUIP_DIR)
        for item in objdata.worn:
            log.debug(' +-> Saving worn item %s', item.name)
            save_object(item, parent_dir=child_dir)
    except:
        pass




def save_to_json(objdata: object, filename: str, obj_id_name: str, force=False):
    """Save an object to JSON file"""
    # Make sure we update Player's playtime if shutting down or logging out
    data = to_json(objdata)
    checksum = make_checksum(data)
    # TODO: if logout, duration was calculated and therefore object should
    # have changed. TEST ME!
    #if object_changed(objdata, checksum) or logout:
    if force or object_changed(objdata, checksum):
        objdata._checksum = checksum
        objdata._last_saved = time.time()
        #log.debug('OBJECT: -----> %s', objdata.__dict__)
        log.info('   + Saving %s: %s', obj_id_name, type(objdata))
        with open(filename, "w") as file:
            file.write(data)
    else:
        log.debug('   - Skipping %s: %s - NOT CHANGED', obj_id_name, type(objdata))


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
    type = objtype(loaded)
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
    if type == 'Room':
        if template:
            log.info(' +-> Loaded object is a Room template')
            GLOBALS.rooms[loaded.vnum] = loaded
        else:
            log.info(' +-> Loaded object is a Room instance')
            GLOBALS.all_locations[loaded.gid] = loaded
        log.debug('ROOM DATA: %s', loaded)
    elif type == 'Player':
        if template:
            log.error(' +-> Loaded object is a Player template (ERROR!)')
        else:
            log.info(' +-> Loaded object is a Player instance')
            GLOBALS.all_actors[loaded.gid] = loaded
            GLOBALS.all_players[loaded.gid] = loaded
    elif type == 'NPC':
        if template:
            log.info(' +-> Loaded object is a NPC template')
            GLOBALS.npcs[loaded.vnum] = loaded
        else:
            log.info(' +-> Loaded object is a NPC instance')
            GLOBALS.all_actors[loaded.gid] = loaded
            GLOBALS.all_npcs[loaded.gid] = loaded
    elif type == 'Race':
        log.info(' +-> Loaded Race()')
        # FIXME: implement something here
    elif type == 'BaseItem':
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