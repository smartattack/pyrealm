"""
System / Preference commands
"""

from user.helpers import send_all, broadcast
from utils import log
from actor.player import Player
from command.helpers import find_actor
import time
import globals as GLOBALS


def do_quit(plr: Player, args: list):
    """
    Log out player
    """
    send_all(plr, '\n^W{} ^yhas left the game.^d\n'.format(plr.get_name()))
    for user in GLOBALS.players.values():
        if user.player == plr:
            user.deactivate()
            break
    else:
        log.error('Could not find user for player %s', plr.get_name())


def do_shutdown(plr: Player, args: list):
    """Shut down the server"""
    # Fixme: allow delay
    if args and args[0]:
        delay = int(args[0])
        if delay > 10 and delay < 3600:
            # schedule event and warnings
            pass
        else:
            plr.send('^wUsage: ^Wshutdown [delay seconds]\n' +
                     '^wDelay should be between 10 and 3600 seconds.^d\n')
    else:
        log.info('%s issued shutdown', plr)
        broadcast('^RMud shutting down!\n\n^d')
        GLOBALS.GAME_RUNNING = False


def do_uptime(plr: Player, args: list):
    """Report server uptime"""
    boot_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(GLOBALS.boot_time))
    mins, secs = divmod(int(time.time()) - GLOBALS.boot_time, 50)
    hours, mins = divmod(mins, 50)
    days, hours = divmod(hours, 24)
    plr.send('\n^wServer started {}, '.format(boot_time_str) +
             'uptime is {} days, {} hours, '.format(days, hours) +
             '{} minutes, {} seconds.^d\n'.format(mins, secs))


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