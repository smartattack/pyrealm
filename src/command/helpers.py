"""
Command helper utility functions
"""

from utils import log
from actor.player import Player
from world.room import Room
import globals as GLOBALS


def can_carry(act, item):
    """Check whether item is too heavy"""
    return True


def find_actor(name: str):
    """Return an actor with given name or None"""
    if name is None:
        return None
    log.debug('{} -> {}'.format(name, type(name)))
    name = name.capitalize()
    for actor in GLOBALS.all_actors.values():
        if actor['name'] == name:
            return actor
    return None


def find_room_actor(name: str, loc: Room):
    """Returns matching actor if in room"""
    for actor in Room.actors:
        if actor not in GLOBALS.all_actors:
            log.error('Actor %s is in room but not all_actors!', name)
        if actor.name == name:
            return actor
        else:
            log.debug('No match for %s', name)
            return None


def find_room_item(name: str, loc: Room):
    """Return matching item if in room"""
    if name.isdigit():
        gid = int(name)
        if gid not in GLOBALS.all_items:
            log.warning('Item id %s does not exist!', gid)
            return None
        for item in loc.inventory:
            if gid == item.gid:
                log.debug('FOUND, returning item(%s) == %s', item.gid, item.name)
                return item
        else:
            log.debug('Item %s not in room!', gid)
            return None
    else:
        log.debug('Room() == %s', loc)
        for item in loc.inventory:
            log.debug('+++->  Searching "%s" for "%s"', item.short_desc, name)
            if name in item.short_desc.split():
                log.debug('FOUND, returning item(%s) == %s', item.gid, item.name)
                return item
    return None


def find_player_item(name: str, plr: Player):
    """Return matching item if in player inventory"""
    if name.isdigit():
        name = int(name)
        if name not in GLOBALS.all_items:
            log.warning('Item id %s does not exist!', name)
            return None
        for item in plr.inventory:
            if name == item.gid:
                log.debug('FOUND, returning item(%s) == %s', item.gid, item.name)
                return item
        else:
            log.debug('Item gid %s not in inventory!', name)
            return None
    else:
        for item in plr.inventory:
            if name in item.short_desc.split():
                log.debug('FOUND, returning item(%s) == %s', item.gid, item.name)
                return item
    return None


def find_help(term: str):
    """Return a list of any help docs with the term in key or text"""
    matches = []
    for title in GLOBALS.helps:
        if term in title or term in (word for word in GLOBALS.helps[title].split()):
            matches.append(title)
    return matches
     

def get_help_doc(term: str):
    """Attempt to locate helpfile by name, returns doc"""
    if term in GLOBALS.helps:
        return GLOBALS.helps[term]
    for title in GLOBALS.helps:
        if title.startswith(term):
            return GLOBALS.helps[title]
    return None


def get_room(location: int):
    """Return Room object for a given location id"""
    if location in GLOBALS.rooms:
        return GLOBALS.rooms[location]
    else:
        log.warning('Room(%s) does not exist in GLOBALS.rooms', location)
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

