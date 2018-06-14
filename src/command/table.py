"""Command Table"""

from collections import namedtuple
from utils import log

# Command table Command Type template
CT = namedtuple('CmdType', 'name func position level args')


def find_command(search: str):
    """Look for a matching command in command table"""
    log.debug('FUNC ENTER: find_command({})'.format(search))
    if search is None or len(search) < 1:
        log.debug('FUNC RETURN: find_command() == None')
        return None
    for c in cmd_table:
        if c.name.startswith(search):
            return c


cmd_table = []


# These are listed here to ensure they are preferred.
# All other commands are included next to their definitions
cmd_table.append(CT('go',          'do_go',     'standing',  0, None))
cmd_table.append(CT('north',       'do_go',     'standing',  0, 'north'))
cmd_table.append(CT('east',        'do_go',     'standing',  0, 'east'))
cmd_table.append(CT('south',       'do_go',     'standing',  0, 'south'))
cmd_table.append(CT('west',        'do_go',     'standing',  0, 'west'))
cmd_table.append(CT('northeast',   'do_go',     'standing',  0, 'northeast'))
cmd_table.append(CT('northwest',   'do_go',     'standing',  0, 'northwest'))
cmd_table.append(CT('southeast',   'do_go',     'standing',  0, 'southeast'))
cmd_table.append(CT('southwest',   'do_go',     'standing',  0, 'southwest'))
cmd_table.append(CT('sit',         'do_sit',    'sleeping',  0, None))
cmd_table.append(CT('stand',       'do_stand',  'sleeping',  0, None))
cmd_table.append(CT('sleep',       'do_sleep',  'sleeping',  0, None))
cmd_table.append(CT('wake',        'do_wake',   'sleeping',  0, None))
cmd_table.append(CT('shutdown',    'do_quit',   'dead',    100, None))
cmd_table.append(CT('who',         'do_who',    'dead',      0, None))
cmd_table.append(CT('uptime',      'do_uptime', 'dead',      0, None))
cmd_table.append(CT('quit',        'do_quit',   'dead',      0, None))