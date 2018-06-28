"""
Info commands
"""

from utils import log
from world.room import *
from actor.player import Player
from actor.npc import NPC
from command.helpers import send_to_room, find_help, get_help_doc
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


def do_help(plr: Player, args: list):
    """Provide online help"""
    # FIXME: if first arg is "find" do a search in text
    # of all help docs and return a list of matching docs
    if not args:
        # Return all help keywords
        keywords = sorted((keyword for keyword in GLOBALS.helps))
        if keywords:
            plr.send('^CHelp topics:\n^w{}\n'.format('\n'.join(keywords)))
        plr.send('\n')
        return
    term = args.pop(0)
    if term == 'find':
        try:
            term = args.pop(0)
        except:
            plr.send('^rWhat do you want to search for?^d\n')
            return
        keywords = find_help(term)
        if keywords:
            output = '^CThe following help docs contain "^g{}^C":^d\n'.format(term)
            output += '\n'.join(keywords) + '\n'
            plr.send(output)
        else:
            plr.send('^rCould not find any matching help docs for "^C{}^r".^d\n'.format(term))
        return
    doc = get_help_doc(term)
    if doc:
        plr.send_wrapped('\n{}\n'.format(doc))
    else:
        plr.send('^rI could not find any help for "^C{}^r".^d\n'.format(term))

cmd_table.append(CT('help',        'do_help',   'dead',      0, None))


def do_inventory(plr: Player, args: list):
    """Display player's inventory"""
    if plr.inventory:
        output = 'You are carrying:\n'
        for item in Player.inventory:
            output += '{}\n'.format(item.short_desc)
    else:    
        output = 'You are not carrying anything.\n'
    plr.send(output)

cmd_table.append(CT('inventory',        'do_inventory',   'dead',      0, None))


def do_look(plr: Player, args: list):
    """Report information about an object/room/actor"""
    if args:
        pass
    else:
        # Assume show room
        plr.send('{}'.format(GLOBALS.rooms[plr.location].show_info(width=plr.client.columns)))
