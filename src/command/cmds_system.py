"""
System / Preference commands
"""

from user.helpers import send_all
from utils import log
from actor.player import Player
from command.helpers import find_actor
import globals as GLOBALS


def do_quit(plr: Player, args: list):
    """
    Log out player
    """
    send_all(plr, '\n^W{} ^yhas left the game.^d\n'.format(plr.get_name()))
    for user in GLOBALS.players:
        if user.player == plr:
            user.deactivate()
            break
    else:
        log.error('Could not find user for player %s', plr.get_name())


def do_who(plr: Player, args: list):
    """
    List players
    """
    here = []
    for user in GLOBALS.players.values():
        if user.player == plr:
            continue
        here.append(user.player.get_name())
    if here:
        if len(here) > 1:
            verb = 'are'
        else:
            verb = 'is'
        plr.send('\n^wAlso here {}:^d\n^b{}^d\n'.format(verb, '^d, ^b'.join(here)))
    else:
        plr.send('^wThere is nobody else here.^d\n')


def do_shout(plr: Player, args: list):
    """Send a message to everyone"""
    send_all(plr, ' '.join(args))


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
