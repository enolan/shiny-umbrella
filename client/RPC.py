import json
from uuid import uuid4

def msg(tag, inner):
    return {"msgId": str(uuid4()), "msgContent": {"tag": tag, "contents": inner}}

def utterance(possibilities):
    return msg("Utterance", possibilities)

def sendMsg(msg, sock):
    encoded = json.dumps(msg)
    encoded += "\n"
    sock.sendall(encoded)
