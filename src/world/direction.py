"""
Room Class
"""

from collections import namedtuple
from utils import log


__all__ = [ 'dir_name', 'match_direction', 'DIR_NAMES', 'DIR_NORTH', 'DIR_EAST',
            'DIR_SOUTH', 'DIR_WEST', 'DIR_UP', 'DIR_DOWN', 'DIR_NORTHEAST',
            'DIR_NORTHWEST', 'DIR_SOUTHEAST', 'DIR_SOUTHWEST', 'DIR_SOMEWHERE' ]


Dir_Text = namedtuple('Dir_Text', 'dirnum dest source map')
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


def dir_name(direction: int, origin=False, map=False):
    """Return a textual direction name"""
    log.debug('FUNC dir_name(%s)', direction)
    try:
        key = DIR_NAMES[direction]
        if map:
            return key.map
        elif origin:
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
    for number, name, ignore, ignore in DIR_NAMES:
        if name.lower().startswith(search):
            log.debug('Matched direction: %s (%s)', number, name)
            return number
    if search == 'ne':
        log.debug('Matched direction: %s (%s)', number, name)
        return DIR_NORTHEAST
    elif search == 'nw':
        log.debug('Matched direction: %s (%s)', number, name)
        return DIR_NORTHWEST
    elif search == 'se':
        log.debug('Matched direction: %s (%s)', number, name)
        return DIR_SOUTHEAST
    elif search == 'sw':
        log.debug('Matched direction: %s (%s)', number, name)
        return DIR_SOUTHWEST
    else:
        return None

