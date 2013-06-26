

# functions shared by both client.py, server.py, and netsupp.py


class Message:
    def __init__(self, where, mtype, args, priority):
        self.where = where
        self.mtype = mtype
        self.args = args
        self.priority = priority

        self.id = -1

    def set_id(self, _id):
        self.id = _id
        

def parse_args(args, fs): # parse arguments in a message
    d = {}
    i = 0
    for n in args.split("@"):
        k, v = n.split(":")
        d[k] = fs[i](v)
        i += 1
    return d


def t2s(t): # tuple to string
    return list(map(int, x.split(",")))
