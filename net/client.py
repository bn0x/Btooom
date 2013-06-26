import socket
from threading import Thread
from net.netshared import *


def c2s_send_message(s, host, port, msg): # send a message from client to server
    send_str = "{0} {1} {2} {3} {4}".format(msg.priority, msg.id, msg.where, msg.mtype, msg.args)
    mbytes = send_str.encode()
    s.sendto(mbytes, (host, port))


def s2c_parse(text): # parse a message from the server
    l = text.split(" ")
    if len(l) > 3: # chat
        id_, type_ = l[:2]
        args = l[2:]
        args = " ".join(args)
    else:
        id_, type_, args = l

    return id_, type_, args



class Client:
    def __init__(self, host, lport, tport):
        self.oqueue = []
        self.iqueue = []

        self.interfaces = { # this will be the final layer between the net stuff and game
            "chat": None,
            "room": None,
            "game": None
            }
        
        self.curr_id = 0

        self.host = host
        self.lport = lport
        self.tport = tport
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host, self.lport))

    def add_interface(self, name, interface):
        self.interfaces[name] = interface

    def start(self, s):
        self.start_receiver_thread(s)
        self.start_iparser_thread()
        self.start_sender_thread(s)

    def add_message(self, msg): # add a message with a unique id

        msg.set_id(self.curr_id)
        self.oqueue.append(msg)
        self.curr_id += 1

    def send(self, s): # send a message from the queue
        if len(self.oqueue) == 0:
            return
        
        msg = self.oqueue.pop(0)
        
        if msg.priority:
            self.oqueue.append(msg)

        c2s_send_message(s, self.host, self.tport, msg)

    def start_sender_thread(self, s):
        t = Thread(target = self.sender, args = (s,))
        t.start()

    def sender(self, s):
        while True:
            self.send(s)

    def start_receiver_thread(self, s):
        t = Thread(target = self.receiver, args = (s,))
        t.start()

    def receiver(self, s):
        while True:
            data, f = s.recvfrom(1024)
            print("Client:", data, "from", f)
            text = data.decode()
            self.iqueue.append(s2c_parse(text))

    def start_iparser_thread(self):
        t = Thread(target = self.iparser)
        t.start()
    
    def iparser(self):
        while True:
            if len(self.iqueue) > 0:
                parseme = self.iqueue.pop(0)
                self.parse_input(parseme)
                #try: self.parse_input(parseme)
                #except Exception: pass

    def parse_input(self, i): # parse messages from the server
        id_, type_, args = i
        if type_ == "acknowledged":
            try:
                ack_msg_index = list(map(lambda x: x.id, self.oqueue)).index(int(id_))
                self.oqueue.pop(ack_msg_index)
            except ValueError: pass

        elif type_ == "chat":
            d = parse_args(args, (str, str))
            n, m = d["name"], d["message"]
            #print(n, m)
            #self.interfaces["chat"].add_message(Chat_Message(n, m))
        
        elif type_ == "game":
            pass

        
