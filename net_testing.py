from net.netsupp import *
from net.client import Client
from net.server import Server
from time import sleep


if __name__ == "__main__":
    host, sport, cport = "localhost", 13371, 13372

    c = Client(host, cport, sport)
    c.start(c.s)
    c.add_message(register_msg("vegard1992", "poop123"))
    c.add_message(auth_msg("vegard1992", "poop123"))
    sleep(1)
    c.add_message(chat_msg("lobby", {"message": "sup nerds"}))
