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
RACE_DIR = 'race'
ROOM_DIR = 'room'

# id number of starting room for new players
START_ROOM = 1

# Dawn of time for the game (YYYY/mm/dd HH:MM:SS)
GAME_EPOCH = '0776/07/04 12:00:00'
TIME_FACTOR = 24

# List of DB tables to load on boot_db
TABLES = [
    { 'name': 'rooms', 'path': ROOM_DIR, 'filename': '*.json', 'on_boot': True},
    { 'name': 'players', 'path': PLAYER_DIR, 'filename': '*.json' }
]

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

# Holds the map, for now
rooms = {}

# Timeouts
PLAYER_TIMEOUT = 1800
LOBBY_TIMEOUT = 90


# default game state
GAME_RUNNING = True

# Scale factor for game time
TIME_FACTOR = 24
