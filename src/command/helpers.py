"""
Command helper utility functions
"""

from utils import log
from actor.player import Player
import globals as GLOBALS


def find_actor(name: str):
    """Return an actor object with given name or None"""
    if name is None:
        return None
    log.debug('{} -> {}'.format(name, type(name)))
    name = name.capitalize()
    for actor in GLOBALS.all_actors.values():
        if actor['name'] == name:
            return actor
    return None


def send_to_room(omit, room_id, msg):
    """Send text to actors in room"""
    log.debug('FUNC send_to_room()')
    if not GLOBALS.rooms[room_id]:
        log.error('send_to_room called on non-existent room %s', room_id)
        return
    for actor in GLOBALS.rooms[room_id].actors:
        if isinstance(actor, Player):
            if actor == omit:
                continue
            actor.send('\n'+msg)