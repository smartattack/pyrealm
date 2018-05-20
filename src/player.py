"""
Player - one connected player
"""

class Player:

    """ Instantiated on new connections
        Player will not yet have a name
    """

    _PLAYER_INIT = 0       # User just connected
    _PLAYER_LOGIN = 1      # User has entered a valid username
    _PLAYER_VALIDATE = 2   # User has entered password
    _PLAYER_PLAYING = 3    # User has authenticated
    
    def __init__(self):
        #
        self.name = None
        self.room = None
        self.state = self._PLAYER_INIT
        
        # Output buffer
        self.output = ""

        # Input parsing
        self.input = ""


