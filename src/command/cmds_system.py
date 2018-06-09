"""
System / Preference commands
"""

from utils import log
from actor.player import Player
import globals as GLOBAL

def do_quit(ch: Player, *args):
    """
    Log out player
    """
    ch._client.deactivate()


def do_who(ch: Player, *args):
    """
    List players
    """
    here = []
    for u in GLOBAL.PLAYERS.values():
        if u.player == ch:
            continue
        here.append(u.player.get_name())
    if len(here) > 0:
        ch.send('\nAlso here are:\n')
        ch.send('{}\n'.format(', '.join(here)))
    else:
        ch.send('There is nobody else here.\n')
    #for u in GLOBAL.PLAYERS.values():
    #    ch.send('{}\n'.format(u.player.get_name()))
    
