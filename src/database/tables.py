"""
Database table definitions
"""

import fnmatch
import os
from utils import log
from command.helpers import get_room, find_actor
from database.help import load_help
from database.index import load_indexes, save_indexes
from database.object import load_object, save_object, save_instances, game_object_type
from database.game_state import save_game_state, load_game_state
from game_object import get_instance
from database.populate import populate
import globals as GLOBALS


def boot_db():
    """Attempt to load game data from storage"""

    # Be sure GameState is initialized before we load data
    load_game_state()
    last_max_gid = GLOBALS.game_state.max_gid
    # Index may not exist - don't freak out
    load_tables()
    try:
        load_indexes()
    except FileNotFoundError:
        pass
    rebuild_links()
    load_help()

    populate()

    # Persist game_state if max_gid changed.
    if GLOBALS.game_state.max_gid > last_max_gid:
        save_game_state()


def sync_db(force=False):
    """Save changed game data, called on shutdown or checkpoint"""
    save_indexes()
    save_instances(force=force)
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
            actor = get_instance(gobj.carried_by)
            if actor:
                log.debug('   ** Adding %s to %s', gobj.name, actor.name)
                actor.inventory.append(gobj)
                gobj.add_to_actor(actor)
                continue
        if hasattr(gobj, 'worn_by') and gobj.worn_by:
            actor = get_instance(gobj.worn_by)
            if actor:
                log.debug('   ** Equipping %s to %s', gobj.name, actor.name)
                #actor.equip_item(gobj)
                #gobj.equip_to_actor(actor)
                continue
            # Find item (container), add item...


def load_tables():
    """Load database tables"""
    log.info('Loading DB tables:')
    for table_entry in GLOBALS.TABLES:
        try:
            if not table_entry['on_boot']:
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
    for room in GLOBALS.rooms.values():
        save_object(room, force=force)
