"""
Base User class - base class for logged in accounts. a FSM.
"""

import sys
import copy
from utils import log
from miniboa import TelnetServer

_def_preferences = {
    'color':   False,
    'prompt':  '>>>',
    'MSP':     False,
    'MCCP':    False,
}

class BaseUser(object):
    """
    Holds information about logged in user accounts.
    Stores terminal related user preferences(??)
    Contains references to client connection and account data.
    Wraps send and get_command functions.
    Do not call directly.
    """

    def __init__(self, client):
        """Create a user and associate with a connected client"""
        self._client = client
        #Global CLIENTS[] = self
        self._preferences = copy.copy(_def_preferences)
        self._state = 'none'

    """
    FIXME: Maybe I should take BaseActor and BaseUser client function wrappers
    and move them into a Mixin that both inherit from, like TelnetWrapperMixing?
    """

    def change_state(self, state):
        """Transition to a new state"""
        self._state = '_state_' + state


    def driver(self):
        """Locate a function for current state and execute"""
        try:
            self.__getattribute__(self._state)()
        except Exception as e:
            # We should never get here
            log.error('Invalid state passed: {} -> {}'.format(self._state, e))
            sys.exit(1)


    def _state_none(self):
        """Empty state to serve as a default"""
        pass


    def send(self, msg):
        """Send text to client, don't wrap but do process colors"""
        self._client.send_cc(msg)
    

    def send_wrapped(self, msg):
        """Send wrapped text to client, processes colors"""
        self._client.send_wrapped(msg)
    

    def send_raw(self, msg):
        """Send text to client without any processing"""
        self._client.send(msg)
    

    def get_command(self):
        """Retrieve a command from the client"""
        return self._client.get_command()


    def get_idle(self):
        """Return idle_time"""
        return self._client.idle()


    def get_duration(self):
        """Return connection duration"""
        return self._client.duration()


    def password_mode_on(self):
        """Disable echo"""
        self._client.password_mode_on()


    def password_mode_off(self):
        """Re-enable echo"""
        self._client.password_mode_off()
 
 
    def deactivate(self):
        """Deactivate client session"""
        self._client.deactivate()


    def get_preference(self, which):
        """Return one preference"""
        if which in self._preferences:
            return self._preferences[which]
        else:
            return None
    
    
    def set_preference(self, which, value):
        """Set a user preference"""
        """
        FIXME: this should actually toggle the underlying client's state
        """
        try:
            self._preferences[which] = value
        except ValueError as e:
            log.warning('Setting user preference FAILED: {} -> {}'.format(self._client['name'], e))