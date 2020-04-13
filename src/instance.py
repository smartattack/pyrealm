"""
Game Object instancer
"""

from weakref import WeakValueDictionary
from utils import log

class objRegistry():
   # Initial value, incremented before return
   gid = 0
   all_instances = weakValueDictionary()
   all_items = weakValueDictionary()
   all_actors = weakValueDictionary()
   all_rooms = weakValueDictionary()
