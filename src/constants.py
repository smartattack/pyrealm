"""
Game data - this is imported inside of main()
"""

logfile = "../log/pyrealm.log"

magic = [
    {"name": "Fire",     "cost":  10,  "damage":  10, "level": 1},
    {"name": "Ice",      "cost":  10,  "damage":  10, "level": 1},
    {"name": "Thunder",  "cost":  12,  "damage":  15, "level": 1}
]

# Shown to players on initial connection
WELCOME_BANNER = """
/*******************
 * PyRealm Server  *
 ******************/
 
What is your name(newuser for new users):"""

