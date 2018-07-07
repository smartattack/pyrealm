"""
Persists game state across restarts.
"""

from utils import log
import globals as GLOBALS
from game_object import InstanceRegistry


class GameState(object):
    """Holds global game persistence info"""

    def __init__(self):
        """Only runs on first boot"""
        self._runtime = 0.0
        self._max_gid = 0
    
    def post_init(self):
        """Needed by load_from_json"""
        pass

    @property
    def runtime(self):
        return self._runtime

    def add_runtime(self, seconds):
        self._runtime += seconds

    @property
    def max_gid(self):
        return self._max_gid
    
    @max_gid.setter
    def max_gid(self, number):
        self._max_gid = number


def save_game_state():
    """Save global game state to disk, called on shutdown or checkpoint"""
    log.debug('FUNC save_game_state()')
    pathname = os.path.join(GLOBALS.DATA_DIR, GLOBALS.STATE_DIR)
    filename = os.path.join(pathname, 'state.json')
    try:
        os.makedirs(pathname, 0o755, True)
    except OSError as err:
        log.critical('Failed to create directory: %s -> %s', pathname, err)
    data = to_json(GLOBALS.game_state)
    log.info('Saving game state')
    with open(filename, "w") as file:
        file.write(data)


def load_game_state():
    """Load or initialize game state"""
    global InstanceRegistry
    try:
        state_file = os.path.join(GLOBALS.DATA_DIR, GLOBALS.STATE_DIR,
                                  'state.json')
        GLOBALS.game_state = load_from_json(state_file)
        log.info('Game state, max_gid = %s, runtime = %s',
                  GLOBALS.game_state.max_gid, GLOBALS.game_state.runtime)
    except Exception as err:
        log.warning('Game state data not found, initializing... %s', err)
        GLOBALS.game_state = GameState()
    # Sync gid counters
    GLOBALS.game_state.max_gid = InstanceRegistry.gid = max(InstanceRegistry.gid,
                                                     GLOBALS.game_state.max_gid)
    log.debug('AFTER SYNC: GLOBALS.game_state.max_gid=%s, InstanceRegistry.gid=%s',
              GLOBALS.game_state.max_gid, InstanceRegistry.gid)