import json
from uuid import uuid4


def msg(tag, inner):
    generatedId = uuid4()
    msgDict = {
        "msgId": str(generatedId),
        "msgContent": {
            "tag": tag,
            "contents": inner
        }
    }
    return (generatedId, msgDict)


def utterance(possibilities):
    return msg("Utterance", possibilities)


def sendMsg(msg, sock):
    encoded = json.dumps(msg, encoding="latin_1")
    encoded += "\n"
    sock.sendall(encoded)
