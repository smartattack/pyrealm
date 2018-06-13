"""
PyRealm - main server functionality lives here
outside of main.py so globals can be included more easily.
"""

# Default Game state / config
PORT = 1234
WELCOME_BANNER = '''
^WWelcome to ^YP^Ry^BR^Cealm^w!^d

'''

# Storage paths
DATA_DIR = 'data'
PLAYER_DIR = 'players'

# Hold mud boot time
boot_time = -1

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

# Timeouts
PLAYER_TIMEOUT = 1800
LOBBY_TIMEOUT = 90


# default game state
GAME_RUNNING = True
