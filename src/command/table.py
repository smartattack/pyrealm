"""Command Table"""

from collections import OrderedDict
from utils import log

POS_DEAD     = 0
POS_SLEEPING = 1
POS_SITTING  = 2
POS_FIGHTING = 3
POS_READY    = 4


class Command():
    """Command table entry definition"""
    def __init__(self, name, func, position = 0, level = 0):
        self.name = name
        self.func = func
        self.position = position
        self.level = level


def find_command(search: str):
    """Look for a matching command in command table"""
    log.debug('FUNC ENTER: find_command({})'.format(search))
    if search is None:
        log.debug('FUNC RETURN: find_command() == None')
        return None
    for c in cmd_table.values():
        if c.name.startswith(search):
            return c


def register_command(entry: Command):
    """Add a command to cmd_table"""
    log.info('++ Adding cmd_table[{}]'.format(entry.name))
    cmd_table[entry.name] = entry


cmd_table = OrderedDict()


# Due to ordered dict, listed here first to assert preference
register_command(Command(name = 'quit',     func = 'do_quit',    position = 0, level = 0))
register_command(Command(name = 'who',      func = 'do_who',     position = 0, level = 0))
