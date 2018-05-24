from player import Player
from server import Server

def login_handler(player):
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
        player.send_now(player.cid, 'Please select a username for your character: ')
        player.state = Player.  _PLAYER_NEWUSER
    else:
        # Check valid names / sanitize here
        player.name = player.input
        player.send_now(player.cid, 'Password: ')
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
    "TODO: implementation needed"
    return False


def validate_login(player):
    """Authenticate player"""
    "TODO: implement password hash and check"

    if player.input == 'password':
        player.output = 'Welcome back, {}!'.format(player.name)
        player.state = Player._PLAYER_PLAYING
    else:
        player.send_now(player.cid, 'Authentication failed!\nEnter your username(newuser for new players): ')
        player.state = Player._PLAYER_USERNAME


def newuser_name(player):
    """Beginning of chargen routine - pick a username"""
    if validate_username(player.input) == False:
        player.send_now(player.cid, "Invalid username, please choose another: ")
        player.state = Player._PLAYER_NEWUSER
    else:
        player.name = player.input.lower()
        player.send_now(player.cid, "You will be known as {} - is this correct? ".format(player.name))
        player.state = Player._PLAYER_USERCONFIRM


def newuser_user_confirm(player):
    """Chargen - confirm username"""
    "TODO: display races / choice selection"
    if player.input.lower() in [ 'y','yes' ]:
        player.send_now(player.cid, "Choose a race: ")
        player.state=Player._PLAYER_RACE
    else:
        player.send_now(player.cid, "Please select a username for your character: ")
        player.state=Player._PLAYER_NEWUSER


def newuser_race(player):
    """Chargen - validate race selection"""
    "TODO: validate selection"
    player.send_now(player.cid, "Select a gender (M/F): ")
    player.state = Player._PLAYER_GENDER


def newuser_gender(player):
    """Chargen - select a gender"""

    if player.input.lower() not in ('m', 'f'):
        player.send_now(player.cid, "Invalid input!\nSelect a gender (M/F): ")
    else:
        if player.input.lower() == 'm':
            player.gender = 'Male'
        else:
            player.gender = 'Female'

        "TODO: display character traits for confirmation"

        player.send_now(player.cid, "Do you accept these choices (Y/N)? ")
        player.state = Player._PLAYER_CONFIRM


def newuser_confirm(player):
    """Chargen final - confirm choices"""
    if player.input.lower() == 'y':
        player.tell("Welcome, {}!\n".format(player.name))
        player.state = Player._PLAYER_PLAYING
    else:
        player.name = None
        player.input = None
        player.state = Player._PLAYER_NEWUSER
        player.send_now(player.cid, "Please choose a name for your character: ")




