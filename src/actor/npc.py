"""
Non-Player Characters (MOBs)
"""

from utils import log
from actor.base_actor import BaseActor
from game_object import InstanceRegistry


class NPC(BaseActor):
    """NPC will have similar traits to players but lack abilities"""
    def __init__(self):
        BaseActor.__init__(self)
        log.debug('Adding NPC %s to instances.all_npcs', self.gid)
        GLOBALS.all_npcs[self.gid] = self

    """FIXME: Implementation needed"""
    def post_init(self):
        """Called after load_from_json deserializes the structure.  Fills in
        missing important bits"""
        self._skip_list.update(['inventory', 'worn'])
        self.inventory = []
        self.worn = []