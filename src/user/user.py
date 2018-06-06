"""
User Class - represents a connected user
"""

from utils import log
from user.base_user import BaseUser


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
        log.debug('Adding "{}" command to player {}'.format(command, self._profile['name']))
        self._commands.add(command)


    def remove_command(self, command):
        log.debug('Removing "{}" command from player {}'.format(command, self._profile['name']))
        self._commands.remove(command)


    def clear_commands(self):
        log.debug('Removing all commands from player {}'.format(self._profile['name']))
        self._commands = set()


    def has_command(self, command):
        if command in self._commands:
            return True
        else:
            return False


    def list_commands(self):
        return list(self._commands)


    def _state_playing(self):
        """User command interpreter"""
        line = self._client.get_command()
        command, args = line.split(' ')
        log.debug('USER INPUT: {} -> {}'.format(command, args))
        self.player.send('{} -> {}'.format(command, args))
        