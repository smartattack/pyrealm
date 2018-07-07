"""
Database Object load/save
"""

import os
import time
from utils import log
from database.json import save_to_json, load_from_json
import globals as GLOBALS


def get_save_path(objdata, save_dir=None):
    """Return the pathname where we should save an object"""
    # FIXME: nested items should have parent dir passed in
        # work around for now, maybe we need a list of actual Players
    type = game_object_type(objdata)
    if hasattr(objdata, 'gid'):
        obj_id_name = str(objdata.gid)
        if save_dir:
            pathname = save_dir
        else:
            pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.INSTANCE_DIR)
        filename = os.path.join(pathname, 'gid_' + obj_id_name + '.json')
    else:
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
        log.debug('   + Updating playtime for %s += %s', objdata.name, 
                  objdata.client.duration())
        # update playtime duration
        if hasattr(objdata, '_playtime'):
            objdata._playtime += objdata.client.duration()
        else:
            objdata._playtime = objdata.client.duration()
    log.debug('Calling save_to_json(%s, %s, %s)', objdata.name, filename, obj_id_name)
    save_to_json(objdata, filename, obj_id_name, force=True)
 

def load_object(filename: str, check_collision=True):
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
    objtype = game_object_type(loaded)
    log.debug("------------> TYPE==", objtype)
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
    if objtype == 'Room':
        if template:
            log.info(' +-> Loaded object is a Room template')
            GLOBALS.rooms[loaded.vnum] = loaded
        else:
            log.info(' +-> Loaded object is a Room instance')
            GLOBALS.all_locations[loaded.gid] = loaded
        log.debug('ROOM DATA: %s', loaded)
    elif objtype == 'Player':
        if template:
            log.error(' +-> Loaded object is a Player template (ERROR!)')
        else:
            log.info(' +-> Loaded object is a Player instance')
            GLOBALS.all_actors[loaded.gid] = loaded
            GLOBALS.all_players[loaded.gid] = loaded
    elif objtype == 'NPC':
        if template:
            log.info(' +-> Loaded object is a NPC template')
            GLOBALS.npcs[loaded.vnum] = loaded
        else:
            log.info(' +-> Loaded object is a NPC instance')
            GLOBALS.all_actors[loaded.gid] = loaded
            GLOBALS.all_npcs[loaded.gid] = loaded
    elif objtype == 'Race':
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


def game_object_type(input: object):
    """Return the class name of the input object"""
    retval = input.__class__.__name__
    log.debug('OBJTYPE of %s is: %s', input, retval)
    return retval