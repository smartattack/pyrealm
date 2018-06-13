"""
Movement commands
"""

from user.helpers import send_all, broadcast
from utils import log
from world.room import *
from actor.player import Player
import globals as GLOBALS


def send_to_room(room_id, msg):
    """Send text to actors in room"""
    log.debug('FUNC send_to_room()')
    if not GLOBALS.rooms[room_id]:
        log.error('send_to_room called on non-existent room %s', room_id)
        return
    for actor in GLOBALS.rooms[room_id].actors:
        if isinstance(actor, Player):
            actor.send(msg)


def move_actor(actor, new_location, direction):
    """Moves an NPC or Player from one room to another"""
    log.debug('FUNC move_actor()')
    # Leave old room
    old_location = actor.location
    GLOBALS.rooms[old_location].remove_actor(actor)
    send_to_room(old_location, 
                 '{} exits to the {}\n'.format(actor.get_name(),
                                               DIR_NAMES[direction]))
    send_to_room(new_location, 
                '{} enters from the {}\n'.format(actor.get_name(),
                                                 DIR_FROM_NAMES[direction]))
    GLOBALS.rooms[new_location].add_actor(actor)
    actor.location = new_location


# match directions
def match_direction(text: str):
    """Match text to direction"""
    log.debug('FUNC match_directions')
    search = text.lower()
    for dir_number, dir_name in DIR_NAMES.items():
        if dir_name.lower().startswith(search):
            log.debug('Matched direction: %s (%s)', dir_number, dir_name)
            return dir_number
    if search == 'ne':
        log.debug('Matched direction: %s (%s)', dir_number, dir_name)
        return DIR_NORTHEAST
    elif search == 'nw':
        log.debug('Matched direction: %s (%s)', dir_number, dir_name)
        return DIR_NORTHWEST
    elif search == 'se':
        log.debug('Matched direction: %s (%s)', dir_number, dir_name)
        return DIR_SOUTHEAST
    elif search == 'sw':
        log.debug('Matched direction: %s (%s)', dir_number, dir_name)
        return DIR_SOUTHWEST
    else:
        return None


def do_go(plr: Player, args: list):
    """
    Handle generic movement command
    Expects a valid direction as first argument
    """
    log.debug('FUNC do_go()')
    if not args:
        plr.send('Which way did you want to go?\n')
        return
    which = match_direction(args[0])
    if which == None:
        plr.send('Try choosing a direction from one of the exits.\n')
        return
    try:
        new_location = GLOBALS.rooms[plr.location].exits[which]['to_room']
        move_actor(plr, new_location, which)
    except Exception as err:
        log.error('do_go() failed: %s', err)
        plr.send('You cannot go that way\n')
        return


def do_north(plr: Player, args: list):
    """
    Move to north room
    """
    try:
        old_location = plr.location
        plr.location = GLOBALS.rooms[plr.location].exits[DIR_NORTH]['to_room']
        send_all('{} left to the north.', plr.get_name())
    except:
        plr.send('You cannot go that way.')
