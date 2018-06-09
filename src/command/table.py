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


def register_command(entry: Command):
    """Add a command to cmd_table"""
    log.info('++ Adding cmd_table[{}]'.format(entry.name))
    cmd_table[entry.name] = entry

cmd_table = OrderedDict()

register_command(name = 'quit',     func = command.do_quit,    0, level = 0)
register_command(name = 'who',      func = command.do_who,     0, level = 0)
