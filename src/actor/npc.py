"""
Non-Player Characters (MOBs)
"""

from utils import log
from actor.base_actor import BaseActor

class NPC(BaseActor):
    """NPC will have similar traits to players but lack abilities"""
    def __init__(self):
        BaseActor.__init__(self)

    """FIXME: Implementation needed"""