"""
Time-based update functions
"""

import time
from utils import log
import globals as GLOBALS
from user.helpers import send_all, broadcast


GLOBALS.EPOCH_S = int(time.strftime('%s', time.strptime(GLOBALS.GAME_EPOCH, '%Y/%m/%d %H:%M:%S')))
log.info('Converted GAME_EPOCH: %s -> %s', GLOBALS.GAME_EPOCH, GLOBALS.EPOCH_S)


def update_time():
    """Process game time update"""

    now = time.time()
    elapsed = now - GLOBALS.last_update
    # Adds elapsed time since last update to global runtime
    GLOBALS.game_state.add_runtime(elapsed)
    GLOBALS.last_update = now
    GLOBALS.game_time = GLOBALS.game_state.runtime * GLOBALS.TIME_FACTOR \
                        + GLOBALS.EPOCH_S

    if daylight_changed():
        broadcast('\n{}\n'.format(GLOBALS.daylight_message[GLOBALS.daylight_level]))


def daylight_changed():
    """Return true if daylight level changed"""
    stime = time.localtime(GLOBALS.game_time)
    if stime.tm_hour < 7:
        if GLOBALS.daylight_level != 0:
            GLOBALS.daylight_level = 0
            return True
    elif stime.tm_hour < 12:
        if GLOBALS.daylight_level != 1:
            GLOBALS.daylight_level = 1
            return True
    elif stime.tm_hour < 17:
        if GLOBALS.daylight_level != 2:
            GLOBALS.daylight_level = 2
            return True
    elif stime.tm_hour < 19:
        if GLOBALS.daylight_level != 3:
            GLOBALS.daylight_level = 3
            return True
    else:
        if GLOBALS.daylight_level != 0:
            GLOBALS.daylight_level = 0
            return True
    return False
