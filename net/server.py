import socket
from threading import Thread
from net.netshared import *
import pickle


def s2c_send_message(s, host, port, msg): # sends a message from server to client
    send_str = "{0} {1} {2}".format(*msg) # ID, TYPE, MESSAGE_ARGS
    mbytes = send_str.encode()
    s.sendto(mbytes, (host, port))


def c2s_parse(text): # parses message from client, returns an instance of Message
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


class Room:
    def __init__(self, master):
        self.id = 0
        self.level = ""
        self.accs = []
        self.master = master


class Server_Data: # class for storing server data, and corresponding functions to work on it i.e. handling users, rooms
    def __init__(self):
        self.userbase = {}
        self.authdict = {}
        self.uid = 0
        
        self.rooms = {}
        self.rid = 0
        
        
    def load_accs(self): 
        with open("users.dump", "rb") as f:
            self.authdict = pickle.load(f)

    def store_accs(self):
        with open("users.dump", "wb") as f:
            pickle.dump(self.authdict, f)
            
                  
    def id_user(self, acc, pw, ip): # authenticate a user, corresponds with an ip, and a unique user-id. creates an instance of User server-side
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

    def register_user(self, acc, pw): # registers a user
        if acc in self.authdict:
            return "Account name already taken."
        self.authdict[acc] = pw
        return "Successfully registered."

    def get_lobbyists(self): # returns whos in the lobby / authenticated
        l = []
        for k in self.userbase.keys():
            i = self.userbase[k].ip
            l.append(i)
        return l

    def get_users_in(self, room): # returns whos in a specific room
        if room not in self.rooms:
            return []
        l = []
        for u in self.rooms[room].accs:
            l.append(self.userbase[u].ip)
        return l

    def get_auth(self, ip): # checks to see if the ip is authenticated, returns the user associated with it or None
        for k in self.userbase.keys():
            name, uip = self.userbase[k].acc, self.userbase[k].ip
            if ip == uip:
                return name
        
    def user_create(self, room, user): # create a room, with user as master
        if room in self.rooms:
            return "Room already exists."

        room_ = Room(user)
        room_.id = self.rid
        self.rid += 1
        self.rooms[room] = room_
        return "Room created."

    def user_join(self, room, user): # join a room
        if room not in self.rooms:
            return "Room not found."

        self.rooms[room].accs.append(user)
        return "Joined room."

    def is_in_room(self, user, room): # check if a user is in a room
        ip = self.userbase[user].ip
        if ip in self.get_users_in(room):
            return True
        return False

    

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


    def send(self, s): # sends a message from the queue
        if len(self.oqueue) == 0:
            return
        msg, hp = self.oqueue.pop(0)
        if hp == "lobby": # send to all users
            for hp in self.data.get_lobbyists():
                h, p = hp
                s2c_send_message(s, h, p, msg)
        elif hp[0:4] == "room": # send to users in a room
            room = hp[4:]
            for hp in self.data.get_users_in(room):
                h, p = hp
                s2c_send_message(s, h, p, msg)
        else: 
            h, p = hp
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
                #try: self.parse_input(parseme)
                #except Exception: pass


    def parse_input(self, msgf): # parse received messages
        msg, f = msgf
      #  print(msg)
        
        if msg.priority == 1:
            self.add_message(((msg.id, "acknowledged", "poo:pee@pee:poo"), f))

        user = self.data.get_auth(f)
        d = parse_args(msg.args, (str, str))
        
        if user == None: # if the user is not authenticated

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

            if msg.mtype == "create":
                sendback = self.data.user_create(d["name"], user)
                self.add_message(((self.id, "chat", "name:Server@message:"+sendback), f))
                self.id += 1

            elif msg.mtype == "join":
                sendback = self.data.user_join(d["name"], user)
                self.add_message(((self.id, "chat", "name:Server@message:"+sendback), f))
                self.id += 1

            elif msg.mtype == "chat":
                message = d["message"]
                if msg.where == "lobby":
                    self.add_message(((self.id, "chat", "name:{0}@message:{1}".format(user, message)), "lobby"))
                elif self.data.is_in_room(user, d["room"]):
                    self.add_message(((self.id, "chat", "name:{0}@message:{1}".format(user, message)), "room"+d["room"]))

                self.id += 1
                    
            elif msg.mtype == "game":
                pass
            
        
