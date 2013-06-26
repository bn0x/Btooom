from net.netsupp import *
from net.client import Client
from net.server import Server
from time import sleep
from sys import argv


if __name__ == "__main__":
    server = Server(13371)
    server.data.load_accs()
    server.start(server.s)
    
