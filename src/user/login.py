"""
Login Handler - Implements a FSM to handle logins and chargen
"""

from actor.player import Player
from user.base_user import BaseUser
from utils import log


class Login(BaseUser):
    """
    Login existing players
    Create new accounts and characters
    """
    def __init__(self, client):
        BaseUser.__init__(self, client)
        self.change_state('ask_username')
        self.driver()


    def _state_ask_username(self):
        """Send username prompt"""
        self.send('What is your name? ')
        self.change_state('check_username')


    def _state_check_username(self):
        """Check username, either enter chargen or request password"""
        username = self.get_command()
        if username.lower() == 'new':
            self.change_state('new_ask_username')
        elif username.lower() == 'quit':
            self.change_state('none')
            self.send('Goodbye\n\n')
            self.deactivate()
        else:
            self.username = username
            self.change_state('ask_password')
        self.driver()


    def _state_ask_password(self):
        """Send password prompt"""
        self.password_mode_on()
        self.send('Password: ')
        self.change_state('check_password')


    def _state_check_password(self):
        """Validate login"""
        #FIXME: actually validate password here
        self.password_mode_off()
        self.send('\n')
        password = self.get_command()
        if password.lower() == 'pass':
            self.send('Welcome: {}\n\n'.format(self.username))
        else:
            self.send('Invalid credentials!\n\n')
            self.change_state('ask_username')
        self.driver()


    # ----------[ chargen ]------------------------------------------------
    
    def _state_new_ask_username(self):
        self.send('Choose a name for yourself (5-20 Letters only): ')
        self.change_state('new_check_username')



    def _state_new_check_username(self):
        import re
        # FIXME: implement
        #self.driver()
        username = self.get_command()
        if len(username) < 5 or len(username) > 20:
            self.send('\nUsername must be between 5-20 characters...\n')
            self.change_state('new_ask_username')
        elif re.search('^[a-zA-Z]', username): # FIXME: THIS IS BROKEN
            self.send('\nUsername must contain only letters...\n')
            self.change_state('new_ask_username')
        else:
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
        # FIXME: implement
        #self.driver()
        pass


    def _state_new_ask_gender(self):
        self.send('Choose a gender (M/F): ')
        self.change_state('new_assign_gender')


    def _state_new_assign_gender(self):
        self.send('\n') 
        g = self.get_command().lower()
        if g in ('m', 'male'):
            gender = 'M'
            self.change_state('new_ask_race')
        elif g in ('f', 'female'):
            gender = 'F'
            self.change_state('new_ask_race')
        else:
            self.send('Please choose only m for male or f for female!\n')
            self.change_state('new_ask_gender')
        self.driver()
        
    def _state_new_ask_race(self):
        # FIXME: implement
        pass


    def _state_new_assign_race(self):
        # FIXME: implement
        self.change_state('new_ask_class')
        self.driver()

    
    def _state_new_ask_class(self):
        # FIXME: implement
        pass
    

    def _state_new_assign_class(self):
        # FIXME: implement
        self.change_state('new_ask_confirm')
        self.driver()


    def _state_new_ask_confirm(self):
        # FIXME: implement
        pass
    

    def _state_new_confirm(self):
        """
        Now that we have a complete profile(assuming 'yes' here):
          - Assign profile to user
          - Commit user account
          - Finalize player(inventory, abilities, place in start room, 
                            assign commandset)
          - change to user_command state
          ** Figure out how to cleanup Login object so we don't leak
          """
        # FIXME: implement
        pass