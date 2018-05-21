"""
Character is the base class for all NPC and players
"""

import random
import logging
mudlog = logging.getLogger('mudlog')

class Character:
    "Not used directly, inherited by player and npc"

    def __init__(self, hp=10, mp=10, attack=10, defense=10, magic=None):

        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.attack = attack
        self.attack_range = 10
        self.defense = defense
        self.magic = magic
        self.isdead = False
        self.location = ''
        self.money = 0
        self.status_effects = []

    def gen_damage(self):
        return random.randrange(self.attack - self.attack_range, self.attack + self.attack_range)

    def gen_defense(self):
        pass

    def apply_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
            self.isdead = True
        return self.hp

    def get_hp(self):
        return self.hp

    def get_maxhp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.maxmp

    ''' Assumes caller has checked whether self.mp > cost '''

    def reduce_mp(self, cost):
        self.mp -= cost

    ''' Do we want these? '''

    def get_spell_name(self, i):
        return self.magic[i]["name"]

    ''' Do we want these? '''

    def get_spell_mp_cost(self, i):
        return self.magic[i]["cost"]
