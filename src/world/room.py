"""
Room Class
"""

from collections import namedtuple
from utils import log
from actor.player import Player
import globals as GLOBALS

__all__ = [ 'Room', 'DIR_NAMES', 'DIR_NORTH', 'DIR_EAST', 'DIR_SOUTH', 'DIR_WEST',
            'DIR_UP', 'DIR_DOWN', 'DIR_NORTHEAST', 'DIR_NORTHWEST', 'DIR_SOUTHEAST',
            'DIR_SOUTHWEST', 'DIR_SOMEWHERE' ]

Dir_Text = namedtuple('Dir_Text', 'dirnum dest source mapstr')
DIR_NAMES = (
    Dir_Text(0, 'North', 'South', 'N'),
    Dir_Text(1, 'East', 'West', 'E'),
    Dir_Text(2, 'South', 'North', 'S'),
    Dir_Text(3, 'West', 'East', 'W'),
    Dir_Text(4, 'Up', 'Above', 'U'),
    Dir_Text(5, 'Down', 'Below', 'D'),
    Dir_Text(6, 'Northeast', 'Southwest', 'NE'),
    Dir_Text(7, 'Northwest', 'Southeast', 'NW'),
    Dir_Text(8, 'Southeast', 'Northwest', 'SE'),
    Dir_Text(9, 'Southwest', 'Northeast', 'SW'),
    Dir_Text(10, 'nothingness', 'the thin air', ''), 
)

# Used by exits.  Compatible with Merc
DIR_NORTH     = 0
DIR_EAST      = 1
DIR_SOUTH     = 2
DIR_WEST      = 3
DIR_UP        = 4
DIR_DOWN      = 5
DIR_NORTHEAST = 6
DIR_NORTHWEST = 7
DIR_SOUTHEAST = 8
DIR_SOUTHWEST = 9
DIR_SOMEWHERE = 10


def dir_name(direction: int, origin=False):
    """Return a textual direction name"""
    try:
        key = DIR_NAMES[direction]
        if origin:
            return key.source
        else:
            return key.dest
    except (KeyError, AttributeError) as err:
        log.warning('DIR_NAMES[%s] does not exist!', direction)


# match directions
def match_direction(text: str):
    """Match text to direction"""
    log.debug('FUNC match_directions')
    search = text.lower()
    for dir_number, dir_name, ignore in DIR_NAMES:
        if dir_name.lower().startswith(search):
            log.debug('Matched direction: %s (%s)', dir_number, dir_name)
            return dir_number
    if search == 'ne':
        log.debug('Matched direction: %s (%s)', dir_number, dir_name)
        return DIR_NORTHEAST
    elif search == 'nw':
        log.debug('Matched direction: %s (%s)', dir_number, dir_name)
        return DIR_NORTHWEST
    elif search == 'se':
        log.debug('Matched direction: %s (%s)', dir_number, dir_name)
        return DIR_SOUTHEAST
    elif search == 'sw':
        log.debug('Matched direction: %s (%s)', dir_number, dir_name)
        return DIR_SOUTHWEST
    else:
        return None


class Room(object):
    """
    A room is basically a container object
    """

    def __init__(self, vnum=None, name=None, desc=None,
                 outside=None, exits=None):
        self.vnum = vnum
        self.name = name
        self.description = desc
        self._outside = outside
        self.actors = []
        self.exits = {}
        if exits:
            self.exits = exits
        self._checksum = ''
        self._last_saved = ''
        log.debug('Room created: %s', self.__repr__())

    
    def __repr__(self):
        return 'Room object, vnum={}, name={}'.format(self.vnum, self.name)

    def is_outside(self):
        """Return true if outside(affected by daylight)"""
        if self._outside:
            return True
        else:
            return False


    def add_actor(self, act):
        """Add a character to a room"""
        log.debug('FUNC Room.add_actor()')
        if not act in self.actors:
            log.debug('Adding %s to room %s', act.get_name(), self.vnum)
            self.actors.append(act)
            if isinstance(act, Player):
                act.send(self.show_info())


    def remove_actor(self, act):
        """Remove character from room"""
        log.debug('FUNC Room.remove_actor()')
        if act in self.actors:
            log.debug('Removing %s from room %s', act.get_name(), self.vnum)
            self.actors.remove(act)


    def _exit_str(self, direction):
        """Show an exit on small map"""
        if direction in self.exits:
            output = '^Y{}^d'.format(self.exits[direction].mapstr)
        else:
            if direction in (DIR_NORTH, DIR_SOUTH):
                output = ' '
            elif direction in (DIR_WEST, DIR_UP, DIR_DOWN, DIR_EAST):
                output = '-'
            else:
                output = '  '
        return output

    def show_exits(self):
        """Return stringified exits"""
        exits = []
        for exit in self.exits:
            log.debug('EXIT == %s, dir_name(exit) == %s', exit, dir_name(exit))
            exits.append('^G{}^d'.format(dir_name(exit)))
        log.debug('EXIT == %s', exits)
        return '^WExits: ^G' + ', '.join(map(str, exits)) + '^w.^d\n\n'


    def show_info(self):
        output = '^W{0:60}^d{}  {}  {}\n'.format(self.name,
                                                self._exit_str(DIR_NORTHWEST),
                                                self._exit_str(DIR_UP),
                                                self._exit_str(DIR_NORTHEAST))
                                                

        return output
"""
        output = '^G{}^d\n'.format(self.name) + \
                 '^g{}^d\n'.format(self.description) + \
                 self.show_exits()
        return output
"""
