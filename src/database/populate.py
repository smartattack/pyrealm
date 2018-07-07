"""
Create some items
"""


from utils import log
from item.base_item import BaseItem
from database.object import save_object


def populate():
    """Temporary item creation for testing.  Later this will be resets"""
    item = BaseItem(name='Magic Wand', description='A magic wand hums with a mysterious energy',
                    short_desc='magic wand')
    item.add_to_room(2)
    save_object(item)