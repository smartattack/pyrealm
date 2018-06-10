"""
System / Preference commands
"""

from utils import log
from actor.player import Player
from user.helpers import send_all
import globals as GLOBALS

def do_quit(ch: Player, *args):
    """
    Log out player
    """
    send_all(ch, '\n^W{} ^yhas left the game.^d\n'.format(ch.get_name()))
    ch._client.deactivate()


def do_who(ch: Player, *args):
    """
    List players
    """
    here = []
    for u in GLOBALS.PLAYERS.values():
        if u.player == ch:
            continue
        here.append(u.player.get_name())
    if len(here) > 0:
        if len(here) > 1:
            verb = 'are'
        else:
            verb = 'is'
        ch.send('\n^wAlso here {}:^d\n'.format(verb))
        ch.send('^b{}^d\n'.format('^d, ^b'.join(here)))
    else:
        ch.send('^wThere is nobody else here.^d\n')
    #for u in GLOBALS.PLAYERS.values():
    #    ch.send('{}\n'.format(u.player.get_name()))
    
