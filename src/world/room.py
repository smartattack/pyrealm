"""
Room Class
"""

from utils import log, wrap_one_line
from miniboa.xterm import word_wrap as miniboa_wrap
from game_object import GameObject, InstanceRegistry
from world.direction import *
import globals as GLOBALS


class Room(GameObject):
    """
    A room is basically a container object
    """
    vnum = None

    def __init__(self, vnum=None, name=None, description=None,
                 outside=None, exits=None):
        """NOTE: I am not called on objects loaded from disk."""
        log.debug("Inside Room.init()")
        super().__init__(name=name, description=description,
                            skip_list=['actors', 'inventory'])
        # vnum is used by exits
        self.vnum = vnum
        self._outside = outside
        # Inventory is a list of instances
        self.inventory = []
        self.actors = []
        self.exits = {}
        if exits:
            self.exits = exits
        log.debug('Registering Room %s with instances.all_rooms', self.gid)
        GLOBALS.all_locations[self.gid] = self
        log.debug('Room created: %s', self.__repr__())


    def post_init(self):
        """This init gets called after a load from disk.  It reconstitutes missing data"""
        self.actors = []
        self.inventory = []
        self._skip_list.update(['actors','inventory'])


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
        log.debug('FUNC Room.add_actor(%s) -> %s', act.name, self.vnum)
        if not act in self.actors:
            log.debug('Adding %s to room %s', act.name, self.vnum)
            self.actors.append(act)
            # Don't send to NPCs
            if hasattr(act, 'send'):
                act.send(self.show_info(act.client.columns))


    def remove_actor(self, act):
        """Remove character from room"""
        log.debug('FUNC Room.remove_actor()')
        if act in self.actors:
            log.debug('Removing %s from room %s', act.name, self.vnum)
            self.actors.remove(act)


    def add_item(self, item):
        """Add an item to room inventory"""
        try:
            self.inventory.append(item)
        except Exception as err:
            log.error('Unable to add %s to Room inventory, type(%s): %s', item, type(item), err)


    def remove_item(self, item):
        """Remove an item from room inventory"""
        if item in self.inventory:
            log.debug('Removing {} from room {} inventory',
                      item.name, self.vnum)
            self.inventory.remove(item)
        else:
            log.warning('Did not find item %s in room %s inventory',
                        item.name, self.vnum)


    def _exitstr(self, direction):
        """Show an exit on small map"""
        log.debug('FUNC _exit_str(%s)', direction)
        output = None
        if direction in self.exits:
            log.debug('%s', self.exits[direction])
            return '^c{}^d'.format(dir_name(direction, map=True))
        else:
            return ''


    def show_exits(self):
        """Return stringified exits"""
        exits = []
        for exit in self.exits:
            log.debug('EXIT == %s, dir_name(exit) == %s', exit, dir_name(exit))
            exits.append('^G{}^d'.format(dir_name(exit)))
        log.debug('EXIT == %s', exits)
        return '^WExits: ^w[^G' + ', '.join(map(str, exits)) + '^w].^d\n\n'


    def show_info(self, width=70):
        """Show room name, exit map, description"""
        log.debug('FUNC show_info(%s)', width)
        swidth = width - 15
        output = '^W{}^d{}   {}  {}\n'.format(
                                self.name.ljust(swidth, ' '),
                                self._exitstr(DIR_NORTHWEST).ljust(2, ' '),
                                self._exitstr(DIR_NORTH).ljust(2,' '),
                                self._exitstr(DIR_NORTHEAST).ljust(2, ' '))
        output += '^w{}^d{}^w--{}^w(^Y*^w){}^w--{}\n'.format(
                                                '-'.ljust(swidth, '-'),
                                self._exitstr(DIR_WEST).ljust(1, '-'),
                                self._exitstr(DIR_UP).ljust(1, '-'),
                                self._exitstr(DIR_DOWN).ljust(1, '-'),
                                self._exitstr(DIR_EAST).ljust(1, '-'))
        (first_line, remaining) = wrap_one_line(self.description, swidth)
        output += '^g{}^d{}   {}  {}\n'.format(
                                first_line.ljust(swidth, ' '),
                                self._exitstr(DIR_SOUTHWEST).ljust(2, ' '),
                                self._exitstr(DIR_SOUTH).ljust(2,' '),
                                self._exitstr(DIR_SOUTHEAST).ljust(2, ' '))
        if remaining:
            log.debug("REMAINING=|%s|", remaining)
            remaining = '\n'.join(miniboa_wrap(remaining, width, indent=0, 
                                              padding=0)).lstrip()
            output += '^g{}^d\n'.format(remaining)
        items = []
        for item in self.inventory:
            items.append(item.short_desc)
        if items:
            output += '^wItems here:\n^M' + '^w, ^M'.join(items) + '\n^d'
        return output