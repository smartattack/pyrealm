"""
Database Object load/save
"""

import os
from utils import log
from database.json import save_to_json, load_from_json
from game_object import InstanceRegistry
import globals as GLOBALS


def save_instances(logout=False, force=False):
    """Persist all live game objects"""
    log.debug("Running save_objects")
    # For now we'll wrap to JSON, later maybe to SQLite
    pname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.INSTANCE_DIR)
    for gobj in GLOBALS.all_instances.values():
        save_object(gobj, save_dir=pname, logout=logout,
                    force=force)

def game_object_filename(gobj: object):
    """Return a filename for a given game object"""
    obj_name = ''.join([words.capitalize() for words in obj.name.split()])
    filename = game_object_type(gobj) + '_' + gobj.gid + '_' + obj_name + '.json'
    log.debug('game_object_filename would be %s', filename)
    return filename


def get_save_path(objdata, save_dir=None):
    """Return the pathname where we should save an object"""
    objtype = game_object_type(objdata)
    if hasattr(objdata, 'gid'):
        obj_id_name = str(objdata.gid)
        if save_dir:
            pathname = save_dir
        else:
            pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.INSTANCE_DIR)
        filename = os.path.join(pathname, 'gid_' + obj_id_name + '.json')
    else:
        log.debug('OBJ_ID_NAME called -> %s (%s)', objdata, objtype)
        obj_id_name = str(objdata.vnum)
        if save_dir:
            pathname = save_dir
        else:
            pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.ROOM_DIR)
        filename = os.path.join(pathname, 'vnum_' + obj_id_name + '.json')
    log.debug('SAVE DATA pathname = %s, filename = %s', pathname, filename)
    return (pathname, filename, obj_id_name)


def save_object(objdata, logout=False, save_dir=None, force=False):
    """Save object to disk"""
    # Do not save instances in items dir if owned by a room or location
    (pathname, filename, obj_id_name) = get_save_path(objdata, save_dir)
    try:
        os.makedirs(pathname, 0o755, True)
    except OSError as err:
        log.error('Failed to create directory: %s -> %s', pathname, err)
    # Update playtime on logout
    if logout and game_object_type(objdata) == 'Player':
        # update playtime duration
        if hasattr(objdata, '_playtime'):
            objdata.playtime = objdata.playtime + objdata.client.duration()
        else:
            objdata.playtime(objdata.client.duration())
    log.debug('Calling save_to_json(%s, %s, %s)', objdata.name, filename, obj_id_name)
    save_to_json(objdata, filename, obj_id_name, force=force)


def load_object(filename: str, check_collision=True):
    """Load an object and add to game data structures"""
    log.debug('FUNC load_object(%s)', filename)
    loaded = None
    template = True
    try:
        loaded = load_from_json(filename)
    except (OSError, NameError, AttributeError, KeyError) as err:
        log.error('Could not load json data: %s', err)
        return
    objtype = game_object_type(loaded)
    if hasattr(loaded, 'gid'):
        template = False
        if check_collision:
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
    if objtype == 'room':
        if template:
            log.info(' +-> Loaded object is a Room template')
            GLOBALS.rooms[loaded.vnum] = loaded
        else:
            log.info(' +-> Loaded object is a Room instance')
            GLOBALS.all_locations[loaded.gid] = loaded
        log.debug('ROOM DATA: %s', loaded)
    elif objtype == 'player':
        log.debug(' +-> Loaded object is a Player instance')
        GLOBALS.all_actors[loaded.gid] = loaded
        GLOBALS.all_players[loaded.gid] = loaded
    elif objtype == 'npc':
        if template:
            log.debug(' +-> Loaded object is a NPC template')
            GLOBALS.npcs[loaded.vnum] = loaded
        else:
            log.debug(' +-> Loaded object is a NPC instance')
            GLOBALS.all_actors[loaded.gid] = loaded
            GLOBALS.all_npcs[loaded.gid] = loaded
    elif objtype == 'item':
        if template:
            log.info(' +-> Loaded object is an Item template')
            GLOBALS.items[loaded.vnum] = loaded
        else:
            log.info(' +-> Loaded object is an Item instance')
            GLOBALS.all_items[loaded.gid] = loaded
    else:
        log.error(' +-> Unrecognized object: %s -> objtype=%s', type(loaded), objtype)
        return
    return loaded


def game_object_type(gobj: object):
    """Return the class name of the input object"""
    classname = gobj.__class__.__name__
    log.debug('Class name of %s is: %s', gobj, classname)
    if classname.endswith('Item'):
        retval = 'item'
    else:
        retval = classname.lower()
    return retval
