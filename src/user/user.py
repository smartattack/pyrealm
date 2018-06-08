"""
User Class - represents a connected user
"""

from utils import log
import globals as GLOBAL
from user.base_user import BaseUser


def user_online(username):
    """Check if a given username is logged in"""
    if username:
        for user in GLOBAL.PLAYERS.values():
            if user.username == username:
                return True
    return False


class User(BaseUser):
    """
    Holds information about a connected user, including available commands
    and reference to associated player object.
    """

    def __init__(self, client):
        log.debug('Inside User.__init__()')
        BaseUser.__init__(self, client)
        # Set of allowed commands
        self.commands = set()


    def add_command(self, command):
        log.debug('Adding "{}" command to player {}'.format(command, self.username))
        self._commands.add(command)


    def remove_command(self, command):
        log.debug('Removing "{}" command from player {}'.format(command, self.username))
        self._commands.remove(command)


    def clear_commands(self):
        log.debug('Removing all commands from player {}'.format(self.username))
        self._commands = set()


    def has_command(self, command):
        if command in self._commands:
            return True
        else:
            return False


    def list_commands(self):
        return list(self._commands)

    def _parse_command(self):
        """Return a command and args[] for user input"""
        line = self._client.get_command()
        words = line.split(' ')
        command = words[0]
        if len(words) > 1:
            args = words[1:]
        else:
            args = []        
        return command, args

    def _state_playing(self):
        """User command interpreter"""
        command, args = self._parse_command()
        log.debug('USER INPUT: {} -> {}'.format(command, args))
        self.send('\n{} -> {}\n'.format(command, args))
        self.send_prompt()
