from net.netsupp import *
from net.client import Client
from net.server import Server
from time import sleep
from sys import argv


if __name__ == "__main__":
    host, sport, cport = "localhost", 13371, 13372
    if argv[1] == "server":
        s = Server(sport)
        s.start(s.s)
    elif argv[1] == "client":
        c = Client(host, cport, sport)
        c.start(c.s)
        c.add_message(register_msg("vegard1992", "poop123"))
        c.add_message(auth_msg("vegard1992", "poop123"))
        sleep(1)
        c.add_message(chat_msg("lobby", {"message": "sup nerds"}))
