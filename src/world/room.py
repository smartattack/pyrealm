"""
Room Class
"""

from collections import namedtuple
from utils import log
from actor.player import Player
import globals as GLOBALS

Dir_Text = namedtuple('Dir_Text', 'dirnum exits enters')
DIR_NAMES = (
    Dir_Text(0, 'North', 'South'),
    Dir_Text(1, 'East', 'West'),
    Dir_Text(2, 'South', 'North'),
    Dir_Text(3, 'West', 'East'),
    Dir_Text(4, 'Up', 'Above'),
    Dir_Text(5, 'Down', 'Below'),
    Dir_Text(6, 'Northeast', 'Southwest'),
    Dir_Text(7, 'Northwest', 'Southeast'),
    Dir_Text(8, 'Southeast', 'Northwest'),
    Dir_Text(9, 'Southwest', 'Northeast'),
    Dir_Text(10, 'nothingness', 'the thin air'), 
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


class Room(object):
    """
    A room is basically a container object
    """

    def __init__(self, id=None, name=None, desc=None,
                 outside=None, exits=None):
        self.id = id
        self.name = name
        self.description = desc
        self._outside = outside
        self.actors = []
        self.exits = {}
        if exits:
            self.exits = exits
        log.debug('Room created: %s', self.__repr__())

    
    def __repr__(self):
        return 'Room object, id={}, name={}'.format(self.id, self.name)

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
            log.debug('Adding %s to room %s', act.get_name(), self.id)
            self.actors.append(act)
            if isinstance(act, Player):
                act.send('^Y{}^d\n^G{}^d\n'.format(self.name, self.description))


    def remove_actor(self, act):
        """Remove character from room"""
        log.debug('FUNC Room.remove_actor()')
        if act in self.actors:
            log.debug('Removing %s from room %s', act.get_name(), self.id)
            self.actors.remove(act)


GLOBALS.rooms[1] = Room(id=1, name='Entrance', desc='A lit entryway', outside=True,
                        exits={DIR_NORTH:{'to_room':2}})

GLOBALS.rooms[2] = Room(id=2, name='Courtyard', desc='An empty courtyard', outside=True,
                        exits={DIR_SOUTH:{'to_room':1}})