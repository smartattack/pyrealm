"""
Social commands
"""

import time
from user.helpers import send_all, broadcast
from utils import log
from actor.player import Player
from command.helpers import find_actor, send_to_room
import globals as GLOBALS
from .table import cmd_table, CT


def do_say(plr: Player, args: list):
    """Send a message to others in the room"""
    if args is None or args == []:
        plr.send('^RWhat do you want to say?^d\n')
        return
    send_to_room(plr, plr.location, '{} says: "^Y{}!^d"\n'.format(plr.get_name(), ' '.join(args)))
    plr.send('You say "^Y{}!^d"\n'.format(' '.join(args)))

cmd_table.append(CT('say',          'do_say',     'dead',      0, None))


def do_shout(plr: Player, args: list):
    """Send a message to everyone"""
    if args is None or args == []:
        plr.send('^RWhat do you want to say?^d\n')
        return
    send_all(plr, '\n{} shouts: "^Y{}!^d"\n'.format(plr.get_name(), ' '.join(args)))
    plr.send('You shout "^Y{}!^d"\n'.format(' '.join(args)))

cmd_table.append(CT('shout',        'do_shout',   'dead',      0, None))


def do_tell(plr: Player, args: list):
    """Tell another actor a message"""
    # First argument should be target
    target = find_actor(args[0][0])
    if target:
        msg = ' '.join(args[0][1:])
        if isinstance(target, Player):
            target.send('\n^w{} says, ^g"{}"^d\n'.format(plr.get_name(), msg))
    else:
        plr.send('\n^wI do not see anyone like that, here.^d\n')

cmd_table.append(CT('tell',        'do_tell',   'dead',      0, None))
