# Test utils functions
import time
import pytest
import sys
import os

PACKAGE_PARENT = '../src'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


from database.tables import to_json, from_json, make_checksum
from actor.player import Player

# Setup

def test_json_conversion():

    errors = []

    jstest = Player()
    
    converted = to_json(jstest)
    restored = from_json(converted)
    if type(restored) != type(jstest):
        errors.append("Restored object type != Original object type")

    converted._skip_list = [ '_name' ]
    converted = to_json(jstest)
    restored = from_json(converted)
    if hasattr(jstest, '_name') != True:
        errors.append("Test object is missing required attribute _name - setup failure")
    if hasattr(restored, '_name') != False:
        errors.append("Test failed: Converted object contains field which should be skipped")

    assert errors == []


def test_make_checksum():
    input = 'Some text to checksum'
    testhash = make_checksum(input)

    assert testhash == '8ca468e971e74fc26372ab0507ef6796'
