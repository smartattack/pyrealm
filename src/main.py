



from classes.character import Character
from constants import *
from communication import *

if __name__ == "__main__":
    player = Character(hp=465, mp=65, attack=60, defense=34, magic=magic)
    send("{}".format(player.gen_damage()))
    send("{}".format(player.gen_damage()))
    send("{}".format(player.gen_damage()))
    send(recv("What are you wanting"))
