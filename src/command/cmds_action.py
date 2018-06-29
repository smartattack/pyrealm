"""
Action commands
"""

from utils import log
from actor.player import Player
from command.helpers import find_actor, get_room, send_to_room, can_carry,\
                            find_room_item, find_room_actor, find_player_item
import globals as GLOBALS
from .table import cmd_table, CT


def do_drop(plr: Player, args: list):
    """Drop an object"""
    if args:
        name = ' '.join(args)
    log.debug('cmd_drop(%s)', name)
    # Identify object
    item = find_player_item(name, plr)
    if not item:
        plr.send('You do not appear to be carrying that.\n')
        return
    room = get_room(plr.location)
    if not room:
        log.error('Could not resolve Room() for location: %s', plr.location)
    # remove from player
    try:
        plr.inventory.remove(item)
    except:
        log.error('Could not remove item %s from %s', item.gid, plr.name)
        return 
    # add to room
    try:
        room.add_item(item)
    except:
        log.warning('Could not add %s to Room(%s)', item.gid, room.name)
    plr.send('You drop the ^M{}^d.\n'.format(item.short_desc))

cmd_table.append(CT('drop',          'do_drop',      'standing',  0, None))


def do_get(plr: Player, args: list):
    """Pick up an object"""
    if args:
        name = ' '.join(args)
    log.debug('cmd_get(%s)', name)
    # Identify object
    log.debug('Player == %s', plr)
    room = get_room(plr.location)
    if not room:
        log.error('Could not find player Room() for location %s', plr.location)
        return
    item = find_room_item(name, room)
    if not item:
        plr.send('I do not see that here.\n')
        return
    # Check if the weigh will exceed our max
    if not can_carry(plr, item):
        plr.send('You cannot carry that, it weighs too much!')
        return

    # remove from room
    try:
        room.remove_item(item)    # Identify object
    except:
        log.warning('Could not remove %s from room %s!', item.gid, room.name)
        return
    # add to player
    try:
        plr.inventory.append(item)
    except:
        log.error('Could not add item %s to %s', item.gid, plr.name)
        return 
    plr.send('You pick up the ^M{}^d.\n'.format(item.short_desc))

cmd_table.append(CT('get',          'do_get',      'standing',  0, None))



def give(plr: Player, args: list):
    """Transfer an object to another player"""
    # Parse for object and target
    # Remove from player
    # Add to target
