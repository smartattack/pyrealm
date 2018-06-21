"""
Track and convert Game Time / Real Time
"""

import time
import datetime
from utils import log
import globals as GLOBALS

def game_epoch():
    """Return game start date"""
    if GLOBALS.GAME_EPOCH:
        epoch = GLOBALS.GAME_EPOCH
        if isinstance(epoch, datetime):
            return time.mktime(epoch.timetuple()) 
        elif isinstance(epoch, time):
            return epoch
    else:
        return server_epoch()


def server_epoch():
    """Return start date of server"""
    return GLOBALS.boot_time


def uptime_runtimes():
    """Update game_time and server_time"""


def game_runtime():
    """Return gameworld runtime in seconds ("now" - epoch)"""
    return game_time() - game_epoch()


def real_time(offset=0):
    """Returns the real time.time() N seconds from now"""
    return time.time() + offset


def game_time(offset=0):
    """Returns game time(s) N seconds from now"""
    return game_epoch() + game_runtime() + (offset * GLOBALS.time_factor)


