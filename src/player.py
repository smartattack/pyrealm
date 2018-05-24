"""
Player is a connected user
"""

import location
from character import Character
import logging
from server import Server

mudlog = logging.getLogger('mudlog')


class Player(Character):
    """ Instantiated on new connections
        Player will not yet have a name
    """
    _PLAYER_DISCONNECT = -1   # Disconnected player
    _PLAYER_INIT = 0          # User just connected
    _PLAYER_USERNAME = 1      # User has entered a valid username
    _PLAYER_PASSWORD = 2      # User has entered password
    _PLAYER_PLAYING = 3       # User has authenticated
    _PLAYER_NEWUSER = 4       # Enter chargen
    _PLAYER_USERCONFIRM = 5   # Confirming new username
    _PLAYER_RACE = 6          # Class selection
    _PLAYER_GENDER = 7        # Gender selection
    _PLAYER_CONFIRM = 8       # Confirm chargen

    def __init__(self):
        self.name = None
        self.state = self._PLAYER_INIT
        self.location = location._limbo

        # Output buffer
        self.output = ""

        # Input parsing
        self.input = ""

        # Used by command parsing
        self.command = None
        self.args = None

        # This will hold the client/connection id
        self.cid = None

        super().__init__()

    """Send output to player - buffered"""

    def tell(self, msg):
        self.output += msg

    def logout(self):
        self.tell('\nGoodbye!\n')
        self.disconnect()
