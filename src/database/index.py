"""
Database Index load/save
"""

from utils import log
from database.json import load_json_index, save_json_index
import globals as GLOBALS

def load_indexes():
    """Load persisted instance indexes"""
    log.debug("Running load_indexes()")
    load_json_index()


def save_indexes():
    """Persist the instance indexes"""
    log.debug("Running save_indexes()")
    data = []
    for instance in GLOBALS.all_instances.values():
        data.append({ 'gid':instance.gid, 'itype':type(instance), 'name':instance.name })
    # Save to JSON for now, maybe SQLite later
    save_json_index(data)