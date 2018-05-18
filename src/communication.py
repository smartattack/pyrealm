'''
Handle communication with players

At first we may use input and printf, later on sockets.
This is meant to abstract the IO.
'''


def send(msg):
    print(msg)


def recv(prompt=None):
    return input(prompt)
