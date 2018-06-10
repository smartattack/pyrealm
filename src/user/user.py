"""
User Class - represents a connected user
"""

from utils import log
import globals as GLOBALS
from actor.player import Player
from user.base_user import BaseUser
import command
from command.table import find_command





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
        cmd, args = self._parse_command()
        log.debug('USER INPUT: {} -> {}'.format(cmd, args))
        c = find_command(cmd)
        if c:
            log.debug('MATCHED COMMAND: {}'.format(c.name))
            # Check level
            if c.level <= self.player.get_stat('level'):
                # Attempt to dispatch the command
                if hasattr(command, c.func):
                    log.debug('Command module has method: {}'.format(c.func))
                    getattr(command, c.func)(self.player, args)
                    log.debug('Calling {}({}, {})'.format(c.func, self.player.get_name(), args))
                    self.send_prompt()
                else:
                    log.debug('Command module does not have method: {}'.format(c.func))
            else:
                log.debug('Player {} has too low a level to invoke command: {}'.format(
                        self.player.get_name(), c.name))
        else:
            self.send('Unknown command!')
            self.send_prompt()
