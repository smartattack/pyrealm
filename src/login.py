from player import Player
from server import Server

def loginHandler(player):
    """ Dispatch login/chargen functions based on state table"""

    #    _PLAYER_INIT = 0        # User just connected
    #    _PLAYER_USERNAME = 1    # User has entered a valid username
    #    _PLAYER_PASSWORD = 2    # User has entered password
    #    _PLAYER_PLAYING = 3     # User has authenticated
    #    _PLAYER_NEWUSER = 4     # Newuser - Username selection
    #    _PLAYER_USERCONFIRM = 5 # Newuser - Confirm username
    #    _PLAYER_RACE   = 6      # Newuser - Class selection
    #    _PLAYER_GENDER = 7      # Newuser - Gender selection
    #    _PLAYER_CONFIRM = 8     # Newuser - Confirm chargen
    login_states = {
        # Player._PLAYER_INIT:      pass,
        Player._PLAYER_USERNAME:    check_username,
        Player._PLAYER_PASSWORD:    validate_login,
        # Player._PLAYER_PLAYING:   pass,
        Player._PLAYER_NEWUSER:     newuser_name,
        Player._PLAYER_USERCONFIRM: newuser_user_confirm,
        Player._PLAYER_RACE:        newuser_race,
        Player._PLAYER_GENDER:      newuser_gender,
        Player._PLAYER_CONFIRM:     newuser_confirm,
    }

    "Call function in state table"
    login_states[player.state](player)


def check_username(player):
    """Check the username, validate or enter chargen"""
    if player.input == 'newuser':
        player.sendnow(player.cid, 'Please select a username for your character: ')
        player.state = Player.  _PLAYER_NEWUSER
    else:
        # Check valid names / sanitize here
        player.name = player.input
        player.sendnow(player.cid, 'Password: ')
        player.state = Player._PLAYER_PASSWORD

def validate_username(username):
    """Verify the validity of username
          Checks for illegal characters
          Checks for bad words"""
    import re
    regex = r'[^a-z0-9-_]'
    if re.search(regex, username.lower()) == None:
        badwords = []
        for x in badwords:
            if x in player.input.lower():
                return False
        return True
    return False


def username_exists(username):
    """Check username against known accounts"""
    "FIXME: implementation needed"
    return False


def validate_login(player):
    """Authenticate player"""
    if player.input == 'password':
        player.output = 'Welcome back, {}!'.format(player.name)
        player.state = Player._PLAYER_PLAYING
    else:
        player.sendnow(player.cid, 'Authentication failed!\nEnter your username(newuser for new players): ')
        player.state = Player._PLAYER_USERNAME

def newuser_name(player):
    """Beginning of chargen routine - pick a username"""
    if validate_username(player.input) == False:
        player.sendnow(player.cid, "Invalid username, please choose another: ")
        player.state = Player._PLAYER_NEWUSER
    else:
        player.name = player.input.lower()
        player.sendnow(player.cid, "You will be known as {} - is this correct? ".format(player.name))
        player.state = Player._PLAYER_CONFIRM

def newuser_user_confirm(object):
    """Chargen - confirm username"""
    player.sendnow(player.cid, 'confirm')
    if player.input.lower() in [ 'y','yes' ]:
        player.sendnow(player.cid, "Choose a race: ")
        player.state=Player._PLAYER_RACE
    else:
        player.sendnow(player.cid, "Please select a username for your character: ")
        player.user = None
        player.stat=Player._PLAYER_NEWUSER

def newuser_race(player):
    """Chargen - pick a race"""
    player.sendnow(player.cid, "Select a gender (M/F): ")
    player.state = Player._PLAYER_GENDER


def newuser_gender(player):
    """Chargen - select a gender"""

    if player.input == 'M':
        player.gender = 'M'
    elif player.input == 'F':
        player.gender = 'F'
    else:
        player.sendnow(player.cid, "Invalid input!\nSelect a gender (M/F): ")
        player.state = Player._PLAYER_GENDER

def newuser_confirm(player):
    """Chargen final - confirm choices"""
    pass



