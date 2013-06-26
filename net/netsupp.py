from net.netshared import Message


def register_msg(acc, pw):
    auth_string = "user:{0}@pass:{1}"
    msg = Message("lobby", "register", auth_string.format(acc, pw), 1)
    return msg

def auth_msg(acc, pw):
    auth_string = "user:{0}@pass:{1}"
    msg = Message("lobby", "identify", auth_string.format(acc, pw), 1)
    return msg

def chat_msg(where, args):
    """ where (lobby, room) to send chat message,
    and a dict, usually containing one entry "message" """
    l = []
    for k in args.keys():
        if k != "message":
            l.append( k + ":" + ",".join(args[k]) )
    l.append( "message"+":"+args["message"] )

    str_args = "@".join(l)
    msg = Message(where, "chat", str_args, 0)
    return msg
