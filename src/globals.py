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

# List of client connections (TelnetClient)
CLIENTS = []

# users in lobby
LOBBY = {}

# logged in users
USERS = {}

# players (in-game characters, owned by a user)
PLAYERS = {}

IDLE_TIMEOUT = 60

# default game state
GAME_RUNNING = True


