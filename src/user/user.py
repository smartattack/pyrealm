"""
User Class - represents a connected user
"""

from utils import log
from user.base_user import BaseUser


class User(BaseUser):
    """
    Holds information about a connected user, including available commands
    and reference to associated player object.
    """

    def __init__(self, client):
        BaseUser.__init__(client)
        # Set of allowed commands
        self.commands = set()


