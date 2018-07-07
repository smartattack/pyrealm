"""
Database table definitions
"""

import fnmatch
import os
from utils import log
from game_object import InstanceRegistry, instances
from world.room import Room
from command.helpers import get_room
from database.help import load_help
from database.index import load_indexes, save_indexes
from database.json import save_json_objects
from database.object import load_object, save_object
from database.game_state import GameState, save_game_state, load_game_state
import globals as GLOBALS


def boot_db():
    """Attempt to load game data from storage"""

    # Be sure GameState is initialized before we load data
    load_game_state()
    last_max_gid = GLOBALS.game_state.max_gid
    # Index may not exist - don't freak out
    try:
        load_indexes()
    except:
        pass
    rebuild_links()
    load_tables()
    load_help()
    """
    item = BaseItem(name='Magic Wand', description='A magic wand hums with a mysterious energy',
                    short_desc='magic wand')
    item.add_to_room(2)
    #save_object(item)
    """
    # Persist game_state if max_gid changed.
    if GLOBALS.game_state.max_gid > last_max_gid:
        save_game_state()



def sync_db(force=False):
    """Save changed game data, called on shutdown or checkpoint"""
    save_indexes()
    save_objects(force=force)
    # By now this is only room templates
    save_tables(force=force)
    save_game_state()


def rebuild_links():
    """Re-assign links between objects"""
    #FIXME: this is way busted
    log.info('Rebuilding game object links...')
    for gid, gobj in GLOBALS.all_instances.items():
        log.debug('  +-> %s(%s)', gobj.name, gid)
        if hasattr(gobj, 'location') and gobj.location:
            room = get_room(gobj.location)
            if room:
                if game_object_type(gobj).endswith('Item'):
                    room.add_item(gobj)
                else:
                    room.add_actor(gobj)
            else:
                log.warning('Could not find room for %s', gobj.location)
        if hasattr(gobj, 'carried_by') and gobj.carried_by:
            actor = find_actor(gid)
            if actor:
                log.debug('   ** Adding %s to %s', gobj.name, actor.name)
                actor.add_item(gobj)
                next
            # Find item (container), add item...


def save_instances(logout=False, force=False):
    """Persist all live game objects"""
    log.debug("Running save_objects")
    # For now we'll wrap to JSON, later maybe to SQLite
    save_json_objects(logout=logout, force=force)


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
    for room in GLOBALS.rooms:
        save_object(room)
