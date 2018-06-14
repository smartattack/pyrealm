"""
Movement commands
"""

from user.helpers import send_all, broadcast
from utils import log
from world.room import *
from actor.player import Player
from actor.npc import NPC
import globals as GLOBALS


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


def move_actor(actor, new_location, direction):
    """Moves an NPC or Player from one room to another"""
    log.debug('FUNC move_actor()')
    # Leave old room
    old_location = actor.location
    GLOBALS.rooms[old_location].remove_actor(actor)
    send_to_room(actor, old_location, 
                 '{} heads {}\n'.format(actor.get_name(),
                                               DIR_NAMES[direction].exits))
    send_to_room(actor, new_location, 
                '{} enters from the {}\n'.format(actor.get_name(),
                                                 DIR_NAMES[direction].enters))
    GLOBALS.rooms[new_location].add_actor(actor)
    actor.location = new_location


# match directions
def match_direction(text: str):
    """Match text to direction"""
    log.debug('FUNC match_directions')
    search = text.lower()
    for dir_number, dir_name, ignore in DIR_NAMES:
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

def do_sit(plr: Player, args: list):
    """Attempt to sit down"""
    if isinstance(plr, NPC):
        return
    if plr.position == 'sleeping':
        plr.send('You need to wake up first!\n')
    elif plr.position == 'sitting':
        plr.send('You are already sitting!\n')
    elif plr.position == 'fighting':
        plr.send('Not while you are fighting!\n')
    else:
        plr.position = 'sitting'
        plr.send('You have a seat.\n')
        send_to_room(plr, plr.location, '{} sits down.\n'.format(plr.get_name()))


def do_sleep(plr: Player, args: list):
    """Attempt to go to sleep"""
    if isinstance(plr, NPC):
        return
    if plr.position == 'fighting':
        plr.send('You are not one to sleep through a fight!\n')
    elif plr.position == 'sleeping':
        plr.send('You are already asleep!\n')
    else:
        plr.position = 'sleeping'
        plr.send('You lay down and take a nap.  Zzzz\n')
        send_to_room(plr, plr.location, '{} lays down to sleep.\n'.format(plr.get_name())) 


def do_stand(plr: Player, args: list):
    """Attempt to stand up"""
    if isinstance(plr, NPC):
        return
    if plr.position == 'sitting':
        plr.send('You stand up.\n')
        send_to_room(plr, plr.location, '{} stands up.\n'.format(plr.get_name()))
        plr.position = 'standing'
    elif plr.position == 'sleeping':
        plr.send('You cannot stand up while you are asleep!\n')
    else:
        plr.send('You are already standing!\n')


def do_wake(plr: Player, args: list):
    """Attempt to go wakep"""
    if isinstance(plr, NPC):
        return
    if plr.position == 'sleeping':
        plr.send('You awaken, sit up and yawn.\n')
        send_to_room(plr, plr.location, '{} awakens.\n'.format(plr.get_name()))
        plr.position = 'sitting'
    else:
        plr.send('You are already awake!\n') 