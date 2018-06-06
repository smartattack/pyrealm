"""
Login Handler - Implements a FSM to handle logins and chargen
"""

from actor.player import Player
from user.base_user import BaseUser
from utils import log
from user.account import create_account, validate_password, hash_password
from user.db import account_exists, save_account, load_account
from user.user import User
import globals as GLOBAL
from datetime import datetime

def player_handoff(player, account):
    """
    Create the user and associate user account
    Set command handler, assign commands, initial room
    """
    log.debug('FUNC: player_handoff()')
    user = User(player._client)
    user.client = player._client
    user.username = account.username
    user.player = player
    user.change_state('player')
    del GLOBAL.LOBBY[player._client]
    GLOBAL.PLAYERS.append(player._client)
    user.send(user.prompt)


class Login(BaseUser):
    """
    Login existing players
    Create new accounts and characters
    """
    def __init__(self, client):
        BaseUser.__init__(self, client)
        self.change_state('ask_username')
        self.driver()
        self.username = 'Guest'


    def _state_ask_username(self):
        """Send username prompt"""
        self.send('What is your name? ')
        self.change_state('check_username')


    def _state_check_username(self):
        """Check username, either enter chargen or request password"""
        username = self.get_command().capitalize()
        if username == 'New':
            self.change_state('new_ask_username')
        elif username == 'Quit':
            self.change_state('none')
            self.send('Goodbye\n\n')
            self.deactivate()
        else:
            self.username = username
            self.change_state('ask_password')
        self.driver()


    def _state_ask_password(self):
        """Send password prompt"""
        self.send('Password: ')
        self.password_mode_on()
        self.change_state('check_password')


    def _state_check_password(self):
        """Validate login"""
        self.password_mode_off()
        self.send('\n')
        password = self.get_command()
        if account_exists(self.username):
            account = load_account(self.username)
            self.account = account
            if validate_password(password = password, hash = account['hash'], salt = account['salt']):
                self.account['failures'] = 0
                self.account['logins'] += 1
                self.account['last_login'] = datetime.now()
                log.info('AUTH LOGIN: {}'.format(self.username))
                # If we are already playing, enter the game
                if self.account['playing']:
                    try:
                        
                        #player = load_player(self.account['playing'])
                        player = Player(self.client)
                        player_handoff(player, account)
                    except:
                        self.account['playing'] = None
                save_account(self.account)
                self.send('Welcome, {}\n\n'.format(self.username))
                self.change_state('new_ask_gender')
            else:
                self.account['failures'] += 1
                log.warning('AUTH WARNING: {} login failures for {}'.format(
                    self.account['failures'], self.username))
                save_account(self.account)
                self.send('Invalid credentials!\n\n')
                self.change_state('ask_username')
        else:
            self.send('Invalid credentials!\n\n')
            self.change_state('ask_username')
        self.driver()


    # ----------[ chargen ]------------------------------------------------
    
    def _state_new_ask_username(self):
        self.send('Choose a name for yourself (5-20 Letters only): ')
        self.change_state('new_check_username')


    def _state_new_check_username(self):
        """Validate a username against the following conditions:
        Between 5 and 20 alphabetic characters in length
        Does not duplicate an existing player name
        If the username passes, save it and move on, else re-prompt
        """
        import re
        # FIXME: add banned/reserved words check
        username = self.get_command().capitalize()
        if len(username) < 5 or len(username) > 20:
            self.send('\nUsername must be between 5-20 characters...\n')
            self.change_state('new_ask_username')
        elif not username.isalpha():
            self.send('\nUsername must contain only letters...\n')
            self.change_state('new_ask_username')
        elif account_exists(username):
            self.send('\nUsername is taken... please choose another.\n')
            self.change_state('new_ask_username')
        else:
            self.username = username
            self.change_state('new_ask_password')
        self.driver()


    def _state_new_ask_password(self):
        self.password_mode_on()
        self.send('\nPlease enter a password(8-10 Characters): ')
        self.change_state('new_ask_pwconfirm')


    def _state_new_ask_pwconfirm(self):
        self.password = self.get_command()
        self.send('\nPlease confirm password: ')
        self.change_state('new_check_password')


    def _state_new_check_password(self):
        confirm = self.get_command()
        if self.password == confirm:
            self.password_mode_off()
            self.send('\n\nPassword assigned... creating account.\n')
            log.debug('Confirmed new password for player, entering assign_account')
            self.change_state('new_assign_account')
        else:
            self.password = ''
            self.change_state('new_ask_password')
        self.driver()


    def _state_new_assign_account(self):
        """We have enough to create an account
        Create the account and initialize a Player
        Do not save either, yet
        """
        self.account = create_account(self.username, self.password)
        # Add to lobby?
        save_account(self.account)
        self.change_state('new_ask_gender')
        self.driver()


    def _state_new_ask_gender(self):
        self.send('Choose a gender (M/F): ')
        self.change_state('new_assign_gender')


    def _state_new_assign_gender(self):
        self.send('\n') 
        g = self.get_command().lower()
        if g in ('m', 'male'):
            self.gender = 'Male'
            self.change_state('new_ask_race')
        elif g in ('f', 'female'):
            self.gender = 'Female' 
            self.change_state('new_ask_race')
        else:
            self.send('Please choose only m for male or f for female!\n')
            self.change_state('new_ask_gender')
        self.driver()


    def _state_new_ask_race(self):
        self.send('\nChoose your race(Human):')
        self.change_state('new_assign_race')


    def _state_new_assign_race(self):
        self.race = 'Human'
        junk = self.get_command()
        del junk
        self.change_state('new_ask_class')
        self.driver()

    
    def _state_new_ask_class(self):
        self.send('\nChoose your class(Warrior):')
        self.change_state('new_assign_class')


    def _state_new_assign_class(self):
        self.pclass = 'Warrior'
        junk = self.get_command()
        del junk
        self.change_state('new_ask_confirm')
        self.driver()


    def _state_new_ask_confirm(self):
        self.send('\nIs this correct? ')
        self.change_state('new_confirm')


    def _state_new_confirm(self):
        """
        Now that we have a complete profile(assuming 'yes' here):
          - Create player object
          - Assign properties to player
          - Finalize player(inventory, abilities, place in start room, 
                            assign commandset)
          - Create user object, assign player to user
          - change to user_command state
          """
        confirm = self.get_command().lower()
        if confirm in ('n', 'no'):
            self.change_state('new_ask_gender')
            self.driver()
        else:
            self.send('\n\nCreating your player...')
            log.debug('Creating Player() object')
            self.player = Player(self._client)
            self.player.set_name(self.username)
            self.player.set_gender(self.gender)
            self.player.set_race(self.race)
            self.player.set_class(self.pclass)
            self.account['playing'] = self.username
            # FIXME: self.player.save()
            self.send('Finished!\n')
            # Enter game
            log.debug('Entering handoff')
            player_handoff(self.player, self.account)
