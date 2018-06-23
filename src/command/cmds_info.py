"""
Info commands
"""

from utils import log
from world.room import *
from actor.player import Player
from actor.npc import NPC
from command.helpers import send_to_room
import globals as GLOBALS
from .table import cmd_table, CT


def do_exits(plr: Player, args: list):
    """List room exits"""
    log.debug('FUNC do_exits()')
    try:
        plr.send(GLOBALS.rooms[plr.location].show_exits())
    except (KeyError, AttributeError):
        plr.send('There are no visible exits.\n{}\n')

cmd_table.append(CT('exits',        'do_exits',   'dead',      0, None))


def do_look(plr: Player, args: list):
    """Report information about an object/room/actor"""
    if args:
        pass
    else:
        # Assume show room
        plr.send('{}'.format(GLOBALS.rooms[plr.location].show_info(width=plr.client.columns)))

