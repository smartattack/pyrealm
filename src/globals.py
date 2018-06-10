"""
PyRealm - main server functionality lives here
outside of main.py so globals can be included more easily.
"""

from utils import log
from miniboa import TelnetServer

# Default Game state / config
PORT = 1234
WELCOME_BANNER = '''
Welcome to PyRealm!

'''

# Storage paths
DATA_DIR = 'data'
PLAYER_DIR = 'players'


# List of client connections (TelnetClient)
clients = []

# users in lobby
lobby = {}

# logged in users
users = {}

# players (in-game characters, owned by a user)
players = {}

# All Players and NPCs
actors = []

IDLE_TIMEOUT = 30

# default game state
GAME_RUNNING = True


