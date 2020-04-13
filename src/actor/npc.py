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
        InstanceRegistry.all_npc[self.gid] = self

    """FIXME: Implementation needed"""