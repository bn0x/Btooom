import socket
from threading import Thread
from time import sleep


def c2s_send_message(s, host, port, msg):
    send_str = "{0} {1} {2} {3} {4}".format(msg.priority, msg.id, msg.where, msg.mtype, msg.args)
    mbytes = send_str.encode()
    s.sendto(mbytes, (host, port))

def s2c_send_message(s, host, port, msg):
    send_str = "{0} {1} {2}".format(*msg)
    mbytes = send_str.encode()
    s.sendto(mbytes, (host, port))


class Message:
    def __init__(self, where, mtype, args, priority):
        self.where = where
        self.mtype = mtype
        self.args = args
        self.priority = priority

        self.id = -1

    def set_id(self, _id):
        self.id = _id


def c2s_parse(text):
    l = text.split(" ")
    if len(l) > 5: # chat
        priority, id_, where, type_ = l[:4]
        args = l[4:]
        args = " ".join(args)
    else:
        priority, id_, where, type_, args = l

    msg = Message(where, type_, args, int(priority))
    msg.set_id(id_)
    return msg

def s2c_parse(text):
    l = text.split(" ")
    if len(l) > 3: # chat
        id_, type_ = l[:2]
        args = l[2:]
        args = " ".join(args)
    else:
        id_, type_, args = l

    return id_, type_, args

def parse_args(args, fs):
    d = {}
    i = 0
    for n in args.split("@"):
        k, v = n.split(":")
        d[k] = fs[i](v)
        i += 1
    return d

def t2s(t):
    return list(map(int, x.split(",")))
    

class Client:
    def __init__(self, host, lport, tport):
        self.oqueue = []
        self.iqueue = []

        self.interfaces = {
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

    def add_message(self, msg):

        msg.set_id(self.curr_id)
        self.oqueue.append(msg)
        self.curr_id += 1

    def send(self, s):
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

    def parse_input(self, i):
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
        

def reg_msg(acc, pw):
    auth_string = "user:{0}@pass:{1}"
    msg = Message("lobby", "register", auth_string.format(acc, pw), 1)
    return msg

def auth_msg(acc, pw):
    auth_string = "user:{0}@pass:{1}"
    msg = Message("lobby", "identify", auth_string.format(acc, pw), 1)
    return msg

def chat_msg(where, args):
    l = []
    for k in args.keys():
        if k != "message":
            l.append( k + ":" + ",".join(args[k]) )
    l.append( "message"+":"+args["message"] )

    str_args = "@".join(l)
    msg = Message(where, "chat", str_args, 0)
    return msg



"""
Client2Server Specs

The format of a message to the server
"<id> <lobby/room> <type> <@-separated message parameters>"
"chat" is an exception. every command is specified before "Message",
after which the message is specified.

Instances;
0 lobby identify user:vegard1992@pass:poop123
1 lobby chat message:Hey nerds
2 lobby join room:dongsquad420
3 room game player_pos:34,54 
4 room chat color:0,0,255@Message:Get on my level
5 room game player_pos:35,55@player_throw_bomb:1,0.45

Everything is validated by the server before reflecting to clients,
as enforcement of game rules.

Some messages have priority, meaning it must be validated that they were
received. These have priority 1, otherwise 0.

Server2Client Specs

The format of a message to the client
"<id> <type> <@-separated message parameters>"

No priority messages can be sent from the server.
"""


class User:
    def __init__(self):
        self.acc = ""

        self.in_lobby = True
        self.room = ""

        self.ip = ""
        self.id = ""


class Chat:
    def __init__(self):
        self.msgs = []


class Room:
    def __init__(self):
        self.chat = Chat()
        self.level = ""


class Server_Data:
    def __init__(self):
        self.userbase = {}
        self.authdict = {}
        self.uid = 0
        
        self.rooms = {}
        self.chat = Chat()

        
    def load_accs(self):
        pass

    def id_user(self, acc, pw, ip):
        if acc not in self.authdict:
            return "Please register the account first."
        if self.authdict[acc] != pw:
            return "Incorrect password"
        
        user = User()
        user.ip = ip
        user.id = self.uid
        self.uid += 1
        user.acc = acc
        self.userbase[acc] = user
        return "Authenticated."

    def register_user(self, acc, pw):
        if acc in self.authdict:
            return "Account name already taken."
        self.authdict[acc] = pw
        return "Successfully registered."

    def get_lobbyists(self):
        l = []
        for k in self.userbase.keys():
            i = self.userbase[k].ip
            l.append(i)
        return l

    def get_auth(self, ip):
        for k in self.userbase.keys():
            name, uip = self.userbase[k].acc, self.userbase[k].ip
            if ip == uip:
                return name
        

class Server:
    def __init__(self, lport):
        self.data = Server_Data()

        self.oqueue = []
        self.iqueue = []

        self.host = "localhost"
        self.lport = lport
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host, self.lport))

        self.id = 0
            
    def start(self, s):
        self.start_receiver_thread(s)
        self.start_iparser_thread()
        self.start_sender_thread(s)

    def add_message(self, msg):
        self.oqueue.append(msg)

    def send(self, s):
        if len(self.oqueue) == 0:
            return
        msg, hp = self.oqueue.pop(0)
        if hp == "lobby": # send to all users
            for hp in self.data.get_lobbyists():
                h, p = hp
                s2c_send_message(s, h, p, msg)
        if hp == "room": # send to users in room
            pass
        else: 
            h, p = hp
            #print(hp)
            s2c_send_message(s, h, p, msg)

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
            print("Server:", data, "from", f)
            text = data.decode()
            self.iqueue.append((c2s_parse(text), f))

    def start_iparser_thread(self):
        t = Thread(target = self.iparser)
        t.start()
    
    def iparser(self):
        while True:
            if len(self.iqueue) > 0:
                parseme = self.iqueue.pop(0)
                self.parse_input(parseme)

    def parse_input(self, msgf):
        msg, f = msgf
        
        if msg.priority == 1:
            self.add_message(((msg.id, "acknowledged", "poo:pee@pee:poo"), f))

        user = self.data.get_auth(f)
        d = parse_args(msg.args, (str, str))
        
        if user == None:

            if msg.mtype == "register":
                sendback = self.data.register_user(d["user"], d["pass"])
                self.add_message(((self.id, "chat", "name:Server@message:"+sendback), f))
                self.id += 1

            elif msg.mtype == "identify":
                sendback = self.data.id_user(d["user"], d["pass"], f)
                self.add_message(((self.id, "chat", "name:Server@message:"+sendback), f))
                self.id += 1

            else:
                self.add_message(((self.id, "chat", "name:Server@message:Not authenticated."), f))
                self.id += 1

        else:

            if msg.mtype == "join":
                sendback = self.data.user_join(d["room"], f)
                self.add_message(((self.id, "chat", "name:Server@message:"+sendback), f))
                self.id += 1

            elif msg.mtype == "chat":
                if msg.where == "lobby":
                    msg = d["message"]
                    self.add_message(((self.id, "chat", "name:{0}@message:{1}".format(user, msg)), f))
                else:
                    pass

            elif msg.mtype == "game":
                pass
            

if __name__ == "__main__":
    argv = __import__("sys").argv
    host, sport, cport = "localhost", 13371, 13372
    if argv[1] == "server":
        s = Server(sport)
        s.start(s.s)
    elif argv[1] == "client":
        c = Client(host, cport, sport)
        c.start(c.s)
        c.add_message(reg_msg("vegard1992", "poop123"))
        c.add_message(auth_msg("vegard1992", "poop123"))
        sleep(1)
        c.add_message(chat_msg("lobby", {"message": "sup nerds"}))
        
