"""
Base User class - base class for logged in accounts
"""

from utils import log
from miniboa import TelnetServer

_def_preferences = {
    color = False,
    prompt = '>>>',
    MSP = False,
    MCCP = False,
}

class BaseUser(object):
    """
    Holds information about logged in user accounts.
    Stores terminal related user preferences.
    Contains references to client connection and account data.
    Wraps send and get_command functions.
    Do not call directly.
    """

    def __init__(self, client):
        """Create a user and associate with a connected client"""
        self._client = client
        #Global CLIENTS[] = self


    def send(self, msg):
        """Send text to client, don't wrap but do process colors"""
        self._client.send_cc(self, msg)
    

    def senc_wrapped(self, msg):
        """Send wrapped text to client, processes colors"""
        self._client.send_wrapped(self, msg)
    

    def send_raw(self, msg):
        """Send text to client without any processing"""
        self._client.send(self, msg)
    


    def get_preference(self, which):
        """Return one preference"""
        if which in self._preferences:
            return self._preference[which]
        else:
            return None
    
    def set_preference(self, which, value):
        """Set a user preference"""
        try:
            self._preference[which] = value
        except ValueError as e:
            log.warning('Setting user preference FAILED: {} -> {}'.format(user._client['name'], e))