import pytest
import sys
import os

PACKAGE_PARENT = '../src'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from actor.player import Player
from database.game_state import GameState
import globals as GLOBALS
from utils import log


def test_player_name():
    GLOBALS.game_state = GameState()
    p = Player()
    assert p.name == 'nobody'

def test_player_set_name():
    GLOBALS.game_state = GameState()
    name = 'Testname'
    p = Player()
    p.name = name
    assert p.name == name

def test_player_attributes():
    GLOBALS.game_state = GameState()
    p = Player()

    assert p.get_attribute('Baloney') == None


def test_player_set_attributes():
    GLOBALS.game_state = GameState()
    p = Player()
    p.update(strength=17)
    assert p.get_attribute('strength') == 17
    
