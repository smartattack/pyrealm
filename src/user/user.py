"""
User Class - represents a connected user
"""

from user.base_user import BaseUser
from actor.player import Positions
from utils import log
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
        self._commands = set()
        self.player = None
        self._last_cmd = None
        self._last_args = []


    def add_command(self, cmd):
        """Add a command to user"""
        log.debug('Adding "%s" command to player %s', cmd, self.username)
        self._commands.add(command)


    def remove_command(self, cmd):
        """Remove a command from user"""
        log.debug('Removing "%s" command from player %s', cmd, self.username)
        self._commands.remove(cmd)


    def clear_commands(self):
        """Clear all user commands"""
        log.debug('Removing all commands from player %s', self.username)
        self._commands = set()


    def has_command(self, cmd):
        """Return bool if user has a command or not"""
        if cmd in self._commands:
            return True
        else:
            return False


    def list_commands(self):
        """List all commands for a user"""
        return list(self._commands)


    def _parse_command(self):
        """Return a command and args[] for user input"""
        line = self.client.get_command()
        words = line.split(' ')
        cmd = words[0]
        if len(words) > 1:
            args = words[1:]
        else:
            args = []
        return cmd, args

    def _state_playing(self):
        """User command interpreter"""
        cmd, args = self._parse_command()
        log.debug('USER INPUT: |%s| -> |%s|', cmd, args)
        if len(cmd) < 1:
            self.send('\n')
            return
        if cmd == '!':
            # Repeat last command
            cmd = self._last_cmd
            args = self._last_args
        match = find_command(cmd)
        if match:
            # Store this command as last_command
            self._last_cmd = cmd
            self._last_args = args
            log.debug('MATCHED COMMAND: %s', match.name)
            # Check level
            if match.level > self.player.get_stat('level'):
                log.debug('Player %s has too low a level to invoke command: %s',
                          self.player.name, match.name)
                return
            if Positions.index(match.position) > Positions.index(self.player.position):
                log.debug('Player %s has too low a position to invoke command: %s',
                          self.player.name, match.name)
                self.send('You cannot do that while you are {}\n'.format(self.player.position))
                return
            # Attempt to dispatch the command, might make this a try/except
            if hasattr(command, match.func):
                # Prepend args if populated in cmd_table entry
                if match.args:
                    args = [ match.args ] + args
                #log.debug('Command module has method: %s', match.func)
                getattr(command, match.func)(self.player, args)
                log.debug('Calling %s(%s, %s)', match.func, self.player.name, args)
            else:
                log.debug('Command module does not have method: %s', match.func)
        else:
            self.send('^rUnknown command!^d\n')

