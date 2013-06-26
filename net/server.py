import socket
from threading import Thread
from net.netshared import *
import pickle


def s2c_send_message(s, host, port, msg):
    send_str = "{0} {1} {2}".format(*msg)
    mbytes = send_str.encode()
    s.sendto(mbytes, (host, port))


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
        with open("users.dump", "rb") as f:
            self.authdict = pickle.load(f)

    def store_accs(self):
        with open("users.dump", "wb") as f:
            pickle.dump(self.authdict, f)
            
                  
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

            self.data.store_accs()

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
            
        
