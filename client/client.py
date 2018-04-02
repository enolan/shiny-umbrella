import json
import socket
import time
from threading import *
from uuid import uuid4

import natlink
from natlinkutils import GrammarBase

import RPC

natlink.natConnect(True)


sock = socket.create_connection(("10.0.2.2", 43238))
RPC.sendMsg(RPC.utterance([["hello", "world"], ["hello", "oh", "whirled"]]), sock)


def getAllWords(resObj):
    choices = []
    n = 0
    while True:
        try:
            choices.append(resObj.getWords(n))
        except natlink.OutOfRange:
            return choices
        n += 1


# Set up a catchall grammar. The whole idea is to forward everything to the
# server, so we don't do any processing here.
class CatchallGrammar(GrammarBase):
    def __init__(self):
        GrammarBase.__init__(self)
        GrammarBase.load(
            self,
            """<dgndictation> imported;
               <catchall> exported = <dgndictation>;""",
            allResults=1,
            hypothesis=1)

    def gotResultsObject(self, recogType, resObj):
        print(type(resObj))
        print(
            "recogType {}, choices {}".format(recogType, getAllWords(resObj)))

    def gotHypothesis(self, words):
        print("hypothesis {}".format(words))


grammar = CatchallGrammar()
grammar.activate("catchall", exclusive=1)

loaded = True


def printLoop():
    while loaded:
        print("loop")
        time.sleep(1)


loopThread = Thread(target=printLoop)
loopThread.start()

natlink.waitForSpeech(10000)

loaded = False
loopThread.join()

grammar.unload()
natlink.natDisconnect()
