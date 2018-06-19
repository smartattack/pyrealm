import pytest
import sys
import os

PACKAGE_PARENT = '../src'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


from actor.player import Player


def test_player_name():
    p = Player()
    assert p.name == 'nobody'

def test_player_set_name():
    name = 'Testname'
    p = Player()
    p.set_name(name)
    assert p.name == name

def test_player_attributes():
    p = Player()

    assert p.get_attribute('Baloney') == None


def test_player_set_attributes():
    p = Player()
    p.update(strength=17)
    assert p.get_attribute('strength') == 17
    
