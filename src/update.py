"""
Time-based update functions
"""

import time
from utils import log
import globals as GLOBALS


GLOBALS.EPOCH_S = int(time.strftime('%s', time.strptime(GLOBALS.GAME_EPOCH, '%Y/%m/%d %H:%M:%S')))
log.info('Converted GAME_EPOCH: %s -> %s', GLOBALS.GAME_EPOCH, GLOBALS.EPOCH_S)


def update_time():
    """Process game time update"""

    now = time.time()
    elapsed = now - GLOBALS.last_update
    # Adds elapsed time since last update to global runtime
    GLOBALS.game_state.add_runtime(elapsed)
    GLOBALS.last_update = now
    GLOBALS.game_time = GLOBALS.game_state.runtime * GLOBALS.TIME_FACTOR + GLOBALS.EPOCH_S
    #print('Elapsed: {}, runtime: {}'.format(elapsed, GLOBALS.game_state.runtime))
    #elapsed = now - GLOBALS.boot_time
    #game_time = elapsed * GLOBALS.TIME_FACTOR + GLOBALS.EPOCH_S
    # This would return a time.time() as a human-readable datetime string
    
