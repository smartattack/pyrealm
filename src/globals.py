"""
PyRealm - main server functionality lives here
outside of main.py so globals can be included more easily.
"""

# Default Game state / config
game_state = None
PORT = 1234
WELCOME_BANNER = '\n^WWelcome to ^YP^Ry^BR^Cealm^w!^d\n\n'

# Storage paths
DATA_DIR = 'data'
HELP_DIR = 'help'
INSTANCE_DIR = 'instances'
ITEM_DIR = 'item'
PLAYER_DIR = 'players'
RACE_DIR = 'race'
ROOM_DIR = 'room'
STATE_DIR = ''

# id number of starting room for new players
START_ROOM = 1

# List of DB tables to load on boot_db
TABLES = [
    { 'name': 'rooms',   'path': ROOM_DIR,
      'filename': '*.json', 'on_boot': True},
    { 'name': 'players', 'path': INSTANCE_DIR + '/' + PLAYER_DIR,
      'filename': '*.json', 'on_boot': False },
    { 'name': 'items', 'path': ITEM_DIR,
      'filename': '*.json', 'on_boot': True },
    { 'name': 'item-instances', 'path': INSTANCE_DIR + '/' + ITEM_DIR,
      'filename': '*.json', 'on_boot': True }
]

# will be populated in main() with current time.time()
boot_time = -1

# List of client connections (TelnetClient)
clients = []

# users in lobby
lobby = {}

# logged in users
users = {}

# All Players and NPCs
players = {}
npcs = {}
actors = {}

# Holds the map, for now
rooms = {}

# Item templates
items = {}

# Help files
helps = {}

# Global instances
all_instances = {}
all_items = {}
all_actors = {}
all_players = {}
all_npcs = {}
all_locations = {}


# Timeouts
PLAYER_TIMEOUT = 1200
LOBBY_TIMEOUT = 180


# default game state
GAME_RUNNING = True

# System resource snapshots
last_snapshot = None
current_snapshot = None

# Dawn of time for the game (YYYY/mm/dd HH:MM:SS)
GAME_EPOCH = '0776/07/04 12:00:00'
TIME_FACTOR = 24

# Scale factor for game time
TIME_FACTOR = 24

# Daylight changes
daylight_level = 0
daylight_message = [
    'The sky is now completely dark.  Only the stars and the moon light your way.',
    'The sky begins to brighten as the sun rises to the east.',
    'The sun is directly overhead.',
    'The sky dims as the sun begins to set.',
]
