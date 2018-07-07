"""
Login Handler - Implements a FSM to handle logins and chargen
"""

import time
import os
from user.base_user import BaseUser
from user.helpers import user_online
from user.account import create_account, validate_password
from user.db import account_exists, save_account, load_account, record_visit
from user.user import User
from database.object import load_object,  save_object
from database.json import save_to_json
from actor.player import Player
from world.room import Room
from game_object import instances
from utils import log
import globals as GLOBALS



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
        self.account = None
        self.player = None
        self.password = None
        self.gender = None
        self.race = None


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
        passwd = self.get_command()
        if not account_exists(self.username):
            self.send('Invalid credentials!\n\n')
            self.username = ''
            self.change_state('ask_username')
            self.driver()
            return None
        self.account = load_account(self.username)
        if not validate_password(password=passwd, pwhash=self.account['hash'],
                                 salt=self.account['salt']):
            self.account['failures'] += 1
            log.warning('AUTH WARNING: %s login failures for %s',
                        self.account['failures'], self.username)
            save_account(self.account)
            self.send('Invalid credentials!\n\n')
            self.username = ''
            self.change_state('ask_username')
            self.driver()
            return None
        # There can be only one
        if user_online(self.username):
            log.warning('Duplicate login detected: %s', self.username)
            self.send('It looks like are already playing!\n\n\n')
            self.flush()
            self.client.deactivate()
            self.change_state('none')
            self.driver()
            return None
        #Looks like we're legit
        self.account['failures'] = 0
        self.account['logins'] += 1
        self.account['last_login'] = int(time.time())
        port_index = self.client.addrport().find(':')
        ipaddr = self.client.addrport()[:port_index]
        hist = {'username': self.username,
                'ip': ipaddr,
                'date': self.account['last_login']}
        record_visit(hist)
        log.info('AUTH LOGIN: %s', self.username)
        # Try to load existing player if found
        if self.account['playing']:
            log.debug(' +-> Playing as %s', self.account['playing'])
            try:
                #filename = os.path.join(GLOBALS.DATA_DIR, GLOBALS.INSTANCE_DIR,
                #                        GLOBALS.PLAYER_DIR,
                #                        self.account['playing'].lower(),
                #                        self.account['playing'].lower() + '.json')
                #self.player = load_object(filename)
                for gid, player in GLOBALS.all_players.items():
                    log.debug('GID, PLAYER == %s, %s', gid, player)
                    if player.name == self.account['playing']:
                        log.info('Found matching player GID %s for "%s"', gid, player.name)
                        self.player = player
                        break
                else:
                    log.error('Could not locate player in global players list')
                self.player.client = self.client
                self.change_state('player_handoff')
                self.send('Welcome back, {}!\n\n'.format(self.username))
            except Exception as err:
                log.warning('FAILED Player.load(%s): %s', self.username, err)
                self.change_state('new_ask_gender')
            self.driver()
        else:
            self.account['playing'] = None
            self.change_state('new_ask_gender')
            save_account(self.account)
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
        save_account(self.account)
        self.change_state('new_ask_gender')
        self.driver()


    def _state_new_ask_gender(self):
        self.send('Choose a gender (M/F): ')
        self.change_state('new_assign_gender')


    def _state_new_assign_gender(self):
        self.send('\n')
        selection = self.get_command().lower()
        if selection in ('m', 'male'):
            self.gender = 'Male'
            self.change_state('new_ask_race')
        elif selection in ('f', 'female'):
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
        elif confirm in ('y', 'yes'):
            self.send('\n\nCreating your player...')
            log.debug('Creating Player() object')
            self.player = Player()
            self.player.client = self.client
            self.player.name = self.username
            self.player.gender = self.gender
            self.player.race = self.race
            log.info('Saving player %s', self.player.name)
            save_object(self.player)
            self.account['playing'] = self.username
            save_account(self.account)
            self.send('Finished!\n')
            # Prepare player to enter game
            self.change_state('player_handoff')
            self.driver()
        else:
            self.send("\nPlease answer only 'y'es or 'n'o\n")
            self.change_state('new_ask_confirm')
            self.driver()


    def _state_player_handoff(self):
        """
        Prepare to enter the game
        Create the user and associate user account
        Set command handler, assign commands, initial room
        """
        user = User(self.player.client)
        log.debug('User created successfully')
        user.client = self.player.client
        user.username = self.account['username']
        user.player = self.player
        user.change_state('playing')
        # Remove us from lobby, should clean up Login() object
        del GLOBALS.lobby[self.player.client]
        # Insert the user into the players dict
        # This enables the user command interpreter via User.driver()
        GLOBALS.players[self.player.client] = user
        if self.player.location == None:
            self.player.location = GLOBALS.START_ROOM
        GLOBALS.rooms[self.player.location].add_actor(self.player)
        user.send('\n')
