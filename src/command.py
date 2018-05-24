"""
Command Interpreter
"""

from player import Player

command_table = {

    "help": "do_help",
    "quit": "do_quit",
}


def do_help(player):
    for command in command_table:
        player.tell("{}\n".format(command))


def do_quit(player):
    player.send_now(player.cid, "Goodbye!\n\n")
    player.mud.disconnect(player.cid)
    player.state = Player._PLAYER_DISCONNECT

def parse_command(player):
    """Parse input line into command and arguments"""
    words = player.input.split(' ')
    player.command = words[0]
    player.args = words[1:]

def find_matching_command(text):
    """Search command_table and find best match"""

    for entry in command_table:
        if text in entry:
            return command_table[text]

    # Not found, return catch-all
    return "unknown"



def command_handler(player):
    """ Dispatch command functions based on parsed command"""

    parse_command(player)
    player_command = find_matching_command(player.command)

    if player_command == 'unknown':
        player.tell("Unrecognized command!")
    else:
        "Call function in command table"
        exec("{}(player)".format(player_command))
    player.command = None
    player.args = None