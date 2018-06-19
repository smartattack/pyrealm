"""
Emote commands
"""

import time
from user.helpers import send_all, broadcast
from utils import log
from actor.player import Player
from command.helpers import find_actor, send_to_room
import globals as GLOBALS
from .table import cmd_table, CT


def do_fart(plr: Player, args: list):
    """fart"""
    if args is None or args == []:
        plr.send('You fart.\n')
        send_to_room(plr, plr.location, '{} farts.\n'.format(plr.name))
        return
    if args[0].lower() in ('in', 'at', 'to', 'for'):
        who = args[1]
    else:
        who = args[0]
    target = find_actor(who)
    if target:
        target.send('\n{} farts at you.\n'.format(plr.name))
        plr.send('You fart at {}.\n'.format(target.name))
    else:
        plr.send('I do not see anyone like that here.\n')

cmd_table.append(CT('fart',        'do_fart', 'dead',      0, None))



def do_smile(plr: Player, args: list):
    """smile"""
    if args is None or args == []:
        plr.send('You smile.\n')
        send_to_room(plr, plr.location, '{} smiles.\n'.format(plr.name))
        return
    if args[0].lower() in ('in', 'at', 'to', 'for'):
        who = args[1]
    else:
        who = args[0]
    target = find_actor(who)
    if target:
        target.send('\n{} smiles at you.\n'.format(plr.name))
        plr.send('You smile at {}.\n'.format(target.name))
    else:
        plr.send('I do not see anyone like that here.\n')

cmd_table.append(CT('smile',        'do_smile', 'dead',      0, None))


def do_smirk(plr: Player, args: list):
    """smirk"""
    if args is None or args == []:
        plr.send('You smirk.\n')
        send_to_room(plr, plr.location, '{} smirks.\n'.format(plr.name))
        return
    if args[0].lower() in ('in', 'at', 'to', 'for'):
        who = args[1]
    else:
        who = args[0]
    target = find_actor(who)
    if target:
        target.send('\n{} smirks at you.\n'.format(plr.name))
        plr.send('You smirk at {}.\n'.format(target.name))
    else:
        plr.send('I do not see anyone like that here.\n')

cmd_table.append(CT('smirk',        'do_smirk', 'dead',      0, None))


def do_wave(plr: Player, args: list):
    """wave"""
    if args is None or args == []:
        plr.send('You wave.\n')
        send_to_room(plr, plr.location, '{} waves.\n'.format(plr.name))
        return
    if args[0].lower() in ('in', 'at', 'to', 'for'):
        who = args[1]
    else:
        who = args[0]
    target = find_actor(who)
    if target:
        target.send('\n{} waves at you.\n'.format(plr.name))
        plr.send('You wave at {}.\n'.format(target.name))
    else:
        plr.send('I do not see anyone like that here.\n')

cmd_table.append(CT('wave',        'do_wave',   'dead',      0, None))
